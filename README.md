# Workforce Pay Equity Analytics

### Salary Differences by Gender, Department, Experience and Salary Band

![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?logo=scipy&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-4C72B0)
![Domain](https://img.shields.io/badge/Domain-HRM-success)
![Data Model](https://img.shields.io/badge/Data%20Model-Single%20Table-blue)

[![Dashboard Preview](screenshots/01_pay_equity_overview.png)](screenshots/01_pay_equity_overview.png)

*Select the image to view it at full size.*

---

## Project Overview

Organisations need to know whether pay differs between employee groups, and whether any difference is explained by factors such as experience or role. Simple averages show what the data contains, but not why it is there.

This project examines salary differences across gender, department, experience and salary band in a synthetic workforce dataset of 300 employees. It reports descriptive comparisons, one statistical test of the overall gender gap, and a two-page Power BI dashboard.

The results can inform whether a pay-equity review is needed and what additional data such a review would require. They do not establish whether pay discrimination exists.

### Data Source

**Data Source:** Synthetically generated for this project. The company, records, and business scenarios are fictional and are intended for learning and portfolio demonstration.

---

## Key Metrics

| Employees | Average Salary (Female) | Average Salary (Male) | Observed Gap (F − M) | Experience–Salary Correlation |
| --- | --- | --- | --- | --- |
| **300** | **42,866** | **43,049** | **−183 (−0.4%)** | **0.86** |

---

## Key Findings

All figures describe the dataset only. The Welch t-test compares female and male salaries; the department and experience comparisons are descriptive.

1. **Average salary is almost identical by gender.** Female average is 42,866 and male average is 43,049, a gap of 183 (0.4% of the male average). The median shows a similar pattern: 42,928 for women and 42,380 for men.
2. **The gender gap is not statistically significant.** Welch t-test p = 0.83, and the effect size (Cohen's d ≈ −0.03) is negligible. The 95% confidence interval for the gap runs from about −1,800 to +1,500, which includes zero.
3. **Department gaps point in both directions and none is significant.** Women's average is higher in Sales (+1,566), Finance (+713), HR (+435) and Marketing (+363). Men's average is higher in IT (−2,938) and Operations (−1,212). The smallest Welch p-value is 0.14 (IT), and Operations has only 14 male employees.
4. **Gaps within experience groups also change direction.** Women's average is higher in the 0–5 and 11–15 year groups (+368 and +498). Men's average is higher in the 6–10 and 16–20 year groups, with the largest gap in the 16–20 group (−2,490). These groups have 28 to 42 employees per gender, so the differences are not tested and should be read as descriptive.
5. **Experience is strongly associated with salary.** The correlation is 0.86. Average salary rises from about 35,500 (0–5 years) to about 51,700 (16–20 years).
6. **Women in this dataset have slightly more experience on average** (10.5 years against 9.8 years).

**What these findings do not show:** They do not show that pay discrimination exists or does not exist, and they do not identify the cause of any difference. Pay equity analysis would need role, level, performance and tenure data, and a regression that controls for them. JobRole is nested within department in this dataset, so comparisons would need to be made within roles.

---

## Business Problem and Objectives

Organisations need to understand whether pay differs between employee groups and whether experience or role explains any difference. The project aims to:

1. Describe average, median, minimum and maximum salary by gender and department.
2. Show how salary varies with experience and salary band.
3. Make the size and direction of observed gender differences explicit, with a clear note on what they do and do not show.

---

## Tools and Methodology

- **Python (pandas):** data checks for missing values, duplicates and duplicate IDs; experience groups; salary bands set to the observed range (25,000 to 65,000 in 10,000 steps).
- **SciPy:** Welch's t-test for the gender gap, and Welch tests within each department.
- **Seaborn and Matplotlib:** correlation heatmap and salary boxplot.
- **Power BI:** one data table, 8 DAX measures, two report pages with slicers, cards, charts and a scatter plot.

**Data notes**
- No missing values, duplicate rows or duplicate IDs.
- Gender: 165 male, 135 female. Binary only.
- Each of the 13 job roles belongs to one department.
- Amounts are treated as US dollars (USD). The dataset does not state a currency.

**Method notes**
- Salary is compared with a Welch t-test, which does not assume equal variance between groups.
- The department and experience comparisons are descriptive. Six department tests are run without a multiple-comparison correction; none is significant, so the correction would not change the conclusion.

---

## Repository Structure

```text
workforce-pay-equity-analytics/
├── README.md
├── dashboard/
│   └── workforce_pay_equity_dashboard.pbix
├── data/
│   ├── pay_equity_raw.csv
│   └── cleaned_pay_equity.csv
├── documentation/
│   └── measures.dax
├── script/
│   └── analysis.py
└── screenshots/
    ├── 01_pay_equity_overview.png
    └── 02_sales_drivers_and_analysis.png
```

---

## Dashboard

The Power BI file has two pages.

1. **[Executive Pay Equity Overview](screenshots/01_pay_equity_overview.png):** cards for total employees, average salary by gender and the observed gap; salary band distribution by gender; employee split by gender; average salary by gender and by department. Slicers: department and gender.
2. **[Salary Drivers & Analysis](screenshots/02_sales_drivers_and_analysis.png):** minimum and maximum salary by gender; experience against salary for each employee; average salary by experience group and gender; department pay gap. Slicers: department, gender and experience group.

The department pay-gap chart on page 2 shows values as decimal fractions of the male average (0.06 means 6%). A positive value means the male average is higher; a negative value means the female average is higher. The sign convention will be corrected in a later update.

Measures are in [`documentation/measures.dax`](documentation/measures.dax).

---

## How to Reproduce

```bash
pip install pandas scipy seaborn matplotlib
python script/analysis.py
```

The script reads `data/pay_equity_raw.csv`, prints the descriptive comparisons and the Welch test, and writes `data/cleaned_pay_equity.csv`.

**Dashboard:** open `dashboard/workforce_pay_equity_dashboard.pbix` in Power BI Desktop. If a file error appears, go to **Home → Transform data → Data source settings** and point the source to `data/cleaned_pay_equity.csv`.

---

## Limitations

- **Synthetic data.** Patterns reflect how the data was generated, not real workforce behaviour.
- **Small groups.** Some department-by-gender cells have 14 to 38 employees, so department comparisons are unstable.
- **Binary gender only.** The dataset records male and female only.
- **Missing controls.** There is no data on performance, location, tenure or level beyond experience years.
- **Descriptive only for subgroups.** The experience-group differences are not tested.
- **Currency not stated** in the dataset.
- **No causal design.** The comparisons do not show why any difference exists.

---

## Disclaimer

This is a portfolio project using synthetic data. Results describe the dataset only and should not be read as evidence about any real organisation.

---

**Author:** [Sarthak Jaykar](https://www.linkedin.com/in/sarthak-jaykar/)
