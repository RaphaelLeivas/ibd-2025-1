def create_db(conn):
    conn.execute('''
    CREATE TABLE IF NOT EXISTS DEPARTMENT (
        Dname VARCHAR(50) NOT NULL,
        Dnumber INT PRIMARY KEY,
        Mgr_ssn CHAR(9),
        Mgr_start_date DATE,
        FOREIGN KEY (Mgr_ssn) REFERENCES EMPLOYEE(Ssn)
    );''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS EMPLOYEE (
        Fname VARCHAR(30) NOT NULL,
        Minit CHAR(1),
        Lname VARCHAR(30) NOT NULL,
        Ssn CHAR(9) PRIMARY KEY,
        Bdate DATE,
        Address VARCHAR(100),
        Sex CHAR(1),
        Salary DECIMAL(10, 2),
        Super_ssn CHAR(9),
        Dno INT,
        FOREIGN KEY (Super_ssn) REFERENCES EMPLOYEE(Ssn),
        FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber)
    );''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS DEPT_LOCATIONS (
        Dnumber INT,
        Dlocation VARCHAR(50),
        PRIMARY KEY (Dnumber, Dlocation),
        FOREIGN KEY (Dnumber) REFERENCES DEPARTMENT(Dnumber)
    );''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS PROJECT (
        Pname VARCHAR(50) NOT NULL,
        Pnumber INT PRIMARY KEY,
        Plocation VARCHAR(50),
        Dnum INT,
        FOREIGN KEY (Dnum) REFERENCES DEPARTMENT(Dnumber)
    );''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS WORKS_ON (
        Essn CHAR(9),
        Pno INT,
        Hours DECIMAL(5, 2),
        PRIMARY KEY (Essn, Pno),
        FOREIGN KEY (Essn) REFERENCES EMPLOYEE(Ssn),
        FOREIGN KEY (Pno) REFERENCES PROJECT(Pnumber)
    );''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS DEPENDENT (
        Essn CHAR(9),
        Dependent_name VARCHAR(50),
        Sex CHAR(1),
        Bdate DATE,
        Relationship VARCHAR(25),
        PRIMARY KEY (Essn, Dependent_name),
        FOREIGN KEY (Essn) REFERENCES EMPLOYEE(Ssn)
    );''')

    conn.commit()

    print("Tables created successfully")

def populate_db(conn):
    conn.execute('''
    INSERT INTO DEPARTMENT (Dname, Dnumber, Mgr_ssn, Mgr_start_date) VALUES
    ('Research', 5, Null, '2020-05-22'), -- '333445555'
    ('Administration', 4, Null, '2018-01-01'), -- '987654321'
    ('Headquarters', 1, Null, '2010-06-19'); -- '888665555'
    ''')

    conn.execute('''
    INSERT INTO EMPLOYEE (Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Super_ssn, Dno) VALUES 
    ('James', 'E', 'Borg', '888665555', '1937-11-10', '450 Stone, Houston, TX', 'M', 55000, NULL, 1),
    ('Franklin', 'T', 'Wong', '333445555', '1955-12-08', '638 Voss, Houston, TX', 'M', 40000, '888665555', 5),
    ('John', 'B', 'Smith', '123456789', '1965-01-09', '731 Fondren, Houston, TX', 'M', 30000, '333445555', 5),
    ('Jennifer', 'S', 'Wallace', '987654321', '1941-06-20', '291 Berry, Bellaire, TX', 'F', 43000, '888665555', 4),
    ('Alicia', 'J', 'Zelaya', '999887777', '1968-01-19', '3321 Castle, Spring, TX', 'F', 25000, '987654321', 4),
    ('Ramesh', 'K', 'Narayan', '666884444', '1962-09-15', '975 Fire Oak, Humble, TX', 'M', 38000, '333445555', 5),
    ('Joyce', 'A', 'English', '453453453', '1972-07-31', '5631 Rice, Houston, TX', 'F', 25000, '333445555', 5),
    ('Ahmad', 'V', 'Jabbar', '987987987', '1969-03-29', '980 Dallas, Houston, TX', 'M', 25000, '333445555', 5);
    ''')

    conn.execute('''
    UPDATE DEPARTMENT
    SET Mgr_ssn = '333445555'
    WHERE Dnumber = 5;
    ''')

    conn.execute('''
    UPDATE DEPARTMENT
    SET Mgr_ssn = '987654321'
    WHERE Dnumber = 4;
    ''')


    conn.execute('''
    UPDATE DEPARTMENT
    SET Mgr_ssn = '888665555'
    WHERE Dnumber = 1;
    ''')

    conn.execute('''
    INSERT INTO DEPT_LOCATIONS (Dnumber, Dlocation) VALUES
    (1, 'Houston'),
    (4, 'Stafford'),
    (5, 'Bellaire'),
    (5, 'Sugarland'),
    (5, 'Houston');
    ''')

    conn.execute('''
    INSERT INTO PROJECT (Pname, Pnumber, Plocation, Dnum) VALUES
    ('ProductX', 1, 'Bellaire', 5),
    ('ProductY', 2, 'Sugarland', 5),
    ('ProductZ', 3, 'Houston', 5),
    ('Computerization', 10, 'Stafford', 4),
    ('Reorganization', 20, 'Houston', 1),
    ('Newbenefits', 30, 'Stafford', 4);
    ''')

    conn.execute('''
    INSERT INTO WORKS_ON (Essn, Pno, Hours) VALUES
    ('123456789', 1, 32.5),
    ('123456789', 2, 7.5),
    ('666884444', 3, 40.0),
    ('453453453', 1, 20.0),
    ('453453453', 2, 20.0),
    ('333445555', 2, 10.0),
    ('333445555', 3, 10.0),
    ('333445555', 10, 10.0),
    ('333445555', 20, 10.0),
    ('999887777', 30, 30.0),
    ('987987987', 10, 35.0),
    ('987987987', 30, 5.0),
    ('987654321', 30, 20.0),
    ('987654321', 20, 15.0);
    ''')


    conn.execute('''
    INSERT INTO DEPENDENT (Essn, Dependent_name, Sex, Bdate, Relationship) VALUES
    ('123456789', 'Alice', 'F', '1986-04-05', 'Daughter'),
    ('123456789', 'Theodore', 'M', '1983-10-25', 'Son'),
    ('123456789', 'Joy', 'F', '1958-05-03', 'Spouse'),
    ('987654321', 'Abner', 'M', '1942-02-28', 'Spouse'),
    ('333445555', 'Michael', 'M', '1988-01-04', 'Son'),
    ('333445555', 'Alice', 'F', '1988-12-30', 'Daughter'),
    ('333445555', 'Elizabeth', 'F', '1967-05-05', 'Spouse');
    ''')

    conn.commit()