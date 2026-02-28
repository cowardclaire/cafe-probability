import pandas as pd

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

def main():
    data = load_data()

    while True:
        print("1. View Report")
        print("2. Exit")
        choice = input("Choose: ")

        if choice == "1":
            show_report(data)
        elif choice == "2":
            break

main()