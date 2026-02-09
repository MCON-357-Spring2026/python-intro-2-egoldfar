import pytest
from exercises.src.classes import *


class TestProduct:
    """Test suite for Exercise 2.1: Product class"""

    def test_product_attributes(self):
        """Test Product constructor and attributes"""
        p1 = Product("Laptop", 999.99, 5)
        assert p1.name == "Laptop", "name attribute failed"
        assert p1.price == 999.99, "price attribute failed"
        assert p1.quantity == 5, "quantity attribute failed"

    def test_product_default_quantity(self):
        """Test Product default quantity"""
        p2 = Product("Book", 19.99)
        assert p2.quantity == 0, "default quantity should be 0"

    def test_product_get_total_value(self):
        """Test Product get_total_value method"""
        p1 = Product("Laptop", 999.99, 5)
        assert abs(p1.get_total_value() - 4999.95) < 0.01, "get_total_value failed"

    def test_product_is_in_stock(self):
        """Test Product is_in_stock method"""
        p1 = Product("Laptop", 999.99, 5)
        p2 = Product("Book", 19.99)
        assert p1.is_in_stock() == True, "is_in_stock should be True"
        assert p2.is_in_stock() == False, "is_in_stock should be False"


class TestBankAccount:
    """Test suite for Exercise 2.2: BankAccount class"""

    def setup_method(self):
        """Reset class attribute before each test"""
        BankAccount.total_accounts = 0

    def test_bank_account_class_attribute(self):
        """Test BankAccount class attribute"""
        assert BankAccount.bank_name == "Python Bank", "bank_name class attribute failed"

    def test_bank_account_default_balance(self):
        """Test BankAccount default balance"""
        acc1 = BankAccount("A001", "Alice")
        assert acc1.balance == 0.0, "default balance should be 0.0"

    def test_bank_account_deposit(self):
        """Test BankAccount deposit method"""
        acc1 = BankAccount("A001", "Alice")
        assert acc1.deposit(100) == 100.0, "deposit failed"

    def test_bank_account_withdraw(self):
        """Test BankAccount withdraw method"""
        acc1 = BankAccount("A001", "Alice")
        acc1.deposit(100)
        assert acc1.withdraw(30) == 70.0, "withdraw failed"

    def test_bank_account_insufficient_funds(self):
        """Test BankAccount raises ValueError for insufficient funds"""
        acc1 = BankAccount("A001", "Alice")
        acc1.deposit(100)

        with pytest.raises(ValueError):
            acc1.withdraw(200)

    def test_bank_account_total_accounts(self):
        """Test BankAccount total_accounts class attribute"""
        acc1 = BankAccount("A001", "Alice")
        acc2 = BankAccount("A002", "Bob", 500)
        assert BankAccount.total_accounts == 2, "total_accounts should be 2"

    def test_bank_account_get_info(self):
        """Test BankAccount get_info method"""
        acc1 = BankAccount("A001", "Alice")
        info = acc1.get_info()
        assert "A001" in info and "Alice" in info, "get_info failed"


class TestTemperature:
    """Test suite for Exercise 2.3: Temperature class"""

    def test_temperature_celsius_attribute(self):
        """Test Temperature celsius attribute"""
        t1 = Temperature(100)
        assert t1.celsius == 100, "celsius attribute failed"

    def test_temperature_to_fahrenheit(self):
        """Test Temperature to_fahrenheit method"""
        t1 = Temperature(100)
        assert t1.to_fahrenheit() == 212.0, "to_fahrenheit failed"

    def test_temperature_to_kelvin(self):
        """Test Temperature to_kelvin method"""
        t1 = Temperature(100)
        assert abs(t1.to_kelvin() - 373.15) < 0.01, "to_kelvin failed"

    def test_temperature_from_fahrenheit(self):
        """Test Temperature from_fahrenheit class method"""
        t2 = Temperature.from_fahrenheit(32)
        assert abs(t2.celsius - 0.0) < 0.01, "from_fahrenheit failed"

    def test_temperature_from_kelvin(self):
        """Test Temperature from_kelvin class method"""
        t3 = Temperature.from_kelvin(273.15)
        assert abs(t3.celsius - 0.0) < 0.01, "from_kelvin failed"


class TestEmployeeHierarchy:
    """Test suite for Exercise 2.4: Employee hierarchy"""

    def test_employee_base_class(self):
        """Test Employee base class"""
        emp = Employee("Alice", "E001", 50000)
        assert emp.get_annual_salary() == 50000, "Employee salary failed"

        info = emp.get_info()
        assert "E001" in info and "Alice" in info, "Employee get_info failed"

    def test_manager_class(self):
        """Test Manager class (inherits from Employee)"""
        mgr = Manager("Bob", "M001", 70000, "Engineering", 10000)
        assert mgr.get_annual_salary() == 80000, "Manager salary should include bonus"

        info = mgr.get_info()
        assert "Manager" in info and "Engineering" in info, "Manager get_info failed"

    def test_developer_class(self):
        """Test Developer class (inherits from Employee)"""
        dev = Developer("Charlie", "D001", 60000, ["Python", "Java"])
        assert dev.get_annual_salary() == 60000, "Developer salary failed"

        dev.add_language("Go")
        assert "Go" in dev.programming_languages, "add_language failed"

        info = dev.get_info()
        assert "Developer" in info, "Developer get_info failed"

