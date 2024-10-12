import psycopg2

file_name = 'categories.txt'

conn = psycopg2.connect(
    dbname='souvenirs_shop',
    user='postgres',
    password='12345',
    port='5432')

cur = conn.cursor()

with open(file_name, 'r', encoding='utf-8') as file:
    column_names = file.readline()
    line = file.readline()
    while line:
        elements = line.split(',')
        category_id = int(elements[0])
        if elements[1] == '':
            parent_category_id = None
        else:
            parent_category_id = int(elements[1])
        category_name = elements[2].strip()

        cur.execute("""
        INSERT INTO souvenirscategories (id, idparent, name)
        VALUES (%s, %s, %s)
        """, (category_id, parent_category_id, category_name))

        line = file.readline()


conn.commit()

cur.close()
conn.close()