from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="crud"
    )

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    connection.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    connection = get_db_connection()
    cursor = connection.cursor()
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    cursor.execute("INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
    connection.commit()
    connection.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_user(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    connection.commit()
    connection.close()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cursor.execute("UPDATE users SET name = %s, email = %s, phone = %s WHERE id = %s", (name, email, phone, id))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()
        connection.close()
        return render_template('update.html', res=user)

if __name__ == '__main__':
    app.run(debug=True)
