from entities.loan import Loan

class CarLoan(Loan):
    def __init__(self, loan_id=None, customer=None, principal_amount=None, 
                 interest_rate=None, loan_term=None, loan_status="Pending", 
                 car_model=None, car_value=None):
        super().__init__(loan_id, customer, principal_amount, interest_rate, 
                         loan_term, "CarLoan", loan_status)
        self.car_model = car_model
        self.car_value = car_value

    def print_info(self):
        super().print_info()
        print(f"Car Model: {self.car_model}")
        print(f"Car Value: {self.car_value}")