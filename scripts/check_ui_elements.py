"""Check if all UI elements exist in HTML."""

from pathlib import Path

html_file = Path('templates/index.html')
html_content = html_file.read_text(encoding='utf-8')

# Check for required elements
required_elements = {
    'Views': [
        'id="initialView"',
        'id="recordingView"',
        'id="uploadView"',
        'id="exportView"',
        'id="smartSearchView"'
    ],
    'Navigation': [
        'data-category="recording"',
        'data-category="upload"',
        'data-category="export"',
        'data-category="smart-search"'
    ],
    'Lists': [
        'id="recordingList"',
        'id="analysisHistoryList"'
    ]
}

print("=" * 60)
print("UI ELEMENTS CHECK")
print("=" * 60)

all_found = True

for category, elements in required_elements.items():
    print(f"\n{category}:")
    for element in elements:
        found = element in html_content
        status = "✅" if found else "❌"
        print(f"  {status} {element}")
        if not found:
            all_found = False

print("\n" + "=" * 60)
if all_found:
    print("✅ ALL ELEMENTS FOUND!")
else:
    print("❌ SOME ELEMENTS MISSING!")
print("=" * 60)
