from entities.loan import Loan

class HomeLoan(Loan):
    def __init__(self, loan_id=None, customer=None, principal_amount=None, 
                 interest_rate=None, loan_term=None, loan_status="Pending", 
                 property_address=None, property_value=None):
        super().__init__(loan_id, customer, principal_amount, interest_rate, 
                         loan_term, "HomeLoan", loan_status)
        self.property_address = property_address
        self.property_value = property_value

    def print_info(self):
        super().print_info()
        print(f"Property Address: {self.property_address}")
        print(f"Property Value: {self.property_value}")
        