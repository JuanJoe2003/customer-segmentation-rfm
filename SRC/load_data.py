import pandas as pd

def load_data():
    df = pd.read_csv('data/online_retail_II.csv', encoding='unicode_escape')
    return df

if __name__ == '__main__':
    df = load_data()
    print("✅ Data loaded successfully!")
    print("Shape:", df.shape)
    print("\nFirst 3 rows:")
    print(df.head(3))
    print("\nColumn names:")
    print(df.columns.tolist())