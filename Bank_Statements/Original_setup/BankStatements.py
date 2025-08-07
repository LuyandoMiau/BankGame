"""
In this document we will try to encapsulate the Balance Sheet, the Income Statement, and the Cash Flow Statement of a bank
into a single class called BalanceSheet.
The bank business is simple in this game.

DEPOSITS: <--- Not influenced by the user
The bank accepts deposits from customers, which are liabilities for the bank. This do not have a part in the game, the user does not influence them, we have a set amount of deposits at the beginning of the game.
The bank pays interest on these deposits, which is an expense for the bank. The interest rate on deposits is set taking in consideration the central bank reference rate and the bank's own policies.
We assume the same interest rate for all the savings. The savings may be affected by economic turns.

RESERVES: <- Not influenced by the user
The bank is required to hold a certain percentage of deposits as reserves, which are not available for lending. This reserve requirement is set by regulatory authorities and is intended to ensure the bank's stability and liquidity. The bank earns no interest on these reserves.
The reserve ratio is set at the beginning of the game and can change, by the central bank, but not by the user.
The reserves are allocated as income for the bank, but they are not available for lending.

LOANS: <--- Influenced by the user but also dependent on the change of the customers conditions through the game and economic shocks.
The bank lends money to customers, which is an asset for the bank. The bank charges interest on these loans, which is income for the bank.
The interest rate on loans is set based on the central bank reference rate, the bank's own policies, and the risk associated with the borrower which is calculated in the PD_LGD_EAD_Modelling module.
Once the bank starts giving loans, it will have to manage the risk of default, which can lead to non-performing loans (NPLs).
So in escence the bank hast two types of loans: performing loans and non-performing loans.
The performing loans are the ones that are being paid on time, while the non-performing loans are the ones that are in default.

GOAL:
As the bank wants to maximize profits, and that is using the interest rate on loans, and this are calculated in the module PD_LGD_EAD_Modelling
The user can decide to take the sugessted interest rate or to set his own interest rate on loans.
However, the user must be aware that each period the bank will have a balance sheet, cash flow, income statement that will be show to him.
He will also be able to see the loans and which are flagged as performing and non-performing.
This will allow the user to make informed decisions and take actions like:
1. Adjusting individual interest rates on given loans based on risk assessment.
2. Managing the reserve ratio to optimize liquidity and profitability, maybe more reserved but never less than the minimum required.
3. Monitoring the balance sheet, income statement, and cash flow statement to ensure the bank's financial health.
4. They can choose to cancel loans and cut the line of remaining credits of loans flagged

In the end, it is all about to increase the profit of the bank. If the management is poor, the game will display that the user is getting close to red numbers.
This in turn can also affect equity, reserves, and the ability to lend more money.
"""

# Packages required
from tabulate import tabulate

# The BalanceSheet class is used to encapsulate all the financial data and operations of the bank.
# Using a class allows us to group related data (like deposits, reserves, loans) and methods (like calculating totals)
# into a single, reusable, and organized structure. This makes the code easier to maintain, extend, and understand.
# It also allows us to create multiple balance sheets if needed, each with its own state.

class BankThreeMainStatements:
    
    """This first function is defining the intial state of the bank's balance sheet.
    It sets up the initial deposits, reserve requirements, interest rates, and other key financial parameters.
    The __init__() function initializes the balance sheet with starting values, such as deposits, reserves, and interest rates.
    This ensures that the balance sheet is ready for use in the simulation or game, providing a structured starting point for financial operations."""
    
    def __init__(self, initial_deposits=1_000_000, reserve_ratio=0.1):
        
        # Initialize the balance sheet with starting values.
        self.period = 0  # Track the current period (e.g., year or quarter)
        self.reserve_ratio = reserve_ratio  # Required reserve ratio set by regulations
        self.reference_rate = 0.02  # Central bank reference rate (2%)
        self.saving_rate = 0.01     # Interest rate paid on savings (1%)
        self.lending_rate_base = 0.04  # Base lending rate before risk margin (4%)

        self.deposits = initial_deposits  # Total customer deposits
        self.required_reserve = self.reserve_ratio * self.deposits  # Minimum reserves required by law
        self.reserves = self.required_reserve  # Actual reserves held by the bank
        self.available_for_loans = self.deposits - self.required_reserve  # Funds available to lend
        self.outstanding_loans = 0  # Total amount of performing loans
        self.non_performing_loans = 0  # Total amount of non-performing (defaulted) loans
        self.bank_equity = 100_000  # Initial capital provided by bank owners

    def total_assets(self):
        # Calculate total assets: reserves + loans (performing and non-performing)
        return self.reserves + self.outstanding_loans + self.non_performing_loans

    def total_liabilities_and_equity(self):
        # Calculate total liabilities and equity: deposits + bank equity
        return self.deposits + self.bank_equity

    def balance_sheet_table(self):
        # Prepare a table showing assets and liabilities/equity side by side for display.
        # This helps visualize the balance sheet and ensures assets = liabilities + equity.
        assets = [
            ["Cash Reserves", f"{self.reserves:,.2f}"],
            ["Outstanding Loans", f"{self.outstanding_loans:,.2f}"],
            ["Non-performing Loans", f"{self.non_performing_loans:,.2f}"],
            ["Total Assets", f"{self.total_assets():,.2f}"],
        ]
        liabilities = [
            ["Deposits (Savings)", f"{self.deposits:,.2f}"],
            ["Bank Equity", f"{self.bank_equity:,.2f}"],
            ["Total Liabilities & Equity", f"{self.total_liabilities_and_equity():,.2f}"],
        ]

        # Combine assets and liabilities for side-by-side display
        max_rows = max(len(assets), len(liabilities))
        table = []
        for i in range(max_rows):
            asset_row = assets[i] if i < len(assets) else ["", ""]
            liability_row = liabilities[i] if i < len(liabilities) else ["", ""]
            table.append([asset_row[0], asset_row[1], liability_row[0], liability_row[1]])
        return table

    def income_statement_table(self):
        # Prepare a table for the income statement (all values zero at start).
        # This can be expanded as the simulation/game progresses.
        income = [
            ["Interest Income from Loans", "0.00"],
            ["Other Income", "0.00"],
        ]
        expenses = [
            ["Interest Paid on Deposits", "0.00"],
            ["Loan Loss Provisions", "0.00"],
            ["Other Expenses", "0.00"],
        ]
        net_income = [["Net Income", "0.00"]]

        # Combine income and expenses for side-by-side display
        max_rows = max(len(income), len(expenses))
        table = []
        for i in range(max_rows):
            income_row = income[i] if i < len(income) else ["", ""]
            expense_row = expenses[i] if i < len(expenses) else ["", ""]
            table.append([income_row[0], income_row[1], expense_row[0], expense_row[1]])
        # Add net income at the end
        table.append([net_income[0][0], net_income[0][1], "", ""])
        return table

def main():
    # Create an instance of the BankThreeMainStatements class
    bs = BankThreeMainStatements()
    print("=== Balance Sheet ===")
    headers = ["Assets", "Amount (€)", "Liabilities & Equity", "Amount (€)"]
    print(tabulate(bs.balance_sheet_table(), headers=headers, tablefmt="fancy_grid"))

    print("\n=== Income Statement (Proposed) ===")
    headers_is = ["Income", "Amount (€)", "Expenses", "Amount (€)"]
    print(tabulate(bs.income_statement_table(), headers=headers_is, tablefmt="fancy_grid"))

    # Check if the balance sheet balances (assets = liabilities + equity)
    if abs(bs.total_assets() - bs.total_liabilities_and_equity()) > 0.01:
        print("\nWARNING: Balance sheet does not balance!")

if __name__ == "__main__":
    main()