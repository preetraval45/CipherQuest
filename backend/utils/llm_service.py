import os
import openai
import time
from threading import Lock

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Simple in-memory rate limiter (per-process, not distributed)
class RateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.lock = Lock()

    def allow(self):
        with self.lock:
            now = time.time()
            # Remove calls outside the period
            self.calls = [t for t in self.calls if now - t < self.period]
            if len(self.calls) < self.max_calls:
                self.calls.append(now)
                return True
            return False

# Example: 60 calls per minute
llm_rate_limiter = RateLimiter(max_calls=60, period=60)

def send_prompt_to_llm(prompt, model="gpt-3.5-turbo"):
    if not OPENAI_API_KEY:
        return {'error': 'AI service is currently unavailable. Please contact support.'}
    if not llm_rate_limiter.allow():
        return {'error': 'Rate limit exceeded. Please try again later.'}
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response['choices'][0]['message']['content']
        return {'response': answer}
    except openai.error.OpenAIError as e:
        return {'error': f'OpenAI API error: {str(e)}'}
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'} 