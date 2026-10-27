# analysis.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --------------------------------------------------
# STEP 1 – Load Dataset
# --------------------------------------------------

df = pd.read_csv("pay_equity_synthetic.csv")
print("Data Loaded Successfully!")
print(df.head())

# --------------------------------------------------
# STEP 2 – Data Cleaning
# --------------------------------------------------

print("\nMissing Values:\n", df.isnull().sum())
print("\nDuplicates:", df.duplicated().sum())

# Remove duplicates
df = df.drop_duplicates()

print("\nData Types:\n", df.dtypes)

# --------------------------------------------------
# STEP 3 – Data Preparation
# --------------------------------------------------

# Convert to category
df['Gender'] = df['Gender'].astype('category')
df['Department'] = df['Department'].astype('category')
df['JobRole'] = df['JobRole'].astype('category')

# Experience Group
df['ExperienceGroup'] = pd.cut(df['ExperienceYears'],
                               bins=[0, 5, 10, 15, 20],
                               labels=['0-5', '6-10', '11-15', '16-20'])

# Salary Band
# Bins set to the observed salary range (28,331 to 63,463). The original
# bins (20,000 to 120,000) left "Very High" empty and "High" with 4 employees.
df['SalaryBand'] = pd.cut(df['Salary'],
                          bins=[25000, 35000, 45000, 55000, 65000],
                          labels=['Low', 'Medium', 'High', 'Very High'])

print("\nData After Feature Engineering:\n", df.head())

# --------------------------------------------------
# STEP 4 – EDA (Pay Equity Analysis)
# --------------------------------------------------

print("\nAverage Salary by Gender:\n", df.groupby('Gender')['Salary'].mean())
print("\nAverage Salary by Department:\n", df.groupby('Department')['Salary'].mean())
print("\nAverage Salary by Experience Group:\n", df.groupby('ExperienceGroup')['Salary'].mean())

# Correlation Heatmap
plt.figure(figsize=(6,4))
sns.heatmap(df[['ExperienceYears', 'Salary']].corr(), annot=True)
plt.title("Correlation Heatmap")
plt.show()

# Salary Boxplot by Gender
plt.figure(figsize=(6,4))
sns.boxplot(x='Gender', y='Salary', data=df)
plt.title("Salary Distribution by Gender")
plt.show()

# --------------------------------------------------
# STEP 5 – Export Cleaned File for Power BI
# --------------------------------------------------

df.to_csv("cleaned_pay_equity.csv", index=False)
print("\nCleaned file exported: cleaned_pay_equity.csv")
