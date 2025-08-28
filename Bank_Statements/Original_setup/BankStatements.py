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
    This ensures that the balance sheet is ready for use in the simulation or game, providing a structured starting point for financial operations.
    The inputs can be adjusted to simulate different scenarios or bank policies.
    Period, outstanding loans and non performing loans are set to zero at the beginning of the game, but they will dynamically change as the game progresses."""
    def __init__(self, 
                 reserve_ratio=0.1, 
                 reference_rate=0.02,
                 saving_rate=0.01,
                 lending_rate_base=0.04,
                 initial_deposits=1_000_000,
                 initial_equity=100_000,
                 retained_earnings=100_000):

        #self is used to represent the instance of the class. It allows us to access attributes and methods associated with the class in Python.

        # ----- Initialize the balance sheet with starting values, paramters that will affect the assets and liabilities of the bank.
        self.period = 0  # Track the current period (e.g., year or quarter)
        self.reserve_ratio = reserve_ratio  # Required reserve ratio set by regulations
        self.reference_rate = reference_rate  # Central bank reference rate (2%)
        self.saving_rate = saving_rate  # Interest rate paid on savings (1%)
        self.lending_rate_base = lending_rate_base  # Base lending rate before risk margin (4%)
        self.margin_rate = self.lending_rate_base - self.saving_rate  # Margin between lending and saving rates (3%)
        
        # ----- Here we will define the initial amounts for deposits, reserves, loans, and equity.
        
        # Deposits are the liabilities of the bank, as they represent money owed to customers.
        self.deposits = initial_deposits  # Total customer deposits
        
        # Reserves are a portion of deposits that the bank must hold and cannot lend out.
        # Initially, the bank holds exactly the required reserves.
        # The bank earns no interest on reserves, but they are crucial for liquidity and regulatory compliance.
        self.required_reserve = self.reserve_ratio * self.deposits  # Minimum reserves required by law
        self.reserves = self.required_reserve  # Actual reserves held by the bank at the start
        
        # Loans are the assets of the bank, as they represent money owed to the bank by borrowers.
        # We will have two types of loans: performing loans and non-performing loans.
        # Performing loans are the ones that are being paid on time, while non-performing loans are the ones that are in default.
        # At the beginning of the game, there are no loans yet.
        self.outstanding_loans = 0  # Total amount of performing loans
        self.non_performing_loans = 0  # Total amount of non-performing (defaulted) loans
        
        # Retained earnings and equity represent the bank's own capital.
        # Retained earnings are profits that have been reinvested in the bank rather than paid out as dividends.
        self.retained_earnings = retained_earnings  # Profits reinvested in the bank
        self.bank_equity = initial_equity + retained_earnings  # Initial capital provided by bank owners
        
        # Reserves are the cash that the bank holds to meet withdrawal demands and regulatory requirements
        self.available_for_loans = self.deposits - self.reserves  # Funds available to lend

    """ The following functions define the total assets and total liabilities and equity of the bank."""
    def total_assets(self):
        # Calculate total assets: reserves + loans (performing and non-performing)
        return self.reserves + self.available_for_loans + self.outstanding_loans + self.non_performing_loans + self.bank_equity

    def total_liabilities_and_equity(self):
        # Calculate total liabilities and equity: deposits + bank equity
        return self.deposits + self.bank_equity
    
    """ The following functions prepare tables for the balance sheet and income statement."""
    def balance_sheet_table(self): # Prepare a table showing assets and liabilities/equity side by side for display. # This helps visualize the balance sheet and ensures assets = liabilities + equity.
        
        # Assets categories and values
        assets = [
            ["Cash Reserves", f"{self.reserves:,.2f}"],
            ["Funds Available for Loans", f"{self.available_for_loans:,.2f}"],
            ["Outstanding Loans", f"{self.outstanding_loans:,.2f}"],
            ["Non-performing Loans", f"{self.non_performing_loans:,.2f}"],
            ["Money from Equity", f"{self.bank_equity:,.2f}"],
        ]
        
        # Liabilities and Equity categories and values
        liabilities = [
            ["Deposits (Savings)", f"{self.deposits:,.2f}"],
            ["Bank Equity", f"{self.bank_equity:,.2f}"],
        ]
        
        # Combine assets and liabilities for side-by-side display
        max_rows = max(len(assets), len(liabilities))
        table = []
        
        # Calculate sums for totals
        sum_assets = 0
        sum_liabilities = 0
        
        # Loop through the maximum number of rows to ensure both sides are displayed completely
        for i in range(max_rows):
            asset_row = assets[i] if i < len(assets) else ["", ""]
            liability_row = liabilities[i] if i < len(liabilities) else ["", ""]
            table.append([asset_row[0], asset_row[1], liability_row[0], liability_row[1]])
            if i < len(assets):
                sum_assets += float(asset_row[1].replace(",", ""))
            if i < len(liabilities):
                sum_liabilities += float(liability_row[1].replace(",", ""))
                
        # Add the net total assets and total liabilities & equity at the bottom
        table.append([
            "Total Assets", f"{sum_assets:,.2f}",
            "Total Liabilities & Equity", f"{sum_liabilities:,.2f}"
        ])
        
        # Return the formatted table
        return table

    """ The income statement function is a proposed structure for future implementation.
    It outlines how income and expenses will be tracked, but currently all values are set to zero.
    This function can be expanded as the simulation/game progresses to reflect actual financial performance.
    """
    def income_statement_table(self):
        # Income categories and values
        income = [
            ["Interest Income from Loans", "0.00"],
            ["Other Income", "0.00"],
        ]
        
        # Expense categories and values
        expenses = [
            ["Interest Paid on Deposits", "0.00"],
            ["Loan Loss Provisions", "0.00"],
            ["Taxes on Income", "0.00"],
            ["Other Expenses", "0.00"],
        ]
        
        # Net Income (total income - total expenses)
        net_income = [["Net Income", "0.00"]]
        
        # To display neatly, we merge the lists in a structured way
        max_len = max(len(income), len(expenses))
        table = []
        for i in range(max_len):
            income_row = income[i] if i < len(income) else ["", ""]
            expense_row = expenses[i] if i < len(expenses) else ["", ""]
            table.append([income_row[0], income_row[1], expense_row[0], expense_row[1]])
        
        # Add the net income at the bottom
        table.append([net_income[0][0], net_income[0][1], "", ""])
        return table
    
    """ This table will define the cash flow statement in the future.
    It will track simple cashflows from operations, investments, loans, deposits, and financing."""
    def cash_flow_statement_table(self):
        # Prepare a table for the cash flow statement (all values zero at start).
        # This can be expanded as the simulation/game progresses.
        cash_flows = [
            
            # Dynamically we will calculate it as: new deposits, loan repayments, interest income
            ["Cash Inflows", "0.00"], # Placeholder for future cash inflows
            
            # Dynamically we will calculate it as: withdrawals, defaults, interest on deposits
            ["Cash Outflows", "0.00"], # Placeholder for future cash outflows
            
            # Net cash flow is inflows minus outflows
            ["Net Cash Flow", "0.00"], # Placeholder for net cash flow calculation
        ]
        
        # We will create a table for display
        table = []
        for row in cash_flows:
            table.append([row[0], row[1]])
        return table



""" The main function demonstrates how to create an instance of the BankThreeMainStatements class
and display the balance sheet and income statement using the tabulate library for formatting."""
def main():
    # Create an instance of the BankThreeMainStatements class
    bs = BankThreeMainStatements()
    print("=== Balance Sheet ===")
    headers = ["Assets", "Amount (€)", "Liabilities & Equity", "Amount (€)"]
    print(tabulate(bs.balance_sheet_table(), headers=headers, tablefmt="fancy_grid"))
    
    # Check if the balance sheet balances (assets = liabilities + equity)
    if abs(bs.total_assets() - bs.total_liabilities_and_equity()) > 0.01:
        print("\nWARNING: Balance sheet does not balance!")

    print("\n=== Income Statement (Proposed) ===")
    headers_is = ["Income", "Amount (€)", "Expenses", "Amount (€)"]
    print(tabulate(bs.income_statement_table(), headers=headers_is, tablefmt="fancy_grid"))
    
    print("\n=== Cash Flow Statement (Proposed) ===")
    headers_cf = ["Cash Flow Item", "Amount (€)"]
    print(tabulate(bs.cash_flow_statement_table(), headers=headers_cf, tablefmt="fancy_grid"))

if __name__ == "__main__":
    main()