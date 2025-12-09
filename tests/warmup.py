
import requests
import time

def warmup():
    print("🔥 Warming up server...")
    try:
        # 1. Trigger History List (Cache warump)
        requests.get('http://localhost:5000/api/history/list')
        print("✅ History List cached")
        
        # 2. Trigger Semantic Search (Model preload)
        # Request will block until model load if logic not perfect, OR return 500 if still loading?
        # My code in get_model waits if model is none.
        # But threading logic starts in __init__.
        # So first request init -> starts thread -> waits for thread?
        # My _get_model checks if model is None, if so loads it (blocking).
        # So the FIRST request is ALWAYS blocking if thread hasn't finished.
        
        # KEY: We send a dummy request NOW so the checking happens NOW.
        # Then the real test runs later and finds it fast.
        
        try:
            requests.post('http://localhost:5000/api/history/semantic-search', 
                          json={"query": "hello", "top_k": 1}, timeout=1) 
                          # Short timeout because we expect it to be slow/hang, 
                          # but we just want to trigger the init
        except requests.exceptions.Timeout:
            print("⏳ Search request timed out (expected for cold start)")
        except Exception as e:
            print(f"ℹ️ Search warmup exception: {e}")
            
        print("✅ Warmup triggered. Waiting 5s for model to settle...")
        time.sleep(5)
        print("🚀 Server ready!")
        
    except Exception as e:
        print(f"❌ Warmup failed: {e}")

if __name__ == "__main__":
    warmup()
