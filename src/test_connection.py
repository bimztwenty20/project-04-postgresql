from connection import get_connection

def main():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            result = cur.fetchone()

            print("Connection succesfully!!")
            print(result[0])

if __name__ == "__main__":
    main()