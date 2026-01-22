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
    name = product_name.lower().replace(" ", "_")
    if name not in inventory_db:
        for key in inventory_db:
            if name in key:
                return {**inventory_db[key], "model_found": key}
    return inventory_db.get(name, {"stock": 0, "base_price": "Unknown"})

available_functions = {
    "check_inventory": check_inventory
}

tools_metadata = [
    {
        "type": "function",
        "function": {
            "name": "check_inventory",
            "description": "Get stock and price for a laptop.",
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