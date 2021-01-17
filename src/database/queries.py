create_categories_table = """
CREATE TABLE IF NOT EXISTS categories(
    category_id INTEGER NOT NULL PRIMARY KEY,
    category TEXT NOT NULL UNIQUE
);
"""

insert_categories = """
INSERT OR IGNORE INTO categories(category) VALUES
    ('студент-сирота'),
    ('cтудент-инвалид'),
    ('cтудент, имеющий детей'),
    ('cтудент из многодетной семьи'),
    ('cтудент-участник военных действий'),
    ('cтудент-чернобылец'),
    ('cтудент, имеющий родителей-инвалидов, родителей-пенсионеров'),
    ('cтудент из неполной семьи'),
    ('cтудент из малоимущей семьи'),
    ('cтудент, находящийся на диспансерном учёте с хроническими заболеваниями'),
    ('студент, проживающий в общежитии');
"""

select_categories = """
SELECT category FROM categories;
"""

create_applications_table = """
CREATE TABLE IF NOT EXISTS applications(
    application_id INTEGER NOT NULL PRIMARY KEY,
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
) VALUES(?, ?, ?, ?, ?, ?, ?, ?);
"""

create_directors_table = """
CREATE TABLE IF NOT EXISTS directors(
    director_id INTEGER NOT NULL PRIMARY KEY,
    director TEXT NOT NULL UNIQUE
);
"""

insert_directors = """
INSERT OR IGNORE INTO directors(director) VALUES
    ('    Н.В. Попова'),
    ('   И.А. Коновал'),
    ('  Т.В. Гаранина'),
    ('   Е.В. Бычкова'),
    ('Н.Ю. Лахметкина');
"""

select_director = """
SELECT director
FROM directors
WHERE director_id = ?;
"""

select_applications = """
SELECT * FROM applications;
"""

select_applications_field_names = """
SELECT name
FROM PRAGMA_TABLE_INFO('applications');
"""

update_application = """
UPDATE applications
SET ok = 1
WHERE application_id = ?;
"""
