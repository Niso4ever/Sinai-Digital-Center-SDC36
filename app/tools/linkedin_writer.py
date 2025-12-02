from app.llm_client import llm_client

class LinkedInWriterTool:
    def generate(self, topic: str, context: str) -> str:
        """Generates a LinkedIn post."""
        system_prompt = """
        You are a master social media strategist for SDC-36.
        Write a short, punchy, high-engagement LinkedIn post about the provided topic.
        Use the provided context as ground truth.
        Style: Professional yet visionary. Use bullet points if appropriate. Add 3-5 relevant hashtags.
        
        CRITICAL INSTRUCTION:
        Use the provided Context to answer the Topic to the best of your ability.
        If the Context is partially relevant, use it to construct a plausible response.
        ONLY if the Context is completely unrelated to the Topic, return EXACTLY:
        "I don't know, please send inquiry to nisoforever2025@gmail.com"
        """
        user_prompt = f"Topic: {topic}\n\nContext:\n{context}"
        return llm_client.generate_response(system_prompt, user_prompt)

linkedin_writer = LinkedInWriterTool()
