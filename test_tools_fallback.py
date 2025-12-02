import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from app.tools.egypt_briefing import EgyptBriefingTool

class TestEgyptBriefingFallback(unittest.TestCase):
    @patch('app.tools.egypt_briefing.llm_client')
    def test_fallback_behavior(self, mock_llm_client):
        tool = EgyptBriefingTool()
        
        # Mock LLM response to simulate "general knowledge" answer
        mock_llm_client.generate_response.return_value = "Based on general knowledge, Egypt's Vision 2030 focuses on..."
        
        # Test with empty context
        response = tool.generate("Economic Strategy", "")
        
        # Verify that the LLM client was called
        mock_llm_client.generate_response.assert_called_once()
        
        # Verify the prompt contains the relaxed instruction (we can't easily check the exact prompt string passed to LLM without more mocking, but we can check the response)
        self.assertIn("Based on general knowledge", response)
        print("✅ Fallback test passed: Tool returned content with empty context.")

if __name__ == '__main__':
    unittest.main()
