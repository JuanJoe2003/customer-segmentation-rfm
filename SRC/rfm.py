import pandas as pd
import sys
sys.path.append('src')
from preprocess import preprocess_data

def calculate_rfm():
    df = preprocess_data()

    # Reference date — one day after the last purchase in dataset
    reference_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    print("Reference date:", reference_date)

    # Build RFM table — one row per customer
    rfm = df.groupby('Customer ID').agg(
        Recency   = ('InvoiceDate', lambda x: (reference_date - x.max()).days),
        Frequency = ('Invoice',     'nunique'),
        Monetary  = ('TotalPrice',  'sum')
    ).reset_index()

    print("\n✅ RFM table created!")
    print("Shape:", rfm.shape)
    print("\nSample:")
    print(rfm.head(10))
    print("\nBasic stats:")
    print(rfm[['Recency','Frequency','Monetary']].describe().round(2))

    return rfm

if __name__ == '__main__':
    rfm = calculate_rfm()