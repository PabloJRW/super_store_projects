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
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
    a_editar = cursor.fetchall()
    db.database.commit()
    
    return render_template('edit.html', data=a_editar)

@app.route('/update/<string:id>')
def update(id):
    nombre = request.form.get('customername')
    estado = request.form.get('state')
    ciudad = request.form.get('city')
    
    if nombre and estado and ciudad:
        cursor = db.database.cursor()
        values_to_edit = (nombre, estado, ciudad, id)
        cursor.execute("UPDATE users SET Nombre=%s, Estado=%s, Ciudad=%s WHERE id=%s", values_to_edit)
        db.database.commit()

    return redirect('/'), print(id)


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