import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from app.llm_client import LLMClient

class TestLLMClient(unittest.TestCase):
    def setUp(self):
        self.client = LLMClient()

    @patch('app.llm_client.OpenAI')
    def test_successful_connection(self, MockOpenAI):
        print("\nTest: Successful connection")
        mock_instance = MockOpenAI.return_value
        mock_instance.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="Hello from OpenAI!"))
        ]
        
        response = self.client.generate_response("System", "User")
        self.assertEqual(response, "Hello from OpenAI!")
        print("✅ Passed")

    @patch('app.llm_client.OpenAI')
    def test_connection_error_and_retry(self, MockOpenAI):
        print("\nTest: Connection error and retry")
        mock_instance = MockOpenAI.return_value
        
        # Configure side_effect: first call raises, second call succeeds
        # Note: We need to ensure the return value for the second call is structured correctly
        success_response = MagicMock()
        success_response.choices = [MagicMock(message=MagicMock(content="Retry successful!"))]
        
        mock_instance.chat.completions.create.side_effect = [
            Exception("Connection error"),
            success_response
        ]
        
        response = self.client.generate_response("System", "User")
        
        # Verify that OpenAI was instantiated twice (initial + retry)
        # Wait, _ensure_client calls OpenAI() only if self.client is None or force_reinit is True
        # 1. First attempt: _ensure_client(False) -> calls OpenAI() (since self.client is None)
        # 2. Exception happens
        # 3. Retry loop: _ensure_client(True) -> calls OpenAI() again
        
        self.assertEqual(MockOpenAI.call_count, 2)
        self.assertEqual(response, "Retry successful!")
        print("✅ Passed")

    @patch('app.llm_client.OpenAI')
    def test_persistent_error(self, MockOpenAI):
        print("\nTest: Persistent error")
        mock_instance = MockOpenAI.return_value
        mock_instance.chat.completions.create.side_effect = Exception("Persistent error")
        
        response = self.client.generate_response("System", "User")
        
        self.assertIn("Error: Persistent error", response)
        print("✅ Passed")

if __name__ == '__main__':
    unittest.main()
