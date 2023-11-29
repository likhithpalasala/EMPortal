import mysql.connector as mysql
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "Secret Key"

# MySQL Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "crud"
}

# Creating MySQL connection
db = mysql.connect(**db_config)
cursor = db.cursor()


# Creating model table for our CRUD database
class Data:
    def __init__(self, id, name, email, phone):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone


# this route is for inserting data to the MySQL database via HTML forms
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        query = "INSERT INTO Employees (id, name, email, phone) VALUES (%s, %s, %s, %s)"
        values = (id, name, email, phone)

        cursor.execute(query, values)
        db.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('index'))


# route to display data from MySQL database on the index page
@app.route('/')
def index():
    cursor.execute("SELECT * FROM Employees")
    result = cursor.fetchall()

    all_data = []
    for row in result:
        id = row[0]
        name = row[1]
        email = row[2]
        phone = row[3]
        data = Data(id, name, email, phone)
        all_data.append(data)
    return render_template("index.html", data=all_data)


# route to update data in MySQL database
@app.route('/update/<id>/', methods=['POST'])
def update(id):
    if request.method == 'POST':
        updated_id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        query = "UPDATE Employees SET name=%s, email=%s, phone=%s WHERE id=%s"
        values = (name, email, phone, updated_id)

        cursor.execute(query, values)
        db.commit()

        flash("Employee Updated Successfully")

        # Fetch updated data after committing changes
        cursor.execute("SELECT * FROM Employees")
        result = cursor.fetchall()

        all_data = []
        for row in result:
            id = row[0]
            name = row[1]
            email = row[2]
            phone = row[3]
            data = Data(id, name, email, phone)
            all_data.append(data)

        return render_template('index.html', data=all_data)

    else:
        flash("Invalid Request")
        return redirect(url_for('index'))




# route to delete data from MySQL database
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    query = "DELETE FROM Employees WHERE id = %s"
    values = (id,)

    cursor.execute(query, values)
    db.commit()

    flash("Employee Deleted Successfully")

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
