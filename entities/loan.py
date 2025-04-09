from entities.customer import Customer

class Loan:
    def __init__(self, loan_id=None, customer=None, principal_amount=None, 
                 interest_rate=None, loan_term=None, loan_type=None, 
                 loan_status="Pending"):
        self.loan_id = loan_id
        self.customer = customer if customer else Customer()
        self.principal_amount = principal_amount
        self.interest_rate = interest_rate
        self.loan_term = loan_term
        self.loan_type = loan_type
        self.loan_status = loan_status

    def print_info(self):
        print(f"Loan ID: {self.loan_id}")
        print(f"Loan Type: {self.loan_type}")
        print(f"Principal Amount: {self.principal_amount}")
        print(f"Interest Rate: {self.interest_rate}%")
        print(f"Loan Term: {self.loan_term} months")
        print(f"Loan Status: {self.loan_status}")
        print("Customer Details:")
        self.customer.print_info()