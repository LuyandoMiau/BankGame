# Packages required
from tabulate import tabulate

"""
The BalanceSheet is defined as a class to neatly encapsulate all the bank's financial data and operations in one place.
The __init__() function initializes the state of the balance sheet at the beginning of the game, setting up initial deposits, 
reserve requirements, interest rates, and other key values. This ensures we have a structured and reusable starting point.
"""

class BalanceSheet:
    def __init__(self, initial_deposits=1_000_000, reserve_ratio=0.1):
        self.period = 0
        self.reserve_ratio = reserve_ratio
        self.reference_rate = 0.02  # Set by the central Bank origininally 2%
        self.saving_rate = 0.01     # Bank pays 1% on savings
        self.lending_rate_base = 0.04  # Base lending rate before risk margin

        self.deposits = initial_deposits
        self.required_reserve = self.reserve_ratio * self.deposits
        self.reserves = self.required_reserve
        self.available_for_loans = self.deposits - self.required_reserve
        self.outstanding_loans = 0
        self.non_performing_loans = 0
        self.bank_equity = 100_000  # Initial bank capital

    def snapshot(self):
        return {
            "Period": self.period,
            "Assets": {
                "Cash Reserves": self.reserves,
                "Outstanding Loans": self.outstanding_loans,
                "Non-performing Loans": self.non_performing_loans,
            },
            "Liabilities": {
                "Deposits": self.deposits,
            },
            "Equity": {
                "Bank Equity": self.bank_equity,
            },
            "Available to Lend": self.available_for_loans,
            "Interest Rates": {
                "Reference Rate": self.reference_rate,
                "Savings Rate": self.saving_rate,
                "Base Lending Rate": self.lending_rate_base,
            }
        }

# A Snapshot of the balance sheet is taken to show the current state of the bank's finances.
def main():
    bs = BalanceSheet()
    snapshot = bs.snapshot()
    print(tabulate(snapshot.items(), headers=["Category", "Details"], tablefmt="fancy_grid"))
    
if __name__ == "__main__":
    main()

# The BalanceSheet class simulates a bank's balance sheet, including deposits, reserves, loans, and interest rates.
# The snapshot method provides a summary of the current state of the balance sheet.
# The class can be extended to include methods for updating the balance sheet, calculating interest, and managing loans.
# The initial deposits and reserve ratio can be adjusted when creating an instance of the BalanceSheet class.