import tempfile
import shutil
import os
import pandas as pd
import json
# from cryptography.fernet import Fernet  # Uncomment if using Fernet for encryption

"""
secure_processing.py
Reusable utilities for secure, privacy-conscious data processing:
- Secure temporary file handling
- Optional encrypted output
- Automated cleanup
"""

def run_analysis(csv_path, temp_dir):
    """
    Example analysis: Reads a CSV, processes it, and writes results to a temp file.
    Replace this with your actual processing logic.
    """
    df = pd.read_csv(csv_path)
    # ... perform processing ...
    results = df.to_dict(orient='records')  # Dummy processing
    temp_output = os.path.join(temp_dir, 'results.json')
    with open(temp_output, 'w') as f:
        json.dump(results, f)
    return temp_output

# Example encryption function (replace with your actual encryption logic)
def encrypt_file(input_path, output_path, key):
    """
    Encrypts the file at input_path and writes the encrypted data to output_path.
    Uses Fernet symmetric encryption (uncomment and install cryptography to use).
    """
    # with open(input_path, 'rb') as f:
    #     data = f.read()
    # fernet = Fernet(key)
    # encrypted = fernet.encrypt(data)
    # with open(output_path, 'wb') as f:
    #     f.write(encrypted)
    pass  # Placeholder for encryption logic

def process_with_cleanup(csv_path, encryption_key=None):
    """
    Securely processes a CSV file:
    - Creates a secure temp directory
    - Runs analysis and writes results to temp file
    - Optionally encrypts the output
    - Cleans up all temp files
    Returns the path to the (optionally encrypted) output file.
    """
    temp_dir = tempfile.mkdtemp()
    try:
        # Process data and write to temp file
        temp_output = run_analysis(csv_path, temp_dir)
        if encryption_key:
            encrypted_output = temp_output + '.enc'
            encrypt_file(temp_output, encrypted_output, encryption_key)
            print(f"Encrypted results saved to: {encrypted_output}")
            return encrypted_output
        else:
            print(f"Results saved to: {temp_output}")
            return temp_output
    finally:
        # Always cleanup temp files
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    # Example usage
    # key = Fernet.generate_key()  # Uncomment if using encryption
    csv_path = 'transactions.csv'  # Replace with your CSV file
    # process_with_cleanup(csv_path, key)
    process_with_cleanup(csv_path) 