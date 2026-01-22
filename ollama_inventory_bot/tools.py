# tools.py

inventory_db = {
    "macbook_air_m1": {"stock": 6, "base_price": 999},
    "macbook_air_m2": {"stock": 4, "base_price": 1199},
    "macbook_air_m3": {"stock": 3, "base_price": 1299},
    "dell_xps_13": {"stock": 5, "base_price": 1399},
    "hp_spectre_x360": {"stock": 4, "base_price": 1499},
    "lenovo_thinkpad_x1": {"stock": 5, "base_price": 1699},
}

def check_inventory(product_name: str):
    """Searches the database for a product."""
    name = product_name.lower().replace(" ", "_")
    # If not found, try a partial match (e.g., 'macbook' finds 'macbook_air_m1')
    if name not in inventory_db:
        for key in inventory_db:
            if name in key:
                return {**inventory_db[key], "model_found": key}
    return inventory_db.get(name, {"stock": 0, "base_price": "Unknown"})

def calculate_loyalty_discount(base_price: float, years_as_customer: int):
    """Calculates a discount based on customer history."""
    discount = min(years_as_customer * 0.05, 0.30)
    final_price = base_price * (1 - discount)
    return {"final_price": round(final_price, 2), "discount_applied": f"{int(discount*100)}%"}

available_functions = {
    "check_inventory": check_inventory,
    "calculate_loyalty_discount": calculate_loyalty_discount
}

tools_metadata = [
    {
        "type": "function",
        "function": {
            "name": "check_inventory",
            "description": "Get stock and price for a laptop (e.g., 'macbook')",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string"}
                },
                "required": ["product_name"]
            }
        }
    }
]