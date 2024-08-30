import psycopg2

from models.Delivery import Delivery

def db_conn():
    return psycopg2.connect(database="postgres", host="localhost", user="", password="", port="5432")

def get_all_deliveries():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM Deliveries''')
    data = cur.fetchall()
    cur.close()
    conn.close()

    deliveries = [Delivery(id=delivery[0], access_code=delivery[1], days=delivery[2], date=delivery[3]) for delivery in data]
    return deliveries


def create_delivery(access_code, days, date):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''INSERT INTO Deliveries (access_code, days, date) VALUES (%s, %s, %s) RETURNING id;''', (access_code, days, date))
    new_delivery_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return new_delivery_id

def get_delivery_by_id(delivery_id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM Deliveries WHERE id = %s''', (delivery_id,))
    delivery_data = cur.fetchone()
    cur.close()
    conn.close()

    if delivery_data:
        return Delivery(id=delivery_data[0], access_code=delivery_data[1], days=delivery_data[2], date=delivery_data[3])
    else:
        return None
    
def update_delivery(delivery_id, access_code, days, date):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''UPDATE Deliveries SET access_code=%s, days=%s, date=%s, WHERE id=%s;''', (access_code, days, date, delivery_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_delivery(delivery_id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''DELETE FROM Deliveries WHERE id = %s;''', (delivery_id,))
    conn.commit()
    cur.close()
    conn.close()