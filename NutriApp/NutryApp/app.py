from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('formulario.html')

@app.route('/resultado', methods=['POST'])
def resultado():

    nombre = request.form.get('nombre', '').strip()
    edad_raw = request.form.get('edad', '')
    peso_raw = request.form.get('peso', '')
    altura_raw = request.form.get('altura', '')
    genero = request.form.get('genero', 'masculino') 

    
    try:
        edad = int(edad_raw)
        peso = float(peso_raw)
        altura = float(altura_raw)
    except (ValueError, TypeError):

        return render_template('formulario.html', nombre=nombre, edad=edad_raw, peso=peso_raw, altura=altura_raw, genero=genero, error="Por favor completa todos los campos correctamente.")

    imc = peso / (altura ** 2)

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

    if genero == "masculino":
        tmb = 10 * peso + 6.25 * (altura * 100) - 5 * edad + 5
    else:
        tmb = 10 * peso + 6.25 * (altura * 100) - 5 * edad - 161

    calorias_mantenimiento = round(tmb * 1.55, 2)

    return render_template(
        'formulario.html',
        nombre=nombre,
        edad=edad,
        peso=peso,
        altura=altura,
        genero=genero,
        imc=round(imc, 2),
        clasificacion=clasificacion,
        recomendacion=recomendacion,
        calorias=calorias_mantenimiento
    )

if __name__ == '__main__':
    app.run(debug=True)