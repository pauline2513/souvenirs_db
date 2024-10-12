-- Задание 1. Создать запрос на выборку сувениров по материалу
SELECT s.id as "id_souvenir", s.name, s.description, m.name as "material" FROM souvenirs as s
INNER JOIN souvenirmaterials as m
ON m.id = s.idmaterial
WHERE m.name = 'алюминий'

-- Задание 2. Создать запрос на выборку поставок сувениров за промежуток времени
SELECT sp.id as "procurement_id", p.name as "Provider", sp.data as "Order date", st.name as "status", 
sv.name as "Souvenir name", ps.amount, ps.price FROM souvenirprocurements as sp
INNER JOIN procurementsouvenirs as ps
ON sp.id = ps.idprocurement
INNER JOIN providers as p
ON p.id = sp.idprovider
INNER JOIN procurementstatuses as st
ON st.id = sp.idstatus
INNER JOIN souvenirs as sv
ON sv.id = ps.idsouvenir
WHERE sp.data >= '2024-09-01' and sp.data < '2024-10-10'

-- Задание 3. Создать запрос на выборку сувениров по категориям и отсортировать по популярности от самого непопулярного
SELECT sv.id as "souvenir id", sv.name, sv.shortname, sc.name, sv.rating FROM souvenirs as sv
INNER JOIN souvenirscategories as sc
ON sv.idcategory = sc.id
WHERE sc.name = 'Фонари'
ORDER BY sv.rating ASC

-- Задание 4. Создать запрос на выборку всех поставщиков, поставляющих категорию товара
SELECT p.name as "provider name", sc.name as "Category name" FROM providers as p
INNER JOIN souvenirprocurements as sp
ON sp.idprovider = p.id
INNER JOIN procurementsouvenirs as ps
ON ps.idprocurement = sp.id
INNER JOIN souvenirs as s
ON s.id = ps.idsouvenir
INNER JOIN souvenirscategories as sc
ON sc.id = s.idcategory
WHERE sc.name = 'Куртки'


-- Задание 5. Создать запрос на выборку поставок сувениров за промежуток времени и отсортировать по статусу
SELECT sp.id as "order id", s.name as "souvenir name", ps.amount, 
ps.price, sp.data as "order date", pst.name as "status" 
FROM souvenirprocurements AS sp
JOIN procurementstatuses AS pst
ON sp.idstatus = pst.id
JOIN procurementsouvenirs as ps
ON ps.idprocurement = sp.id
JOIN souvenirs AS s
ON s.id = ps.idsouvenir
WHERE sp.data >= '2024-09-16' and sp.data < '2024-10-10'
ORDER BY pst.id ASC


-- Задание 6. Создать объект для вывода категорий, в зависимости от выбранной

CREATE OR REPLACE FUNCTION list_of_subcategories(category_id int)
RETURNS TABLE(subcategory_id bigint, subcategory_name varchar) AS $$
BEGIN
    RETURN QUERY
		SELECT s.id, s.name 
		FROM souvenirscategories AS s
		WHERE s.idparent = category_id;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM list_of_subcategories(4047)

-- Задание 7. Создать объект для проверки правильности занесения данных в таблицу SouvenirsCategories

CREATE FUNCTION category_addition() RETURNS trigger AS $$
	BEGIN
		IF NEW.name IS NULL THEN
			RAISE EXCEPTION 'category name cannot be null';
        END IF;
		IF NOT EXISTS (SELECT * FROM souvenirscategories AS s 
					   WHERE s.id = NEW.idparent) THEN
			RAISE EXCEPTION 'there is no category with such parent category id';
        END IF;
		IF EXISTS (SELECT * FROM souvenirscategories AS s 
					   WHERE s.id = NEW.id) THEN
			RAISE EXCEPTION 'category with this id already exists';
        END IF;
		RETURN NEW;
	END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER category_addition BEFORE INSERT OR UPDATE ON souvenirscategories
    FOR EACH ROW EXECUTE PROCEDURE category_addition();
	
insert into souvenirscategories (id, idparent, name)
values (2, 4047, NULL)

-- Задание 8. Создать объект оповещения пользователя при отсутствии поставок товаров, отсутствующих на складе или количество которых меньше чем 50 шт.

CREATE VIEW check_procurements AS
	SELECT ps.idsouvenir FROM procurementsouvenirs AS ps
	INNER JOIN souvenirprocurements AS sp
	ON sp.id = ps.idprocurement
	WHERE sp.idstatus != 5

CREATE FUNCTION store_amount_check() RETURNS trigger AS $$
	BEGIN
		IF NEW.amount < 50 AND NOT EXISTS 
		(SELECT * FROM check_procurements AS cp 
		 WHERE NEW.idsouvenir = cp.idsouvenir) THEN
			RAISE NOTICE 'Less than 50 items remained';
			NEW.amount = 10;
		END IF;
		RETURN NEW;
	END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER store_amount_check BEFORE INSERT OR UPDATE ON souvenirstores
    FOR EACH ROW EXECUTE PROCEDURE store_amount_check();

UPDATE souvenirstores SET amount = 10 WHERE id = 3;
