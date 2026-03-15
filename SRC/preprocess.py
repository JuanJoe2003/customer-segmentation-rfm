import pandas as pd
import sys
sys.path.append('src')
from load_data import load_data

def preprocess_data():
    df = load_data()
    
    print("=== BEFORE CLEANING ===")
    print("Shape:", df.shape)
    print("\nMissing values:")
    print(df.isnull().sum())
    
    # Step 1 — Remove rows with no Customer ID
    df = df.dropna(subset=['Customer ID'])
    
    # Step 2 — Remove cancelled orders
    df = df[~df['Invoice'].astype(str).str.startswith('C')]
    
    # Step 3 — Remove negative or zero quantity
    df = df[df['Quantity'] > 0]
    
    # Step 4 — Remove negative or zero price
    df = df[df['Price'] > 0]
    
    # Step 5 — Fix date column type
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Step 6 — Add total price column
    df['TotalPrice'] = df['Quantity'] * df['Price']
    
    print("\n=== AFTER CLEANING ===")
    print("Shape:", df.shape)
    print("\nMissing values:")
    print(df.isnull().sum())
    print("\nSample:")
    print(df.head(3))
    
    return df

if __name__ == '__main__':
    df = preprocess_data()