import os
from flask import Flask, render_template, request, redirect, url_for
import database as db


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')


app = Flask(__name__, template_folder=template_dir)

# Principal 
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


# Ruta para la página de registro de usuarios
@app.route('/register')
def register():
    return render_template('register.html')


# Ruta para guardar clientes en la base de datos
@app.route('/user', methods=["POST"])
def addUser():
    nombre = request.form['customername']
    estado = request.form['state']
    ciudad = request.form['city']

    if nombre and estado and ciudad:
        cursor = db.database.cursor()
        sql = "INSERT INTO users (nombre, estado, ciudad) VALUES (%s, %s, %s)"
        data = (nombre, estado, ciudad)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

# Ruta para editar los datos de los clientes
@app.route('/edit/<string:id>')
def edit(id):
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
    response = cursor.fetchall()
    columnNames  = [column[0] for column in cursor.description]
    a_editar=[]
    for record in response:
        a_editar.append(dict(zip(columnNames, record)))
    cursor.close()
    
    return render_template('edit.html', data=a_editar)


# Ruta para actualizar los datos editados de los clientes
@app.route('/update/<string:id>')
def update(id):
    nombre = request.form.get('customername', False)
    estado = request.form.get('state', False)
    ciudad = request.form.get('city', False)
   
    if nombre and estado and ciudad:
        cursor = db.database.cursor()
        values_to_edit = (nombre, estado, ciudad, id)
        cursor.execute("UPDATE users SET nombre=%s, estado=%s, ciudad=%s WHERE id=%s", values_to_edit)
        db.database.commit()

    return redirect(url_for('home')), print(id,nombre,estado, ciudad)


# Ruta para eliminar registro de usuario
@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id=%s" 
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True) 