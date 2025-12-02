from app.llm_client import llm_client

class AudienceClassifierTool:
    def classify(self, query: str) -> str:
        """
        Classifies the target audience for a given query.
        Returns one of: 'LINKEDIN', 'POLICY_US', 'INVESTOR', 'EGYPT_GOV', 'TECHNICAL', 'GENERAL'
        """
        system_prompt = """
        You are an expert audience classifier for the SDC-36 initiative.
        Classify the user's request into one of the following categories:
        - LINKEDIN: Social media posts, public announcements.
        - POLICY_US: U.S. government, policy makers, formal briefs.
        - INVESTOR: Financial, ROI, market analysis, pitch decks.
        - EGYPT_GOV: Egyptian government, sovereign strategy, local partnerships.
        - TECHNICAL: Engineering, architecture, subsea cables, AI infrastructure.
        - GENERAL: General inquiries.
        
        Return ONLY the category name.
        """
        response = llm_client.generate_response(system_prompt, query, temperature=0.0)
        return response.strip().upper()

audience_classifier = AudienceClassifierTool()
