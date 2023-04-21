class Product:
    def __init__(self,
                 product_id,
                 name,
                 category_id,
                 price_pr_unit,
                 co2,
                 co2_per_kg,
                 color,
                 weight):
        self.product_id = product_id
        self.name = name
        self.category_id = category_id
        self.price_pr_unit = price_pr_unit
        self.co2 = co2
        self.co2_per_kg = co2_per_kg
        self.weight = weight
        self.color = color

    def __str__(self):
        return f"User: {self.name} ({self.product_id})"
