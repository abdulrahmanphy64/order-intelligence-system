import os
from loader import DataLoader
from decision_engine import run_decision_engine


def main():
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    log_path = "output/decisions.log"

    # Load data
    loader = DataLoader()
    orders_df = loader.load_orders()
    inventory_df = loader.load_inventory()

    # Run decision engine
    decisions = run_decision_engine(orders_df, inventory_df)

    # Write decisions to log and print to console
    with open(log_path, "w") as f:
        for d in decisions:
            line = (
                f"{d['OrderID']} | "
                f"{d['ProductCode']} | "
                f"{d['OrderDate']} | "
                f"{d['Decision']} | "
                f"{d['Reason']}"
            )
            print(line)
            f.write(line + "\n")


if __name__ == "__main__":
    main()
