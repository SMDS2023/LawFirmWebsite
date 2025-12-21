#!/usr/bin/env python3
"""
Website Update Script with Logging
Reads audit/style guide, identifies one update task, outputs instructions for Claude Code.
Logs all activity to _AI_Repair_Log.csv.

Usage:
    python website_update.py                    # Get next task
    python website_update.py --topic SEO        # Get next SEO task
    python website_update.py --dry-run          # Show task without logging start
    python website_update.py --view-log         # View repair log
    python website_update.py --complete --outcome success --changes "Description of changes"
"""

import csv
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
KNOWLEDGE_DIR = PROJECT_ROOT / ".claude" / "knowledge"
LOG_FILE = SCRIPT_DIR / "_AI_Repair_Log.csv"

# Knowledge files
AUDIT_FILE = KNOWLEDGE_DIR / "MASTER-AUDIT.md"
TRACKER_FILE = KNOWLEDGE_DIR / "OPTIMIZATION-TRACKER.md"
BRAND_FILE = KNOWLEDGE_DIR / "BRAND-GUIDE.md"

# Priority order
PRIORITY_ORDER = ["Critical", "High", "Medium", "Low"]

# Session state file (tracks current task)
SESSION_FILE = SCRIPT_DIR / "_current_session.txt"


def get_next_change_number() -> int:
    """Get next change number from existing log."""
    if not LOG_FILE.exists():
        return 1

    with open(LOG_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            return 1
        try:
            last_num = int(rows[-1].get('Change_Number', 0))
            return last_num + 1
        except (ValueError, KeyError):
            return len(rows) + 1


def read_tracker_tasks() -> list:
    """Parse OPTIMIZATION-TRACKER.md for pending tasks."""
    if not TRACKER_FILE.exists():
        print(f"Error: Tracker file not found: {TRACKER_FILE}")
        return []

    content = TRACKER_FILE.read_text(encoding='utf-8')
    tasks = []

    # Parse sections by priority
    current_priority = None
    current_task = None
    in_task = False

    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Detect priority section headers
        if '## CRITICAL TASKS' in line:
            current_priority = 'Critical'
        elif '## HIGH PRIORITY TASKS' in line:
            current_priority = 'High'
        elif '## MEDIUM PRIORITY TASKS' in line:
            current_priority = 'Medium'
        elif '## LOW PRIORITY TASKS' in line:
            current_priority = 'Low'
        elif '## COMPLETED TASKS' in line or '## ONGOING MAINTENANCE' in line:
            current_priority = None  # Stop parsing

        # Skip if we're past active tasks
        if current_priority is None:
            continue

        # Detect task headers (### 1. Task Name)
        task_match = re.match(r'^### (\d+)\. (.+)$', line)
        if task_match:
            # Save previous task if exists
            if current_task:
                tasks.append(current_task)

            current_task = {
                'number': int(task_match.group(1)),
                'title': task_match.group(2).strip(),
                'priority': current_priority,
                'status': 'Not Started',
                'category': '',
                'effort': '',
                'impact': '',
                'next_steps': [],
                'line_number': i + 1
            }
            in_task = True
            continue

        # Parse task metadata
        if current_task and in_task:
            if line.startswith('**Status:**'):
                current_task['status'] = line.replace('**Status:**', '').strip()
            elif line.startswith('**Category:**'):
                current_task['category'] = line.replace('**Category:**', '').strip()
            elif line.startswith('**Effort:**'):
                current_task['effort'] = line.replace('**Effort:**', '').strip()
            elif line.startswith('**Impact:**'):
                current_task['impact'] = line.replace('**Impact:**', '').strip()
            elif line.startswith('**Next Steps:**'):
                # Start collecting next steps
                pass
            elif re.match(r'^\d+\.\s', line.strip()) and current_task:
                current_task['next_steps'].append(line.strip())

    # Add last task
    if current_task:
        tasks.append(current_task)

    return tasks


def get_actionable_tasks(tasks: list, topic_filter: str = None) -> list:
    """Filter to actionable (Not Started) tasks, sorted by priority."""
    actionable = [t for t in tasks if t['status'] == 'Not Started']

    if topic_filter:
        actionable = [t for t in actionable if topic_filter.lower() in t['category'].lower()]

    # Sort by priority
    actionable.sort(key=lambda t: PRIORITY_ORDER.index(t['priority']) if t['priority'] in PRIORITY_ORDER else 99)

    return actionable


def read_brand_guide_summary() -> str:
    """Load key brand guide info for reference."""
    if not BRAND_FILE.exists():
        return "Brand guide not found."

    content = BRAND_FILE.read_text(encoding='utf-8')

    # Extract key sections (first 50 lines or up to ## section)
    lines = content.split('\n')[:50]
    return '\n'.join(lines)


def log_entry(change_num: int, topic: str, search_desc: str, detailed_desc: str):
    """Append entry to CSV log."""
    file_exists = LOG_FILE.exists()

    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'Change_Number', 'DateTime', 'Topic', 'Search_Description', 'Detailed_Description'
        ])

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'Change_Number': change_num,
            'DateTime': datetime.now().isoformat(),
            'Topic': topic,
            'Search_Description': search_desc,
            'Detailed_Description': detailed_desc
        })


def save_session(task: dict, change_num: int, start_time: str):
    """Save current session state."""
    with open(SESSION_FILE, 'w', encoding='utf-8') as f:
        f.write(f"Change_Number: {change_num}\n")
        f.write(f"Start_Time: {start_time}\n")
        f.write(f"Task_Number: {task['number']}\n")
        f.write(f"Task_Title: {task['title']}\n")
        f.write(f"Topic: {task['category']}\n")


def load_session() -> dict:
    """Load current session state."""
    if not SESSION_FILE.exists():
        return None

    session = {}
    with open(SESSION_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                key, value = line.split(':', 1)
                session[key.strip()] = value.strip()
    return session


def clear_session():
    """Clear session file."""
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()


def view_log():
    """Display the repair log."""
    if not LOG_FILE.exists():
        print("No repair log found. Run updates first.")
        return

    with open(LOG_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("Repair log is empty.")
        return

    print(f"\n{'='*80}")
    print(f" AI REPAIR LOG - {len(rows)} entries")
    print(f"{'='*80}\n")

    for row in rows[-10:]:  # Show last 10 entries
        print(f"[{row['Change_Number']}] {row['DateTime'][:16]}")
        print(f"    Topic: {row['Topic']}")
        print(f"    {row['Search_Description']}")
        print(f"    {row['Detailed_Description'][:100]}...")
        print()


def output_task_instructions(task: dict, change_num: int):
    """Output structured instructions for Claude Code."""
    print(f"\n{'='*80}")
    print(f" WEBSITE UPDATE TASK #{change_num}")
    print(f"{'='*80}\n")

    print(f"TASK:     {task['title']}")
    print(f"PRIORITY: {task['priority']}")
    print(f"CATEGORY: {task['category']}")
    print(f"EFFORT:   {task['effort']}")
    print(f"IMPACT:   {task['impact']}")
    print()

    print("NEXT STEPS:")
    for step in task['next_steps'][:5]:  # Show first 5 steps
        print(f"  {step}")
    print()

    print("INSTRUCTIONS FOR CLAUDE CODE:")
    print("-" * 40)
    print(f"Please execute task #{task['number']}: {task['title']}")
    print(f"Refer to OPTIMIZATION-TRACKER.md line {task['line_number']} for full details.")
    print(f"Follow BRAND-GUIDE.md for style consistency.")
    print()

    print("WHEN COMPLETE, RUN:")
    print(f'  python website_update.py --complete --outcome success --changes "Description of what was done"')
    print()
    print(f"{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(description='Website Update Script with Logging')
    parser.add_argument('--topic', type=str, help='Filter by topic (SEO, Content, UX, etc.)')
    parser.add_argument('--dry-run', action='store_true', help='Show task without logging start')
    parser.add_argument('--view-log', action='store_true', help='View repair log')
    parser.add_argument('--complete', action='store_true', help='Log task completion')
    parser.add_argument('--outcome', type=str, choices=['success', 'partial', 'failed'],
                        help='Task outcome (used with --complete)')
    parser.add_argument('--changes', type=str, help='Description of changes (used with --complete)')

    args = parser.parse_args()

    # View log mode
    if args.view_log:
        view_log()
        return

    # Complete mode - log completion of current task
    if args.complete:
        session = load_session()
        if not session:
            print("Error: No active session found. Start a task first with: python website_update.py")
            return

        if not args.outcome:
            print("Error: --outcome required (success, partial, failed)")
            return

        change_num = int(session.get('Change_Number', 0))
        start_time = session.get('Start_Time', 'unknown')
        task_title = session.get('Task_Title', 'Unknown Task')
        topic = session.get('Topic', 'General')

        end_time = datetime.now().isoformat()
        changes = args.changes or "No changes described"

        detailed = f"Task: {task_title}. Start: {start_time[:16]}. End: {end_time[:16]}. Outcome: {args.outcome}. Changes: {changes}"

        log_entry(
            change_num=change_num,
            topic=topic,
            search_desc=f"{task_title} - {args.outcome}",
            detailed_desc=detailed
        )

        clear_session()
        print(f"\n[OK] Logged completion of Change #{change_num}")
        print(f"  Outcome: {args.outcome}")
        print(f"  Topic: {topic}")
        print(f"  Changes: {changes}")
        return

    # Check for existing session
    existing_session = load_session()
    if existing_session and not args.dry_run:
        print(f"\nWarning: Active session exists (Change #{existing_session.get('Change_Number')})")
        print(f"Task: {existing_session.get('Task_Title')}")
        print(f"Started: {existing_session.get('Start_Time', 'unknown')[:16]}")
        print()
        print("Options:")
        print("  1. Complete it:  python website_update.py --complete --outcome success --changes \"...\"")
        print("  2. Cancel it:    python website_update.py --complete --outcome failed --changes \"Cancelled\"")
        print("  3. View anyway:  python website_update.py --dry-run")
        return

    # Get next task
    tasks = read_tracker_tasks()
    if not tasks:
        print("No tasks found in tracker.")
        return

    actionable = get_actionable_tasks(tasks, args.topic)
    if not actionable:
        filter_msg = f" matching topic '{args.topic}'" if args.topic else ""
        print(f"No actionable (Not Started) tasks found{filter_msg}.")
        print(f"Total tasks in tracker: {len(tasks)}")
        return

    # Select highest priority task
    task = actionable[0]
    change_num = get_next_change_number()
    start_time = datetime.now().isoformat()

    # Output task instructions
    output_task_instructions(task, change_num)

    # Save session (unless dry-run)
    if not args.dry_run:
        save_session(task, change_num, start_time)
        print(f"Session started. Run --complete when done.\n")
    else:
        print(f"(Dry run - session not started)\n")


if __name__ == "__main__":
    main()
