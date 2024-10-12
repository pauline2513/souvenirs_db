import pandas as pd
from io import StringIO
import psycopg2
import csv
import ast


def fill_in_table(column_name, df, new_column_name, table_name):
    unique_elements = pd.unique(data[column_name])
    id_elements = {}
    index = 1
    for element in unique_elements:
        id_elements[element] = index
        index += 1
    for element in unique_elements:
        cur.execute(f"""
        INSERT INTO {table_name} (id, name)
        VALUES (%s, %s)
        """, (id_elements[element], element))

    # изменим столбец на новый в data
    df[new_column_name] = data[column_name].replace(id_elements)
    data.drop(columns=[column_name], inplace=True)
    return id_elements

conn = psycopg2.connect(
    dbname='souvenirs_shop',
    user='postgres',
    password='12345',
    port='5432')

cur = conn.cursor()

file_name = 'data.xlsx'

data = pd.read_excel(file_name)
data.drop(columns=['currencyid', 'vendorcode'], inplace=True)
data.rename(columns={'Unnamed: 0':'id'}, inplace=True)
data['fullCategories'] = data['fullCategories'].apply(lambda x: ', '.join(ast.literal_eval(x)))
data['description'] = data['description'].fillna("no description")
data['rating'] = data['rating'].fillna(0.0)
data.rename(columns={'prodsize': 'size'}, inplace=True)
data['size'] = data['size'].fillna("no info")


# заполним таблицу colors
data['color'] = data['color'].fillna("unknown color")
fill_in_table('color', data, 'idcolor', 'colors')
#
# # заполним таблицу applicationmetods
data['applicMetod'] = data['applicMetod'].fillna("unknown method")
fill_in_table('applicMetod', data, 'idapplicmetod', 'applicationmetods')
#
# # заполним таблицу souvenirmaterials
data['material'] = data['material'].fillna("unknown material")
fill_in_table('material', data, 'idmaterial', 'souvenirmaterials')

data = data.reindex(columns = ['id', 'url', 'shortname', 'name', 'description', 'rating', 'categoryid',
                               'idcolor', 'size', 'idmaterial','weight', 'qtypics','picssize','idapplicmetod',
                               'fullCategories','dealerPrice','price'])

data['rating'] = data['rating'].astype('Int64')
data.fillna('', inplace=True)

sio = StringIO()
writer = csv.writer(sio)
writer.writerows(data.values)
sio.seek(0)

cur.copy_expert(
        sql="""
        COPY souvenirs (
            id, 
            url, 
            shortname, 
            name, 
            description, 
            rating, 
            idcategory,
            idcolor, 
            size, 
            idmaterial,
            weight, 
            qtypics,
            picssize,
            idapplicmetod,
            allcategories,
            dealerprice,
            price
        ) FROM STDIN WITH CSV""",
        file=sio
    )
conn.commit()
cur.close()
conn.close()