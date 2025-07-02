import pandas as pd
import json
from datetime import datetime
import re
import argparse
import sys


def clean_merchant_name(merchant):
    """Standardize merchant names for consistency"""
    if not isinstance(merchant, str):
        return "Unknown"
    # Remove common suffixes and clean up
    merchant = re.sub(r'#\d+', '', merchant)  # Remove store numbers
    merchant = re.sub(r'\*\d+', '', merchant)  # Remove transaction IDs
    merchant = merchant.strip().upper()
    
    # Map common variations
    merchant_map = {
        'AMZN': 'AMAZON',
        'AMAZONCOM': 'AMAZON',
        'AMAZON.COM': 'AMAZON',
        'STARBUCKS': 'STARBUCKS',
        'SBUX': 'STARBUCKS',
        'WHOLEFDS': 'WHOLE FOODS',
        'WHOLE FOODS MARKET': 'WHOLE FOODS'
    }
    
    for pattern, replacement in merchant_map.items():
        if pattern in merchant:
            return replacement
    
    return merchant

def parse_date(date_str):
    """Parse date string into ISO format (YYYY-MM-DD) if possible"""
    if not isinstance(date_str, str):
        return str(date_str)
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_str, fmt).date().isoformat()
        except Exception:
            continue
    return date_str  # fallback to original if parsing fails

def clean_amount(amount):
    """Clean and convert amount to float"""
    try:
        return float(str(amount).replace('$', '').replace(',', '').strip())
    except Exception:
        return 0.0

def preprocess_transactions(csv_path):
    """Load and clean transaction data"""
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)
    
    # Standardize column names
    df.columns = [col.lower().strip() for col in df.columns]
    
    # Clean merchant names
    if 'description' in df.columns:
        df['clean_merchant'] = df['description'].apply(clean_merchant_name)
    else:
        df['clean_merchant'] = 'Unknown'
    
    transactions = []
    for _, row in df.iterrows():
        date_val = row['date'] if 'date' in row else ''
        amount_val = row['amount'] if 'amount' in row else 0.0
        desc_val = row['description'] if 'description' in row else ''
        clean_merchant_val = row['clean_merchant'] if 'clean_merchant' in row else desc_val
        transaction = {
            "date": parse_date(date_val),
            "merchant": clean_merchant_val,
            "amount": clean_amount(amount_val),
            "original_description": desc_val
        }
        transactions.append(transaction)
    
    return transactions

def main():
    parser = argparse.ArgumentParser(description="Preprocess bank transaction CSVs for LLM analysis.")
    parser.add_argument('csv_path', help='Path to the input CSV file')
    parser.add_argument('-o', '--output', default='cleaned_transactions.json', help='Output JSON file (default: cleaned_transactions.json)')
    args = parser.parse_args()

    transactions = preprocess_transactions(args.csv_path)
    try:
        with open(args.output, 'w') as f:
            json.dump(transactions, f, indent=2)
        print(f"Processed {len(transactions)} transactions. Output written to {args.output}")
    except Exception as e:
        print(f"Error writing JSON: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 