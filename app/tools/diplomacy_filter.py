from app.llm_client import llm_client

class DiplomacyFilterTool:
    def filter(self, content: str) -> str:
        """Filters content for diplomatic sensitivity."""
        system_prompt = """
        You are a diplomatic censor.
        Review the provided content for any language that could be considered offensive, politically insensitive, or risky for international relations (specifically US-Egypt relations).
        If the content is safe, YOU MUST RETURN THE ORIGINAL CONTENT EXACTLY AS IS. DO NOT ADD ANY COMMENTS.
        If not, rewrite it to be diplomatic and neutral while retaining the core message.
        RETURN ONLY THE FINAL CONTENT. NO PREAMBLE.
        """
        return llm_client.generate_response(system_prompt, content)

diplomacy_filter = DiplomacyFilterTool()
