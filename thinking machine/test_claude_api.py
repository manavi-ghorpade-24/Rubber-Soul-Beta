"""
Test script to verify Claude API connection and find working model
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ ANTHROPIC_API_KEY not found in .env file")
    exit(1)

print("✅ API key found")
print(f"Key starts with: {api_key[:10]}...")

client = Anthropic(api_key=api_key)

# List of models to try
models_to_test = [
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-3-5-sonnet",  # Without date
    "claude-3-sonnet",    # Without date
]

print("\n🔍 Testing models...\n")

working_model = None

for model in models_to_test:
    try:
        print(f"Testing: {model}...", end=" ")
        response = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print("✅ WORKS!")
        working_model = model
        break
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not_found" in error_msg.lower():
            print("❌ Not found")
        else:
            print(f"❌ Error: {error_msg[:50]}")

if working_model:
    print(f"\n✅ Found working model: {working_model}")
    print(f"\nAdd this to your .env file:")
    print(f"CLAUDE_MODEL={working_model}")
else:
    print("\n❌ No working models found. Possible issues:")
    print("1. API key might not have access to Claude models")
    print("2. API key might be invalid")
    print("3. Check Anthropic console: https://console.anthropic.com/")
    print("4. Model names might have changed - check latest docs")

