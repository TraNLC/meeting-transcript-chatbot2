"""
API Keys Testing Tool
Tests all API keys from .env file to verify they are working

Usage: python tools/test_api_keys.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print formatted header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")


def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")


def print_info(text):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")


def test_gemini_api():
    """Test Gemini API key (Google Direct)."""
    print_header("Testing Gemini API (Google Direct)")
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print_error("GEMINI_API_KEY not found in .env")
        return False
    
    print_info(f"API Key: {api_key[:20]}...{api_key[-10:]}")
    
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Test with simple prompt
        response = model.generate_content("Say 'Hello' in one word")
        result_text = response.text.strip()
        
        print_success(f"Gemini API is working!")
        print_info(f"Test response: {result_text}")
        return True
        
    except Exception as e:
        print_error(f"Gemini API failed: {str(e)}")
        return False


def test_gemini_portal_api():
    """Test Gemini Portal API (via aiportalapi)."""
    print_header("Testing Gemini Portal API (aiportalapi)")
    
    api_key = os.getenv('GEMINI_PORTAL_API_KEY')
    endpoint = os.getenv('GEMINI_PORTAL_ENDPOINT')
    model = os.getenv('GEMINI_PORTAL_MODEL')
    
    if not api_key:
        print_warning("GEMINI_PORTAL_API_KEY not found in .env - skipping")
        return None
    
    print_info(f"API Key: {api_key[:20]}...{api_key[-10:]}")
    print_info(f"Endpoint: {endpoint}")
    print_info(f"Model: {model}")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=api_key,
            base_url=endpoint
        )
        
        # Test with simple prompt
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say 'Hello' in one word"}
            ],
            max_tokens=10
        )
        
        result_text = response.choices[0].message.content.strip()
        
        print_success(f"Gemini Portal API is working!")
        print_info(f"Test response: {result_text}")
        return True
        
    except Exception as e:
        print_error(f"Gemini Portal API failed: {str(e)}")
        return False


def test_openai_api():
    """Test OpenAI API key."""
    print_header("Testing OpenAI API")
    
    api_key = os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('OPENAI_BASE_URL')
    
    if not api_key:
        print_error("OPENAI_API_KEY not found in .env")
        return False
    
    print_info(f"API Key: {api_key[:20]}...{api_key[-10:]}")
    print_info(f"Base URL: {base_url}")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        # Test with simple prompt
        response = client.chat.completions.create(
            model="GPT-5.1",
            messages=[
                {"role": "user", "content": "Say 'Hello' in one word"}
            ],
            max_tokens=10
        )
        
        result_text = response.choices[0].message.content.strip()
        
        print_success(f"OpenAI API is working!")
        print_info(f"Test response: {result_text}")
        print_info(f"Model: {response.model}")
        return True
        
    except Exception as e:
        print_error(f"OpenAI API failed: {str(e)}")
        
        # Check specific error types
        error_str = str(e).lower()
        if '401' in error_str or 'authentication' in error_str:
            print_warning("Authentication failed - API key may be invalid or expired")
        elif '429' in error_str or 'quota' in error_str:
            print_warning("Rate limit or quota exceeded")
        elif '404' in error_str:
            print_warning("Endpoint not found - check base URL")
        
        return False


def test_azure_openai_embedding():
    """Test Azure OpenAI Embedding API."""
    print_header("Testing Azure OpenAI Embedding API")
    
    api_key = os.getenv('AZURE_OPENAI_EMBEDDING_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_EMBEDDING_ENDPOINT')
    model = os.getenv('AZURE_OPENAI_EMBED_MODEL')
    
    if not api_key:
        print_error("AZURE_OPENAI_EMBEDDING_API_KEY not found in .env")
        return False
    
    print_info(f"API Key: {api_key[:20]}...{api_key[-10:]}")
    print_info(f"Endpoint: {endpoint}")
    print_info(f"Model: {model}")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=api_key,
            base_url=endpoint
        )
        
        # Test embedding
        response = client.embeddings.create(
            model=model,
            input="Hello world"
        )
        
        embedding = response.data[0].embedding
        
        print_success(f"Azure OpenAI Embedding API is working!")
        print_info(f"Embedding dimension: {len(embedding)}")
        return True
        
    except Exception as e:
        print_error(f"Azure OpenAI Embedding API failed: {str(e)}")
        return False


def test_azure_openai_llm():
    """Test Azure OpenAI LLM API."""
    print_header("Testing Azure OpenAI LLM API")
    
    api_key = os.getenv('AZURE_OPENAI_LLM_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_LLM_ENDPOINT')
    model = os.getenv('AZURE_OPENAI_LLM_MODEL')
    
    if not api_key:
        print_error("AZURE_OPENAI_LLM_API_KEY not found in .env")
        return False
    
    print_info(f"API Key: {api_key[:20]}...{api_key[-10:]}")
    print_info(f"Endpoint: {endpoint}")
    print_info(f"Model: {model}")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=api_key,
            base_url=endpoint
        )
        
        # Test with simple prompt
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say 'Hello' in one word"}
            ],
            max_tokens=10
        )
        
        result_text = response.choices[0].message.content.strip()
        
        print_success(f"Azure OpenAI LLM API is working!")
        print_info(f"Test response: {result_text}")
        return True
        
    except Exception as e:
        print_error(f"Azure OpenAI LLM API failed: {str(e)}")
        return False


def test_all_keys():
    """Test all API keys."""
    print(f"\n{Colors.BOLD}API Keys Testing Tool{Colors.RESET}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Test each API
    results['Gemini (Google)'] = test_gemini_api()
    gemini_portal_result = test_gemini_portal_api()
    if gemini_portal_result is not None:
        results['Gemini (Portal)'] = gemini_portal_result
    results['OpenAI'] = test_openai_api()
    results['Azure Embedding'] = test_azure_openai_embedding()
    results['Azure LLM'] = test_azure_openai_llm()
    
    # Print summary
    print_header("Test Summary")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for name, status in results.items():
        if status:
            print_success(f"{name}: PASSED")
        else:
            print_error(f"{name}: FAILED")
    
    print(f"\n{Colors.BOLD}Total: {total} | Passed: {passed} | Failed: {failed}{Colors.RESET}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All API keys are working!{Colors.RESET}\n")
    elif passed > 0:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  Some API keys are not working{Colors.RESET}\n")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ All API keys failed{Colors.RESET}\n")
    
    return passed == total


def main():
    """Main function."""
    try:
        success = test_all_keys()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Test interrupted by user{Colors.RESET}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {str(e)}{Colors.RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
