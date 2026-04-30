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

- Calculates expected cash automatically. 
- Counts actual cash using bill and coin denominations.
- Detects shortages or overages.
- Calculates daily, monthly and total profit.
- Stores only verified cash cuts (when cash balances correctly).
- Tracks historical cash cuts.

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

Frontend (HTML/CSS/JavaScript) → FastAPI Backend → SQLite Database → Render Deployment.

## How to Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```


Then open:

```text
http://127.0.0.1:8000
```






