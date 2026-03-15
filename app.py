import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

st.set_page_config(page_title="Customer Segmentation", layout="wide")

# Header
st.title("🛍️ Customer Segmentation Dashboard")
st.markdown("**RFM Analysis + K-Means Clustering** on 1,067,371 real e-commerce transactions")
st.divider()

# Load data
@st.cache_data
def load_segments():
    return pd.read_csv('Output/customer_segments.csv')

df = load_segments()

# Colors
colors = {
    'Lost Customer':     '#E8593C',
    'At-Risk Customer':  '#EF9F27',
    'Loyal Customer':    '#7F77DD',
    'VIP Champion':      '#1D9E75'
}

# ── Metric cards ──
st.subheader("📊 Segment Overview")
col1, col2, col3, col4 = st.columns(4)
segments = df['Segment'].value_counts()

with col1:
    st.metric("🟢 VIP Champions",    segments.get('VIP Champion', 0))
with col2:
    st.metric("🟣 Loyal Customers",  segments.get('Loyal Customer', 0))
with col3:
    st.metric("🟡 At-Risk Customers", segments.get('At-Risk Customer', 0))
with col4:
    st.metric("🔴 Lost Customers",   segments.get('Lost Customer', 0))

st.divider()

# ── Charts ──
st.subheader("📈 Visual Analysis")
col_left, col_right = st.columns(2)

with col_left:
    # Bar chart
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    counts = df['Segment'].value_counts()
    bars = ax1.bar(range(len(counts)), counts.values,
                   color=[colors[s] for s in counts.index])
    ax1.set_xticks(range(len(counts)))
    ax1.set_xticklabels(counts.index, rotation=15, ha='right', fontsize=9)
    ax1.set_title('Customers per segment', fontweight='bold')
    ax1.set_ylabel('Number of customers')
    for bar, val in zip(bars, counts.values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                 str(val), ha='center', fontsize=9, fontweight='bold')
    st.pyplot(fig1)

with col_right:
    # Pie chart
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    revenue = df.groupby('Segment')['Monetary'].sum()
    ax2.pie(revenue.values,
            labels=revenue.index,
            colors=[colors[s] for s in revenue.index],
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 9})
    ax2.set_title('Revenue share by segment', fontweight='bold')
    st.pyplot(fig2)

st.divider()

# ── Scatter plot ──
st.subheader("🔍 Recency vs Frequency")
fig3, ax3 = plt.subplots(figsize=(12, 5))
for segment, group in df.groupby('Segment'):
    ax3.scatter(group['Recency'], group['Frequency'],
                c=colors[segment], label=segment, alpha=0.5, s=20)
ax3.set_xlabel('Recency (days since last purchase)')
ax3.set_ylabel('Frequency (number of orders)')
ax3.legend()
ax3.set_title('Customer clusters by Recency vs Frequency', fontweight='bold')
st.pyplot(fig3)

st.divider()

# ── Summary table ──
st.subheader("📋 Segment Summary Table")
summary = df.groupby('Segment').agg(
    Customers    = ('Customer ID', 'count'),
    Avg_Recency  = ('Recency',    'mean'),
    Avg_Frequency= ('Frequency',  'mean'),
    Avg_Monetary = ('Monetary',   'mean')
).round(1).reset_index()
summary['Avg_Monetary'] = summary['Avg_Monetary'].apply(lambda x: f'£{x:,.0f}')
summary.columns = ['Segment', 'Customers', 'Avg Recency (days)', 'Avg Orders', 'Avg Spend']
st.dataframe(summary, use_container_width=True, hide_index=True)

st.divider()

# ── Raw data explorer ──
st.subheader("🔎 Explore Customer Data")
selected = st.selectbox("Filter by segment", ["All"] + list(df['Segment'].unique()))
if selected == "All":
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.dataframe(df[df['Segment'] == selected], use_container_width=True, hide_index=True)