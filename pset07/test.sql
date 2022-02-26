CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(20)
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(20),
    department_id integer,
    FOREIGN KEY(department_id) REFERENCES departments(id)
);

INSERT INTO
    departments (name)
VALUES
    ('Marketing'),
    ('Product');

INSERT INTO
    employees (name, department_id)
VALUES
    ('Vita', 1),
    ('Ala', 1),
    ('Blo', 2),
    ('Clow', 2),
    ('Delta', 2),
    ('Elie', 3)


