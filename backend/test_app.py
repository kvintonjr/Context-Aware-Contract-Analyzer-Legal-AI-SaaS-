import os
import unittest
import json
from unittest.mock import patch, MagicMock
from app import create_app

class ContractAnalyzerTestCase(unittest.TestCase):
    def setUp(self):
        # Set a dummy API key for testing.
        # Even though we mock the client, the code still creates an instance.
        os.environ['OPENAI_API_KEY'] = 'test-key'

    @patch('app.OpenAI')
    def test_analyze_contract_success(self, MockOpenAI):
        mock_instance = MockOpenAI.return_value
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = json.dumps({
            "summary": "This is a mock summary.",
            "risks": [{"clause": "Non-compete", "risk_level": "High", "explanation": "Mock explanation."}],
            "risk_score": 80
        })
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_instance.chat.completions.create.return_value = mock_response

        app = create_app(testing=True)
        client = app.test_client()

        payload = {"contract_text": "This is a test contract."}
        response = client.post('/analyze', data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['summary'], "This is a mock summary.")

    def test_analyze_contract_no_text(self):
        app = create_app(testing=True)
        client = app.test_client()

        payload = {"contract_text": ""}
        response = client.post('/analyze', data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('error', data)

    @patch('app.OpenAI')
    def test_analyze_contract_api_error(self, MockOpenAI):
        mock_instance = MockOpenAI.return_value
        mock_instance.chat.completions.create.side_effect = Exception("API Error")

        app = create_app(testing=True)
        client = app.test_client()

        payload = {"contract_text": "This is a test contract."}
        response = client.post('/analyze', data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
