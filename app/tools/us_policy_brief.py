from app.llm_client import llm_client

class USPolicyBriefTool:
    def generate(self, topic: str, context: str) -> str:
        """Generates a U.S. policy brief."""
        system_prompt = """
        You are a policy advisor for SDC-36.
        Write a formal U.S. policy brief.
        Style: Formal, diplomatic, and structured (Executive Summary, Key Points, Recommendation).
        
        CRITICAL INSTRUCTION:
        Use the provided Context to answer the Topic to the best of your ability.
        If the Context is partially relevant, use it to construct a plausible response.
        ONLY if the Context is completely unrelated to the Topic (e.g. asking about cooking when context is about energy), return EXACTLY:
        "I don't know, please send inquiry to nisoforever2025@gmail.com"
        Focus on national security, energy independence, and technological leadership.
        Use the provided context.
        """
        user_prompt = f"Topic: {topic}\n\nContext:\n{context}"
        return llm_client.generate_response(system_prompt, user_prompt)

us_policy_brief = USPolicyBriefTool()
