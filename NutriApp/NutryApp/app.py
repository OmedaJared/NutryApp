from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests

API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
API_KEY = "tN2XZsdySpg5RvS75AJNOLrDHJPbny4W64vfX3N"

# ...existing code...
app = Flask(__name__)
app.secret_key = 'cambia_esto_en_produccion'

# **DICCIONARIO DE RECETAS — AGREGAR AQUÍ**
RECIPES = [
    {
        'id': 1,
        'title': 'Bowl de avena con frutas y frutos secos',
        'description': 'Desayuno energético con avena, leche, plátano, frutos secos y miel.',
        'ingredients': [
            '1 taza de avena',
            '1 plátano rebanado',
            '1/2 taza de frutos secos (almendras, nueces)',
            '1 taza de leche',
            '1 cucharada de miel'
        ],
        'steps': [
            'Cocina la avena en la leche según instrucciones del empaque',
            'Vierte en un plato',
            'Agrega el plátano rebanado',
            'Espolvorea los frutos secos',
            'Rocía miel al gusto'
        ],
        'diet': ['vegetariano'],
        'difficulty': 'fácil',
        'time_min': 10,
        'calories': 420,
        'meal_prep': False,
        'beginner': True
    },
    {
        'id': 2,
        'title': 'Ensalada de quinoa y pollo',
        'description': 'Almuerzo balanceado con proteína magra y carbohidratos complejos.',
        'ingredients': [
            '200g de pechuga de pollo',
            '1 taza de quinoa cocida',
            '1 tomate',
            '1 pepino',
            'Lechuga mixta',
            'Limón y aceite de oliva'
        ],
        'steps': [
            'Cocina el pollo a la plancha',
            'Prepara la quinoa según instrucciones',
            'Pica vegetales',
            'Mezcla todo en un plato',
            'Aliña con limón y aceite'
        ],
        'diet': ['sin_gluten'],
        'difficulty': 'media',
        'time_min': 25,
        'calories': 550,
        'meal_prep': True,
        'beginner': True
    },
    {
        'id': 3,
        'title': 'Salmón al horno con vegetales',
        'description': 'Cena rica en proteínas y grasas saludables.',
        'ingredients': [
            '200g de salmón fresco',
            '200g de brócoli',
            '100g de zanahorias',
            'Aceite de oliva',
            'Limón y ajo',
            'Sal y pimienta'
        ],
        'steps': [
            'Precalienta el horno a 200°C',
            'Coloca el salmón en una bandeja',
            'Agrega vegetales alrededor',
            'Rocía con aceite, limón y ajo',
            'Hornea 20-25 minutos'
        ],
        'diet': [],
        'difficulty': 'media',
        'time_min': 30,
        'calories': 600,
        'meal_prep': False,
        'beginner': False
    },
    {
        'id': 4,
        'title': 'Tostadas integrales con aguacate y huevo',
        'description': 'Desayuno rico en grasas saludables y proteína.',
        'ingredients': [
            '2 rebanadas de pan integral',
            '1 aguacate',
            '2 huevos',
            'Tomate',
            'Sal y pimienta',
            'Aceite de oliva'
        ],
        'steps': [
            'Tuesta el pan integral',
            'Aplasta el aguacate con sal y pimienta',
            'Fríe los huevos en aceite de oliva',
            'Coloca aguacate y huevo en el pan',
            'Agrega tomate fresco'
        ],
        'diet': ['vegetariano'],
        'difficulty': 'fácil',
        'time_min': 8,
        'calories': 380,
        'meal_prep': False,
        'beginner': True
    },
    {
        'id': 5,
        'title': 'Batido proteico de frutos rojos',
        'description': 'Merienda rápida para recuperación muscular.',
        'ingredients': [
            '200ml de leche de almendras',
            '30g de proteína en polvo (vainilla)',
            '100g de frutos rojos (arándanos, fresas)',
            '1 plátano',
            '1 cucharada de mantequilla de maní',
            'Hielo'
        ],
        'steps': [
            'Vierte la leche en la licuadora',
            'Agrega proteína en polvo',
            'Añade frutos rojos y plátano',
            'Agrega mantequilla de maní',
            'Licúa hasta obtener consistencia homogénea'
        ],
        'diet': ['vegano'],
        'difficulty': 'fácil',
        'time_min': 5,
        'calories': 300,
        'meal_prep': False,
        'beginner': True
    },
    {
        'id': 6,
        'title': 'Salteado de garbanzos y espinacas',
        'description': 'Plato vegetariano alto en fibra y proteína vegetal.',
        'ingredients': [
            '1 lata de garbanzos',
            '200g de espinacas frescas',
            '1 cebolla',
            '3 dientes de ajo',
            'Aceite de oliva',
            'Especias (comino, pimentón)'
        ],
        'steps': [
            'Calienta aceite en una sartén',
            'Sofríe cebolla y ajo',
            'Agrega los garbanzos',
            'Añade espinacas',
            'Sazona con especias y cocina 10 minutos'
        ],
        'diet': ['vegetariano', 'vegano'],
        'difficulty': 'fácil',
        'time_min': 15,
        'calories': 420,
        'meal_prep': True,
        'beginner': True
    },
    {
        'id': 7,
        'title': 'Pollo a la parrilla con arroz integral',
        'description': 'Plato clásico de musculación con proteína y carbohidratos complejos.',
        'ingredients': [
            '250g de pechuga de pollo',
            '1 taza de arroz integral cocido',
            '1 taza de vegetales mixtos',
            'Limón',
            'Sal y pimienta',
            'Aceite en spray'
        ],
        'steps': [
            'Condimenta el pollo con sal, pimienta y limón',
            'Cocina a la parrilla 15-20 minutos',
            'Prepara el arroz integral',
            'Saltea los vegetales',
            'Sirve todo junto'
        ],
        'diet': [],
        'difficulty': 'fácil',
        'time_min': 20,
        'calories': 580,
        'meal_prep': True,
        'beginner': True
    },
    {
        'id': 8,
        'title': 'Smoothie bowl de acai',
        'description': 'Desayuno instagrameable y nutritivo.',
        'ingredients': [
            '100g de pulpa de açaí',
            '200ml de leche de coco',
            'Granola',
            'Cocos rallados',
            'Plátano rebanado',
            'Miel'
        ],
        'steps': [
            'Mezcla el açaí con leche de coco',
            'Vierte en un plato',
            'Agrega granola en la parte superior',
            'Distribuye plátano y coco',
            'Rocía miel y sirve'
        ],
        'diet': ['vegano'],
        'difficulty': 'fácil',
        'time_min': 5,
        'calories': 380,
        'meal_prep': False,
        'beginner': True
    }
]

# ...existing code (rutas)...

@app.route('/')
def inicio():
    return render_template('info.html')

@app.route('/formulario')
def formulario():
    """Muestra el formulario de registro."""
    user = session.get('user', {})
    return render_template('formulario.html', **user)

@app.route('/resultado', methods=['POST'])
def resultado():
    """Procesa formulario, calcula IMC y guarda en sesión."""
    try:
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        correo_electronico = request.form.get('correo_electronico', '').strip()
        contraseña = request.form.get('contraseña', '')
        edad = int(request.form.get('edad', 0))
        peso = float(request.form.get('peso', 0))
        altura = float(request.form.get('altura', 0))
        genero = request.form.get('genero', 'masculino').lower()
        
        if not nombre or not apellido or not correo_electronico or not contraseña:
            flash('❌ Por favor completa todos los campos requeridos.', 'danger')
            return redirect(url_for('formulario'))
        
        if edad <= 0 or peso <= 0 or altura <= 0:
            flash('❌ Edad, peso y altura deben ser mayores a 0.', 'danger')
            return redirect(url_for('formulario'))
        
        # Calcular IMC
        imc = peso / (altura ** 2)
        imc = round(imc, 2)
        
        if imc < 18.5:
            clasificacion = 'Bajo peso'
            recomendacion = 'Consulta con un profesional para aumentar peso de forma saludable.'
        elif imc < 25:
            clasificacion = 'Peso normal'
            recomendacion = 'Mantén tu peso actual con ejercicio y buena alimentación.'
        elif imc < 30:
            clasificacion = 'Sobrepeso'
            recomendacion = 'Considera aumentar actividad física y revisar tu dieta.'
        else:
            clasificacion = 'Obesidad'
            recomendacion = 'Consulta con un profesional de la salud.'
        
        # Calcular TMB (Harris-Benedict)
        altura_cm = altura * 100
        if genero == 'masculino':
            tmb = 88.362 + (13.397 * peso) + (4.799 * altura_cm) - (5.677 * edad)
        else:
            tmb = 447.593 + (9.247 * peso) + (3.098 * altura_cm) - (4.330 * edad)
        
        tmb = round(tmb, 2)
        calorias = round(tmb * 1.55, 2)
        
        # Recopilar objetivos y preferencias
        objetivos = request.form.getlist('objetivos')
        alergias = request.form.get('alergias', '').strip()
        intolerancias = request.form.get('intolerancias', '').strip()
        dieta_especifica = request.form.get('dieta_especifica', '').strip()
        alimentos_no_gustan = request.form.get('alimentos_no_gustan', '').strip()
        experiencia = request.form.get('experiencia', 'principiante').strip()
        
        # **GUARDAR EN SESIÓN — ESTO ES CRUCIAL**
        session['user'] = {
            'nombre': nombre,
            'apellido': apellido,
            'edad': edad,
            'peso': peso,
            'altura': altura,
            'correo_electronico': correo_electronico,
            'contraseña': contraseña,  # En producción: usar hash
            'genero': genero,
            'imc': imc,
            'clasificacion': clasificacion,
            'recomendacion': recomendacion,
            'calorias': calorias,
            'tmb': tmb,
            'objetivos': objetivos,
            'alergias': alergias,
            'intolerancias': intolerancias,
            'dieta_especifica': dieta_especifica,
            'alimentos_no_gustan': alimentos_no_gustan,
            'experiencia': experiencia
        }
        session.modified = True  # **FUERZA GUARDAR LA SESIÓN**
        
        flash(f'✅ ¡Bienvenido, {nombre}! Datos guardados correctamente.', 'success')
        return render_template('formulario.html', 
                             imc=imc,
                             clasificacion=clasificacion,
                             recomendacion=recomendacion,
                             calorias=calorias,
                             **session['user'])
    
    except (ValueError, TypeError) as e:
        flash(f'❌ Error: por favor verifica que todos los campos sean válidos. ({str(e)})', 'danger')
        return redirect(url_for('formulario'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login con email y contraseña guardados en sesión."""
    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()
        contraseña = request.form.get('contraseña', '')
        
        # Obtener datos guardados en sesión
        user = session.get('user', {})
        
        # Validar credenciales
        if not user:
            flash('❌ No hay datos registrados. Por favor completa el formulario primero.', 'warning')
            return redirect(url_for('formulario'))
        
        if user.get('correo_electronico') == correo and user.get('contraseña') == contraseña:
            # Credenciales correctas
            session['authenticated'] = True
            session.modified = True
            flash(f'✅ ¡Bienvenido, {user.get("nombre")}!', 'success')
            return redirect(url_for('rutina'))
        else:
            flash('❌ Email o contraseña incorrectos.', 'danger')
            return render_template('login.html', error='Email o contraseña incorrectos.')
    
    return render_template('login.html')

@app.route('/rutina')
def rutina():
    """Muestra rutina personalizada. Requiere autenticación."""
    user = session.get('user')
    if not user:
        flash('❌ Primero debes llenar el formulario o iniciar sesión.', 'warning')
        return redirect(url_for('formulario'))
    
    # Extraer datos
    peso = float(user.get('peso', 0))
    altura_m = float(user.get('altura', 0))
    altura_cm = altura_m * 100
    edad = int(user.get('edad', 0))
    genero = user.get('genero', 'masculino').lower()
    imc = float(user.get('imc', 0))
    tmb = float(user.get('tmb', 0))
    
    # Decidir objetivo según IMC
    if imc < 18.5:
        objetivo = 'ganar'
        delta_cal = 500
        prot_per_kg = 2.2
    elif imc < 25:
        objetivo = 'mantener'
        delta_cal = 0
        prot_per_kg = 1.8
    else:
        objetivo = 'perder'
        delta_cal = -500
        prot_per_kg = 2.0
    
    # Calorías objetivo
    mantenimiento = user.get('calorias') or round(tmb * 1.55, 2)
    calorias_obj = max(1200, round(mantenimiento + delta_cal, 0))
    
    # Macros
    prot_g = round(prot_per_kg * peso, 1)
    prot_kcal = prot_g * 4
    fat_g = round((calorias_obj * 0.25) / 9, 1)
    carb_g = round((calorias_obj - prot_kcal - (fat_g * 9)) / 4, 1)
    
    # Rutina semanal
    if genero == 'masculino':
        plan = [
            {'dia': 'Lunes', 'actividad': 'Fuerza — Pecho/Tríceps (4 ejercicios, 3-4x8-12)'},
            {'dia': 'Martes', 'actividad': 'Cardio: Intervalos 20-25 min'},
            {'dia': 'Miércoles', 'actividad': 'Fuerza — Espalda/Bíceps (4 ejercicios, 3-4x8-12)'},
            {'dia': 'Jueves', 'actividad': 'Piernas y core (4 ejercicios, 3x8-12)'},
            {'dia': 'Viernes', 'actividad': 'Full body ligero + movilidad'},
            {'dia': 'Sábado', 'actividad': 'Actividad recreativa o cardio suave'},
            {'dia': 'Domingo', 'actividad': 'Descanso activo'}
        ]
    else:
        plan = [
            {'dia': 'Lunes', 'actividad': 'Fuerza — Tren inferior + glúteos (4x8-12)'},
            {'dia': 'Martes', 'actividad': 'Cardio moderado 30 min + movilidad'},
            {'dia': 'Miércoles', 'actividad': 'Fuerza — Tren superior (3-4 ejercicios)'},
            {'dia': 'Jueves', 'actividad': 'Pilates / Core y movilidad'},
            {'dia': 'Viernes', 'actividad': 'Circuito full body (condición + fuerza)'},
            {'dia': 'Sábado', 'actividad': 'Actividad recreativa ligera'},
            {'dia': 'Domingo', 'actividad': 'Descanso activo'}
        ]
    
    # Dieta
    dieta = {
        'objetivo': {
            'ganar': 'Superávit calórico moderado (+300-500 kcal)',
            'mantener': 'Calorías de mantenimiento',
            'perder': 'Déficit moderado (-300-600 kcal)'
        }[objetivo],
        'calorias_objetivo': calorias_obj,
        'macros': {
            'proteina_g': prot_g,
            'carbohidratos_g': carb_g,
            'grasas_g': fat_g
        },
        'ejemplo': {
            'desayuno': 'Avena con leche, fruta y proteína',
            'almuerzo': 'Proteína + carbohidrato complejo + vegetales',
            'merienda': 'Batido proteico o yogur',
            'cena': 'Pescado/Pollo/Legumbres con verduras'
        }
    }
    
    rutina_detalle = {
        'descripcion': f'Objetivo: {objetivo} — TMB: {tmb} kcal/día',
        'plan_semanal': plan,
        'dieta': dieta
    }
    
    return render_template('rutina.html', user=user, rutina=rutina_detalle)

@app.route('/perfil')
def perfil():
    """Muestra el perfil del usuario."""
    user = session.get('user')
    if not user:
        flash('❌ Debes iniciar sesión primero.', 'warning')
        return redirect(url_for('login'))
    return render_template('perfil.html', user=user)

@app.route('/recetas')
def recetas():
    """Lista de recetas con filtros."""
    dieta = request.args.get('dieta', '').lower()
    dificultad = request.args.get('dificultad', '').lower()
    tiempo_max = request.args.get('tiempo_max')
    max_cal = request.args.get('max_cal')
    meal_prep = request.args.get('meal_prep')
    beginner = request.args.get('beginner')

    filtered = RECIPES
    if dieta:
        filtered = [r for r in filtered if dieta in (', '.join(r.get('diet', []))).lower()]
    if dificultad:
        filtered = [r for r in filtered if r.get('difficulty','').lower() == dificultad]
    if tiempo_max:
        try:
            tm = int(tiempo_max)
            filtered = [r for r in filtered if r.get('time_min', 0) <= tm]
        except ValueError:
            pass
    if max_cal:
        try:
            mc = int(max_cal)
            filtered = [r for r in filtered if r.get('calories', 0) <= mc]
        except ValueError:
            pass
    if meal_prep:
        filtered = [r for r in filtered if r.get('meal_prep', False) is True]
    if beginner:
        filtered = [r for r in filtered if r.get('beginner', False) is True]

    return render_template('recetas.html', recetas=filtered, filtros=request.args)

@app.route('/recetas/<int:receta_id>')
def receta_detalle(receta_id):
    """Detalle de una receta."""
    receta = next((r for r in RECIPES if r['id'] == receta_id), None)
    if not receta:
        flash('❌ Receta no encontrada.', 'danger')
        return redirect(url_for('recetas'))
    return render_template('receta_detalle.html', receta=receta)

@app.route('/educacion')
def educacion():
    """Página de educación."""
    return render_template('educacion.html')

@app.route('/tmb', methods=['GET', 'POST'])
def tmb():
    """Calculadora de TMB."""
    if request.method == 'POST':
        try:
            peso = float(request.form.get('peso', 0))
            altura = float(request.form.get('altura', 0))
            edad = int(request.form.get('edad', 0))
            genero = request.form.get('genero', 'masculino').lower()
            
            altura_cm = altura * 100
            if genero == 'masculino':
                tmb_calc = 88.362 + (13.397 * peso) + (4.799 * altura_cm) - (5.677 * edad)
            else:
                tmb_calc = 447.593 + (9.247 * peso) + (3.098 * altura_cm) - (4.330 * edad)
            
            tmb_calc = round(tmb_calc, 2)
            return render_template('tmb.html', tmb=tmb_calc, peso=peso, altura=altura, edad=edad, genero=genero)
        except (ValueError, TypeError):
            return render_template('tmb.html', error='❌ Valores inválidos.')
    
    return render_template('tmb.html')

@app.route('/gct', methods=['GET', 'POST'])
def gct():
    """Calculadora de GCT."""
    if request.method == 'POST':
        try:
            tmb_val = float(request.form.get('tmb', 0))
            actividad = float(request.form.get('actividad', 1.55))
            gct_calc = round(tmb_val * actividad, 2)
            return render_template('gct.html', gct=gct_calc, tmb=tmb_val, actividad=actividad)
        except (ValueError, TypeError):
            return render_template('gct.html', error='❌ Valores inválidos.')
    
    return render_template('gct.html')

@app.route('/peso_ideal', methods=['GET', 'POST'])
def peso_ideal():
    """Calculadora de peso ideal."""
    if request.method == 'POST':
        try:
            altura_cm = float(request.form.get('altura', 0))
            genero = request.form.get('genero', 'masculino').lower()
            
            if genero == 'masculino':
                ideal = 50 + (2.3 * (altura_cm - 152.4))
            else:
                ideal = 45.5 + (2.3 * (altura_cm - 152.4))
            
            ideal = round(ideal, 2)
            return render_template('peso_ideal.html', ideal=ideal, altura=altura_cm, genero=genero)
        except (ValueError, TypeError):
            return render_template('peso_ideal.html', error='❌ Altura inválida.')
    
    return render_template('peso_ideal.html')

@app.route('/macros', methods=['GET', 'POST'])
def macros():
    """Calculadora de macros."""
    if request.method == 'POST':
        try:
            calorias = float(request.form.get('calorias', 0))
            p_pct = float(request.form.get('p', 30))
            c_pct = float(request.form.get('c', 40))
            g_pct = float(request.form.get('g', 30))
            
            prot = round((calorias * p_pct / 100) / 4, 2)
            carb = round((calorias * c_pct / 100) / 4, 2)
            fat = round((calorias * g_pct / 100) / 9, 2)
            
            macros_result = {'prot': prot, 'carb': carb, 'fat': fat}
            return render_template('macros.html', macros=macros_result, calorias=calorias, p=p_pct, c=c_pct, g=g_pct)
        except (ValueError, TypeError):
            return render_template('macros.html', error='❌ Valores inválidos.')
    
    return render_template('macros.html')

@app.route('/nutrientes', methods=['GET', 'POST'])
def nutrientes():
    """Busca alimentos en la base de datos USDA y muestra nutrientes.
    Soporta búsqueda en español."""
    alimento = None
    alimentos = None
    error = None

    if request.method == 'POST':
        termino_busqueda = request.form.get('termino', '').strip()
        
        if not termino_busqueda:
            error = '❌ Por favor ingresa un alimento para buscar.'
            return render_template('nutrientes.html', alimento=alimento, alimentos=alimentos, error=error)
        
        try:
            # Parámetros para la API
            params = {
                'query': termino_busqueda,
                'pageSize': 10,
                'api_key': API_KEY
            }
            
            # Realizar petición a USDA
            response = requests.get(API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Procesar resultados
            if 'foods' in data and len(data['foods']) > 0:
                alimentos = []
                for food in data['foods']:
                    food_data = {
                        'fdcId': food.get('fdcId', 'N/A'),
                        'description': food.get('description', 'Sin descripción'),
                        'brand': food.get('brandName', 'Genérico'),
                        'nutrientes': {}
                    }
                    
                    # Extraer nutrientes principales
                    if 'foodNutrients' in food:
                        for nutrient in food['foodNutrients']:
                            nutrient_name = nutrient.get('nutrientName', '').lower()
                            nutrient_value = nutrient.get('value', 0)
                            unit = nutrient.get('unitName', '')
                            
                            # Mapear nutrientes importantes
                            if 'energy' in nutrient_name and 'kcal' in unit.lower():
                                food_data['nutrientes']['Calorías'] = f"{nutrient_value:.1f} {unit}"
                            elif 'protein' in nutrient_name:
                                food_data['nutrientes']['Proteína'] = f"{nutrient_value:.1f} {unit}"
                            elif 'carbohydrate' in nutrient_name:
                                food_data['nutrientes']['Carbohidratos'] = f"{nutrient_value:.1f} {unit}"
                            elif 'fat' in nutrient_name and 'total' in nutrient_name:
                                food_data['nutrientes']['Grasas'] = f"{nutrient_value:.1f} {unit}"
                            elif 'fiber' in nutrient_name:
                                food_data['nutrientes']['Fibra'] = f"{nutrient_value:.1f} {unit}"
                            elif 'sodium' in nutrient_name:
                                food_data['nutrientes']['Sodio'] = f"{nutrient_value:.1f} {unit}"
                            elif 'calcium' in nutrient_name:
                                food_data['nutrientes']['Calcio'] = f"{nutrient_value:.1f} {unit}"
                            elif 'iron' in nutrient_name:
                                food_data['nutrientes']['Hierro'] = f"{nutrient_value:.1f} {unit}"
                    
                    alimentos.append(food_data)
            else:
                error = f'❌ No se encontraron resultados para "{termino_busqueda}"'
        
        except requests.exceptions.Timeout:
            error = '❌ Error: la solicitud tardó demasiado. Intenta de nuevo.'
        except requests.exceptions.ConnectionError:
            error = '❌ Error de conexión. Verifica tu conexión a internet.'
        except requests.exceptions.HTTPError as e:
            error = f'❌ Error HTTP: {e.response.status_code}'
        except ValueError:
            error = '❌ Error al procesar la respuesta de la API.'
        except Exception as e:
            error = f'❌ Error inesperado: {str(e)}'

    return render_template('nutrientes.html', alimento=alimento, alimentos=alimentos, error=error)
@app.route('/logout')
def logout():
    """Cierra sesión."""
    session.clear()
    flash('✅ Sesión cerrada correctamente.', 'success')
    return redirect(url_for('inicio'))

@app.route('/clear')
def clear():
    """Borra datos del usuario."""
    session.clear()
    flash('🗑️ Datos borrados.', 'info')
    return redirect(url_for('formulario'))

# ...existing code (RECIPES dictionary, etc.)...

if __name__ == '__main__':
    app.run(debug=True)