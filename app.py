from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv


# Configuration

app = Flask(__name__)

load_dotenv()



# app.config["MYSQL_HOST"] = os.getenv('host')
# app.config["MYSQL_USER"] = os.getenv('user')
# app.config["MYSQL_PASSWORD"] = os.getenv('sauce')
# app.config["MYSQL_DB"] = os.getenv('mysql_db')
# app.config["MYSQL_CURSORCLASS"] = os.getenv('cursor_class')
mysql = MySQL(app)


# Routes

@app.route('/')
def home():
    return render_template("home.j2")


@app.route('/customers', methods=["POST", "GET"])
def customers():
    if request.method == "GET":
        query = """
                SELECT id AS `ID`, CONCAT(first_name, " ", last_name) AS `Customer Name`, 
                phone_number AS `Phone Number`, email AS `Email`, zip_code AS `Zip Code`, 
                CASE
                    WHEN membership = 1 THEN '&#10004;'
                    ELSE ' '
                END AS `Membership`
                FROM Customers
                ORDER BY id;
                """
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        customer_data = cursor.fetchall()
        
        return render_template("customers.j2", data=customer_data)

    elif request.method == "POST":
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        phone_number = request.form.get("phoneNumber")
        email = request.form.get("email")
        zip_code = request.form.get("zipCode")
        membership = request.form.get("membership")
        query = """
                INSERT INTO Customers (first_name, last_name, phone_number, email, zip_code, membership)
                VALUES (%s, %s, %s, %s, %s, %s);
                """
        cur = mysql.connection.cursor()
        cur.execute(query, (first_name, last_name, phone_number, email, zip_code, membership))
        mysql.connection.commit()

        return redirect("/customers")


@app.route('/vinyls', methods=["POST", "GET"])
def vinyls():
    if request.method == "GET":
        query = """
                SELECT Vinyls.id AS `ID`, Albums.album_name AS `Album Name`, 
                Artists.artist_name AS `Artist`, Conditions.description AS `Condition`, 
                CONCAT('$', Vinyls.retail_price) AS `Price`, Vinyls.qty_in_stock AS `In Stock`
                FROM Vinyls
                JOIN Albums ON Vinyls.album_id = Albums.id
                JOIN Artists ON Albums.artist_id = Artists.id
                JOIN Conditions ON Vinyls.condition_id = Conditions.id;
                """
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        vinyls_data = cursor.fetchall()

        query2 = "SELECT * FROM Conditions ORDER BY id"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        condition_data = cur.fetchall()

        query3 = """
                SELECT Albums.id, Albums.artist_id, Albums.album_name, Artists.artist_name AS artist_name, Artists.id
                FROM Albums
                JOIN Artists ON Albums.artist_id = Artists.id;
                """
        cur = mysql.connection.cursor()
        cur.execute(query3)
        album_data = cur.fetchall() 
        
        return render_template("vinyls.j2", data=vinyls_data, albums=album_data, conditions=condition_data)

    elif request.method == "POST":
        album_id = request.form.get("albumName")
        condition_id = request.form.get("condition")
        price = request.form.get("price")
        quantity = request.form.get("quantity")

        query = """
                INSERT INTO Vinyls (album_id, condition_id, retail_price, qty_in_stock)
                VALUES (%s, %s, %s, %s);
                """
        cur = mysql.connection.cursor()
        cur.execute(query, (album_id, condition_id, price, quantity))
        mysql.connection.commit()

        return redirect("/vinyls")


@app.route("/edit_vinyl/<int:vinyl_id>", methods=["POST", "GET"])
def edit_vinyl(vinyl_id):
    if request.method == "GET":
        query = """
                SELECT Vinyls.id, Albums.album_name, Conditions.description, 
                Vinyls.retail_price, Vinyls.qty_in_stock
                FROM Vinyls
                JOIN Albums ON Vinyls.album_id = Albums.id
                JOIN Conditions ON Vinyls.condition_id = Conditions.id
                WHERE Vinyls.id = %s; 
                """ % (vinyl_id)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        vinyl_data = cursor.fetchall()

        query2 = """
                SELECT id, description
                FROM Conditions
                ORDER BY id;
                """
        cur = mysql.connection.cursor()
        cur.execute(query2)
        condition_data = cur.fetchall()

        query3 = """
                SELECT Albums.id, Albums.artist_id, Albums.album_name, Artists.artist_name AS artist_name, Artists.id
                FROM Albums
                JOIN Artists ON Albums.artist_id = Artists.id;
                """
        cur = mysql.connection.cursor()
        cur.execute(query3)
        album_data = cur.fetchall() 

        return render_template("edit_vinyl.j2", data=vinyl_data, albums=album_data, conditions=condition_data)

    elif request.method == "POST":
        if request.form.get('edit_vinyl'):
            album_id = request.form["albumName"]
            condition = request.form["condition"]
            price = request.form["price"]
            quantity = request.form["quantity"]
            
            query = "UPDATE Vinyls SET album_id = %s, condition_id = %s, retail_price = %s, qty_in_stock = %s WHERE id = %s;"
                
            cur = mysql.connection.cursor()
            cur.execute(query, (album_id, condition, price, quantity, vinyl_id))
            mysql.connection.commit()

    return redirect("/vinyls")


@app.route("/delete_vinyl/<int:vinyl_id>")
def delete_vinyl(vinyl_id):
    query = "DELETE FROM Vinyls WHERE id=%s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (vinyl_id,))
    mysql.connection.commit()

    return redirect("/vinyls")


@app.route('/albums', methods=["POST", "GET"])
def albums():
    if request.method == "GET":
        query = """
                SELECT Albums.id AS `ID`, Albums.album_name AS `Album Name`, 
                Artists.artist_name AS `Artist Name`, Albums.album_year AS `Release`
                FROM Albums
                JOIN Artists ON Albums.artist_id = Artists.id
                ORDER BY id;
                """
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        album_data = cursor.fetchall()

        query2 = "SELECT id, artist_name FROM Artists"
        cursor = mysql.connection.cursor()
        cursor.execute(query2)
        artist_data = cursor.fetchall()

        query3 = "SELECT id, description FROM Genres"
        cursor = mysql.connection.cursor()
        cursor.execute(query3)
        genre_data = cursor.fetchall()
        
        return render_template("albums.j2", data=album_data, artists=artist_data, genres=genre_data)

    elif request.method == "POST":
        album_name = request.form.get("albumName")
        artist_name = request.form.get("artistName")
        genre = request.form.get("genre")
        album_year = request.form.get("albumYear")
        query = """
                INSERT INTO Albums (artist_id, genre_id, album_name, album_year)
                VALUES (%s, %s, %s, %s);
                """
        cur = mysql.connection.cursor()
        cur.execute(query, (artist_name, genre, album_name, album_year))
        mysql.connection.commit()

    return redirect("/albums")


@app.route('/artists', methods=["POST", "GET"])
def artists():
    if request.method == "GET":
        query = """
                SELECT id AS `ID`, artist_name AS `Artist Name`
                FROM Artists
                ORDER BY id;
                """
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        artist_data = cursor.fetchall()
        
        return render_template("artists.j2", data=artist_data)
    
    elif request.method == "POST":
        artist_name = request.form.get("artistName")
        query = """
                INSERT INTO Artists (artist_name)
                VALUES (%s);
                """
        cur = mysql.connection.cursor()
        cur.execute(query, (artist_name,))
        mysql.connection.commit()

    return redirect("/artists")


@app.route("/edit_artist/<int:artist_id>", methods=["POST", "GET"])
def edit_artist(artist_id):
    if request.method == "GET":
        query = """
                SELECT id, artist_name
                FROM Artists
                WHERE id=%s;
                """ % (artist_id)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        artist_data = cursor.fetchall()

        return render_template("edit_artist.j2", data=artist_data)

    elif request.method == "POST":
        if request.form.get('edit_artist'):
            artist_name = request.form["artistName"]
            query = """
                    UPDATE Artists
                    SET artist_name=%s
                    WHERE id=%s;
                    """
            print(artist_name, artist_id)
            cur = mysql.connection.cursor()
            cur.execute(query, (artist_name, artist_id))
            mysql.connection.commit()

    return redirect("/artists")


@app.route("/delete_artist/<int:artist_id>")
def delete_artist(artist_id):
    query = "DELETE FROM Artists WHERE id=%s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (artist_id,))
    mysql.connection.commit()

    return redirect("/artists")


@app.route('/genres', methods=["POST", "GET"])
def genres():
    if request.method == "GET":
        query = """
                SELECT id AS `ID`, description AS `Description`
                FROM Genres
                ORDER BY id;
                """
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        genre_data = cursor.fetchall()
        
        return render_template("genres.j2", data=genre_data)
    
    elif request.method == "POST":
        genre_description = request.form.get("genre")
        query = """
                INSERT INTO Genres (description)
                VALUES (%s);
                """
        cur = mysql.connection.cursor()
        cur.execute(query, (genre_description,))
        mysql.connection.commit()

    return redirect("/genres")


@app.route("/edit_genre/<int:genre_id>", methods=["POST", "GET"])
def edit_genre(genre_id):
    if request.method == "GET":
        query = """
                SELECT id, description
                FROM Genres
                WHERE id=%s;
                """ %(genre_id)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        genre_data = cursor.fetchall()

        return render_template("edit_genre.j2", data=genre_data)

    elif request.method == "POST":
        if request.form.get('edit_genre'):
            description = request.form["genre"]
            query = """
                    UPDATE Genres
                    SET description=%s
                    WHERE id=%s;
                    """
            
            cur = mysql.connection.cursor()
            cur.execute(query, (description, genre_id))
            mysql.connection.commit()

    return redirect("/genres")


@app.route("/delete_genre/<int:genre_id>")
def delete_genre(genre_id):
    query = "DELETE FROM Genres WHERE id=%s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (genre_id,))
    mysql.connection.commit()

    return redirect("/genres")


@app.route('/conditions', methods=["POST", "GET"])
def conditions():
    if request.method == "GET":
        query = """
                SELECT id AS `ID`, description AS `Description`
                FROM Conditions
                ORDER BY id;
                """
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        condition_data = cursor.fetchall()
        
        return render_template("conditions.j2", data=condition_data)
    
    elif request.method == "POST":
        condition_description = request.form.get("condition")
        query = """
                INSERT INTO Conditions (description)
                VALUES (%s);
                """
        cur = mysql.connection.cursor()
        cur.execute(query, (condition_description,))
        mysql.connection.commit()

    return redirect("/conditions")


@app.route("/edit_condition/<int:condition_id>", methods=["POST", "GET"])
def edit_condition(condition_id):
    if request.method == "GET":
        query = """
                SELECT id, description
                FROM Conditions
                WHERE id=%s;
                """ %(condition_id)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        condition_data = cursor.fetchall()

        return render_template("edit_condition.j2", data=condition_data)

    elif request.method == "POST":
        if request.form.get('edit_condition'):
            description = request.form["condition"]
            query = """
                    UPDATE Conditions
                    SET description=%s
                    WHERE id=%s;
                    """
            
            cur = mysql.connection.cursor()
            cur.execute(query, (description, condition_id))
            mysql.connection.commit()

    return redirect("/conditions")


@app.route("/delete_condition/<int:condition_id>")
def delete_condition(condition_id):
    query = "DELETE FROM Conditions WHERE id=%s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (condition_id,))
    mysql.connection.commit()

    return redirect("/conditions")


@app.route('/customer-purchases', methods=["POST", "GET"])
def customer_purchases():
    if request.method == "GET":
        query = """
                SELECT CustomerPurchases.id AS `ID`, Albums.album_name AS `Album Name`, 
                Artists.artist_name AS `Artist`, CustomerPurchaseItems.quantity AS `Quantity`, 
                CONCAT('$', CustomerPurchaseItems.purchase_price) AS `Total Purchase`,
                DATE_FORMAT(CustomerPurchases.purchase_date, '%m-%d-%Y') AS `Purchase Date`, 
                CONCAT(Customers.first_name, ' ', Customers.last_name) AS `Customer`
                FROM CustomerPurchases
                JOIN Customers ON CustomerPurchases.customer_id = Customers.id
                JOIN CustomerPurchaseItems ON CustomerPurchases.id = CustomerPurchaseItems.customer_purchase_id
                JOIN Vinyls ON CustomerPurchaseItems.vinyl_id = Vinyls.id
                JOIN Albums ON Vinyls.album_id = Albums.id
                JOIN Artists ON Albums.artist_id = Artists.id;
                """
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        customer_purchase_data = cursor.fetchall()

        query2 = "SELECT id, first_name, last_name FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        customer_data = cur.fetchall()

        query3 = """
                SELECT DISTINCT Albums.id, Albums.artist_id, Albums.album_name, Artists.artist_name AS artist_name,
                Artists.id
                FROM Vinyls
                JOIN Albums ON Vinyls.album_id = Albums.id
                JOIN Artists ON Albums.artist_id = Artists.id
                WHERE Vinyls.qty_in_stock > 0;
                """ 
        cur = mysql.connection.cursor()
        cur.execute(query3)
        album_data = cur.fetchall()

        query4 = """
                SELECT DISTINCT Conditions.id, Conditions.description
                FROM Vinyls
                JOIN Conditions ON Vinyls.condition_id = Conditions.id
                WHERE Vinyls.qty_in_stock > 0
                ORDER BY id;
                """ 
        cur = mysql.connection.cursor()
        cur.execute(query4)
        condition_data = cur.fetchall()
        
        return render_template("customer-purchases.j2", data=customer_purchase_data, customers=customer_data, albums=album_data, conditions=condition_data)

    elif request.method == "POST":
        customer_id = request.form.get("customerName")
        purchase_date = request.form.get("purchaseDate")
        album_name = request.form.get("albumName")
        condition = request.form.get("condition")
        price = request.form.get("price")
        quantity = request.form.get("quantity")
        submit_button = request.form["button"]

        query = """
                INSERT INTO CustomerPurchases (customer_id, purchase_date)
                VALUES (%s, %s)
                """
        cur = mysql.connection.cursor()
        cur.execute(query, (customer_id, purchase_date))
        mysql.connection.commit()
        

        query2 = """
                INSERT INTO CustomerPurchaseItems (customer_purchase_id, vinyl_id, quantity, purchase_price)
                VALUES ((SELECT id
                        FROM CustomerPurchases
                        ORDER BY id DESC
                        LIMIT 1), 
                        (SELECT Vinyls.id
                        FROM Vinyls
                        JOIN Albums ON Vinyls.album_id = Albums.id
                        JOIN Conditions ON Vinyls.condition_id = Conditions.id
                        WHERE Vinyls.album_id = %s and Vinyls.condition_id = %s), 
                        %s, 
                        (SELECT retail_price * %s
                        FROM Vinyls
                        WHERE album_id = %s and condition_id = %s));
                """
        cur.execute(query2, (album_name, condition, quantity, quantity, album_name, condition))
        mysql.connection.commit()

        # Updates "In Stock" Column on Vinyls page when purchase is made
        query3 = """
                UPDATE Vinyls
                SET qty_in_stock = qty_in_stock - %s
                WHERE qty_in_stock >= 0 and album_id = %s and condition_id = %s;
                 """
        cur.execute(query3, (quantity, album_name, condition))
        mysql.connection.commit()
        
        return redirect("/customer-purchases")


@app.route('/store-purchases', methods=["POST", "GET"])
def store_purchases():
    if request.method == "GET":
        query = """
                SELECT StorePurchases.id AS `ID`, Albums.album_name AS `Album Name`, 
                Artists.artist_name AS `Artist`, StorePurchaseItems.quantity AS `Quantity`, 
                CONCAT('$', StorePurchaseItems.purchase_price) AS `Total Purchase`,
                DATE_FORMAT(StorePurchases.purchase_date, '%m-%d-%Y') AS `Purchase Date`, 
                CONCAT(Customers.first_name, ' ', Customers.last_name) AS `Customer`
                FROM StorePurchases
                JOIN Customers ON StorePurchases.customer_id = Customers.id
                JOIN StorePurchaseItems ON StorePurchases.id = StorePurchaseItems.store_purchase_id
                JOIN Vinyls ON StorePurchaseItems.vinyl_id = Vinyls.id
                JOIN Albums ON Vinyls.album_id = Albums.id
                JOIN Artists ON Albums.artist_id = Artists.id;
                """
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        store_purchase_data = cursor.fetchall()

        query2 = "SELECT id, first_name, last_name FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        customer_data = cur.fetchall() 

        #Dynmaically generates condition data in store-purchases.j2 for loop
        query3 = """
                SELECT id, description
                FROM Conditions
                ORDER BY id;
                """
        cur = mysql.connection.cursor()
        cur.execute(query3)
        condition_data = cur.fetchall()

        #Dynamically album data in store-purchases.j2 for loop
        query4 = """
                SELECT Albums.id, Albums.artist_id, Albums.album_name, Artists.artist_name AS artist_name, Artists.id
                FROM Albums
                JOIN Artists ON Albums.artist_id = Artists.id;
                """
        cur = mysql.connection.cursor()
        cur.execute(query4)
        album_data = cur.fetchall() 
        
        return render_template("store-purchases.j2", data=store_purchase_data, customers=customer_data, albums=album_data, conditions=condition_data)

    elif request.method == "POST":
        customer_id = request.form.get("customerName")
        purchase_date = request.form.get("purchaseDate")
        album_name = request.form.get("albumName")
        condition = request.form.get("condition")
        price = request.form.get("price")
        quantity = request.form.get("quantity")

        #Inserts values from "Seller's Information" into StorePurchases table
        query = """
                INSERT INTO StorePurchases (customer_id, purchase_date)
                VALUES (%s, %s)
                """
        cur = mysql.connection.cursor()
        cur.execute(query, (customer_id, purchase_date))
        mysql.connection.commit()

        query2 = """
                SELECT id
                FROM Vinyls
                WHERE album_id = %s and condition_id = %s
                """
        cur.execute(query2, (album_name, condition))
        existing_vinyl = cur.fetchone()

        if existing_vinyl is not None:
                query3 = """
                        UPDATE Vinyls
                        SET qty_in_stock = qty_in_stock + %s
                        WHERE album_id = %s and condition_id = %s;
                        """
                cur.execute(query3, (quantity, album_name, condition))
                mysql.connection.commit()

                query4 = """
                        INSERT INTO StorePurchaseItems (store_purchase_id, vinyl_id, quantity, purchase_price)
                        VALUES ((SELECT id
                                FROM StorePurchases
                                ORDER BY id DESC
                                LIMIT 1), 
                                (SELECT Vinyls.id
                                FROM Vinyls
                                JOIN Albums ON Vinyls.album_id = Albums.id
                                JOIN Conditions ON Vinyls.condition_id = Conditions.id
                                WHERE Vinyls.album_id = %s and Vinyls.condition_id = %s), 
                                %s, 
                                (SELECT ((retail_price * %s) - ((retail_price * 0.40) * %s)) 
                                FROM Vinyls
                                WHERE album_id = %s AND condition_id = %s));
                        """
                cur.execute(query4, (album_name, condition, quantity, quantity, quantity, album_name, condition))
                mysql.connection.commit()

        else:
                #Inserts values from "Store Purchased Item" into Vinyls table    
                query3 = """
                        INSERT INTO Vinyls (album_id, condition_id, retail_price, qty_in_stock)
                        VALUES (%s, %s, ((%s + (%s * 0.40)) / %s ) , %s);
                        """
                cur.execute(query3, (album_name, condition, price, price, quantity, quantity))
                mysql.connection.commit()

                #Inserts values from both "Seller's Information" and "Store Purchased Item" into StorePurchaseItems table
                query4 = """
                        INSERT INTO StorePurchaseItems (store_purchase_id, vinyl_id, quantity, purchase_price)
                        VALUES ((SELECT id
                                FROM StorePurchases
                                ORDER BY id DESC
                                LIMIT 1), 
                                (SELECT Vinyls.id
                                FROM Vinyls
                                JOIN Albums ON Vinyls.album_id = Albums.id
                                JOIN Conditions ON Vinyls.condition_id = Conditions.id
                                WHERE Vinyls.album_id = %s and Vinyls.condition_id = %s), 
                                %s, %s);
                        """
                cur.execute(query4, (album_name, condition, quantity, price))
                mysql.connection.commit()


        return redirect("/store-purchases")

#Route autopopulates coditions in "Customer Purchased Item" form based on the album selected
@app.route('/conditions/<int:artist_id>', methods=["GET"])
def get_conditions(artist_id):
    query = """
            SELECT Conditions.id, Conditions.description
            FROM Vinyls
            JOIN Conditions ON Vinyls.condition_id = Conditions.id
            JOIN Albums ON Vinyls.album_id = Albums.id
            WHERE Albums.artist_id = %s and Vinyls.qty_in_stock > 0
            ORDER BY id;
            """ 
    cur = mysql.connection.cursor()
    cur.execute(query, (artist_id,))
    condition_data = cur.fetchall()

    return jsonify(condition_data)

@app.route('/get_max_quantity')
def get_max_quantity():
    album_id = request.args.get('album_id')
    condition_id = request.args.get('condition_id')
    
    query = """
            SELECT qty_in_stock 
            FROM Vinyls 
            WHERE album_id = %s AND condition_id = %s;
            """
    cur = mysql.connection.cursor()
    cur.execute(query, (album_id, condition_id))
    max_quantity = cur.fetchone()
    
    return str(max_quantity['qty_in_stock'])

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(port=port, debug=True)

