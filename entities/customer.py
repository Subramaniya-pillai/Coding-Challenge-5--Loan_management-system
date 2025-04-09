class Customer:
    def __init__(self, customer_id=None, name=None, email_address=None, 
                 phone_number=None, address=None, credit_score=None):
        self.customer_id = customer_id
        self.name = name
        self.email_address = email_address
        self.phone_number = phone_number
        self.address = address
        self.credit_score = credit_score

    def print_info(self):
        print(f"Customer ID: {self.customer_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email_address}")
        print(f"Phone: {self.phone_number}")
        print(f"Address: {self.address}")
        print(f"Credit Score: {self.credit_score}")