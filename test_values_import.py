import psycopg2
import datetime

conn = psycopg2.connect(
    dbname='souvenirs_shop',
    user='postgres',
    password='12345',
    port='5432')

cur = conn.cursor()


# заполним таблицу ProcurementStatuses
cur.execute(f"""
        INSERT INTO procurementstatuses (id, name)
        VALUES
        (1, 'Заказ создан'),
        (2, 'Заказ в обработке'),
        (3, 'Заказ на сборке'),
        (4, 'Заказ в доставке'),
        (5, 'Заказ получен')
        """)

# # заполним таблицу Providers
cur.execute(f"""
        INSERT INTO providers (id, name, email, contactperson, comments)
        VALUES
        (1, 'First provider', 'address1@email.com', 'Иванов Иван Иванович', NULL),
        (2, 'Second provider', 'address2@email.com', 'Тимофеева Фая Богдановна', NULL),
        (3, 'Third provider', 'address3@email.com', 'Фомина Любовь Ростиславовна', NULL),
        (4, 'Fourth provider', 'address4@email.com', 'Князев Мартин Тимурович', NULL),
        (5, 'Fifth provider', 'address5@email.com', 'Лазарев Сергей Христофорович', 'some comments')
        """)

# заполним таблицу SouvenirProcurements
cur.execute(f"""
        INSERT INTO souvenirprocurements (id, idprovider, data, idstatus)
        VALUES
        (1, 1, %s, 1),
        (2, 5, %s, 4),
        (3, 1, %s, 5),
        (4, 2, %s, 3),
        (5, 3, %s, 1)
        """, (datetime.date(2024, 10, 1),
              datetime.date(2024, 9, 15),
              datetime.date(2024, 8, 4),
              datetime.date(2024, 10, 5),
              datetime.date(2024, 9, 28)))

#заполним таблицу ProcurementSouvenirs
cur.execute(f"""
        INSERT INTO procurementsouvenirs (id, idsouvenir, idprocurement, amount, price)
        VALUES
        (1, 13115, 1, 150, 7000.00),
        (2, 8888, 3, 200, 8945.50),
        (3, 8135, 2, 50, 4999.00),
        (4, 10133, 4, 1000, 32750.00),
        (5, 10200, 5, 500, 13999.99)
        """)

#заполним таблицу SouvenirStores
cur.execute(f"""
        INSERT INTO souvenirstores (id, idsouvenir, idprocurement, amount, comments)
        VALUES 
        (1, 10200, 5, 5000, NULL),
        (2, 10133, 4, 10000, NULL),
        (3, 8888, 2, 7639, NULL),
        (4, 8135, 3, 127, 'Есть товар с браком'),
        (5, 13115, 1, 111, 'Остались только куртки большого размера')
        """)


conn.commit()
cur.close()
conn.close()