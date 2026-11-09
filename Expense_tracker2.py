"""A terminal expense tracker with local storage."""

from decimal import Decimal, InvalidOperation
from pathlib import Path
from tempfile import NamedTemporaryFile

DATA_FILE = Path("expenses.txt")
MENU = """
PERSONAL EXPENSE TRACKER
1. Add expense
2. View expenses
3. Delete expense
4. View category totals
5. Exit"""


def parse_expense(amount, category, description, date):
    try:
        amount = Decimal(amount)
    except InvalidOperation:
        raise ValueError("Enter a valid amount.") from None
    if not amount.is_finite() or amount <= 0:
        raise ValueError("Amount must be a finite number greater than zero.")

    fields = [field.strip() for field in (category, description, date)]
    if not all(fields):
        raise ValueError("Fill in all expense details.")
    if any("|" in field for field in fields):
        raise ValueError("Expense details cannot contain the pipe character (|).")

    return amount, *fields


def load_expenses(path):
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []

    expenses = []
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            amount, category, description, date = line.split("|")
            expenses.append(parse_expense(amount, category, description, date))
        except ValueError:
            raise ValueError(f"Invalid expense record on line {number}.") from None
    return expenses


def save_expenses(path, expenses):
    temporary = None
    try:
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False,
        ) as file:
            temporary = Path(file.name)
            for amount, category, description, date in expenses:
                file.write(f"{amount}|{category}|{description}|{date}\n")
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def view_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    total = Decimal(0)
    for number, (amount, category, description, date) in enumerate(expenses, start=1):
        print(f"\nExpense Number: {number}")
        print(f"Date: {date}")
        print(f"Category: {category}")
        print(f"Description: {description}")
        print(f"Amount: ₹{amount:,.2f}")
        total += amount
    print(f"\nTotal Expenses: ₹{total:,.2f}")


def view_category_totals(expenses):
    if not expenses:
        print("No expenses found.")
        return

    totals = {}
    for amount, category, _, _ in expenses:
        totals[category] = totals.get(category, Decimal(0)) + amount

    for category, total in totals.items():
        print(f"{category}: ₹{total:,.2f}")


def main(path=DATA_FILE):
    try:
        expenses = load_expenses(path)
    except (OSError, ValueError) as error:
        print(f"Could not load {path.name}: {error}")
        return

    try:
        while True:
            print(MENU)
            choice = input("Enter your choice: ").strip()
            try:
                if choice == "1":
                    expense = parse_expense(
                        input("Enter amount: "),
                        input("Enter category: "),
                        input("Enter description: "),
                        input("Enter date: "),
                    )
                    updated = [*expenses, expense]
                    save_expenses(path, updated)
                    expenses = updated
                    print("Expense added successfully.")
                elif choice == "2":
                    view_expenses(expenses)
                elif choice == "3":
                    if not expenses:
                        print("No expenses found.")
                        continue
                    for number, (amount, _, description, _) in enumerate(expenses, start=1):
                        print(f"{number}. {description} (₹{amount:,.2f})")
                    try:
                        number = int(input("Enter expense number to delete: "))
                    except ValueError:
                        raise ValueError("Enter a valid expense number.") from None
                    if not 1 <= number <= len(expenses):
                        raise ValueError("Invalid expense number.")
                    updated = expenses[:number - 1] + expenses[number:]
                    save_expenses(path, updated)
                    expenses = updated
                    print("Expense deleted successfully.")
                elif choice == "4":
                    view_category_totals(expenses)
                elif choice == "5":
                    break
                else:
                    print("Please select a number from 1 to 5.")
            except ValueError as error:
                print(error)
            except OSError as error:
                print(f"Could not save {path.name}: {error}")
    except (EOFError, KeyboardInterrupt):
        print()

    print("Expense Tracker closed.")


if __name__ == "__main__":
    main()
