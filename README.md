# Order Intelligence System

A simple AI Ops–style order decision engine that evaluates incoming orders against inventory and daily production constraints.

The system reads orders and inventory from CSV files.
It validates inputs and prevents negative inventory.
Orders are evaluated sequentially by date and priority.
Each order is approved, delayed, split, or escalated.
Every decision includes a human-readable reason.

## How to Run
pip install pandas
python src/main.py
