import mysql.connector
from typing import List
from dao.loan_repository import ILoanRepository
from entities.customer import Customer
from entities.loan import Loan
from entities.home_loan import HomeLoan
from entities.car_loan import CarLoan
from exceptions.invalid_loan_exception import InvalidLoanException
from util.db_conn_util import DBConnUtil
from util.db_property_util import DBPropertyUtil

class ILoanRepositoryImpl(ILoanRepository):
    def __init__(self):
        self.connection_params = DBPropertyUtil.get_connection_string("config.ini")
        self.connection = DBConnUtil.get_connection(self.connection_params)
    
    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
    
    def apply_loan(self, loan: Loan) -> None:
        confirmation = input("Confirm loan application (yes/no): ").lower()
        if confirmation != 'yes':
            print("Loan application cancelled.")
            return
        
        try:
            cursor = self.connection.cursor()
            
            # Insert customer
            cursor.execute("""
                INSERT INTO Customer (customer_id, name, email_address, phone_number, address, credit_score)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                email_address = VALUES(email_address),
                phone_number = VALUES(phone_number),
                address = VALUES(address),
                credit_score = VALUES(credit_score)
            """, (
                loan.customer.customer_id,
                loan.customer.name,
                loan.customer.email_address,
                loan.customer.phone_number,
                loan.customer.address,
                loan.customer.credit_score
            ))
            
            # Insert loan
            cursor.execute("""
                INSERT INTO Loan (loan_id, customer_id, principal_amount, interest_rate, loan_term, loan_type, loan_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                loan.loan_id,
                loan.customer.customer_id,
                loan.principal_amount,
                loan.interest_rate,
                loan.loan_term,
                loan.loan_type,
                loan.loan_status
            ))
            
            # Insert specific loan type
            if isinstance(loan, HomeLoan):
                cursor.execute("""
                    INSERT INTO HomeLoan (loan_id, property_address, property_value)
                    VALUES (%s, %s, %s)
                """, (
                    loan.loan_id,
                    loan.property_address,
                    loan.property_value
                ))
            elif isinstance(loan, CarLoan):
                cursor.execute("""
                    INSERT INTO CarLoan (loan_id, car_model, car_value)
                    VALUES (%s, %s, %s)
                """, (
                    loan.loan_id,
                    loan.car_model,
                    loan.car_value
                ))
            
            self.connection.commit()
            print("Loan application submitted successfully. Status: Pending")
            
        except mysql.connector.Error as e:
            self.connection.rollback()
            raise InvalidLoanException(f"Error applying for loan: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()

    def calculate_interest(self, loan_id: int) -> float:
        loan = self.get_loan_by_id(loan_id)
        if not loan:
            raise InvalidLoanException(f"Loan not found with ID: {loan_id}")
        return self.calculate_interest_amount(
            loan.principal_amount,
            loan.interest_rate,
            loan.loan_term
        )
    
    def calculate_interest_amount(self, principal_amount: float, 
                               interest_rate: float, 
                               loan_term: int) -> float:
        return (principal_amount * interest_rate * loan_term) / (12 * 100)
    
    def loan_status(self, loan_id: int) -> str:
        loan = self.get_loan_by_id(loan_id)
        if not loan:
            raise InvalidLoanException(f"Loan not found with ID: {loan_id}")
        
        status = "Approved" if loan.customer.credit_score > 650 else "Rejected"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE Loan SET loan_status = %s WHERE loan_id = %s
            """, (status, loan_id))
            self.connection.commit()
            
            loan.loan_status = status
            return status
            
        except mysql.connector.Error as e:
            self.connection.rollback()
            raise InvalidLoanException(f"Error updating loan status: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()

    def calculate_emi(self, loan_id: int) -> float:
        loan = self.get_loan_by_id(loan_id)
        if not loan:
            raise InvalidLoanException(f"Loan not found with ID: {loan_id}")
        return self.calculate_emi_amount(
            loan.principal_amount,
            loan.interest_rate,
            loan.loan_term
        )
    
    def calculate_emi_amount(self, principal_amount: float,
                          interest_rate: float,
                          loan_term: int) -> float:
        monthly_rate = interest_rate / 12 / 100
        emi = (principal_amount * monthly_rate * (1 + monthly_rate)**loan_term) / \
              ((1 + monthly_rate)**loan_term - 1)
        return emi
    
    def loan_repayment(self, loan_id: int, amount: float) -> None:
        emi = self.calculate_emi(loan_id)
        if amount < emi:
            raise InvalidLoanException("Payment amount is less than one EMI. Payment rejected.")
        
        number_of_emis = int(amount // emi)
        remaining_amount = amount - (number_of_emis * emi)
        
        print(f"Payment successful. {number_of_emis} EMIs paid.")
        if remaining_amount > 0:
            print(f"Remaining amount: {remaining_amount:.2f} will not be applied to next EMI.")
    
    def get_all_loans(self) -> List[Loan]:
        loans = []
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT l.*, c.* FROM Loan l 
                JOIN Customer c ON l.customer_id = c.customer_id
            """)
            
            for row in cursor.fetchall():
                customer = Customer(
                    customer_id=row['customer_id'],
                    name=row['name'],
                    email_address=row['email_address'],
                    phone_number=row['phone_number'],
                    address=row['address'],
                    credit_score=row['credit_score']
                )
                
                if row['loan_type'] == "HomeLoan":
                    cursor2 = self.connection.cursor(dictionary=True)
                    cursor2.execute("""
                        SELECT * FROM HomeLoan WHERE loan_id = %s
                    """, (row['loan_id'],))
                    home_loan_row = cursor2.fetchone()
                    loan = HomeLoan(
                        loan_id=row['loan_id'],
                        customer=customer,
                        principal_amount=row['principal_amount'],
                        interest_rate=row['interest_rate'],
                        loan_term=row['loan_term'],
                        loan_status=row['loan_status'],
                        property_address=home_loan_row['property_address'],
                        property_value=home_loan_row['property_value']
                    )
                    cursor2.close()
                elif row['loan_type'] == "CarLoan":
                    cursor2 = self.connection.cursor(dictionary=True)
                    cursor2.execute("""
                        SELECT * FROM CarLoan WHERE loan_id = %s
                    """, (row['loan_id'],))
                    car_loan_row = cursor2.fetchone()
                    loan = CarLoan(
                        loan_id=row['loan_id'],
                        customer=customer,
                        principal_amount=row['principal_amount'],
                        interest_rate=row['interest_rate'],
                        loan_term=row['loan_term'],
                        loan_status=row['loan_status'],
                        car_model=car_loan_row['car_model'],
                        car_value=car_loan_row['car_value']
                    )
                    cursor2.close()
                else:
                    loan = Loan(
                        loan_id=row['loan_id'],
                        customer=customer,
                        principal_amount=row['principal_amount'],
                        interest_rate=row['interest_rate'],
                        loan_term=row['loan_term'],
                        loan_type=row['loan_type'],
                        loan_status=row['loan_status']
                    )
                
                loans.append(loan)
                
        except mysql.connector.Error as e:
            raise InvalidLoanException(f"Error retrieving loans: {e}")
        finally:
            if cursor:
                cursor.close()
        
        return loans
    
    def get_loan_by_id(self, loan_id: int) -> Loan:
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT l.*, c.* FROM Loan l 
                JOIN Customer c ON l.customer_id = c.customer_id
                WHERE l.loan_id = %s
            """, (loan_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            customer = Customer(
                customer_id=row['customer_id'],
                name=row['name'],
                email_address=row['email_address'],
                phone_number=row['phone_number'],
                address=row['address'],
                credit_score=row['credit_score']
            )
            
            if row['loan_type'] == "HomeLoan":
                cursor2 = self.connection.cursor(dictionary=True)
                cursor2.execute("""
                    SELECT * FROM HomeLoan WHERE loan_id = %s
                """, (loan_id,))
                home_loan_row = cursor2.fetchone()
                loan = HomeLoan(
                    loan_id=row['loan_id'],
                    customer=customer,
                    principal_amount=row['principal_amount'],
                    interest_rate=row['interest_rate'],
                    loan_term=row['loan_term'],
                    loan_status=row['loan_status'],
                    property_address=home_loan_row['property_address'],
                    property_value=home_loan_row['property_value']
                )
                cursor2.close()
            elif row['loan_type'] == "CarLoan":
                cursor2 = self.connection.cursor(dictionary=True)
                cursor2.execute("""
                    SELECT * FROM CarLoan WHERE loan_id = %s
                """, (loan_id,))
                car_loan_row = cursor2.fetchone()
                loan = CarLoan(
                    loan_id=row['loan_id'],
                    customer=customer,
                    principal_amount=row['principal_amount'],
                    interest_rate=row['interest_rate'],
                    loan_term=row['loan_term'],
                    loan_status=row['loan_status'],
                    car_model=car_loan_row['car_model'],
                    car_value=car_loan_row['car_value']
                )
                cursor2.close()
            else:
                loan = Loan(
                    loan_id=row['loan_id'],
                    customer=customer,
                    principal_amount=row['principal_amount'],
                    interest_rate=row['interest_rate'],
                    loan_term=row['loan_term'],
                    loan_type=row['loan_type'],
                    loan_status=row['loan_status']
                )
            
            return loan
            
        except mysql.connector.Error as e:
            raise InvalidLoanException(f"Error retrieving loan: {e}")
        finally:
            if cursor:
                cursor.close()