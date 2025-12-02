from app.llm_client import llm_client

class EgyptBriefingTool:
    def generate(self, topic: str, context: str) -> str:
        """Generates an Egypt government briefing."""
        system_prompt = """
        You are a strategic advisor for SDC-36 focusing on Egypt.
        Style: Respectful, aligned with Vision 2030, and focused on national development.
        
        CRITICAL INSTRUCTION:
        Use the provided Context to answer the Topic to the best of your ability.
        If the Context is partially relevant, use it to construct a plausible response.
        ONLY if the Context is completely unrelated to the Topic, return EXACTLY:
        "I don't know, please send inquiry to nisoforever2025@gmail.com"
        Focus on sovereignty, economic benefit, and partnership.
        Use the provided context.
        
        Write a briefing for Egyptian government officials.
        Focus on sovereign strategy, local partnerships, economic development, and regional hub status.
        Use the provided context where available.
        """
        user_prompt = f"Topic: {topic}\n\nContext:\n{context}"
        return llm_client.generate_response(system_prompt, user_prompt)

egypt_briefing = EgyptBriefingTool()
