"""Test UI navigation by checking if views switch correctly."""

import requests
from bs4 import BeautifulSoup

# Test if app is running
try:
    response = requests.get('http://localhost:5000', timeout=5)
    print("✅ App is running at http://localhost:5000")
    print(f"   Status: {response.status_code}")
    
    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check for views
    views = [
        'initialView',
        'recordingView',
        'uploadView',
        'exportView',
        'smartSearchView'
    ]
    
    print("\n📋 Checking Views in HTML:")
    for view_id in views:
        element = soup.find(id=view_id)
        if element:
            display = element.get('style', '')
            is_visible = 'display: none' not in display
            status = "👁️  VISIBLE" if is_visible else "🙈 HIDDEN"
            print(f"   {status} - {view_id}")
        else:
            print(f"   ❌ MISSING - {view_id}")
    
    # Check for navigation links
    print("\n🔗 Checking Navigation Links:")
    nav_links = soup.find_all('a', {'data-category': True})
    for link in nav_links:
        category = link.get('data-category')
        text = link.get_text(strip=True)
        print(f"   ✅ {category}: {text}")
    
    print("\n" + "=" * 60)
    print("💡 To test navigation:")
    print("   1. Open http://localhost:5000 in browser")
    print("   2. Open Developer Console (F12)")
    print("   3. Click on sidebar tabs:")
    print("      - Ghi âm (Tab 1)")
    print("      - Tải lên (Tab 2)")
    print("      - Xuất file (Tab 3)")
    print("      - AI Search (Tab 4)")
    print("   4. Check console for 'Switching to view:' messages")
    print("=" * 60)
    
except requests.exceptions.ConnectionError:
    print("❌ App is NOT running!")
    print("   Start with: python app_flask.py")
except Exception as e:
    print(f"❌ Error: {e}")
