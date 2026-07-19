import duckdb
import pandas as pd
import matplotlib.pyplot as plt

conn = duckdb.connect("bank_ledger.db")

# Finding only negative amounts, so we can filter out deposits (to find spending)
spending_query = """
    SELECT
        tc.category_name,
        ABS(SUM(t.amount)) AS total_spent
    FROM transactions t
    JOIN Transaction_categories tc ON t.category_id = tc.category_id
    WHERE t.amount < 0
    GROUP BY tc.category_name
    ORDER BY total_spent DESC;
"""
df_spending = conn.execute(spending_query).fetchdf()

# Finding total asset balance by account type
balance_query = """
    SELECT
        act.type_name,
        SUM(acc.balance) AS total_balance
    FROM Accounts acc
    JOIN Account_types act ON acc.account_type_id = act.account_type_id
    GROUP BY act.type_name;
"""
df_balance = conn.execute(balance_query).fetchdf()
conn.close()

# Matplotlib Bar Chart and Pie Chart
# Visual design
bg_colour = '#f7f9fa'
bar_colour = '#003153'
grid_colour = '#ffffff'
pie_colours = ['#003153', '#2a52be', '#6495ed']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
fig.patch.set_facecolor(bg_colour)

# Left panel (spending values - bar chart)
ax1.set_facecolor(bg_colour)
ax1.bar(df_spending['category_name'], df_spending['total_spent'], color=bar_colour, edgecolor='black', zorder=3)

ax1.set_title('Total outbound spending volume', fontsize=14, fontweight='bold', pad=15, color='#1a1a1a')
ax1.set_xlabel('Transaction Category', fontsize=11, labelpad=8, color='#333333')
ax1.set_ylabel('Total Expenditure (£)', fontsize=11, labelpad=8, color='#333333')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color('#cccccc')
ax1.spines['bottom'].set_color('#cccccc')
ax1.grid(axis='y', linestyle='-', color=grid_colour, linewidth=1.2, zorder=0)
ax1.tick_params(colors='#333333', labelsize=9)

ax1.set_xticks(range(len(df_spending['category_name'])))
ax1.set_xticklabels(df_spending['category_name'], rotation=15, ha='right')

# Right panel (asset distribution - pie chart)
ax2.set_facecolor(bg_colour)
wedges, texts, autotexts = ax2.pie(
    df_balance['total_balance'],
    labels=df_balance['type_name'],
    autopct='%1.1f%%',
    startangle=140,
    colors=pie_colours,
    wedgeprops={'edgecolor': 'black', 'linewidth': 1, 'antialiased': True}
)

# Style adjustments for the pie chart
ax2.set_title('Total Asset Distribution by Account Type', fontsize=14, fontweight='bold', pad=15, color='#1a1a1a')
plt.setp(texts, color='#333333', fontsize=11)
plt.setp(autotexts, color='white', weight='bold', fontsize=10)


# Rendering
plt.suptitle('Bank Ledger Analytics Dashboard', fontsize=18, fontweight='bold', y=0.98, color='#1a1a1a')
plt.tight_layout()
plt.show()
