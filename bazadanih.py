# Логвиненко Максим Юрійович

import sqlite3


def create_bd():

    db = sqlite3.connect("Gruber.db")
    kurs = db.cursor()

    kurs.execute("DROP TABLE IF EXISTS Orders")
    kurs.execute("DROP TABLE IF EXISTS Customers")
    kurs.execute("DROP TABLE IF EXISTS Salespeople")
    kurs.execute("DROP TABLE IF EXISTS Author")

    # Таблиця автора

    kurs.execute("""
    CREATE TABLE Author(
        id INTEGER PRIMARY KEY,
        fullname TEXT NOT NULL
    )
    """)

    kurs.execute("""
    INSERT INTO Author(fullname)
    VALUES ('Логвиненко Максим Юрійович')
    """)

    # Таблиця продавців

    kurs.execute("""
    CREATE TABLE Salespeople(
        snum INTEGER PRIMARY KEY,
        sname TEXT NOT NULL,
        city TEXT,
        comm REAL NOT NULL
    )
    """)

    prodavci = [
        (1001,'Peel','London',0.12),
        (1002,'Serres','San Jose',0.13),
        (1003,'Axelrod','New York',0.10),
        (1004,'Motika','London',0.11),
        (1005,'Rifkin','Barcelona',0.15),
        (1006,'Brown','Paris',0.14),
        (1007,'Smith','Berlin',0.12),
        (1008,'Taylor','Rome',0.11),
        (1009,'White','Madrid',0.13),
        (1010,'Black','Prague',0.14),
        (1011,'Ivanov','Kyiv',0.15),
        (1012,'Petrenko','Lviv',0.12),
        (1013,'Green','Odesa',0.11),
        (1014,'Wilson','Warsaw',0.13),
        (1015,'King','Vienna',0.14)
    ]

    kurs.executemany(
        "INSERT INTO Salespeople VALUES(?,?,?,?)",
        prodavci
    )

    # Таблиця покупців

    kurs.execute("""
    CREATE TABLE Customers(
        cnum INTEGER PRIMARY KEY,
        cname TEXT NOT NULL,
        city TEXT,
        rating INTEGER,
        snum INTEGER
    )
    """)

    pokupci = [
        (2001,'Hoffman','London',100,1001),
        (2002,'Giovanni','Rome',200,1003),
        (2003,'Liu','San Jose',200,1002),
        (2004,'Grass','Berlin',300,1002),
        (2005,'Clemens','London',100,1001),
        (2006,'Cisneros','San Jose',300,1007),
        (2007,'Pereira','Rome',100,1004),
        (2008,'James','Paris',200,1005),
        (2009,'Miller','Madrid',150,1006),
        (2010,'Scott','Prague',250,1008),
        (2011,'Koval','Kyiv',180,1011),
        (2012,'Melnyk','Lviv',220,1012),
        (2013,'Bondar','Odesa',270,1013),
        (2014,'Nowak','Warsaw',190,1014),
        (2015,'Fischer','Vienna',240,1015)
    ]

    kurs.executemany(
        "INSERT INTO Customers VALUES(?,?,?,?,?)",
        pokupci
    )

    # Таблиця замовлень

    kurs.execute("""
    CREATE TABLE Orders(
        onum INTEGER PRIMARY KEY,
        amt REAL,
        odate TEXT,
        cnum INTEGER,
        snum INTEGER
    )
    """)

    zamovlennya = [
        (3001,18.69,'2025-01-01',2001,1001),
        (3002,1900.10,'2025-01-02',2002,1003),
        (3003,767.19,'2025-01-03',2003,1002),
        (3004,5160.45,'2025-01-04',2004,1002),
        (3005,1098.16,'2025-01-05',2005,1001),
        (3006,75.75,'2025-01-06',2006,1007),
        (3007,4723.00,'2025-01-07',2007,1004),
        (3008,1713.23,'2025-01-08',2008,1005),
        (3009,1309.95,'2025-01-09',2009,1006),
        (3010,9891.88,'2025-01-10',2010,1008),
        (3011,100.00,'2025-01-11',2011,1011),
        (3012,200.00,'2025-01-12',2012,1012),
        (3013,300.00,'2025-01-13',2013,1013),
        (3014,400.00,'2025-01-14',2014,1014),
        (3015,500.00,'2025-01-15',2015,1015),
        (3016,600.00,'2025-01-16',2001,1001),
        (3017,700.00,'2025-01-17',2002,1003),
        (3018,800.00,'2025-01-18',2003,1002),
        (3019,900.00,'2025-01-19',2004,1002),
        (3020,1000.00,'2025-01-20',2005,1001),
        (3021,1100.00,'2025-01-21',2006,1007),
        (3022,1200.00,'2025-01-22',2007,1004),
        (3023,1300.00,'2025-01-23',2008,1005),
        (3024,1400.00,'2025-01-24',2009,1006),
        (3025,1500.00,'2025-01-25',2010,1008),
        (3026,1600.00,'2025-01-26',2011,1011),
        (3027,1700.00,'2025-01-27',2012,1012),
        (3028,1800.00,'2025-01-28',2013,1013),
        (3029,1900.00,'2025-01-29',2014,1014),
        (3030,2000.00,'2025-01-30',2015,1015)
    ]

    kurs.executemany(
        "INSERT INTO Orders VALUES(?,?,?,?,?)",
        zamovlennya
    )

    db.commit()
    db.close()

    print("База даних успішно створена.")


def zapit3():

    db = sqlite3.connect("Gruber.db")
    kurs = db.cursor()

    kurs.execute("""
    SELECT city, MAX(rating)
    FROM Customers
    GROUP BY city
    """)

    print("\nЗапит №3:")
    for city, rating in kurs.fetchall():
        print(f"For the city {city} the highest rating is: {rating}")

    db.close()


def zapit5():

    db = sqlite3.connect("Gruber.db")
    kurs = db.cursor()

    kurs.execute("""
    SELECT ROUND(amt * comm, 2)
    FROM Orders, Customers, Salespeople
    WHERE Orders.cnum = Customers.cnum
    AND Orders.snum = Salespeople.snum
    AND rating > 100
    """)

    print("\nЗапит №5:")
    for row in kurs.fetchall():
        print(row[0])

    db.close()


def zapit7():

    db = sqlite3.connect("Gruber.db")
    kurs = db.cursor()

    kurs.execute("""
    SELECT DISTINCT c.cname, c.rating
    FROM Customers c
    JOIN Orders o ON c.cnum = o.cnum
    WHERE o.amt >
    (
        SELECT AVG(amt)
        FROM Orders
    )
    """)

    print("\nЗапит №7:")
    for row in kurs.fetchall():
        print(row)

    db.close()


while True:

    print("\n===== MENU =====")
    print("1 - Створити базу даних")
    print("2 - Виконати запит №3")
    print("3 - Виконати запит №5")
    print("4 - Виконати запит №7")
    print("0 - Вихід")

    vybir = input("Ваш вибір: ")

    if vybir == "1":
        create_bd()

    elif vybir == "2":
        zapit3()

    elif vybir == "3":
        zapit5()

    elif vybir == "4":
        zapit7()

    elif vybir == "0":
        print("Програму завершено.")
        break

    else:
        print("Невірний вибір")