import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable

df = pd.read_csv("county_economic_status_2024.csv", skiprows = 4, 
    skipfooter = 2, engine = "python", thousands = ',')


df.columns = [
    'FIPS','State','County','ArcCounty','EconStatus2024','UnempRate',
    'Income2021','Poverty','UnempPctUS','PCMIPctUS','PCMInvUS',
    'PovertyPctUS', 'CompIndex2024', 'IndexRank', 'Quartile'
]
df = df.iloc[1:, :]

print("Poverty Rate Summary Statistics")
print("Mean Poverty Rate:", df["Poverty"].mean())
print("Standard Deviation of Poverty Rate:", df["Poverty"].std())
print("Minimum Poverty Rate:", df["Poverty"].min())
print("Maximum Poverty Rate:", df["Poverty"].max())

print(type(df['State']))

print(df['State'].value_counts())

df["Income2021"] = pd.to_numeric(df["Income2021"], errors="coerce")
df["Poverty"] = pd.to_numeric(df["Poverty"], errors="coerce")

grouped = df.groupby("State").agg(
    counties=("County", "count"),
    mean_income=("Income2021", "mean"),
    median_income=("Income2021", "median"),
    mean_poverty=("Poverty", "mean")
)

top10 = grouped.sort_values("counties", ascending=False).head(10)

table = PrettyTable()
table.field_names = ["State", "# Counties", "PCI (Mean)", "PCI (Median)", "Poverty Rate"]

for state, row in top10.iterrows():
    table.add_row([
        state,
        row["counties"],
        f"{row['mean_income']:.2f}",
        f"{row['median_income']:.2f}",
        f"{row['mean_poverty']:.2f}"
    ])

print("Top 10 States by Number of Counties:")
print(table)

filtered = grouped[grouped.index != "District of Columbia"]


bottom10 = filtered.sort_values("counties", ascending=True).head(10)


bottom_table = PrettyTable()
bottom_table.field_names = ["State", "# Counties", "PCI (Mean)", "PCI (Median)", "Poverty Rate"]


for state, row in bottom10.iterrows():
    bottom_table.add_row([
        state,
        row["counties"],
        f"{row['mean_income']:.2f}",
        f"{row['median_income']:.2f}",
        f"{row['mean_poverty']:.2f}"
    ])


print("Bottom 10 States by Number of Counties (excluding D.C.):")
print(bottom_table)