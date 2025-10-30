import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable

df = pd.read_csv("county_economic_status_2024.csv", skiprows = 4, 
        skipfooter = 2, engine = "python", thousands = ',')

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
}
    
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))


def loadData():
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
    df["UnempRate"] = pd.to_numeric(df["UnempRate"], errors="coerce")

    grouped = df.groupby("State").agg(
        counties=("County", "count"),
        mean_income=("Income2021", "mean"),
        median_income=("Income2021", "median"),
        mean_poverty=("Poverty", "mean"),
        mean_unemp=("UnempRate", "mean")
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

    top10 = filtered.sort_values("mean_poverty", ascending=False).head(10)
    poverty_table = PrettyTable()
    poverty_table.field_names = ["State", "County", "Per capita income", "Poverty rate", "Avg Unemployment"]

    for state, row in top10.iterrows():
        poverty_table.add_row([
            state,
            row["counties"],
            f"{row['mean_income']:.2f}",
            f"{row['mean_poverty']:.2f}",
            f"{row['mean_unemp']:.2f}"
        ])

    print("Top 10 States by Average Poverty Rate (excluding D.C.):")
    print(poverty_table)

    return df

def printTableBy(df: pd.DataFrame, field: str, how_many: int, title: str) -> None:
    top = df.sort_values(field, ascending=False).head(how_many)
    top_table = PrettyTable()
    top_table.field_names = ["State", "County", "Per capita income", "Poverty rate", "Avg Unemployment"]
    for _, row in top.iterrows():
        top_table.add_row([
            row["State"],
            row["County"],
            f"{row['Income2021']:.2f}",
            f"{row['Poverty']:.2f}",
            f"{row['UnempRate']:.2f}",
        ])
    print(f"\nTop {how_many} by {field} (desc)")
    print(top_table)

    bottom = df.sort_values(field, ascending=True).head(how_many)
    bottom_table = PrettyTable()
    bottom_table.field_names = ["State", "County", "Per capita income", "Poverty rate", "Avg Unemployment"]
    for _, row in bottom.iterrows():
        bottom_table.add_row([
            row["State"],
            row["County"],
            f"{row['Income2021']:.2f}",
            f"{row['Poverty']:.2f}",
            f"{row['UnempRate']:.2f}",
        ])
    print(f"\nBottom {how_many} by {field} (asc)")
    print(bottom_table)

def createByStateBarPlot(df: pd.DataFrame, field: str, filename: str, title: str, ylabel: str) -> None:
    s = df.dropna(subset=[field]).groupby("State")[field].mean().sort_values()

    plt.figure(figsize=(12, 6))
    plt.bar(s.index, s.values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(filename, dpi=200)
    plt.close()

    print(f"Bar plot saved to {filename}")
    




def main():
    
    df = loadData()
    
    printTableBy(df, "Poverty", 10, "Counties sorted by Poverty")
    printTableBy(df, "Income2021", 5, "Counties sorted by PCI")
    printTableBy(df, "UnempRate", 3, "Counties sorted by Unemployment Rate")

    createByStateBarPlot(df, "Poverty", "by_state_poverty.png", "States by Poverty Rate", "Poverty Rate (%)")
    
    createByStateBarPlot(df, "UnempRate", "by_state_unemployment.png", "States by Avg Unemployment", "Unemployment Rate (%)")
    
    createByStateBarPlot(df, "Income2021", "by_state_income.png", "States by Per-Capita Income (2021)", "Income (USD)")

if __name__ == "__main__":
    main()