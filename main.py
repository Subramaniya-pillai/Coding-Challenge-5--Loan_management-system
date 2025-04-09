from dao.loan_repository_impl import ILoanRepositoryImpl
from entities.customer import Customer
from entities.home_loan import HomeLoan
from entities.car_loan import CarLoan
from exceptions.invalid_loan_exception import InvalidLoanException

def main():
    loan_repo = ILoanRepositoryImpl()
    
    while True:
        print("\nLoan Management System")
        print("1. Apply for Loan")
        print("2. Get All Loans")
        print("3. Get Loan by ID")
        print("4. Check Loan Status")
        print("5. Calculate EMI")
        print("6. Make Loan Repayment")
        print("7. Exit")
        
        try:
            choice = int(input("Enter your choice: "))
            
            if choice == 1:
                apply_loan_menu(loan_repo)
            elif choice == 2:
                display_all_loans(loan_repo)
            elif choice == 3:
                get_loan_by_id_menu(loan_repo)
            elif choice == 4:
                check_loan_status_menu(loan_repo)
            elif choice == 5:
                calculate_emi_menu(loan_repo)
            elif choice == 6:
                make_repayment_menu(loan_repo)
            elif choice == 7:
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                
        except ValueError:
            print("Please enter a valid number.")
        except InvalidLoanException as e:
            print(f"Error: {e}")

def apply_loan_menu(loan_repo):
    print("\nApply for Loan")
    print("1. Home Loan")
    print("2. Car Loan")
    loan_type = int(input("Enter loan type: "))
    
    customer_id = int(input("Enter Customer ID: "))
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")
    address = input("Enter Address: ")
    credit_score = int(input("Enter Credit Score: "))
    
    customer = Customer(customer_id, name, email, phone, address, credit_score)
    
    loan_id = int(input("Enter Loan ID: "))
    principal = float(input("Enter Principal Amount: "))
    rate = float(input("Enter Interest Rate: "))
    term = int(input("Enter Loan Term (months): "))
    
    if loan_type == 1:
        property_address = input("Enter Property Address: ")
        property_value = int(input("Enter Property Value: "))
        loan = HomeLoan(loan_id, customer, principal, rate, term, "Pending", 
                       property_address, property_value)
    else:
        car_model = input("Enter Car Model: ")
        car_value = int(input("Enter Car Value: "))
        loan = CarLoan(loan_id, customer, principal, rate, term, "Pending", 
                      car_model, car_value)
    
    loan_repo.apply_loan(loan)

def display_all_loans(loan_repo):
    loans = loan_repo.get_all_loans()
    if not loans:
        print("No loans found.")
    else:
        print("\nAll Loans:")
        for loan in loans:
            loan.print_info()
            print("----------------------")

def get_loan_by_id_menu(loan_repo):
    loan_id = int(input("\nEnter Loan ID: "))
    loan = loan_repo.get_loan_by_id(loan_id)
    if loan:
        loan.print_info()
    else:
        print(f"No loan found with ID: {loan_id}")

def check_loan_status_menu(loan_repo):
    loan_id = int(input("\nEnter Loan ID: "))
    status = loan_repo.loan_status(loan_id)
    print(f"Loan Status: {status}")

def calculate_emi_menu(loan_repo):
    loan_id = int(input("\nEnter Loan ID: "))
    emi = loan_repo.calculate_emi(loan_id)
    print(f"EMI for loan {loan_id}: {emi:.2f} per month")

def make_repayment_menu(loan_repo):
    loan_id = int(input("\nEnter Loan ID: "))
    amount = float(input("Enter Payment Amount: "))
    loan_repo.loan_repayment(loan_id, amount)

if __name__ == "__main__":
    main()