from openai import OpenAI
from app.config import settings

class LLMClient:
    def __init__(self):
        self.client = None
        self.model = settings.OPENAI_MODEL

    def _ensure_client(self, force_reinit: bool = False):
        if self.client and not force_reinit:
            return self.client
        
        try:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            return self.client
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
            return None

    def generate_response(self, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
        """
        Generates a response from the LLM.
        """
        max_retries = 1
        for attempt in range(max_retries + 1):
            # Force re-init on retry
            force_reinit = (attempt > 0)
            client = self._ensure_client(force_reinit=force_reinit)
            
            if not client:
                if attempt < max_retries:
                    print(f"Client init failed, retrying ({attempt+1}/{max_retries})...")
                    continue
                return "Error: OpenAI client not initialized. Check API key."

            try:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Error generating response (attempt {attempt+1}/{max_retries+1}): {e}")
                if attempt < max_retries:
                    continue
                return f"Error: {str(e)}"

    def generate_tool_call(self, system_prompt: str, user_prompt: str, tools: list, tool_choice: str = "auto"):
        """
        Generates a response with tool calls.
        """
        max_retries = 1
        for attempt in range(max_retries + 1):
            # Force re-init on retry
            force_reinit = (attempt > 0)
            client = self._ensure_client(force_reinit=force_reinit)
            
            if not client:
                if attempt < max_retries:
                    print(f"Client init failed, retrying ({attempt+1}/{max_retries})...")
                    continue
                print("Error: OpenAI client not initialized.")
                return None

            try:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    tools=tools,
                    tool_choice=tool_choice
                )
                return response.choices[0].message
            except Exception as e:
                print(f"Error generating tool call (attempt {attempt+1}/{max_retries+1}): {e}")
                if attempt < max_retries:
                    continue
                return None

llm_client = LLMClient()
