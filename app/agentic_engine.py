from pydantic import BaseModel
from app.tools.audience_classifier import audience_classifier
from app.tools.linkedin_writer import linkedin_writer
from app.tools.investor_pitch import investor_pitch
from app.tools.us_policy_brief import us_policy_brief
from app.tools.egypt_briefing import egypt_briefing
from app.tools.diplomacy_filter import diplomacy_filter
from app.tools.tech_explainer import tech_explainer
from app.tools.narrative_builder import narrative_builder
from app.rag_vertex import vertex_rag

class GenerationRequest(BaseModel):
    query: str

class AgenticEngine:
    def process(self, request: GenerationRequest):
        query = request.query
        
        # 1. Classify Audience
        audience = audience_classifier.classify(query)
        print(f"Detected Audience: {audience}")

        if audience == "LINKEDIN":
            return self._linkedin_chain(query)
        elif audience == "POLICY_US":
            return self._us_policy_chain(query)
        elif audience == "INVESTOR":
            return self._investor_chain(query)
        elif audience == "EGYPT_GOV":
            return self._egypt_chain(query)
        elif audience == "TECHNICAL":
            return self._technical_chain(query)
        else:
            return self._general_chain(query)

    def _log_context(self, source: str, chunks: list):
        print(f"[{source}] Retrieved {len(chunks)} chunks.")
        for i, chunk in enumerate(chunks):
            print(f"[{source}] Chunk {i+1} preview: {chunk[:100]}...")

    def _linkedin_chain(self, query: str):
        # VertexRAG (top 2 chunks)
        context_chunks = vertex_rag.search(query, num_neighbors=2)
        self._log_context("LinkedIn", context_chunks)
        context = "\n".join(context_chunks)
        # LinkedInWriterTool
        return linkedin_writer.generate(query, context)

    def _us_policy_chain(self, query: str):
        # Deep VertexRAG (8-12 chunks)
        context_chunks = vertex_rag.search(query, num_neighbors=10)
        self._log_context("USPolicy", context_chunks)
        context = "\n".join(context_chunks)
        # USPolicyBriefTool
        draft = us_policy_brief.generate(query, context)
        # DiplomacyFilterTool
        return diplomacy_filter.filter(draft)

    def _investor_chain(self, query: str):
        # VertexRAG targeting finance/tech
        context_chunks = vertex_rag.search(query, num_neighbors=5)
        self._log_context("Investor", context_chunks)
        context = "\n".join(context_chunks)
        # InvestorPitchTool
        pitch = investor_pitch.generate(query, context)
        # TechExplainerTool (optional addition for depth)
        tech_context = tech_explainer.explain(query, context)
        return f"{pitch}\n\nTechnical Context:\n{tech_context}"

    def _egypt_chain(self, query: str):
        # VertexRAG targeting sovereign strategy
        context_chunks = vertex_rag.search(query, num_neighbors=5)
        self._log_context("Egypt", context_chunks)
        context = "\n".join(context_chunks)
        # EgyptBriefingTool
        brief = egypt_briefing.generate(query, context)
        # NarrativeBuilderTool
        return narrative_builder.build(brief, context)

    def _technical_chain(self, query: str):
        # Technical VertexRAG
        context_chunks = vertex_rag.search(query, num_neighbors=5)
        self._log_context("Technical", context_chunks)
        context = "\n".join(context_chunks)
        # TechExplainerTool
        return tech_explainer.explain(query, context)

    def _general_chain(self, query: str):
        context_chunks = vertex_rag.search(query, num_neighbors=3)
        self._log_context("General", context_chunks)
        context = "\n".join(context_chunks)
        return linkedin_writer.generate(query, context) # Default to simple output

agentic_engine = AgenticEngine()
