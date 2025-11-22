# API KEYS CONFIGURATION

**⚠️ QUAN TRỌNG: Không commit file này lên GitHub!**

## Hướng Dẫn Sử Dụng

1. Copy nội dung dưới đây vào file `.env` ở root project
2. Thay thế `[YOUR_KEY_HERE]` bằng API keys thực tế
3. File `.env` đã được thêm vào `.gitignore`

```env
# LLM
AZURE_OPENAI_LLM_ENDPOINT=https://aiportalapi.stu-platform.live/jpe
AZURE_OPENAI_LLM_API_KEY=[YOUR_AZURE_LLM_KEY]
AZURE_OPENAI_LLM_MODEL=GPT-4o

# Embeddings
AZURE_OPENAI_EMBEDDING_ENDPOINT=https://aiportalapi.stu-platform.live/jpe
AZURE_OPENAI_EMBEDDING_API_KEY=[YOUR_AZURE_EMBEDDING_KEY]
AZURE_OPENAI_EMBED_MODEL=text-embedding-3-small

# Optional
TAVILY_API_KEY=[YOUR_TAVILY_KEY]

# Gemini API Key
GEMINI_API_KEY=[YOUR_GEMINI_KEY]

# LLM Configuration
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.5-flash
TEMPERATURE=0.5
MAX_TOKENS=4000
```

## Lấy API Keys

**Gemini API:**
- Truy cập: https://aistudio.google.com/apikey
- Tạo API key miễn phí

**Azure OpenAI:**
- Liên hệ team lead để lấy credentials

**Tavily (Optional):**
- Truy cập: https://tavily.com
- Sign up và lấy API key

## Security Notes

- Không share API keys qua chat/email
- Không commit vào Git
- Rotate keys định kỳ
- Sử dụng environment variables