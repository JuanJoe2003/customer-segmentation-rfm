import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys
sys.path.append('src')

# Load the final results
df = pd.read_csv('output/customer_segments.csv')

# Colors for each segment
colors = {
    'Lost Customer':     '#E8593C',
    'At-Risk Customer':  '#EF9F27',
    'Loyal Customer':    '#7F77DD',
    'VIP Champion':      '#1D9E75'
}
segment_colors = df['Segment'].map(colors)

fig = plt.figure(figsize=(16, 10))
fig.suptitle('Customer Segmentation Dashboard', fontsize=20, fontweight='bold', y=0.98)
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

# ── Chart 1 — Segment count (bar chart) ──
ax1 = fig.add_subplot(gs[0, 0])
counts = df['Segment'].value_counts()
bars = ax1.bar(range(len(counts)), counts.values,
               color=[colors[s] for s in counts.index])
ax1.set_xticks(range(len(counts)))
ax1.set_xticklabels(counts.index, rotation=15, ha='right', fontsize=8)
ax1.set_title('Customers per segment', fontweight='bold')
ax1.set_ylabel('Number of customers')
for bar, val in zip(bars, counts.values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
             str(val), ha='center', va='bottom', fontsize=9, fontweight='bold')

# ── Chart 2 — Revenue share (pie chart) ──
ax2 = fig.add_subplot(gs[0, 1])
revenue = df.groupby('Segment')['Monetary'].sum()
ax2.pie(revenue.values,
        labels=revenue.index,
        colors=[colors[s] for s in revenue.index],
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 8})
ax2.set_title('Revenue share by segment', fontweight='bold')

# ── Chart 3 — Average monetary value ──
ax3 = fig.add_subplot(gs[0, 2])
avg_monetary = df.groupby('Segment')['Monetary'].mean().sort_values(ascending=True)
bars3 = ax3.barh(range(len(avg_monetary)), avg_monetary.values,
                  color=[colors[s] for s in avg_monetary.index])
ax3.set_yticks(range(len(avg_monetary)))
ax3.set_yticklabels(avg_monetary.index, fontsize=8)
ax3.set_title('Avg spend per customer (£)', fontweight='bold')
ax3.set_xlabel('£ Average spend')
for bar, val in zip(bars3, avg_monetary.values):
    ax3.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2,
             f'£{val:,.0f}', va='center', fontsize=8, fontweight='bold')

# ── Chart 4 — Recency vs Frequency scatter ──
ax4 = fig.add_subplot(gs[1, 0:2])
for segment, group in df.groupby('Segment'):
    ax4.scatter(group['Recency'], group['Frequency'],
                c=colors[segment], label=segment,
                alpha=0.5, s=20)
ax4.set_title('Recency vs Frequency by segment', fontweight='bold')
ax4.set_xlabel('Recency (days since last purchase)')
ax4.set_ylabel('Frequency (number of orders)')
ax4.legend(fontsize=8)

# ── Chart 5 — Segment summary table ──
ax5 = fig.add_subplot(gs[1, 2])
ax5.axis('off')
summary = df.groupby('Segment').agg(
    Customers  = ('Customer ID', 'count'),
    Avg_Recency   = ('Recency',   'mean'),
    Avg_Frequency = ('Frequency', 'mean'),
    Avg_Monetary  = ('Monetary',  'mean')
).round(1).reset_index()
summary.columns = ['Segment', 'Count', 'Avg R', 'Avg F', 'Avg £']
summary['Avg £'] = summary['Avg £'].apply(lambda x: f'£{x:,.0f}')
table = ax5.table(
    cellText=summary.values,
    colLabels=summary.columns,
    cellLoc='center',
    loc='center'
)
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1.2, 1.8)
ax5.set_title('Segment summary', fontweight='bold', pad=20)

plt.savefig('output/dashboard.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Dashboard saved to output/dashboard.png")