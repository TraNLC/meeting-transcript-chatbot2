import os
from pinecone import Pinecone

api_key = "pcsk_5Zg3DW_251rNTDPvMMDQY8RAQXTrZvcaCKZ39rMMzzC5Jwof17xXD2dfAyPqVVFLoJfq9d"

try:
    print(f"Testing Pinecone API Key...")
    pc = Pinecone(api_key=api_key)
    indexes = pc.list_indexes()
    print("✅ Connection Successful!")
    print(f"Indexes found: {[i.name for i in indexes]}")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
