# analysis.py
# Workforce pay equity: data checks, derived bands, descriptive comparisons,
# one Welch t-test for the gender gap, and export of the cleaned file.
#
# Run from any folder:  python script/analysis.py
# Reads:   data/pay_equity_raw.csv
# Writes:  data/cleaned_pay_equity.csv

from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "pay_equity_raw.csv"
CLEAN = ROOT / "data" / "cleaned_pay_equity.csv"

# --------------------------------------------------
# STEP 1 – Load Dataset
# --------------------------------------------------
df = pd.read_csv(RAW)
print("Data loaded:", df.shape)

# --------------------------------------------------
# STEP 2 – Data Cleaning
# --------------------------------------------------
print("\nMissing values:\n", df.isnull().sum())
print("\nDuplicates:", df.duplicated().sum())
df = df.drop_duplicates()
print("Duplicate employee IDs:", df.EmployeeID.duplicated().sum())

# --------------------------------------------------
# STEP 3 – Data Preparation
# --------------------------------------------------
for col in ["Gender", "Department", "JobRole"]:
    df[col] = df[col].astype("category")

df["ExperienceGroup"] = pd.cut(df["ExperienceYears"],
                               bins=[0, 5, 10, 15, 20],
                               labels=["0-5", "6-10", "11-15", "16-20"])

# Bands set to the observed salary range (28,331 to 63,463), in 10,000 steps.
df["SalaryBand"] = pd.cut(df["Salary"],
                          bins=[25000, 35000, 45000, 55000, 65000],
                          labels=["Low", "Medium", "High", "Very High"])

assert df.SalaryBand.notna().all(), "Salary outside the band range"

# --------------------------------------------------
# STEP 4 – Descriptive comparisons
# --------------------------------------------------
print("\nAverage salary by gender:\n", df.groupby("Gender", observed=True)["Salary"].mean().round(2))
print("\nMedian salary by gender:\n", df.groupby("Gender", observed=True)["Salary"].median())
print("\nAverage salary by department:\n", df.groupby("Department", observed=True)["Salary"].mean().round(0))
print("\nAverage salary by experience group:\n", df.groupby("ExperienceGroup", observed=True)["Salary"].mean().round(0))
print("\nCorrelation, experience vs salary:", round(df.ExperienceYears.corr(df.Salary), 3))

# --------------------------------------------------
# STEP 5 – Gender gap: Welch t-test (descriptive support, not causal)
# --------------------------------------------------
female = df.loc[df.Gender == "Female", "Salary"]
male = df.loc[df.Gender == "Male", "Salary"]
t_stat, p_val = stats.ttest_ind(female, male, equal_var=False)
pooled_sd = (((female.var() * (len(female) - 1)) + (male.var() * (len(male) - 1)))
             / (len(female) + len(male) - 2)) ** 0.5
cohens_d = (female.mean() - male.mean()) / pooled_sd
print(f"\nGender gap (F-M): {female.mean() - male.mean():,.0f}")
print(f"Welch t = {t_stat:.3f}, p = {p_val:.3f}, Cohen's d = {cohens_d:.3f}")

print("\nDepartment gaps (F-M), Welch p-values:")
for dept, g in df.groupby("Department", observed=True):
    a = g.loc[g.Gender == "Female", "Salary"]
    b = g.loc[g.Gender == "Male", "Salary"]
    print(f"  {dept}: {a.mean() - b.mean():,.0f} (n={len(a)} F, {len(b)} M), p = {stats.ttest_ind(a, b, equal_var=False).pvalue:.2f}")

# --------------------------------------------------
# STEP 6 – Plots (display only)
# --------------------------------------------------
plt.figure(figsize=(6, 4))
sns.heatmap(df[["ExperienceYears", "Salary"]].corr(), annot=True)
plt.title("Correlation Heatmap")
plt.show()

plt.figure(figsize=(6, 4))
sns.boxplot(x="Gender", y="Salary", data=df)
plt.title("Salary Distribution by Gender")
plt.show()

# --------------------------------------------------
# STEP 7 – Export cleaned file for Power BI
# --------------------------------------------------
df.to_csv(CLEAN, index=False)
print("\nCleaned file written:", CLEAN.relative_to(ROOT))
