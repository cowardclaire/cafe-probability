import pandas as pd

def load_data(filename='data.csv'):
    return pd.read_csv(filename)

def show_report(df):
    print("===== SALES REPORT =====")

    outliers = detect_outliers(df)

    print("Outliers:", outliers)


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