def orders_for(cursor, customer_email, status):
    cursor.execute(
        f"SELECT * FROM orders WHERE customer_email = '{customer_email}' "
        f"AND status = '{status}' ORDER BY created_at DESC LIMIT 50"
    )
    return cursor.fetchall()
