import sys
sys.path.append('src')

from load_data import load_data
from preprocess import preprocess_data
from rfm import calculate_rfm
from clustering import run_clustering

def main():
    print("=" * 50)
    print("  CUSTOMER SEGMENTATION PIPELINE")
    print("=" * 50)

    print("\n📂 STEP 1 — Loading data...")
    df = load_data()
    print(f"   Loaded {df.shape[0]:,} rows")

    print("\n🧹 STEP 2 — Cleaning data...")
    df_clean = preprocess_data()
    print(f"   Clean rows: {df_clean.shape[0]:,}")

    print("\n📊 STEP 3 — Calculating RFM scores...")
    rfm = calculate_rfm()
    print(f"   Unique customers: {rfm.shape[0]:,}")

    print("\n🤖 STEP 4 — Running K-Means clustering...")
    results = run_clustering()

    print("\n" + "=" * 50)
    print("  PIPELINE COMPLETE!")
    print("=" * 50)
    print("\nFinal segment breakdown:")
    print(results['Segment'].value_counts())
    print(f"\n✅ Results saved to output/customer_segments.csv")

if __name__ == '__main__':
    main()