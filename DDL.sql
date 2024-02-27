-- Project Record Ranch DDL
-- Team [Object object] (Group 51)
-- Members: Jordan Howell and Henry Christiani
 
 -- Create Tables

CREATE TABLE Genres (
    id smallint auto_increment NOT NULL UNIQUE,
    description varchar(50) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE Conditions (
    id tinyint auto_increment NOT NULL UNIQUE,
    description varchar(50) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE Artists  (
    id int auto_increment NOT NULL UNIQUE,
    artist_name varchar(100) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE Albums (
    id int auto_increment NOT NULL UNIQUE,
    artist_id int NOT NULL,
    genre_id smallint,
    album_name varchar(255) NOT NULL,
    album_year smallint,
    PRIMARY KEY (id),
    FOREIGN KEY (artist_id) REFERENCES Artists(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES Genres(id) ON DELETE SET NULL,
    CONSTRAINT unique_album UNIQUE(album_name, album_year)
);

CREATE TABLE Vinyls (
    id int auto_increment NOT NULL UNIQUE,
    album_id int NOT NULL,
    condition_id tinyint,
    retail_price decimal(8, 2),
    qty_in_stock int NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (album_id) REFERENCES Albums(id) ON DELETE RESTRICT,
    FOREIGN KEY (condition_id) REFERENCES Conditions(id) ON DELETE SET NULL,
    CONSTRAINT vinyl_condition UNIQUE(album_id, condition_id)
);

CREATE TABLE Customers (
    id int auto_increment NOT NULL UNIQUE,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    phone_number varchar(15),
    email varchar(50),
    zip_code varchar(10),
    membership boolean DEFAULT FALSE,
    PRIMARY KEY (id),
    CONSTRAINT customer_phone_number UNIQUE(first_name, last_name, phone_number),
    CONSTRAINT customer_email UNIQUE(first_name, last_name, email)
);

CREATE TABLE CustomerPurchases (
    id int auto_increment NOT NULL UNIQUE,
    customer_id int,
    purchase_date date NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (customer_id) REFERENCES Customers(id) ON DELETE SET NULL
);

CREATE TABLE CustomerPurchaseItems (
    customer_purchase_id int NOT NULL,
    vinyl_id int NOT NULL,
    quantity smallint NOT NULL,
    purchase_price decimal(8, 2) NOT NULL,
    PRIMARY KEY (customer_purchase_id, vinyl_id),
    FOREIGN KEY (customer_purchase_id) REFERENCES CustomerPurchases(id) ON DELETE CASCADE,
    FOREIGN KEY (vinyl_id) REFERENCES Vinyls(id) ON DELETE CASCADE
);

CREATE TABLE StorePurchases (
    id int auto_increment NOT NULL UNIQUE,
    customer_id int,
    purchase_date date NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (customer_id) REFERENCES Customers(id) ON DELETE SET NULL
);

CREATE TABLE StorePurchaseItems (
    store_purchase_id int NOT NULL,
    vinyl_id int NOT NULL,
    quantity smallint NOT NULL,
    purchase_price decimal(8, 2) NOT NULL,
    PRIMARY KEY (store_purchase_id, vinyl_id),
    FOREIGN KEY (store_purchase_id) REFERENCES StorePurchases(id) ON DELETE CASCADE,
    FOREIGN KEY (vinyl_id) REFERENCES Vinyls(id) ON DELETE CASCADE
);

-- Insert Example Data

INSERT INTO Artists (artist_name)
VALUES 
    ('The Beatles'),
    ('Pink Floyd'),
    ('Journey'),
    ('Kendrick Lamar'),
    ('Tame Impala'),
    ('Herbie Hancock');

INSERT INTO Conditions (description)
VALUES 
    ('New'),
    ('Like New'),
    ('Good'),
    ('Worn');

INSERT INTO Genres (description)
VALUES 
    ('Pop'),
    ('Country'),
    ('Rock'),
    ('Hip-Hop'),
    ('Jazz'),
    ('Electronic');

INSERT INTO Albums (artist_id, genre_id, album_name, album_year)
VALUES
    ((SELECT id FROM Artists WHERE artist_name='Pink Floyd'), (SELECT id FROM Genres WHERE description='Rock'), 'Dark Side of the Moon', 1973),
    ((SELECT id FROM Artists WHERE artist_name='Kendrick Lamar'), (SELECT id FROM Genres WHERE description='Hip-Hop'), 'To Pimp a Butterfly', 2015),
    ((SELECT id FROM Artists WHERE artist_name='Herbie Hancock'), (SELECT id FROM Genres WHERE description='Jazz'), 'Head Hunters', 1973),
    ((SELECT id FROM Artists WHERE artist_name='Tame Impala'), (SELECT id FROM Genres WHERE description='Rock'), 'Lonerism', 2012);

INSERT INTO Vinyls (album_id, condition_id, retail_price, qty_in_stock)
VALUES
    ((SELECT id FROM Albums WHERE album_name='Dark Side of the Moon'), (SELECT id FROM Conditions WHERE description='New'), 29.99, 5),
    ((SELECT id FROM Albums WHERE album_name='Dark Side of the Moon'), (SELECT id FROM Conditions WHERE description='Like New'), 20, 2),
    ((SELECT id FROM Albums WHERE album_name='To Pimp a Butterfly'), (SELECT id FROM Conditions WHERE description='New'), 29.99, 6),
    ((SELECT id FROM Albums WHERE album_name='Head Hunters'), (SELECT id FROM Conditions WHERE description='Like New'), 59.99, 1),
    ((SELECT id FROM Albums WHERE album_name='Lonerism'), (SELECT id FROM Conditions WHERE description='Good'), 14.99, 3);

INSERT INTO Customers (first_name, last_name, phone_number, email, zip_code, membership)
VALUES
    ('Jordan', 'Howell', NULL, 'howelljo@oregonstate.edu', NULL, TRUE),
    ('John', 'Smith', '541-123-1234', NULL, '97268', FALSE),
    ('Jane', 'Doe', '503-321-4321', 'jane.d@domain.com', '97324', FALSE),
    ('Henry', 'Christiani', NULL, 'chrishen@oregonstate.edu', '97508', TRUE),
    ('Herman', 'Cain', '503-888-8888', 'iamhermancain@hotmail.com', '97035', TRUE),
    ('Danny ', 'Devito', '503-999-9999', 'thetrashman@aol.com', '97021', FALSE);

INSERT INTO CustomerPurchases (customer_id, purchase_date)
VALUES
    ((SELECT id FROM Customers WHERE email='thetrashman@aol.com'), '2023-02-14'),
    ((SELECT id FROM Customers WHERE phone_number='503-321-4321'), '2023-03-28'),
    ((SELECT id FROM Customers WHERE first_name='Herman' AND last_name='Cain'), '2023-04-25');

INSERT INTO CustomerPurchaseItems (customer_purchase_id, vinyl_id, quantity, purchase_price)
VALUES
    (1, 
        (
            SELECT Vinyls.id FROM Vinyls 
            JOIN Albums ON Vinyls.album_id = Albums.id 
            JOIN Artists ON Albums.artist_id = Artists.id 
            JOIN Conditions ON Vinyls.condition_id = Conditions.id 
            WHERE Conditions.description='New' 
            AND Albums.album_name='To Pimp a Butterfly'
            AND Artists.artist_name = 'Kendrick Lamar' 
        ), 
        1, 29.99),
    (2, 
        (
            SELECT Vinyls.id FROM Vinyls 
            JOIN Albums ON Vinyls.album_id = Albums.id 
            JOIN Artists ON Albums.artist_id = Artists.id
            JOIN Conditions ON Vinyls.condition_id = Conditions.id 
            WHERE Conditions.description='New' 
            AND Albums.album_name='Dark Side of the Moon'
            AND Artists.artist_name = 'Pink Floyd'
        ), 
        1, 34.99),
    (3, 
        (
            SELECT Vinyls.id FROM Vinyls 
            JOIN Albums ON Vinyls.album_id = Albums.id 
            JOIN Artists ON Albums.artist_id = Artists.id
            JOIN Conditions ON Vinyls.condition_id = Conditions.id
            WHERE Conditions.description='Good' 
            AND Albums.album_name='Lonerism'
            AND Artists.artist_name = 'Tame Impala'
        ), 
        2, 20.99),
    (3, (
            SELECT Vinyls.id FROM Vinyls 
            JOIN Albums ON Vinyls.album_id = Albums.id 
            JOIN Artists ON Albums.artist_id = Artists.id
            JOIN Conditions ON Vinyls.condition_id = Conditions.id 
            WHERE Conditions.description='New' 
            AND Albums.album_name='Dark Side of the Moon'
            AND Artists.artist_name = 'Pink Floyd'
        ), 
        1, 29.99);

INSERT INTO StorePurchases (customer_id, purchase_date)
VALUES
    ((SELECT id FROM Customers WHERE first_name='Herman' AND last_name='Cain'), '2023-01-21'),
    (NULL, '2023-03-15'),
    ((SELECT id FROM Customers WHERE email='chrishen@oregonstate.edu'), '2023-03-20');

INSERT INTO StorePurchaseItems (store_purchase_id, vinyl_id, quantity, purchase_price)
VALUES
    (1, 
        (
            SELECT Vinyls.id FROM Vinyls 
            JOIN Albums ON Vinyls.album_id = Albums.id 
            JOIN Artists ON Albums.artist_id = Artists.id
            JOIN Conditions ON Vinyls.condition_id = Conditions.id 
            WHERE Conditions.description='Good' 
            AND Albums.album_name='Lonerism'
            AND Artists.artist_name = 'Tame Impala' 
        ), 
        3, 13.49),
    (2, 
        (
            SELECT Vinyls.id FROM Vinyls 
            JOIN Albums ON Vinyls.album_id = Albums.id 
            JOIN Artists ON Albums.artist_id = Artists.id
            JOIN Conditions ON Vinyls.condition_id = Conditions.id 
            WHERE Conditions.description='Like New' 
            AND Albums.album_name='Dark Side of the Moon'
            AND Artists.artist_name = 'Pink Floyd'
        ), 
        1, 6),
    (3, 
        (
            SELECT Vinyls.id FROM Vinyls 
            JOIN Albums ON Vinyls.album_id = Albums.id 
            JOIN Artists ON Albums.artist_id = Artists.id
            JOIN Conditions ON Vinyls.condition_id = Conditions.id 
            WHERE Conditions.description='Like New' 
            AND Albums.album_name='Head Hunters'
            AND Artists.artist_name = 'Herbie Hancock'
        ), 
        1, 18),
    (3, (
            SELECT Vinyls.id FROM Vinyls 
            JOIN Albums ON Vinyls.album_id = Albums.id 
            JOIN Artists ON Albums.artist_id = Artists.id
            JOIN Conditions ON Vinyls.condition_id = Conditions.id 
            WHERE Conditions.description='Like New' 
            AND Albums.album_name='Dark Side of the Moon'
            AND Artists.artist_name = 'Pink Floyd'
        ), 
        1, 15);
