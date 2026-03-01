import pandas as pd
import math
import numpy as np
import scipy.stats as stats

def load_data(filename='data.csv'):
    try:
        df = pd.read_csv(filename)
        print(f'Successfuly loaded data {len(df)}')
        return df
    except FileNotFoundError:
        print("Sales data not found")

def analyse_variability(df):
    print('Variability & Shape Skewness')

    std_dev = df['Total_Sales'].std()
    print(f"Standard Deviation: {std_dev:.2f}")

    skew = df['Total_Sales'].skew()
    print(f"Skewness Score: {skew:.2f}")

    if -0.5< skew < 0.5:
        print("Fairly symmetrical")
    elif skew >= 0.5:
        print("Positively Skewed")
    else :
        print("Negatively Skewed")

def show_report(df):
    print("===== SALES REPORT =====")

    outliers = detect_outliers(df)
    analyse_variability(df)

    if not outliers.empty:
        print(f"Alert! Found {len(outliers)} outlier(s)") 
        for i, row in outliers.iterrows():
            print(f"Day : {row['Day']} | Sales: {row['Total_Sales']:.2f}")
    else:
        print("No outliers deteceted")


def detect_outliers(df):
    if len(df) < 4:
        return pd.DataFrame()

    Q1 = df['Total_Sales'].quantile(0.25)
    Q3 = df['Total_Sales'].quantile(0.75)
    IQR = Q3 - Q1

    upper_fence = Q3 + ( 1.5 * IQR)
    lower_fence = Q3 - (1.5 * IQR)

    outlier = df[(df["Total_Sales"]> upper_fence) | (df["Total_Sales"] < lower_fence)]

    return outlier

def calculate_sample_size(variance, mde):

    if mde == 0: return 0

    n_required = (16 * variance) / (mde ** 2)

    return math.ceil(n_required) #rounds up to the nearest whole number(you cannot have half a person)

def run_ab_test_simulation():   


#Calculate sample size, generate random data, perform t-test, and calculate financial impact here

    print("\n" + "="*40)
    print("Running A/B Test Simulation...")
    print("Scenario: New Menu in Cafe Promotion")
    print("\n" + "="*40)

    #Group A (current menu)
    avg_daily_sales = 220.0
    std_dev_a = 30.0 #how much sales typically fluctuate day to day with the current menu
    variance = std_dev_a  ** 2
    # Minimum Detectable Effect - how much we want the new menu to improve sales by
    mde = 25.0
    # Sample size calculation
    n_days = calculate_sample_size(variance, mde)

    print(n_days,"<========","Sample Size Required for A/B Test")  

    # Group A: This is the control group with the current menu
    # We're generate random sales data for a number of days based on the average daily sales and standard deviation

    group_a = np.random.normal(loc=avg_daily_sales, scale=std_dev_a, size=n_days)

    std_dev_b = 40.0
    actual_uplift = 35.0 #This is the actual improvement due to the new menu

    group_b = np.random.normal(loc=avg_daily_sales+actual_uplift, scale=std_dev_b, size=n_days)

    mean_a = np.mean(group_a) # average sales of current menu
    mean_b = np.mean(group_b) # average sales of new menu

    print(f"Group A (Current Menu) - Mean Sales: £{mean_a:.2f}")
    print(f"Group B (New Menu) - Mean Sales: £{mean_b:.2f}") 
    print(f"Actual Uplift: £{mean_b - mean_a:.2f}") 

    t_statistic, p_value = stats.ttest_ind(group_a, group_b)
    print(f"P-value: {p_value:.5f}")

    significance_check = False

    if p_value < 0.05:
        print("Result is statistically significant! We can reject the null hypothesis.")
        significance_check = True
    else:
        print("Result is not statistically significant. We fail to reject the null hypothesis.")

def main():
    data = load_data()

    while True:
        print("1. View Report")
        print("2. Run A/B Test Simulation")
        print("3. Exit")
        choice = input("Choose: ")

        if choice == "1":
            show_report(data)
        elif choice == "2":
            run_ab_test_simulation()
        elif choice == "3":
            print("Exiting... Goodbye!")
            

            break

main()