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

def print_simulation_header():
    print("\n" + "="*40)
    print("Running A/B Test Simulation...")
    print("Scenario: New Menu in Cafe Promotion")
    print("\n" + "="*40)

def get_simulation_parameters():
    return {
        'avg_daily_sales': 220.0,
        'std_dev_a': 30.0,
        'mde': 25.0,
        'std_dev_b': 40.0,
        'actual_uplift': 35.0,
        'ad_cost_per_day': 20.0
    }

def generate_group_data(avg_sales, std_dev, n_days):
    return np.random.normal(loc=avg_sales, scale=std_dev, size=n_days)

def perform_t_test(group_a, group_b):
    t_statistic, p_value = stats.ttest_ind(group_a, group_b)
    significant = p_value < 0.05
    return t_statistic, p_value, significant

def calculate_economic_impact(mean_a, mean_b, ad_cost):
    daily_gain = mean_b - mean_a
    net_result = daily_gain - ad_cost
    return daily_gain, net_result

def print_results(n_days, mean_a, mean_b, uplift, p_value, significant, daily_gain, net_result):
    print(f"{n_days} <======== Sample Size Required for A/B Test")
    print(f"Group A (Current Menu) - Mean Sales: £{mean_a:.2f}")
    print(f"Group B (New Menu) - Mean Sales: £{mean_b:.2f}")
    print(f"Actual Uplift: £{uplift:.2f}")
    print(f"P-value: {p_value:.5f}")
    if significant:
        print("Result is statistically significant! We can reject the null hypothesis.")
    else:
        print("Result is not statistically significant. We fail to reject the null hypothesis.")
    print(f"Daily Gain from New Menu: £{daily_gain:.2f}")
    print(f"Net Result after Ad Cost: £{net_result:.2f}")
    if significant and net_result > 0:
        print("Recommendation: Implement the new menu promotion!")
    elif significant and net_result <= 0:
        print("Recommendation: New menu is effective but not cost efficient. Consider other promotional strategies.")
    else:
        print("Recommendation: Do not implement the new menu promotion.")

def run_ab_test_simulation():
    print_simulation_header()

    params = get_simulation_parameters()
    variance = params['std_dev_a'] ** 2
    n_days = calculate_sample_size(variance, params['mde'])

    group_a = generate_group_data(params['avg_daily_sales'], params['std_dev_a'], n_days)
    group_b = generate_group_data(params['avg_daily_sales'] + params['actual_uplift'], params['std_dev_b'], n_days)

    mean_a = np.mean(group_a)
    mean_b = np.mean(group_b)
    uplift = mean_b - mean_a

    t_statistic, p_value, significant = perform_t_test(group_a, group_b)
    daily_gain, net_result = calculate_economic_impact(mean_a, mean_b, params['ad_cost_per_day'])

    print_results(n_days, mean_a, mean_b, uplift, p_value, significant, daily_gain, net_result)

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