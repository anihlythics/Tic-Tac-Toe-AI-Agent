from dotenv import load_dotenv
import os

print("Loading environment variables...")  # Debugging print

# Load .env file
load_dotenv()

# Retrieve API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
genai_api_key = os.getenv("GENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

# Print loaded keys (only showing first 5 characters for security)
print("OpenAI API Key:", openai_api_key[:5] + "****" if openai_api_key else "Not Found")
print("GenAI API Key:", genai_api_key[:5] + "****" if genai_api_key else "Not Found")
print("Groq API Key:", groq_api_key[:5] + "****" if groq_api_key else "Not Found")
print("DeepSeek API Key:", deepseek_api_key[:5] + "****" if deepseek_api_key else "Not Found")
