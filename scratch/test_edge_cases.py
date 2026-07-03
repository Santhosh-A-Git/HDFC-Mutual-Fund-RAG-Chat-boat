import requests
import time

API_URL = "http://localhost:8000/api/chat"

test_cases = [
    {
        "name": "1. Advisory / Opinion Intent",
        "query": "Which HDFC fund is best for my retirement in 10 years?"
    },
    {
        "name": "2. Out of Domain (Non-Financial)",
        "query": "What is the capital of France?"
    },
    {
        "name": "3. Out of Domain (Other Bank)",
        "query": "What is the expense ratio of SBI Small Cap Fund?"
    },
    {
        "name": "4. Gibberish / Meaningless",
        "query": "asdfghjkl"
    },
    {
        "name": "5. Vague / Broad Query",
        "query": "Tell me about HDFC"
    }
]

def run_tests():
    print("Starting Edge Case Tests against live API...\n")
    print("-" * 50)
    for case in test_cases:
        print(f"Testing: {case['name']}")
        print(f"Query: '{case['query']}'")
        
        try:
            start_time = time.time()
            response = requests.post(API_URL, json={"query": case["query"]})
            latency = time.time() - start_time
            
            print(f"Status Code: {response.status_code} (Took {latency:.2f}s)")
            
            if response.status_code == 200:
                print(f"Response:\n{response.json().get('response')}")
            else:
                print(f"Error Response:\n{response.text}")
        except Exception as e:
            print(f"Request failed: {e}")
            
        print("-" * 50)

if __name__ == "__main__":
    run_tests()
