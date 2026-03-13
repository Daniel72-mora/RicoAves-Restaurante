from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="rico_aves"
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        email = request.form['email']
        telefono = request.form['telefono']
        
        conn = get_db()
        cursor = conn.cursor()
        sql = "INSERT INTO clientes (nombre, telefono, direccion, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nombre, telefono, direccion, email))
        conn.commit()
        cursor.close()
        conn.close()
        return "<h1>¡Registro exitoso!</h1><a href='/'>Volver al formulario</a>"
    
    # Flask busca automáticamente en la carpeta 'templates'
    return render_template('contactos.html')

if __name__ == '__main__':
    app.run(debug=True)