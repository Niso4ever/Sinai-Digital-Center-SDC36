from app.llm_client import llm_client

class TechExplainerTool:
    def explain(self, topic: str, context: str) -> str:
        """Generates a technical explanation."""
        system_prompt = """
        You are a chief engineer for SDC-36.
        Explain the technical architecture, AI infrastructure, energy systems, or subsea cables.
        Style: Clear, technical but accessible, and detailed.
        
        CRITICAL INSTRUCTION:
        Use the provided Context to answer the Topic to the best of your ability.
        If the Context is partially relevant, use it to construct a plausible response.
        ONLY if the Context is completely unrelated to the Topic, return EXACTLY:
        "I don't know, please send inquiry to nisoforever2025@gmail.com"
        Use technical terminology correctly.
        Use the provided context.
        """
        user_prompt = f"Topic: {topic}\n\nContext:\n{context}"
        return llm_client.generate_response(system_prompt, user_prompt)

tech_explainer = TechExplainerTool()
