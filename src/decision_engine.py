from collections import defaultdict

MAX_DAILY_CAPACITY = 200


def run_decision_engine(orders_df, inventory_df):
    """
    Core decision-making engine.
    Takes validated orders and inventory DataFrames.
    Returns a list of decision records.
    """

    # Prepare inventory lookup: product_code -> available_stock
    inventory = {
        row["ProductCode"]: int(row["AvailableStock"])
        for _, row in inventory_df.iterrows()
    }

    decisions = []

    # Group orders by date
    orders_by_date = defaultdict(list)
    for _, row in orders_df.iterrows():
        orders_by_date[row["OrderDate"].date()].append(row)

    # Process each date in ascending order
    for order_date in sorted(orders_by_date.keys()):
        remaining_capacity = MAX_DAILY_CAPACITY

        # Sort: Urgent first, then Normal
        daily_orders = sorted(
            orders_by_date[order_date],
            key=lambda x: 0 if x["Priority"] == "urgent" else 1
        )

        for order in daily_orders:
            order_id = order["OrderID"]
            product_code = order["ProductCode"]
            quantity = int(order["Quantity"])
            priority = order["Priority"]

            available_stock = inventory.get(product_code, 0)

            decision = None
            reason = None

            # 1. Escalation: no stock at all
            if available_stock == 0:
                decision = "Escalate"
                reason = (
                    f"No inventory available for product {product_code}."
                )

            # 2. Escalation: urgent order but no capacity
            elif remaining_capacity == 0 and priority == "urgent":
                decision = "Escalate"
                reason = (
                    "Urgent order cannot be processed due to exhausted daily capacity."
                )

            # 3. Approve: enough stock and capacity
            elif available_stock >= quantity and remaining_capacity >= quantity:
                decision = "Approve"
                reason = (
                    f"Sufficient inventory ({available_stock}) and "
                    f"daily capacity ({remaining_capacity})."
                )
                inventory[product_code] -= quantity
                remaining_capacity -= quantity

            # 4. Split: partial fulfillment possible
            elif available_stock > 0 and remaining_capacity > 0:
                split_qty = min(available_stock, remaining_capacity)

                inventory[product_code] -= split_qty
                remaining_capacity -= split_qty

                if priority == "urgent":
                    decision = "Split"
                    reason = (
                        f"Only {split_qty} units could be processed due to "
                        f"inventory/capacity limits. Remaining quantity escalated."
                    )
                else:
                    decision = "Split"
                    reason = (
                        f"Only {split_qty} units could be processed due to "
                        f"inventory/capacity limits. Remaining quantity delayed."
                    )

            # 5. Delay: stock exists but no capacity
            elif available_stock >= quantity and remaining_capacity < quantity:
                decision = "Delay"
                reason = (
                    f"Inventory available ({available_stock}) but daily "
                    f"capacity exhausted ({remaining_capacity})."
                )

            # 6. Safety fallback
            else:
                decision = "Escalate"
                reason = "Unhandled decision scenario. Manual intervention required."

            # Safety checks (should never trigger)
            if inventory.get(product_code, 0) < 0:
                raise RuntimeError("Inventory went negative. Logic error detected.")

            if remaining_capacity < 0:
                raise RuntimeError("Daily capacity went negative. Logic error detected.")

            decisions.append({
                "OrderID": order_id,
                "ProductCode": product_code,
                "OrderDate": str(order_date),
                "RequestedQuantity": quantity,
                "Decision": decision,
                "Reason": reason
            })

    return decisions
