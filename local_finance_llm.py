import requests
import json
from typing import List, Dict, Optional

class LocalFinanceLLM:
    def __init__(self, model="llama3:8b", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.categories = [
            "Food & Dining", "Transportation", "Entertainment", 
            "Utilities", "Groceries", "Shopping", "Healthcare",
            "Income", "Rent/Mortgage", "Insurance", "Education",
            "Personal Care", "Miscellaneous"
        ]
    
    def query_llm(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """Query the local LLM with retry logic"""
        url = f"{self.base_url}/api/generate"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.1
        }
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=30)
                response.raise_for_status()
                return response.json()['response'].strip()
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    print(f"Error querying Ollama after {max_retries} attempts: {e}")
                    return None
        return None
    
    def categorize_transaction(self, transaction: Dict) -> str:
        """Categorize a single transaction"""
        prompt = f'''Categorize this transaction into exactly one category.

Categories: {', '.join(self.categories)}

Examples:
- "UBER TECHNOLOGIES" → Transportation
- "WALMART GROCERY" → Groceries
- "NETFLIX.COM" → Entertainment
- "PACIFIC GAS & ELECTRIC" → Utilities

Transaction: {transaction['merchant']} for ${abs(transaction['amount'])}

Category:
'''
        response = self.query_llm(prompt)
        if response and any(cat.lower() in response.lower() for cat in self.categories):
            for cat in self.categories:
                if cat.lower() in response.lower():
                    return cat
        return "Miscellaneous"
    
    def batch_categorize(self, transactions: List[Dict], batch_size: int = 10) -> List[Dict]:
        """Process transactions in batches to respect context limits"""
        categorized = []
        for i in range(0, len(transactions), batch_size):
            batch = transactions[i:i + batch_size]
            batch_prompt = f'''Categorize these transactions. 
Categories: {', '.join(self.categories)}

Respond with a JSON array where each item has 'index' and 'category'.

Transactions:
'''
            for idx, trans in enumerate(batch):
                batch_prompt += f"{idx}: {trans['merchant']} - ${abs(trans['amount'])}\n"
            batch_prompt += "\nJSON Response:"
            response = self.query_llm(batch_prompt)
            try:
                if response is not None:
                    results = json.loads(response)
                    for item in results:
                        idx = item['index']
                        batch[idx]['category'] = item['category']
                else:
                    raise ValueError('No response from LLM')
            except:
                for trans in batch:
                    trans['category'] = self.categorize_transaction(trans)
            categorized.extend(batch)
            print(f"Processed {len(categorized)}/{len(transactions)} transactions...")
        return categorized 