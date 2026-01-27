#!/usr/bin/env python3
"""
Optimize intox8000-anomalies.html by externalizing embedded JSON data.
Reduces HTML size from 7.9MB to ~40KB for faster page load.
"""

def optimize_intox8000():
    input_file = "intox8000-anomalies.html"
    output_file = "intox8000-anomalies-optimized.html"

    print(f"Reading {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Original size: {len(content) / 1024 / 1024:.2f} MB")

    # Find where the embedded data starts
    embed_start = content.find('const embeddedData = {')
    embed_end = content.find('// Initialize', embed_start)

    if embed_start == -1 or embed_end == -1:
        print("Error: Could not find embedded data markers")
        return

    print(f"Found embedded data at position {embed_start}")

    # Extract parts
    before_embed = content[:embed_start]
    after_embed = content[embed_end:]

    # Add loading spinner CSS (insert before </style>)
    style_end = before_embed.rfind('</style>')
    loading_css = """
        /* Loading spinner */
        #loading {
            display: none;
            text-align: center;
            padding: 80px 20px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #4a90d9;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        #content {
            display: none;
        }
    """

    before_embed = before_embed[:style_end] + loading_css + before_embed[style_end:]

    # Add loading spinner HTML (insert after <main>)
    main_start = before_embed.find('<main class="main-content"')
    main_tag_end = before_embed.find('>', main_start) + 1

    loading_html = """
        <!-- Loading spinner -->
        <div id="loading">
            <div class="spinner"></div>
            <h2>Loading Anomaly Data...</h2>
            <p>Please wait while we load 24,000+ breath test records...</p>
        </div>

        <!-- Main content (hidden until data loads) -->
        <div id="content">
    """

    before_embed = before_embed[:main_tag_end] + loading_html + before_embed[main_tag_end:]

    # Add closing div for content wrapper (before </main>)
    main_end = before_embed.rfind('</main>')
    before_embed = before_embed[:main_end] + '\n        </div>' + before_embed[main_end:]

    # New loadData function
    new_load_function = """
        // Load data from external JSON file
        async function loadData() {
            const loadingEl = document.getElementById('loading');
            const contentEl = document.getElementById('content');

            try {
                loadingEl.style.display = 'block';
                contentEl.style.display = 'none';

                const response = await fetch('intox8000-data.json');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                allData = await response.json();

                document.getElementById('totalRecords').textContent = allData.total_records.toLocaleString();
                document.getElementById('totalMachines').textContent = allData.total_machines.toLocaleString();
                document.getElementById('totalAgencies').textContent = allData.total_agencies.toLocaleString();
                document.getElementById('totalOfficers').textContent = allData.total_officers.toLocaleString();
                document.getElementById('dataDate').textContent = new Date(allData.generated).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

                populateDropdowns();

                loadingEl.style.display = 'none';
                contentEl.style.display = 'block';
            } catch (error) {
                loadingEl.innerHTML = '<div style="color: #d32f2f; text-align: center; padding: 40px;"><h2>Error Loading Data</h2><p>' + error.message + '</p><p>Please refresh the page or contact support at 407-500-7000.</p></div>';
                console.error('Error loading data:', error);
            }
        }

        """

    # Combine all parts
    optimized = before_embed + new_load_function + after_embed

    print(f"Optimized size: {len(optimized) / 1024:.2f} KB")
    print(f"Size reduction: {(1 - len(optimized)/len(content)) * 100:.1f}%")

    # Write optimized version
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(optimized)

    print(f"\n✓ Created {output_file}")
    print(f"✓ Original: {len(content) / 1024 / 1024:.2f} MB")
    print(f"✓ Optimized: {len(optimized) / 1024:.2f} KB")
    print(f"✓ Data will now load from: intox8000-data.json")

    # Backup original
    backup_file = "intox8000-anomalies.html.backup"
    import shutil
    shutil.copy(input_file, backup_file)
    print(f"✓ Backed up original to: {backup_file}")

    return True

if __name__ == "__main__":
    optimize_intox8000()
