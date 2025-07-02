# Local LLM-based Personal Finance: Transaction Pre-processing & Analysis

This project provides Python scripts to preprocess exported bank transaction CSV files, categorize them using a local LLM (Ollama/Llama 3), analyze spending, and generate privacy-conscious reports.

## Features
- Cleans and standardizes merchant names
- Robust date and amount parsing
- Categorizes transactions using a local LLM (Ollama/Llama 3)
- Batch and single transaction categorization
- Spending analysis and recurring transaction detection
- Generates text and chart-based reports
- Command-line interface (CLI) for pre-processing

## Requirements
- Python 3.7+
- pandas
- requests
- matplotlib

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Workflow Overview
1. **Preprocess CSV**: Clean and standardize your exported bank transactions.
2. **Categorize Transactions**: Use a local LLM (Ollama/Llama 3) to assign categories.
3. **Analyze & Report**: Analyze spending, find recurring transactions, and generate reports.

## Usage

### 1. Preprocess Transactions
Run the script from the command line:
```bash
python preprocess_transactions.py path/to/your/transactions.csv
```
Optionally, specify an output file:
```bash
python preprocess_transactions.py path/to/your/transactions.csv -o my_cleaned.json
```

### 2. Categorize Transactions with LLM
```python
from local_finance_llm import LocalFinanceLLM
import json

# Load cleaned transactions
with open('cleaned_transactions.json') as f:
    transactions = json.load(f)

llm = LocalFinanceLLM(model="llama3:8b")
categorized = llm.batch_categorize(transactions)

# Save categorized transactions
with open('categorized_transactions.json', 'w') as f:
    json.dump(categorized, f, indent=2)
```

### 3. Analyze Spending & Generate Reports
```python
from finance_analysis import analyze_spending, generate_report, find_recurring_transactions
from local_finance_llm import LocalFinanceLLM
import json

# Load categorized transactions
with open('categorized_transactions.json') as f:
    categorized = json.load(f)

llm = LocalFinanceLLM(model="llama3:8b")

# Analyze spending
analysis = analyze_spending(categorized, llm)

# Find recurring transactions
recurring = find_recurring_transactions(categorized, llm)

# Generate report
report_path = generate_report(analysis)
print(f"Report saved to: {report_path}")
```

## Input CSV Format
The script expects a CSV file with at least the following columns (case-insensitive):
- `date` (e.g., 2023-01-15 or 01/15/2023)
- `description` (merchant or transaction description)
- `amount` (transaction amount, can include $ or commas)

Extra columns are ignored.

## Output
- **Preprocessing**: JSON file with cleaned transactions
- **Categorization**: JSON file with category for each transaction
- **Analysis**: Text and chart-based reports in the `reports/` directory

## Example
**Input CSV:**
```
Date,Description,Amount
2023-01-15,AMZN Mktp US*2A3CD, -23.45
2023-01-16,Starbucks #1234, 4.50
2023-01-17,WholeFds, 56.78
```

**Command:**
```bash
python preprocess_transactions.py transactions.csv
```

**Categorization & Analysis:**
See the Python code examples above.

## LLM Setup
- Requires Ollama running locally with a Llama 3 model (e.g., `llama3:8b`).
- See [Ollama documentation](https://ollama.com/) for setup instructions.

## Security Considerations
Running this locally doesn't mean ignoring security:

- **Encrypted Storage**: Process data in memory and store results encrypted.
- **Access Control**: Run the service on localhost only.
- **Data Minimization**: Don't persist full transaction details after processing.
- **Regular Cleanup**: Automate deletion of temporary files.

**Expanded Example: Secure temporary file handling and encryption in Python**
```python
import tempfile
import shutil
import pandas as pd
import json
import os
# from cryptography.fernet import Fernet  # Uncomment if using Fernet for encryption

def run_analysis(csv_path, temp_dir):
    # Example: Read CSV, process, and write results to a temp file
    df = pd.read_csv(csv_path)
    # ... perform processing ...
    results = df.to_dict(orient='records')  # Dummy processing
    temp_output = os.path.join(temp_dir, 'results.json')
    with open(temp_output, 'w') as f:
        json.dump(results, f)
    return temp_output

# Example encryption function (replace with your actual encryption logic)
def encrypt_file(input_path, output_path, key):
    # with open(input_path, 'rb') as f:
    #     data = f.read()
    # fernet = Fernet(key)
    # encrypted = fernet.encrypt(data)
    # with open(output_path, 'wb') as f:
    #     f.write(encrypted)
    pass  # Placeholder for encryption logic

def process_with_cleanup(csv_path, encryption_key):
    temp_dir = tempfile.mkdtemp()
    try:
        # Process data and write to temp file
        temp_output = run_analysis(csv_path, temp_dir)
        # Encrypt the output before saving permanently
        encrypted_output = temp_output + '.enc'
        encrypt_file(temp_output, encrypted_output, encryption_key)
        print(f"Encrypted results saved to: {encrypted_output}")
        return encrypted_output
    finally:
        # Always cleanup temp files
        shutil.rmtree(temp_dir)

# Usage example:
# key = Fernet.generate_key()
# process_with_cleanup('transactions.csv', key)
```

## License
MIT 