class Order:
    def __init__(self, order_id,
                 user_id,
                 warehouse_id,
                 product_id,
                 price_pr_unit,
                 order_quantity,
                 transportation_id,
                 order_date):
        self.order_id = order_id
        self.user_id = user_id
        self.warehouse_id = warehouse_id
        self.product_id = product_id
        self.price_pr_unit = price_pr_unit
        self.order_quantity = order_quantity
        self.transportation_id = transportation_id
        self.order_date = order_date
