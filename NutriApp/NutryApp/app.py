from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'cambia_esto_en_produccion'

def _get_first(form, *keys, default=''):
    """Returns the first non-empty value from the form for the given keys."""
    for k in keys:
        v = form.get(k)
        if v is not None:
            return v
    return default

@app.route('/clear')
def clear():
    """Borrar datos del usuario guardados en sesión y volver al formulario."""
    session.pop('user', None)
    session.pop('authenticated', None)
    flash('Datos borrados.')
    return redirect(url_for('formulario'))

@app.route('/')
def inicio():
    """Home page with information about the application."""
    return render_template('info.html')

@app.route('/formulario')
def formulario():
    """Page that contains the form for user input."""
    user = session.get('user', {})
    return render_template('formulario.html', **user)

@app.route('/resultado', methods=['POST'])
def resultado():
    """Processes the form data and calculates BMI and caloric needs."""
    nombre = _get_first(request.form, 'nombre', 'Nombre', '').strip()
    apellido = _get_first(request.form, 'apellido', 'Apellido', '').strip()
    edad_raw = _get_first(request.form, 'edad', 'Edad', '')
    peso_raw = _get_first(request.form, 'peso', 'Peso', '')
    altura_raw = _get_first(request.form, 'altura', 'Altura', '')
    contraseña = _get_first(request.form, 'contraseña', 'contrasena', '')
    correo_electronico = _get_first(request.form, 'correo_electronico', 'correo', '')
    genero = _get_first(request.form, 'genero', 'Genero', 'masculino')

    try:
        edad = int(edad_raw)
        peso = float(peso_raw)
        altura = float(altura_raw)
    except (ValueError, TypeError):
        error_msg = "Por favor completa todos los campos correctamente."
        return render_template(
            'formulario.html',
            nombre=nombre,
            apellido=apellido,
            edad=edad_raw,
            peso=peso_raw,
            altura=altura_raw,
            genero=genero,
            correo_electronico=correo_electronico,
            contraseña=contraseña,
            error=error_msg
        )

    imc = round(peso / (altura ** 2), 2)

    if imc < 18.5:
        clasificacion = "Bajo peso"
        recomendacion = "Aumenta tu ingesta calórica con alimentos saludables y realiza ejercicios de fuerza."
    elif imc < 25:
        clasificacion = "Peso normal"
        recomendacion = "Mantén una dieta equilibrada y continúa con actividad física regular."
    elif imc < 30:
        clasificacion = "Sobrepeso"
        recomendacion = "Reduce azúcares y grasas, e incrementa tu consumo de frutas y verduras."
    else:
        clasificacion = "Obesidad"
        recomendacion = "Consulta a un especialista y adopta un plan de alimentación controlado."

    if genero.lower() == "masculino":
        tmb = 10 * peso + 6.25 * (altura * 100) - 5 * edad + 5
    else:
        tmb = 10 * peso + 6.25 * (altura * 100) - 5 * edad - 161

    calorias_mantenimiento = round(tmb * 1.55, 2)

    session['user'] = {
        'nombre': nombre,
        'apellido': apellido,
        'edad': edad,
        'peso': peso,
        'altura': altura,
        'correo_electronico': correo_electronico,
        'contraseña': contraseña,
        'genero': genero,
        'imc': imc,
        'clasificacion': clasificacion,
        'recomendacion': recomendacion,
        'calorias': calorias_mantenimiento
    }

    return render_template(
        'formulario.html',
        nombre=nombre,
        apellido=apellido,
        edad=edad,
        peso=peso,
        altura=altura,
        correo_electronico=correo_electronico,
        contraseña=contraseña,
        genero=genero,
        imc=imc,
        clasificacion=clasificacion,
        recomendacion=recomendacion,
        calorias=calorias_mantenimiento
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login with correo and contraseña stored from formulario."""
    if request.method == 'GET':
        return render_template('login.html')
    correo = request.form.get('correo', '').strip()
    contraseña = request.form.get('contraseña', '')
    user = session.get('user')
    if not user:
        flash('No hay datos registrados. Completa primero el formulario.')
        return redirect(url_for('formulario'))
    if correo == user.get('correo_electronico') and contraseña == user.get('contraseña'):
        session['authenticated'] = True
        return redirect(url_for('rutina'))
    flash('Correo o contraseña incorrectos.')
    return render_template('login.html')

@app.route('/rutina')
def rutina():
    """Muestra rutina y plan basado en los datos guardados.

    Permite acceso si existe 'user' en sesión incluso cuando no hay flag
    'authenticated' (para que el botón 'Ir a rutina' funcione sin pedir login).
    """
    user = session.get('user')
    if not user:
        flash('Completa el formulario o inicia sesión para ver tu rutina.')
        return redirect(url_for('formulario'))

    if not session.get('authenticated'):
        session['authenticated'] = True
    return render_template('rutina.html', user=user)

@app.route("/tmb", methods=["GET", "POST"])
def tmb():
    if request.method == "POST":
        try:
            peso = float(request.form["peso"])
            altura = float(request.form["altura"])
            edad = int(request.form["edad"])
            genero = request.form["genero"]

            if genero == "masculino":
                tmb = 88.36 + 13.4 * peso + 4.8 * altura - 5.7 * edad
            else:
                tmb = 447.6 + 9.2 * peso + 3.1 * altura - 4.3 * edad

            return render_template("tmb.html", tmb=round(tmb, 2), peso=peso,
                                altura=altura, edad=edad, genero=genero)
        except:
            return render_template("tmb.html", error="Datos inválidos")

    return render_template("tmb.html")

@app.route('/perfil')
def perfil():
    """Muestra toda la información del usuario y botón para cerrar sesión."""
    if not session.get('authenticated'):
        flash('Inicia sesión para ver tu perfil.')
        return redirect(url_for('login'))
    user = session.get('user', {})
    return render_template('perfil.html', user=user)

@app.route("/gct", methods=["GET", "POST"])
def gct():
    if request.method == "POST":
        tmb = float(request.form["tmb"])
        actividad = float(request.form["actividad"])
        gct = tmb * actividad
        return render_template("gct.html", gct=round(gct, 1))
    return render_template("gct.html")

@app.route('/logout')
def logout():
    """Cerrar sesión y regresar al inicio."""
    session.pop('authenticated', None)

    session.pop('user', None)
    flash('Sesión cerrada.')
    return redirect(url_for('inicio'))

@app.route("/peso_ideal", methods=["GET", "POST"])
def peso_ideal():
    if request.method == "POST":
        altura = float(request.form["altura"])
        genero = request.form["genero"]

        base = altura - 152.4

        if genero == "masculino":
            ideal = 50 + 0.9 * base
        else:
            ideal = 45.5 + 0.9 * base

        return render_template("peso_ideal.html", ideal=round(ideal, 1))

    return render_template("peso_ideal.html")

@app.route("/macros", methods=["GET", "POST"])
def macros():
    if request.method == "POST":
        calorias = float(request.form["calorias"])
        p = float(request.form["p"])
        c = float(request.form["c"])
        g = float(request.form["g"])

        kcal_p = calorias * p / 100
        kcal_c = calorias * c / 100
        kcal_g = calorias * g / 100

        resultado = {
            "prot": round(kcal_p / 4, 1),
            "carb": round(kcal_c / 4, 1),
            "fat": round(kcal_g / 9, 1)
        }

        return render_template("macros.html", macros=resultado)

    return render_template("macros.html")

@app.route("/recetas", methods=["GET", "POST"])
def recetas():
    if request.method == "POST":
        texto = request.form["ingredientes"].strip().split("\n")

        total = 0
        for l in texto:
            try:
                kcal = float(l.split()[-2]) if "kcal" in l else float(l.split()[-1])
                total += kcal
            except:
                pass

        return render_template("recetas.html", total=round(total, 1))

    return render_template("recetas.html")

if __name__ == '__main__':
    app.run(debug=True)