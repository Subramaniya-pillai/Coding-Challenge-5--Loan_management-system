from abc import ABC, abstractmethod
from entities.loan import Loan
from exceptions.invalid_loan_exception import InvalidLoanException

class ILoanRepository(ABC):
    @abstractmethod
    def apply_loan(self, loan: Loan) -> None:
        pass
    
    @abstractmethod
    def calculate_interest(self, loan_id: int) -> float:
        pass
    
    @abstractmethod
    def calculate_interest_amount(self, principal_amount: float, 
                               interest_rate: float, 
                               loan_term: int) -> float:
        pass
    
    @abstractmethod
    def loan_status(self, loan_id: int) -> str:
        pass
    
    @abstractmethod
    def calculate_emi(self, loan_id: int) -> float:
        pass
    
    @abstractmethod
    def calculate_emi_amount(self, principal_amount: float,
                          interest_rate: float,
                          loan_term: int) -> float:
        pass
    
    @abstractmethod
    def loan_repayment(self, loan_id: int, amount: float) -> None:
        pass
    
    @abstractmethod
    def get_all_loans(self) -> list[Loan]:
        pass
    
    @abstractmethod
    def get_loan_by_id(self, loan_id: int) -> Loan:
        pass