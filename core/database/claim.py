import psycopg2


async def save_data(num_invoice, e_mail, description, amount, photo_scan):
    conn = psycopg2.connect(
        host="localhost",
        database="users_managers",
        user="postgres",
        password="123"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'claims'")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute("""
            CREATE TABLE claims (
                id SERIAL PRIMARY KEY,
                num_invoice TEXT,
                e_mail TEXT,
                description TEXT,
                amount TEXT,
                photo_scan TEXT
            );
        """)

    cursor.execute("SELECT 1 FROM information_schema.columns WHERE table_name = 'claims' AND column_name = 'photo_scan'")
    column_exists = cursor.fetchone()

    if not column_exists:
        cursor.execute("""
            ALTER TABLE claims ADD COLUMN photo_scan TEXT;
        """)

    sql_query = """
        INSERT INTO claims (
            num_invoice,
            e_mail,
            description,
            amount,
            photo_scan
        ) VALUES (
            %s,
            %s,
            %s,
            %s,
            %s
        ) RETURNING id;;
    """

    cursor.execute(sql_query, (num_invoice, e_mail, description, amount, photo_scan))

    conn.commit()

    conn.close()
