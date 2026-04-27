import json
import re
from groq import Groq
from app.config import settings
from llm.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


client = Groq(api_key=settings.GROQ_API_KEY)


def detect_intent(message: str, telegram_id: int, name: str) -> dict:
    """
    Converts natural language into an MCP tool call dict.
    Uses Groq LLM to parse intent and extract parameters.
    Returns a dict with 'action' and relevant parameters.
    """
    prompt = USER_PROMPT_TEMPLATE.format(message=message)

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        content = response.choices[0].message.content.strip()

        # Try to extract JSON from the response (handles markdown code blocks)
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match:
            intent = json.loads(json_match.group(1))
        else:
            start = content.find('{')
            end = content.rfind('}')
            if start != -1 and end != -1:
                intent = json.loads(content[start:end+1])
            else:
                intent = json.loads(content)

    except (json.JSONDecodeError, Exception) as e:
        print(f"Intent detection error: {e}")
        return {"action": "unknown"}

    # Attach telegram_id and name automatically
    intent["telegram_id"] = telegram_id
    intent["name"] = name
    intent["message"] = message

    return intent


def call_llm(prompt: str) -> str:
    """
    Utility function to send a prompt to the LLM and return the response text.
    Used by the RAG pipeline.
    """
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"LLM call error: {e}")
        return "Sorry, I could not generate an answer at this time."