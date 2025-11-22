Nombre de la escuela  
Materia: Emplea Framwork para el desarrollo de software.
Actividad: Investigación de APIs Nutricionales.
Alumno: Jared Olmeda y Angel Frías.
Docente: Juan Rubén Treviño Tapia.
Fecha: 25/sep/2025

1. Tabla comparativa de APIs nutricionales
| API               | Tipo de datos                                               | Costo / Plan gratuito          | Límites de uso                     | Facilidad de implementación | Calidad de documentación          |
|-------------------|-------------------------------------------------------------|--------------------------------|------------------------------------|-----------------------------|----------------------------------|  
| Nutritionix       | Alimentos de marca, restaurantes, datos nutricionales, entrada en lenguaje natural | Plan gratuito limitado         | Restricción en número de peticiones y usuarios activos | Fácil, REST estándar        | Buena, con ejemplos claros       |
| Edamam           | Análisis nutricional de recetas/ingredientes, búsqueda de alimentos, etiquetas dietas/alergias | Desde $29/mes (sin plan gratis) | Límite de peticiones según plan    | Fácil de usar con SDKs y ejemplos | Muy completa, con guías y ejemplos |
| USDA FoodData Central | Base de datos pública con composición nutricional de alimentos genéricos y de marca | Gratis (pública)               | 1,000 requests/hora/IP            | Muy sencilla (REST, JSON)   | Excelente, con OpenAPI y ejemplos |
| Spoonacular      | Datos de recetas, cálculo nutricional, búsqueda de menús y productos | Plan gratuito (~3,000 requests/mes) | Límite en plan gratuito           | Buena, endpoints variados      | Clara, con SDKs y Postman       |
2. API seleccionada y justificación
He elegido USDA FoodData Central API porque:
• Es gratuita y no tiene costos ocultos.
• Ofrece datos confiables, actualizados y públicos.
• Tiene documentación muy clara y fácil de seguir.
• Permite probar rápidamente con herramientas como Postman o curl.
• Es ideal para fines académicos y proyectos de aprendizaje.
3. Registro y obtención de API Key
1. Ingresé a la página oficial de la API: https://fdc.nal.usda.gov/api-guide
2. Solicité una clave API gratuita proporcionando mi correo electrónico.
3. Recibí la API key en mi correo (se usa en cada solicitud con el parámetro api_key).
Ejemplo de uso en consulta:
```bash
curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=apple&api_key=TU_API_KEY"
```
4. Ejemplos de solicitudes y respuestas
🔎 Búsqueda de alimentos
Solicitud (curl):
```bash
curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=banana&api_key=TU_API_KEY"
```
Respuesta JSON simplificada:
```json
{
  "foods": [
    {
      "fdcId": 110265,
      "description": "Banana, raw",
      "foodNutrients": [
        { "nutrientName": "Protein", "value": 1.09, "unitName": "G" },
        { "nutrientName": "Fat", "value": 0.33, "unitName": "G" },
        { "nutrientName": "Carbohydrate", "value": 22.84, "unitName": "G" },
        { "nutrientName": "Energy", "value": 89, "unitName": "KCAL" }
      ]
    }
  ]
}
```
📊 Detalle de alimento por ID
Solicitud:
```bash
curl "https://api.nal.usda.gov/fdc/v1/food/110265?api_key=TU_API_KEY"
```
Respuesta JSON simplificada:
```json
{
  "fdcId": 110265,
  "description": "Banana, raw",
  "foodNutrients": [
    { "nutrientName": "Protein", "value": 1.09, "unitName": "G" },
    { "nutrientName": "Fat", "value": 0.33, "unitName": "G" },
    { "nutrientName": "Carbohydrate", "value": 22.84, "unitName": "G" },
    { "nutrientName": "Energy", "value": 89, "unitName": "KCAL" }
  ]
}
```
5. Dificultades encontradas y soluciones
| Dificultad               | Causa                          | Solución                                 |
|--------------------------|--------------------------------|------------------------------------------|
| Clave API no funcionaba  | Error al copiar/pegar          | Revisar espacios y parámetro api_key      |
| Exceso de peticiones     | Superar límite 1000/hora       | Esperar 1h o cachear resultados            |
| Alimentos no encontrados | Nombre distinto en DB          | Probar términos genéricos/sinónimos         |
| Demasiados resultados    | Muchos alimentos coinciden     | Usar paginación pageNumber/pageSize            |




## Resumen rápido
NutriApp es una aplicación Flask que calcula IMC, estima TMB y calorías de mantenimiento, sugiere macros y rutinas básicas. Usa plantillas Jinja2 y Bootstrap para la interfaz, y un CSS en static/styles/colors.css para paleta.

## Estructura del proyecto
- app.py — lógica backend (rutas y cálculos).
- templates/ — plantillas HTML (pages).
- static/styles/colors.css — variables y estilos globales.
- README.md — documentación.

## app.py — explicación por secciones
- `from flask import Flask, render_template, request, redirect, url_for, flash, session`
  - Importa las funciones y objetos de Flask usados: creación de app, renderizado de templates, lectura de formularios, redirecciones, mensajes flash y sesión de usuario.

- `app = Flask(__name__)`
  - Crea la instancia de la aplicación Flask.

- `app.secret_key = 'cambia_esto_en_produccion'`
  - Clave usada para firmar cookies de sesión y mensajes flash. Cambiar en producción por una cadena segura.

- `_get_first(form, *keys, default='')`
  - Función auxiliar que devuelve el primer valor no vacío entre varias claves de un formulario. (Útil para aceptar múltiples nombres de campo equivalentes). Devuelve `default` si no hay valores válidos.

Rutas principales:
- `@app.route('/') -> inicio()`
  - Renderiza `info.html`, página de inicio / explicación.

- `@app.route('/formulario') -> formulario()`
  - Muestra el formulario de registro. Obtiene datos previos de `session['user']` si existen y muestra errores almacenados en sesión.

- `@app.route('/resultado', methods=['POST']) -> resultado()`
  - Lógica central:
    1. Lee campos del formulario: nombre, apellido, correo, contraseña, género, edad, peso, altura.
    2. Valida que edad/peso/altura sean numéricos y mayores que 0; en errores guarda mensaje y redirige al formulario.
    3. Calcula IMC: `peso / (altura ** 2)` (altura en metros).
    4. Clasifica IMC (Bajo peso / Peso normal / Sobrepeso / Obesidad) y genera una recomendación básica.
    5. Calcula TMB (Harris-Benedict aproximado) según género:
       - Masculino: 88.362 + 13.397*peso + 4.799*altura_cm - 5.677*edad
       - Femenino: 447.593 + 9.247*peso + 3.098*altura_cm - 4.330*edad
    6. Estima calorías de mantenimiento multiplicando TMB por factor de actividad (ej. 1.55).
    7. Guarda un diccionario `user` en `session` con todos los valores calculados y devuelve la plantilla con resultados.

- `@app.route('/login', methods=['GET','POST']) -> login()`
  - GET: muestra formulario de login (`login.html`).
  - POST: compara correo/contraseña enviados con los guardados en `session['user']`. Si coinciden, marca `session['authenticated'] = True` y redirige a `/rutina`. Si no, muestra mensaje flash.

- `@app.route('/rutina') -> rutina()`
  - Comprueba `session['user']` y renderiza `rutina.html`, que muestra resumen de IMC, clasificación, calorías y sugerencias de rutina y alimentación según clasificación.

- `@app.route('/perfil') -> perfil()`
  - Muestra `perfil.html` con todos los datos almacenados del usuario (nombre, peso, altura, IMC, etc.). Requiere que existan datos en sesión.

- `@app.route('/tmb', methods=['GET','POST']) -> tmb()`
  - Calculadora independiente de TMB. GET muestra el formulario; POST calcula TMB con los campos enviados y devuelve resultado en la misma plantilla.

- `@app.route('/gct', methods=['GET','POST']) -> gct()`
  - Calculadora de Gasto Calórico Total: recibe TMB y un factor de actividad y devuelve GCT = TMB * factor.

- `@app.route('/peso_ideal', methods=['GET','POST']) -> peso_ideal()`
  - Calcula peso ideal usando la fórmula de Devine (entrada en cm y género). Devuelve resultado redondeado.

- `@app.route('/macros', methods=['GET','POST']) -> macros()`
  - Dado un número de calorías y porcentajes para proteína/carbohidratos/grasas, convierte a gramos:
    - Proteína y carbohidratos: 4 kcal/g.
    - Grasas: 9 kcal/g.
  - Devuelve los gramos aproximados por macro.

- `@app.route('/clear') -> clear()`
  - Borra `session['user']` y `session['authenticated']`, muestra mensaje flash y redirige al formulario.

- `@app.route('/logout') -> logout()`
  - Borra sesión y redirige a inicio con mensaje.

- `if __name__ == '__main__': app.run(debug=True)`
  - Ejecuta la app en modo debug (no usar en producción). Escucha por defecto en 127.0.0.1:5000.

## Templates (templates/*.html) — explicación de campos y bloques
- base.html
  - Contiene cabecera HTML, import de Bootstrap CDN y enlace a `static/styles/colors.css`.
  - Barra de navegación con enlaces a rutas principales.
  - Bloque para mensajes flash (se muestran con alert de Bootstrap).
  - Bloque `{% block contenido %}` que rellenan las otras plantillas.
  - Footer con aviso legal / orientativo.

- formulario.html
  - Extiende base.html.
  - Campos del formulario (nombres de input importantes):
    - `nombre`, `apellido` (text)
    - `edad` (number, años)
    - `genero` (select: masculino/femenino)
    - `peso` (kg, number)
    - `altura` (m, number; se usa para IMC directamente en metros)
    - `correo_electronico` (email)
    - `contraseña` (password)
  - Al enviar, POST a `/resultado`.
  - Si hay `imc` en contexto, muestra resultados: IMC, clasificación, recomendación y calorías estimadas.

- tmb.html, gct.html, macros.html, peso_ideal.html
  - Cada uno tiene un pequeño formulario que POSTea a su misma ruta y muestra resultado si existe variable de resultado en contexto (`tmb`, `gct`, `macros`, `ideal`).

- rutina.html y perfil.html
  - Usan datos de `user` en sesión para mostrar recomendaciones y detalles del usuario.
  - Botones para volver a formulario o cerrar sesión.

- login.html
  - Formulario de inicio de sesión que verifica correo y contraseña contra `session['user']`. Si no hay user, pide completar el formulario primero.

- info.html
  - Página de inicio con descripción de la aplicación y enlaces a formulario o login.

## static/styles/colors.css — explicación
- Define variables CSS en `:root`:
  - `--bg`, `--primary`, `--accent`, `--muted`, `--texto`
  - Usadas para tema (fondo, color de texto, botones).
- Clases útiles:
  - `.brand`, `.accent`, `.muted` — colores aplicables a títulos o textos.
  - `.container-card`, `.card-soft` — estilos para centrar y dar tarjeta con fondo suave.
  - `.btn-brand` — botón con color primario del tema.

## Comandos útiles (Windows)
1. Crear entorno virtual:
   - python -m venv venv
2. Activar:
   - venv\Scripts\activate
3. Instalar Flask:
   - pip install flask
4. Ejecutar la app:
   - python app.py
   - o set FLASK_APP=app.py && flask run

(En PowerShell usar `$env:FLASK_APP = "app.py"; flask run`).
