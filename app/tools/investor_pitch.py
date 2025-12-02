from app.llm_client import llm_client

class InvestorPitchTool:
    def generate(self, topic: str, context: str) -> str:
        """Generates investor messaging."""
        system_prompt = """
        Style: Persuasive, data-driven, and confident. Focus on ROI and market opportunity.
        
        CRITICAL INSTRUCTION:
        Use the provided Context to answer the Topic to the best of your ability.
        If the Context is partially relevant, use it to construct a plausible response.
        ONLY if the Context is completely unrelated to the Topic, return EXACTLY:
        "I don't know, please send inquiry to nisoforever2025@gmail.com"
        Highlight ROI and market opportunity.
        Write a message targeting investors (VC/PE/Sovereign Wealth).
        Focus on ROI, CAPEX/OPEX, TAM, and market logic.
        Use the provided context.
        """
        user_prompt = f"Topic: {topic}\n\nContext:\n{context}"
        return llm_client.generate_response(system_prompt, user_prompt)

investor_pitch = InvestorPitchTool()
