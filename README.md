# Caja-Gallo
Cash reconcilation and profit estimation app using FastAPI, design to detect discrepancies in daily cash flow


## Features

- Receives cash cut data via POST endpoint.
- Validates input using Pydantic.
- Identifies mismatches between expected and actual cash.
- Calculates:
    - Cash sales.
    - Expected cash.
    - Counted cash.
    - Cash discrepancies.
    - Estimated profit.

## Use case

This project was inspired by a real problem needed in a bar from Guadalajara, México to track daily cash flow and detect inconsistencies in cash handling. 

## Stack

- Python.
- FastAPI.
- Pydantic.
- Uvicorn.

## How to run

```bash
pip install fastapi uvicorn
uvicorn main:app --reload

then open http://127.0.0.1:8000/docs

Endpoint

POST/corte-caja 

Accepts JSON input with: 

- Sales data.
- Expenses.
- Cash denominations.

Returns:

- Expected cash.
- Counted cash.
- Discrepancies.
- Profit estimation.

## Future improvements

- SQLite data base for persistence. 
- Frontend UI (CSS/HTML/JS).
- Data visualization with charts.
- Github Actions CI/CD pipeline.





