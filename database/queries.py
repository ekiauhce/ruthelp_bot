#Сырые sql запросы

create_categories_table = \
"""
CREATE TABLE IF NOT EXISTS categories(
    category_id INTEGER NOT NULL PRIMARY KEY,
    category TEXT NOT NULL
);
"""

insert_categories = \
"""
INSERT INTO categories(category) VALUES
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

select_categories = \
"""
SELECT * FROM categories;
"""

create_applications_table = \
"""
CREATE TABLE IF NOT EXISTS applications(
    application_id INTEGER NOT NULL PRIMARY KEY,
    category TEXT NOT NULL,
    group_name TEXT NOT NULL,
    gender TEXT NOT NULL,
    surname TEXT NOT NULL,
    name TEXT NOT NULL,
    patronymic TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    inn TEXT NOT NULL
);
"""

insert_application = \
"""
INSERT INTO applications(
    category,
    group_name,
    gender,
    surname,
    name,
    patronymic,
    phone_number,
    inn
) VALUES(?, ?, ?, ?, ?, ?, ?, ?);
"""