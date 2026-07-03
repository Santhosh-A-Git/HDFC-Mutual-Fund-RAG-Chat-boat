import requests
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup

url = "https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

print(f"Status Code: {response.status_code}")
print(f"Length of text: {len(soup.get_text(strip=True))}")
if "Expense Ratio" in response.text:
    print("Found 'Expense Ratio'")
else:
    print("Could not find 'Expense Ratio'")
