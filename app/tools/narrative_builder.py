from app.llm_client import llm_client

class NarrativeBuilderTool:
    def build(self, key_points: str, context: str) -> str:
        """Builds a cohesive narrative from key points."""
        system_prompt = """
        You are a master storyteller for SDC-36.
        Weave the provided key points into a cohesive, compelling narrative.
        The narrative should highlight the strategic vision and impact of SDC-36.
        Use the provided context.
        """
        user_prompt = f"Key Points: {key_points}\n\nContext:\n{context}"
        return llm_client.generate_response(system_prompt, user_prompt)

narrative_builder = NarrativeBuilderTool()
