import os
from flask import Flask, render_template, request, redirect, url_for
import database as db


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')


app = Flask(__name__, template_folder=template_dir)

# Rutas de la aplicación 
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    # Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()

    return render_template('index.html', data=insertObject)



# Ruta para guardar usuarios en la base de datos
@app.route('/user', methods=["POST"])
def addUser():
    nombre = request.form['customername']
    estado = request.form['state']
    ciudad = request.form['city']

    if nombre and estado and ciudad:
        cursor = db.database.cursor()
        sql = "INSERT INTO users (Nombre, Estado, Ciudad) VALUES (%s, %s, %s)"
        data = (nombre, estado, ciudad)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))


@app.route('/edit/<string:id>')
def edit(id):
    return render_template('edit.html')


@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=5050) 