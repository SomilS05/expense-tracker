# Expense Tracker

A terminal app for recording expenses, listing them, deleting entries, and viewing spending by category. It uses decimal arithmetic and displays amounts in rupees.

## Run

Requires Python 3.8 or later. The app uses the standard library.

```sh
python3 Expense_tracker2.py
```

An expense includes a positive amount, a category, a description, and a date. Use a consistent date format such as `2026-11-09`. The pipe character (`|`) separates fields in storage.

The app reads and saves `expenses.txt` in the current working directory and accepts existing four-field records. If a record cannot be read, the app reports its line number and leaves the file intact. Adds and deletes replace the file only after the updated list has been written. The data file is ignored by Git.
