import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
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
    print("No missing values! The dataset is clean.")
print()

#Basic statistics for the columns

print("-" * 40)
print("BASIC STATISTICS")
print("-" * 40)
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

print("\n--- Match Outcome Disribution ---")
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

print("\n--- Average Goals By Leagues ---")
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
print("Data analysis completed !")
print("-" * 40)

#Step 3: Preprocessing and Feature Engineering

print("-" * 40)
print("STEP 3: PREPROCESSING & FEATURE ENGINEERING")
print("-" * 40)

# 1. Dropping Irellevant Columns

print("\n--- Dropping irellevant columns ---")
print(f"Columns before: {len(df.columns)}")

columns_to_drop = ["match_id", "referee_id", "home_team_id", "away_team_id",
                   "status", "season", "stage", "date_utc", "referee",
                   "home_points", "away_points", "halftime_result",
                   "fulltime_home", "fulltime_away", "goal_difference", "total_goals"]

df_model = df.drop(columns=columns_to_drop, errors="ignore")
print(f"Columns after: {len(df_model.columns)}")
print(f"Remaining columns: {list(df_model.columns)}")
print()

# 2. Handle Missing Values

print("--- Handle Missing Values ---")
missing_count = df_model.isnull().sum().sum()
if missing_count > 0:
    print(f"Found {missing_count} missing values")
    # Fill numeric columns with the median
    numeric_cols = df_model.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df_model[col].isnull().sum() > 0:
            median_val = df_model[col].median()
            df_model[col] = df_model[col].fillna(median_val)
            print(f"  Filled {col} with median: {median_val}")
 
    # Fill text columns with mode
    text_cols = df_model.select_dtypes(include=["object"]).columns
    for col in text_cols:
        if df_model[col].isnull().sum() > 0:
            mode_val = df_model[col].mode()[0]
            df_model[col] = df_model[col].fillna(mode_val)
            print(f"  Filled {col} with mode: {mode_val}")
    print("All missing values handled!")
else:
    print("No missing values found - dataset is clean!")
print()

# 3. Encoding The Data Froe The ML

print("--- Encode The Data ---")

label_encoders = {}
columns_to_encode = ["home_team", "away_team", "competition_name", "competition_code"]

for col in columns_to_encode:
    le = LabelEncoder()
    df_model[col + "_encoded"] = le.fit_transform(df_model[col])
    label_encoders[col] = le
    print(f"Encoded {col}: {df_model[col + '_encoded'].nunique()} unique values")

df_model = df_model.drop(columns=columns_to_encode)
print()

# 4. Feature Engineering

print("--- Feature Engineering ---")

# Feature 1: Did home team score in the first half?
df_model["home_scored_first_half"] = (df_model["halftime_home"] > 0).astype(int)
 
# Feature 2: Did away team score in the first half?
df_model["away_scored_first_half"] = (df_model["halftime_away"] > 0).astype(int)
 
# Feature 3: Halftime goal difference
df_model["halftime_goal_diff"] = df_model["halftime_home"] - df_model["halftime_away"]

# Feature 4: Total halftime goals
df_model["halftime_total_goals"] = df_model["halftime_home"] + df_model["halftime_away"]

print("New features created:")
new_features = ["home_scored_first_half", "away_scored_first_half",
                "halftime_goal_diff", "halftime_total_goals"]
for features in new_features:
    print(f"  {features}: min={df_model[features].min()}, max={df_model[features].max()}, mean={df_model[features].mean():.2f}")
print()

# 5. Separate Features (X) and Target (y) 

print("--- Separate Features and Target ---")
 
# Encode the target variable (match_outcome) to numbers

target_encoder = LabelEncoder()
y = target_encoder.fit_transform(df_model["match_outcome"])
print(f"Target classes: {list(target_encoder.classes_)}")
print(f"  Encoded as:{list(range(len(target_encoder.classes_)))}")
 
# X = everything EXCEPT the target

X = df_model.drop(columns=["match_outcome"])
 
print(f"\nFeatures (X): {X.shape[1]} columns")
print(f"Target (y):   {len(y)} values")
print(f"Feature names: {list(X.columns)}")
print()

# 6. Normaliztaion And Standardization

print("--- Normalization And Standardization")

print("\nBefore scaling (first 3 rows):")
print(X.head(3).to_string())

# I chose the standard scaler since football have a lot of outliers like one sided matches.

scaler = StandardScaler()
X_scaled = pd.DataFrame(
    scaler.fit_transform(X), 
    columns=X.columns, 
    index=X.index
)

print("\nAfter StandardScaler (first 3 rows):")
print(X_scaled.head(3).round(3).to_string())

# Show The Effect Of Scalling 

print("\nScaling comparison for 'halftime_home':")
print(f"  Before: min={X['halftime_home'].min()}, max={X['halftime_home'].max()}, mean={X['halftime_home'].mean():.2f}")
print(f"  After:  min={X_scaled['halftime_home'].min():.3f}, max={X_scaled['halftime_home'].max():.3f}, mean={X_scaled['halftime_home'].mean():.3f}")
 
print()
 
# Plot: Before vs After Scaling Comparison

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
 
# Before scaling

axes[0].set_title("Before Scaling", fontsize=12, fontweight="bold")
axes[0].boxplot([X["halftime_home"], X["halftime_away"], X["matchday"]],
                labels=["halftime_home", "halftime_away", "matchday"])
axes[0].set_ylabel("Original Values")
 
# After StandardScaler

axes[1].set_title("After StandardScaler", fontsize=12, fontweight="bold")
axes[1].boxplot([X_scaled["halftime_home"], X_scaled["halftime_away"], X_scaled["matchday"]],
                labels=["halftime_home", "halftime_away", "matchday"])
axes[1].set_ylabel("Standardized Values")
 
plt.suptitle("Effect of Scaling on Features", fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("chart_08_scaling_comparison.png", dpi=150)
plt.show()

# 7. Train/Test Split

print("--- Train/Test Split")
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

print(f"Training set: {X_train.shape[0]} matches ({X_train.shape[0]/len(X_scaled)*100:.0f}%)")
print(f"Test set: {X_test.shape[0]} matches ({X_test.shape[0]/len(X_scaled)*100:.0f}%)")

print()
print("-" * 40)
print("PREPROCESSING COMPLETE!")
print("-" * 40)

# Step 4: Machine Leaning Model

print("-" * 40)
print("STEP 4: MACHINE LEARNING MODEL")
print("-" * 40)

# 1. Decision Tree Model
print("\n--- Decision Tree Model---")

dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)

# Make predictions on the test set
dt_predictions = dt_model.predict(X_test)

# Check accuracy
dt_accuracy = accuracy_score(y_test, dt_predictions)
print(f"Decision Tree Accuracy: {dt_accuracy * 100:.1f}%")

# 2. Random Forest Model

print("\n--- Random Forest Model")

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions on the test set

rf_predictions = rf_model.predict(X_test)
 
# Check accuracy

rf_accuracy = accuracy_score(y_test, rf_predictions)
print(f"Random Forest Accuracy: {rf_accuracy * 100:.1f}%")

# 3. Comparing The Models

print("\n--- Model Comparison ---")
print(f"Decision Tree: {dt_accuracy * 100:.1f}%")
print(f"Random Forest: {rf_accuracy * 100:.1f}%")
if rf_accuracy >= dt_accuracy:
    print("Winner: Random Forest!")
    best_model = rf_model
    best_predictions = rf_predictions
    best_name = "Random Forest"
else:
    print("Winner: Decision Tree!")
    best_model = dt_model
    best_predictions = dt_predictions
    best_name = "Decision Tree"
 
# 4. Model Accuracy Comparison
plt.figure(figsize=(8, 5))
models = ["Decision Tree", "Random Forest"]
accuracies = [dt_accuracy * 100, rf_accuracy * 100]
bar_colors = ["#3498db", "#2ecc71"]
bars = plt.bar(models, accuracies, color=bar_colors, edgecolor="black")
for bar, acc in zip(bars, accuracies):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
             f"{acc:.1f}%", ha="center", fontsize=12, fontweight="bold")
plt.title("Model Accuracy Comparison", fontsize=14, fontweight="bold")
plt.ylabel("Accuracy (%)")
plt.ylim(0, 105)
plt.tight_layout()
plt.savefig("chart_09_model_comparison.png", dpi=150)
plt.show()

# Step 5: Model Evaluation

print("-" * 40)
print(f"STEP 5: MODEL EVALUATION (using {best_name})")
print("-" * 40)

# 1. Model Report

print("\n--- Model Report ---")

class_names = list(target_encoder.classes_)
print(classification_report(y_test, best_predictions, target_names=class_names))

# 2. Confusion Matrix

print("\n--- Confusion Matrix ---")

cm = confusion_matrix(y_test, best_predictions)
print("Rows = Actual outcome, Columns = Predicted outcome")
print()

# 3. Confusion Matrix Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=class_names, yticklabels=class_names)
plt.title(f"Confusion Matrix - {best_name}", fontsize=14, fontweight="bold")
plt.xlabel("Predicted Outcome")
plt.ylabel("Actual Outcome")
plt.tight_layout()
plt.savefig("chart_10_confusion_matrix.png", dpi=150)
plt.show()

# 4. Features Importance

print("--- Feature Importance ---")
print("Which features matter most for prediction")

feature_importance = pd.Series(
    best_model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

# Top 10 Features

for i, (feature, importance) in enumerate(feature_importance.head(10).items(), 1):
    bar = "#" * int(importance * 50)
    print(f"  {i:2d}. {feature} {importance:.3f} {bar}")

# Plot: Feature Importance
plt.figure(figsize=(10, 6))
top_features = feature_importance.head(10)
top_features.plot(kind="barh", color="#9b59b6", edgecolor="black")
plt.title(f"Top 10 Most Important Features - {best_name}", fontsize=14, fontweight="bold")
plt.xlabel("Importance Score")
plt.ylabel("")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("chart_11_feature_importance.png", dpi=150)
plt.show()

# Step 6: Save Results for Tableau/PowerBI
print("\n--- Save Results for Tableau/PowerBI ---")
 
# Add predictions back to the original data for visualization
results_df = df.copy()
# Only add predictions for test set rows
results_df["predicted_outcome"] = ""
test_indices = X_test.index.tolist()
for i, idx in enumerate(test_indices):
    results_df.loc[idx, "predicted_outcome"] = class_names[best_predictions[i]]
 
# Mark which rows were in training vs test set
results_df["dataset_split"] = "Training"
for idx in test_indices:
    results_df.loc[idx, "dataset_split"] = "Test"
 
# Add a column showing if prediction was correct
results_df["prediction_correct"] = ""
for i, idx in enumerate(test_indices):
    actual = results_df.loc[idx, "match_outcome"]
    predicted = results_df.loc[idx, "predicted_outcome"]
    results_df.loc[idx, "prediction_correct"] = "Yes" if actual == predicted else "No"
 
results_df.to_csv("football_results_for_dashboard.csv", index=False)
print("Saved 'football_results_for_dashboard.csv' for Tableau/PowerBI")
print("This file contains the original data + predictions + correct/incorrect labels")
 
print()
print("-" * 40)
print("PROJECT COMPLETE!")
print("-" * 40)
print(f"\nBest model: {best_name} with {max(dt_accuracy, rf_accuracy) * 100:.1f}% accuracy")
print("\nFiles created:")
print("  - football_results_for_dashboard.csv (for Tableau/PowerBI)")











