#!/usr/bin/env python3
"""Build privacy-safe aggregate DUI scatter data for the static page.

The public artifact contains only canonical agency/officer labels, anonymized
filing-period buckets, formal title/last officer labels, aggregate case counts,
bucket median BAC, and under-.08 counts. It intentionally excludes case numbers,
defendant names, exact dates, raw filing text, and database credentials.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import polars as pl


DEFAULT_DATA_ROOT = Path.home() / "data-analysis" / "output"
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "data" / "dui-scatter-data.js"
MIN_OFFICER_CASES = 6
MIN_BUCKET_CASES = 3

ORANGE_COUNTY_AGENCY_NAMES = {
    "Apopka Police Department",
    "Belle Isle Police Department",
    "Eatonville Police Department",
    "Edgewood Police Department",
    "Maitland Police Department",
    "Oakland Police Department",
    "Ocoee Police Department",
    "Orange County Sheriff's Office",
    "Orlando Police Department",
    "UCF Police Department",
    "University of Central Florida Police Department",
    "Windermere Police Department",
    "Winter Garden Police Department",
    "Winter Park Police Department",
}

STATE_ENFORCEMENT_AGENCY_TYPES = {
    "Highway Patrol",
    "State Agency",
}

FORBIDDEN_KEYS = {
    "case_number",
    "defendant",
    "dob",
    "address",
    "dl_num",
    "citation_number",
    "raw_file_id",
    "file_date",
    "offense_date",
    "arrest_date",
}


def _read_sources(data_root: Path) -> tuple[pl.LazyFrame, pl.LazyFrame, pl.LazyFrame]:
    current = data_root / "current_state"
    dims = data_root / "dims"
    return (
        pl.scan_parquet(current / "court_filings.parquet"),
        pl.scan_parquet(dims / "dim_agency.parquet"),
        pl.scan_parquet(dims / "dim_officer.parquet"),
    )


def _add_months(value: date, months: int) -> date:
    month_index = value.year * 12 + (value.month - 1) + months
    return date(month_index // 12, (month_index % 12) + 1, 1)


def _start_month(max_filing_date: date) -> date:
    # Inclusive 12-month public chart window ending in the latest filing month.
    return _add_months(date(max_filing_date.year, max_filing_date.month, 1), -11)


def build_rows(data_root: Path) -> tuple[list[dict], dict]:
    filings, dim_agency, dim_officer = _read_sources(data_root)
    max_filing_date = (
        filings
        .filter((pl.col("is_dui") == True) & pl.col("file_date").is_not_null())
        .select(pl.col("file_date").max())
        .collect()
        .item()
    )
    if max_filing_date is None:
        raise RuntimeError("No DUI filing dates available")

    period_start = _start_month(max_filing_date)
    agency_dim = dim_agency.select(["agency_key", "display_name", "agency_type", "officer_title"])
    officer_dim = dim_officer.select(["officer_key", "canonical_name", "name_full_formal"])

    case_level = (
        filings
        .filter(
            (pl.col("is_dui") == True)
            & (~pl.col("is_future").fill_null(False))
            & pl.col("file_date").is_not_null()
            & (pl.col("file_date") >= pl.lit(period_start))
            & pl.col("primary_agency_key").is_not_null()
            & pl.col("primary_officer_key").is_not_null()
            & pl.col("bac_value").is_not_null()
            & pl.col("bac_value").is_between(0, 0.50)
        )
        .select([
            "case_number",
            "file_date",
            "primary_agency_key",
            "primary_officer_key",
            "primary_agency",
            "primary_officer",
            "bac_value",
        ])
        .group_by("case_number")
        .agg([
            pl.col("file_date").min().alias("file_date"),
            pl.col("primary_agency_key").drop_nulls().first().alias("agency_key"),
            pl.col("primary_officer_key").drop_nulls().first().alias("officer_key"),
            pl.col("primary_agency").drop_nulls().first().alias("primary_agency"),
            pl.col("primary_officer").drop_nulls().first().alias("primary_officer"),
            pl.col("bac_value").max().alias("bac"),
        ])
        .join(agency_dim, on="agency_key", how="left")
        .join(officer_dim, on="officer_key", how="left")
        .with_columns([
            pl.coalesce([pl.col("display_name"), pl.col("primary_agency")]).alias("agency"),
            pl.coalesce([
                pl.col("name_full_formal"),
                pl.col("canonical_name"),
                pl.col("primary_officer"),
            ]).alias("officer"),
            (
                ((pl.col("file_date").dt.year() - period_start.year) * 12)
                + pl.col("file_date").dt.month()
                - period_start.month
                + 1
            ).cast(pl.Int64).alias("month"),
        ])
        .filter(
            pl.col("agency").is_not_null()
            & pl.col("officer").is_not_null()
            & _public_agency_scope_expr()
        )
    )

    officer_totals = (
        case_level
        .group_by(["agency", "officer"])
        .agg(pl.len().alias("total_cases"))
        .filter(pl.col("total_cases") >= MIN_OFFICER_CASES)
    )

    bucketed = (
        case_level
        .join(officer_totals, on=["agency", "officer"], how="inner")
        .group_by(["agency", "officer", "officer_title", "month"])
        .agg([
            pl.len().alias("caseCount"),
            pl.col("bac").median().round(3).alias("bac"),
            (pl.col("bac") < 0.08).sum().alias("under08Count"),
        ])
        .filter(pl.col("caseCount") >= MIN_BUCKET_CASES)
        .sort(["agency", "officer", "month"])
        .collect()
    )

    rows = [
        {
            "agency": row["agency"],
            "officer": row["officer"],
            "officerLabel": _formal_officer_label(row["officer"], row.get("officer_title")),
            "month": int(row["month"]),
            "bac": float(row["bac"]),
            "caseCount": int(row["caseCount"]),
            "under08Count": int(row["under08Count"]),
        }
        for row in bucketed.iter_rows(named=True)
    ]

    metadata = {
        "source": "court_filings current_state parquet joined to dim_agency.display_name and dim_officer display fields",
        "grain": "agency/officer/anonymized filing-period bucket",
        "period": "last 12 court-filing months",
        "agencyScope": "Orange County local/in-county agencies plus state enforcement agencies; out-of-county agencies excluded",
        "minOfficerCases": MIN_OFFICER_CASES,
        "minBucketCases": MIN_BUCKET_CASES,
        "rowCount": len(rows),
        "agencyCount": len({row["agency"] for row in rows}),
        "officerCount": len({(row["agency"], row["officer"]) for row in rows}),
    }
    return rows, metadata


def assert_safe_payload(payload: dict) -> None:
    text = json.dumps(payload, sort_keys=True)
    for key in FORBIDDEN_KEYS:
        if key in text:
            raise RuntimeError(f"Forbidden field leaked into artifact: {key}")
    for row in payload["rows"]:
        missing = {"agency", "officer", "officerLabel", "month", "bac", "caseCount", "under08Count"} - set(row)
        if missing:
            raise RuntimeError(f"Row missing required keys: {sorted(missing)}")
        if not (1 <= int(row["month"]) <= 12):
            raise RuntimeError(f"Month bucket out of range: {row['month']}")
        if int(row["caseCount"]) < MIN_BUCKET_CASES:
            raise RuntimeError("Bucket support below public threshold")


def _public_agency_scope_expr() -> pl.Expr:
    return (
        pl.col("agency").is_in(sorted(ORANGE_COUNTY_AGENCY_NAMES))
        | pl.col("agency_type").is_in(sorted(STATE_ENFORCEMENT_AGENCY_TYPES))
    )


def _formal_officer_label(name: str | None, title: str | None) -> str:
    cleaned_name = " ".join(str(name or "").replace(",", " ").split())
    cleaned_title = " ".join(str(title or "").split()) or "Officer"
    if not cleaned_name:
        return cleaned_title or "Officer"
    last_name = cleaned_name.split()[-1]
    return f"{cleaned_title} {last_name}".strip() or cleaned_name


def write_artifact(rows: list[dict], metadata: dict, out_path: Path) -> None:
    payload = {"metadata": metadata, "rows": rows}
    assert_safe_payload(payload)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        "window.duiScatterDataPayload = "
        + json.dumps(payload, indent=2, sort_keys=True)
        + ";\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    rows, metadata = build_rows(args.data_root)
    write_artifact(rows, metadata, args.out)
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
