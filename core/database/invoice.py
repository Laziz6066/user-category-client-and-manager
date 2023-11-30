import psycopg2


async def save_data(user_id, description, weight, dimensions, send_address, receiving_address, payment):
    conn = psycopg2.connect(
        host="localhost",
        database="users_managers",
        user="postgres",
        password="123"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'invoice'")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute("""
            CREATE TABLE invoice (
                id SERIAL PRIMARY KEY,
                user_id TEXT,
                description TEXT,
                weight TEXT,
                dimensions TEXT,
                send_address TEXT,
                receiving_address TEXT,
                payment TEXT
            );
        """)

    cursor.execute("SELECT 1 FROM information_schema.columns WHERE table_name = 'invoice' AND column_name = 'payment'")
    column_exists = cursor.fetchone()

    if not column_exists:
        cursor.execute("""
            ALTER TABLE users ADD COLUMN payment TEXT;
        """)

    sql_query = """
        INSERT INTO invoice (
            user_id,
            description,
            weight,
            dimensions,
            send_address,
            receiving_address,
            payment
        ) VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        ) RETURNING id;;
    """

    cursor.execute(sql_query, (user_id, description, weight, dimensions, send_address, receiving_address, payment))
    id_invoice = cursor.fetchone()[0]

    conn.commit()

    conn.close()
    return id_invoice