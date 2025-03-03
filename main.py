import pandas as pd 
import csv 
from datetime import datetime
from data_entry import get_amount, get_description, get_category, get_date


class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['date','amount','category','description']
    FORMAT = '%d-%m-%Y'

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError: 
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            'date': date,
            'amount': amount,
            'category': category,
            'description': description
        }
        with open(cls.CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry Added Successfully") 

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df['date'] = pd.to_datetime(df['date'],format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df['date']>=start_date) & (df['date']<=end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('No Transaction found in the given date range')
        else:
            print(f"Transaction found in the given date range from {start_date.strftime(CSV.FORMAT)} and {end_date.strftime(CSV.FORMAT)}")
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                    )
            )

            total_income = filtered_df[filtered_df['category'] == 'Income']['amount'].sum()
            total_expenses = filtered_df[filtered_df['category'] == 'Expense']['amount'].sum()

            print('\n Summary')
            print(f"Total Incomes: ${total_income:.2f}")
            print(f"Total Expenses: ${total_expenses:.2f}")
            print(f"Net Savings: ${(total_income - total_expenses):.2f}")

            return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date('Enter the date of the transaction (dd-mm-yyyy):', allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def main():
    while True:
        print('\n1. Add a Transaction')
        print('2. View Transactions within date range')
        print('3. Exit')

        choice = input('Enter you choice 1-3: ')

        if choice == '1':
            add()
        elif choice == '2':
            start_date = input("Enter start date (dd-mm-yyyy): ")
            end_date =  input("Enter end date (dd-mm-yyyy): ")
            CSV.get_transactions(start_date, end_date)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid Choice")

if __name__ == '__main__':
    main()