from flask import Flask, render_template, request, url_for, redirect

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/resultados")
def resultados():
    return render_template("resultados.html")

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    nombre = request.form['nombre']
    return f'Formulario enviado por {nombre}'

if __name__ == "__main__":
    app.run(debug=True, port=3500)

