import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, 
    classification_report, 
    confusion_matrix, 
    ConfusionMatrixDisplay
)
#Step 1: Loading the Data and showing relevant data and organize before the data analysis
url = "https://raw.githubusercontent.com/tarekmasryo/football-matches-2025-dataset/main/data/football_matches_2024_2025.csv"
df = pd.read_csv(url)

#Dataset size
print("-" * 40)
print("DATASET SHAPE")
print("-" * 40)
print(f"Rows (matches): {df.shape[0]}")
print(f"Columns:        {df.shape[1]}")
print()

#Show all the columns we have in the dataset
print("-" * 40)
print("ALL COLUMNS")
print("-" * 40)
for i, col in enumerate(df.columns, 1):
    print(f"{i}. {col}")
print()

#first 5 rows
print("-" * 40)
print("FIRST 5 ROWS")
print("-" * 40)
print(df.head().to_string())
print()

#All the data types in the dataset
print("-" * 40)
print("DATA TYPES")
print("-" * 40)
print(df.dtypes)
print()

#Checking for missing values
print("-" * 40)
print("MISSING VALUES")
print("-" * 40)
missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    "Missing Count": missing,
    "Missing %": missing_pct
})
# This will show only columns with missing values
has_missing = missing_df[missing_df["Missing Count"] > 0]
if len(has_missing) > 0:
    print(has_missing)
else:
    print("✅ No missing values! The dataset is clean.")
print()

#Basic statistics for the columns
print("=" * 60)
print("📈 BASIC STATISTICS (numeric columns)")
print("=" * 60)
print(df.describe().round(2).to_string())
print()

#Dataset summary
print("-" * 40)
print("DATASET SUMMARY")
print("-" * 40)
print(f"Competitions: {df['competition_name'].nunique()}, {', '.join(df['competition_name'].unique())}")
print(f"Total matches: {len(df)}")
print(f"Total teams: {df['home_team'].nunique()}")
print(f"Date range: {df['date_utc'].min()} to {df['date_utc'].max()}")
print()

#Match outcomes, relevant for the prediction
print("-" * 40)
print("MATCH OUTCOMES")
print("-" * 40)
outcome_counts = df["match_outcome"].value_counts()
outcome_pct = (df["match_outcome"].value_counts(normalize=True) * 100).round(1)
for outcome in outcome_counts.index:
    print(f" {outcome}: {outcome_counts[outcome]:4d} matches ({outcome_pct[outcome]}%)")
print()

#Save for the data analysis 
df.to_csv("football_data.csv", index=False)
print("Saved local copy as 'football_data.csv'")


#Step 2: Data analysis

print("-" * 40)
print("STEP 2: DATA ANALYSIS")
print("=" * 60)
# 1. Match Outcome Distribution: How many Home Wins vs Away Wins vs Draws 
print("\n --- Match Outcome Disribution ---")
outcome_counts = df["match_outcome"].value_counts()
outcome_pct = (df["match_outcome"].value_counts(normalize=True) * 100).round(1)
for outcome in outcome_counts.index:
    print(f"{outcome}: {outcome_counts[outcome]:4d} matches ({outcome_pct[outcome]}%)")

#Match outcome bar chart
plt.figure(figsize=(8, 5))
colors = ["#2ecc71", "#e74c3c", "#3498db"]
ax = outcome_counts.plot(kind="bar", color=colors, edgecolor="black")
plt.title("Match Outcome Distribution", fontsize=14, fontweight="bold")
plt.xlabel("Outcome")
plt.ylabel("Number of Matches")
plt.xticks(rotation=0)
# Add count labels on top of each bar
for i, (count, pct) in enumerate(zip(outcome_counts, outcome_pct)):
    ax.text(i, count + 10, f"{count} ({pct}%)", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig("chart_01_outcome_distribution.png", dpi=150)
plt.show()

# 2. Match Outcome By League: Which league has more upsets
print("\n--- Match Outcomes by League ---")
league_outcomes = pd.crosstab(df["competition_name"], df["match_outcome"])
print(league_outcomes)

# Stacked Bar Chart for Match Outcomes By League
plt.figure(figsize=(10, 6))
league_outcomes_pct = league_outcomes.div(league_outcomes.sum(axis=1), axis=0) * 100
league_outcomes_pct.plot(kind="barh", stacked=True, color=colors, edgecolor="black", figsize=(10, 6))
plt.title("Match Outcome Distribution by League (%)", fontsize=14, fontweight="bold")
plt.xlabel("Percentage (%)")
plt.ylabel("")
plt.legend(title="Outcome", bbox_to_anchor=(1.02, 1))
plt.tight_layout()
plt.savefig("chart_02_outcomes_by_league.png", dpi=150)
plt.show()

# 3. Goals Per Match Distribution:  How many goals are typical?
print("\n --- Goals Per Match Statistics ---")
print(f" Average goals per match: {df['total_goals'].mean():.2f}")
print(f" Median goals per match: {df['total_goals'].median():.2f}")
print(f" Max goals in a match: {df['total_goals'].max()}")
print(f" Matches with 0 goals: {(df['total_goals'] == 0).sum()}")

#Histogram Of Total Goals
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="total_goals", bins=range(0, df["total_goals"].max() + 2),
             color="#3498db", edgecolor="black")
plt.title("Distribution of Total Goals Per Match", fontsize=14, fontweight="bold")
plt.xlabel("Total Goals")
plt.ylabel("Number of Matches")
plt.xticks(range(0, df["total_goals"].max() + 1))
plt.tight_layout()
plt.savefig("chart_03_goals_distribution.png", dpi=150)
plt.show()

# 4. Home vs Away Goals: Is there a home advantage?
print("\n--- Home vs Away Goals ---")
print(f" Average home goals: {df['fulltime_home'].mean():.2f}")
print(f" Average away goals: {df['fulltime_away'].mean():.2f}")
print(f" Home advantage: {df['fulltime_home'].mean() - df['fulltime_away'].mean():.2f} more goals at home")

# Box Plot for Home vs Away Comparison
plt.figure(figsize=(8, 5))
goals_melted = pd.DataFrame({
    "Goals": pd.concat([df["fulltime_home"], df["fulltime_away"]], ignore_index=True),
    "Type": ["Home Goals"] * len(df) + ["Away Goals"] * len(df)
})
sns.boxplot(data=goals_melted, x="Type", y="Goals", palette=["#2ecc71", "#e74c3c"])
plt.title("Home vs Away Goals Distribution", fontsize=14, fontweight="bold")
plt.ylabel("Goals Scored")
plt.xlabel("")
plt.tight_layout()
plt.savefig("chart_04_home_vs_away_goals.png", dpi=150)
plt.show()

# 5. Average Goals By League: Which league is most intresting
print("\n --- Average Goals By Leagues ---")
avg_goals_league = df.groupby("competition_name")["total_goals"].mean().sort_values(ascending=False)
for league, avg in avg_goals_league.items():
    print(f"  {league:<25s}: {avg:.2f} goals/match")

#Bar Chart for Average Goals By League
plt.figure(figsize=(10, 5))
avg_goals_league.plot(kind="bar", color="#9b59b6", edgecolor="black")
plt.title("Average Goals Per Match by League", fontsize=14, fontweight="bold")
plt.xlabel("")
plt.ylabel("Average Goals")
plt.xticks(rotation=45, ha="right")
# Add value labels
for i, val in enumerate(avg_goals_league):
    plt.text(i, val + 0.03, f"{val:.2f}", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig("chart_05_avg_goals_by_league.png", dpi=150)
plt.show()

# 6. Home Win Rate By League: Where is home advantage strongest?
print("\n--- Home Win Rate by League ---")
leagues = df["competition_name"].unique()
home_win_rates = {}
 
for league in leagues:
    league_matches = df[df["competition_name"] == league]
    total = len(league_matches)
    home_wins = len(league_matches[league_matches["match_outcome"] == "Home Win"])
    rate = (home_wins / total) * 100
    home_win_rates[league] = rate
 
# Sort from highest to lowest
rates_series = pd.Series(home_win_rates).sort_values(ascending=False)
 
for league, rate in rates_series.items():
    print(f"  {league:<25s}: {rate:.1f}%")

# 7. Correlation Heatmap For ML model
print("\n--- Correlation Between Numeric Features ---")
numeric_cols = ["fulltime_home", "fulltime_away", "halftime_home", "halftime_away",
                "goal_difference", "total_goals", "home_points", "away_points"]
corr_matrix = df[numeric_cols].corr()
 
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="RdYlBu_r",
            center=0, square=True, linewidths=0.5)
plt.title("Correlation Heatmap of Match Features", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("chart_06_correlation_heatmap.png", dpi=150)
plt.show()

# 8. Halftime vs Fulltime Relationship: Does leading at halftime mean you win?
print("\n--- Halftime Leading to Fulltime Win ---")
df["halftime_result"] = np.where(
    df["halftime_home"] > df["halftime_away"], "Home Leading",
    np.where(df["halftime_home"] < df["halftime_away"], "Away Leading", "Draw at HT")
)
ht_vs_ft = pd.crosstab(df["halftime_result"], df["match_outcome"], normalize="index") * 100
print(ht_vs_ft.round(1))

# Bar Chart for Halftime vs Fulltime Outcome
plt.figure(figsize=(10, 6))
ht_vs_ft.plot(kind="bar", color=colors, edgecolor="black", figsize=(10, 6))
plt.title("How Often Does the Halftime Leader Win?", fontsize=14, fontweight="bold")
plt.xlabel("Halftime Situation")
plt.ylabel("Percentage (%)")
plt.xticks(rotation=0)
plt.legend(title="Final Outcome", bbox_to_anchor=(1.02, 1))
plt.tight_layout()
plt.savefig("chart_07_halftime_vs_fulltime.png", dpi=150)
plt.show()

print("-" * 40)
print("Data analysis complete !")
print("-" * 40)








