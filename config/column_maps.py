# Map input filenames to standard column names used in the system.
COLUMN_MAPS = {
    'shop1.csv': {'id':'customer_id', 'order_id':'order_id', 'date':'order_date', 'sum':'order_amount'},
    'shop2.csv': {'client':'customer_id', 'order_id':'order_id', 'last_order':'order_date', 'amount':'order_amount'},
    'new_clients.csv': {'cust_id':'customer_id', 'order_id':'order_id', 'signup_date':'order_date', 'initial_purchase':'order_amount'},
}
