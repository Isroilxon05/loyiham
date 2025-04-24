from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_mysqldb import MySQL
from datetime import datetime 

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'Donir'
    
db = MySQL(app)

@app.route("/olish")
def olish():
    return render_template("olish.html")

@app.route("/savat")
def savat():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM savat;")
    students = cur.fetchall()
    return render_template("savat.html", students=students)

@app.route("/delete_card/<int:id>", methods=["POST"])
def delete_card(id):
    cur = db.connection.cursor()
    cur.execute(f"DELETE FROM cards WHERE ID={id}")
    db.connection.commit()
    return redirect(url_for('card'))

@app.route("/")
def menu():
    return render_template("menu.html")

@app.route("/card", methods=["GET", "POST"])
def card():
    cur = db.connection.cursor()

 
    card_id = request.cookies.get('card_id')

    if card_id:
        cur.execute(f"SELECT * FROM cards WHERE id = {card_id}")
        card = cur.fetchone()
    else:
        card = None

    if request.method == "POST":
        card_number = request.form['card_number']
        expiry_date = request.form['expiry_date']

        
        if len(card_number) != 16 or not card_number.isdigit():
            return "Karta raqami 16 ta raqamdan iborat bo'lishi kerak!"

        
        now = datetime.now()  
        exp_month, exp_year = expiry_date.split('/')
        exp_year = int('20' + exp_year)
        exp_month = int(exp_month)

        if exp_year < now.year or (exp_year == now.year and exp_month < now.month):
            return "Amal qilish muddati tugagan!"

      
        cur.execute(f'INSERT INTO cards (card_number, expiry_date) VALUES ("{card_number}", "{expiry_date}")')
        db.connection.commit()
        card_id = cur.lastrowid

 
        response = make_response(redirect(url_for('card')))
        response.set_cookie('card_id', str(card_id), max_age=60 * 60 * 24 * 365)  
        return response

    return render_template("card_get.html", card=card)

@app.route("/mendagi_donirlar")
def mendagi_dopnirlar():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM mendagi_donirlar;")
    students = cur.fetchall()
    return render_template("mendagi_donorlar.html", students=students)

@app.route("/index")
def index():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM Donirlar;")
    students = cur.fetchall()
    return render_template("index.html", students=students)

@app.route("/index1")
def index1():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM Donirlar;")
    students = cur.fetchall()
    return render_template("olish.html", students=students)

@app.route("/qidruv")
def qidruv():
    if request.method == "POST":
        donor_name = request.form['Donor_name']
        cur = db.connection.cursor()
        cur.execute(f"SELECT * FROM Donirlar where nomi='{donor_name}';")
        students = cur.fetchall()
        return render_template("qidruv.html", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        address = request.form['address']
        Phone_number = request.form['Phone_number']
        Donor_name = request.form["Donor_name"]
        price = request.form["price"]

        cur = db.connection.cursor()
        cur.execute(f'INSERT INTO mendagi_donirlar(Ism, Familiya , Manzil, Tel_raqam , Nomi , Narxi) VALUES("{name}", "{surname}", "{address}", "{Phone_number}", "{Donor_name}", "{price}" );')
        db.connection.commit()
        cur.execute(f'INSERT INTO Donirlar(Ism, Familiya , Manzil, Tel_raqam , Nomi , Narxi) VALUES("{name}", "{surname}", "{address}", "{Phone_number}", "{Donor_name}", "{price}" );')
        db.connection.commit()
        return redirect(url_for('index'))

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit_student(id):
    cur = db.connection.cursor()
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        address = request.form['address']
        Phone_number = request.form['Phone_number']
        Donor_name = request.form["Donor_name"]
        price = request.form["price"]

        cur.execute(f"UPDATE Donirlar SET Ism='{name}', Familiya='{surname}', manzil='{address}', tel_raqam ='{Phone_number}', Nomi='{Donor_name}' , Narxi='{price}' WHERE id='{id}'")
        db.connection.commit()
        return redirect(url_for('index'))

    cur.execute(f"SELECT * FROM Donirlar WHERE id={id}")
    student = cur.fetchone()
    return render_template('edit.html', student = student)

@app.route("/savatga_olish/<int:id>/<string:name>/<string:surname>/<string:address>/<string:phone_number>/<string:donor_name>/<string:price>")
def savatga_olish(id, name, surname, address, phone_number, donor_name, price):
    cur = db.connection.cursor()
    cur.execute(f'INSERT INTO Savat VALUES("{id}","{name}", "{surname}", "{address}", "{phone_number}", "{donor_name}", "{price}" );')
    db.connection.commit()
    cur.execute("SELECT * FROM Donirlar;")
    students = cur.fetchall()
    return render_template("olish.html", students=students)

@app.route("/delete/<int:id>")
def delete_donor(id):
    cur = db.connection.cursor()
    cur.execute(f"DELETE FROM DONIRLAR WHERE ID={id}")
    db.connection.commit()
    cur.execute(f"DELETE FROM savat WHERE id={id}")
    db.connection.commit()
    cur.execute("SELECT * FROM savat;")
    students = cur.fetchall()
    return render_template("savat.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)
