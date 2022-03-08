create_categories_table = """
CREATE TABLE IF NOT EXISTS categories(
    category_id SERIAL PRIMARY KEY,
    category TEXT NOT NULL UNIQUE
);
"""

select_category_id_by_category = """
SELECT category_id
FROM categories
WHERE category like %s;
"""

create_documents_table = """
CREATE TABLE IF NOT EXISTS documents(
    documents_id SERIAL PRIMARY KEY,
    document TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id)
    REFERENCES categories(category_id)
);
"""

insert_documents = """
INSERT INTO documents(document, category_id) VALUES
    ('копии свидетельства о смерти родителей', 1),
    ('копии свидетельства о лишении родительских прав', 1),
    ('копии свидетельства о рождении ребенка (студента)', 1),
    ('копия свидетельства об инвалидности', 2),
    ('копия свидетельства о рождении родителя', 3),
    ('копии свидетельства о рождении ребенка', 3),
    ('копия удостоверения многодетной матери', 4),
    ('справка о составе семьи (дата рождения детей, род деятельности', 4),
    ('копии свидетельства о рождении ребенка (студента)', 4),
    ('справка об участии в военных действиях', 5),
    ('копия военного билета студента', 5),
    ('копия удостверения о проживании в зоне с льготным социально-экономическим статусом', 6),
    ('копия справки из центра социальной защиты населения', 6),
    ('копия удостверения инвалидности, пенсионного удостоверения родителей', 7),
    ('копии свидетельства о рождении ребенка (студента)', 7),
    ('копии свидетельства о смерти одного из родителей', 8),
    ('копия свидетельства о разводе', 8),
    ('копии свидетельства о рождении ребенка (студента)', 8),
    ('копия справки из центра социальной защиты населения', 9),
    ('справка из больницы (поликлиники) (состоит на диспансерном учете у ... с диагнозом ... нуждается в диет. питании) (подлинник)', 10),
    ('дополнительных документов не требуется', 11)
ON CONFLICT DO NOTHING;
"""

select_documents = """
SELECT document
FROM documents
WHERE category_id = %s;
"""

insert_categories = """
INSERT INTO categories(category) VALUES
    ('студент-сирота'),
    ('студент-инвалид'),
    ('студент, имеющий детей'),
    ('студент из многодетной семьи'),
    ('студент-участник военных действий'),
    ('студент-чернобылец'),
    ('студент, имеющий родителей-инвалидов'),
    ('студент из неполной семьи'),
    ('студент из малоимущей семьи'),
    ('студент, находящийся на диспансерном учёте с хроническими заболеваниями'),
    ('студент, проживающий в общежитии'),
    ('студент, имеющий родителей-пенсионеров')
ON CONFLICT DO NOTHING;
"""

select_categories = """
SELECT category FROM categories;
"""

create_applications_table = """
CREATE TABLE IF NOT EXISTS applications(
    application_id SERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    group_name TEXT NOT NULL,
    gender TEXT NOT NULL,
    surname TEXT NOT NULL,
    name TEXT NOT NULL,
    middle_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    inn TEXT NOT NULL,
    ok INTEGER NOT NULL DEFAULT 0
);
"""

insert_application = """
INSERT INTO applications(
    category,
    group_name,
    gender,
    surname,
    name,
    middle_name,
    phone_number,
    inn
) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
"""

create_directors_table = """
CREATE TABLE IF NOT EXISTS directors(
    director_id SERIAL PRIMARY KEY,
    director TEXT NOT NULL
);
"""

insert_directors = """
INSERT INTO directors(director) VALUES
    ('Н.В. Попова'),
    ('И.М. Самойлова'),
    ('Е.В. Бычкова'),
    ('И.А. Коновал'),
    ('Т.В. Гаранина'),
    ('М.А. Васильева'),
    ('М.А. Васильева')
ON CONFLICT DO NOTHING;
"""

select_director = """
SELECT director
FROM directors
WHERE director_id = %s;
"""

select_applications = """
SELECT * FROM applications;
"""

select_applications_field_names = """
SELECT
    column_name
FROM
    information_schema.columns
WHERE
    table_name = 'applications';
"""

update_application = """
UPDATE applications
SET ok = 1
WHERE application_id = %s;
"""
