import psycopg2
import random
from datetime import datetime, timedelta

conn = psycopg2.connect(database="postgres", host="localhost", user="", password="", port="5432")
cur = conn.cursor()

cur.execute('''DROP TABLE Deliveries''')

cur.execute('''CREATE TABLE IF NOT EXISTS Deliveries (id serial PRIMARY KEY, access_code varchar(6), days INTEGER, date DATE)''')

for i in range(1,7):
    access_code = str(random.randint(10000, 99999))

    start_date = datetime.now() - timedelta(days=365)
    random_date = start_date + timedelta(days=random.randint(358, 365))
    formatted_date = random_date.strftime('%d/%m/%Y')

    today = datetime.now()
    days = (today - random_date).days

    insert_query = '''INSERT INTO Deliveries (access_code, days, date) VALUES (%s, %s, TO_DATE(%s, 'DD/MM/YYYY'))'''
    cur.execute(insert_query, (access_code, days, formatted_date))

# cur.execute('''INSERT INTO Deliveries (access_code, days, date) VALUES ('18296', 3, TO_DATE('4/8/2024', 'DD/MM/YYYY'))''')
# cur.execute('''INSERT INTO Deliveries (access_code, days, date) VALUES ('12345', 2, TO_DATE('5/8/2024', 'DD/MM/YYYY'))''')
# cur.execute('''INSERT INTO Deliveries (access_code, days, date) VALUES ('26468', 1, TO_DATE('6/8/2024', 'DD/MM/YYYY'))''')
# cur.execute('''INSERT INTO Deliveries (access_code, days, date) VALUES ('87437', 0, TO_DATE('7/8/2024', 'DD/MM/YYYY'))''')

conn.commit()
cur.close()
conn.close()