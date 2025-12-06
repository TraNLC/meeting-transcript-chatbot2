import requests
import json

def test_search():
    url = "http://localhost:5000/api/rag/smart-search"
    payload = {
        "query": "marketing",
        "k": 5
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_search()
