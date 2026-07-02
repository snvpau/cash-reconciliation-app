# CuadraCaja - Cash Reconciliation App

A full-stack system built to reduce human errors during daily cash cuts in small businesses.

This project was inspired by a real operational problem in a bar in Guadalajara, Mexico.

## Live Demo

https://cash-reconciliation-app.onrender.com

## Problem

Manual cash cuts using Excel or handwritten notes often led to:

- Human input errors.
- Cash discrepancies.
- Inaccurate profit calculations.
- Lack of historical tracking.

## Solution

I built a cash reconciliation app, a web application that:

- Validates incoming requests using Pydantic.
- Separates business logic from API routes.
- Persists validated transactions in SQLite.
- Exposes REST endpoints using FastAPI.
- Calculates expected cash and profit based on business rules.

## Features

### Backend

- REST API with FastAPI.
- Input validation with Pydantic.
- Business rule validation.
- Profit calculation logic.

### Database

- SQLite persistence.
- Historical records.
- Monthly profit metrics.

### Frontend

- Built with HTML, CSS, and JavaScript.
- Dynamic dashboard UI.
- Mobile-friendly usage.

### Deployment

- Deployed to Render.
- Accessible from desktop and mobile devices.

## Stack

- Python.
- FastAPI.
- Pydantic.
- SQLite.
- JavaScript.
- HTML/CSS.
- Render.

## Architecture

Browser
     │
     ▼
HTML / CSS / JavaScript
     │
     ▼
FastAPI REST API
     │
     ▼
Business Services
     │
     ▼
SQLite Database

## Project Structure

cash-reconciliation-app/
│
├── app/
│   ├── database.py
│   ├── services.py
│   ├── models.py
│   ├── routers/
│
├── frontend/
│
├── main.py
│
└── requirements.txt

## Request Flow

1. User enters cash cut data.
2. Frontend sends a POST request.
3. FastAPI validates the request.
4. Business logic calculates:
   - Expected cash
   - Difference
   - Profit
5. If the cash balances, the record is stored.
6. Frontend displays the results.

## How to Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```


Then open:

```text
http://127.0.0.1:8000
```

## Future Improvements

- User authentication
- Interactive charts
- Docker deployment
- Automated testing




