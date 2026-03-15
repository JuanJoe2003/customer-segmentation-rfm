import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('src')
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from rfm import calculate_rfm

def run_clustering():
    rfm = calculate_rfm()

    # Step 1 — Normalize R, F, M scores
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])

    # Step 2 — Elbow method to find best K
    inertia = []
    K_range = range(2, 11)
    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(rfm_scaled)
        inertia.append(km.inertia_)

    # Plot elbow curve
    plt.figure(figsize=(8, 4))
    plt.plot(K_range, inertia, marker='o', color='purple')
    plt.title('Elbow Method — Finding Best K')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Inertia')
    plt.xticks(K_range)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('output/elbow_curve.png')
    plt.show()
    print("✅ Elbow curve saved to output/elbow_curve.png")

    # Step 3 — Run K-Means with K=4
    k = 4
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    rfm['Cluster'] = km.fit_predict(rfm_scaled)

    # Step 4 — See what each cluster looks like
    print("\nCluster summary:")
    print(rfm.groupby('Cluster')[['Recency','Frequency','Monetary']].mean().round(2))

    # Step 5 — Label the clusters
    cluster_means = rfm.groupby('Cluster')['Recency'].mean()
    
    def label_cluster(cluster_num):
        means = rfm.groupby('Cluster')[['Recency','Frequency','Monetary']].mean()
        r = means.loc[cluster_num, 'Recency']
        f = means.loc[cluster_num, 'Frequency']
        m = means.loc[cluster_num, 'Monetary']
        if r < 10 and f > 100:
            return 'VIP Champion'
        elif r < 50 and f > 50:
            return 'Loyal Customer'
        elif r < 100:
            return 'At-Risk Customer'
        else:
            return 'Lost Customer'

    rfm['Segment'] = rfm['Cluster'].apply(label_cluster)

    print("\nSegment counts:")
    print(rfm['Segment'].value_counts())

    # Step 6 — Save to CSV
    rfm.to_csv('output/customer_segments.csv', index=False)
    print("\n✅ Saved to output/customer_segments.csv")

    return rfm

if __name__ == '__main__':
    rfm = run_clustering()