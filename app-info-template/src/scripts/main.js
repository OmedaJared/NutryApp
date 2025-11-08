// main.js
document.addEventListener('DOMContentLoaded', function() {
    const appInfo = {
        title: "Aplicación de Ejemplo",
        purpose: "Esta aplicación tiene como objetivo proporcionar una interfaz sencilla para gestionar tareas.",
        features: [
            "Agregar tareas",
            "Eliminar tareas",
            "Marcar tareas como completadas"
        ],
        usage: "Para usar la aplicación, simplemente ingrese una tarea en el campo de entrada y haga clic en 'Agregar'."
    };

    const introSection = document.createElement('div');
    introSection.style.color = 'black'; // Color del texto
    introSection.style.backgroundColor = 'lightgray'; // Color de fondo

    const titleElement = document.createElement('h1');
    titleElement.textContent = appInfo.title;
    introSection.appendChild(titleElement);

    const purposeElement = document.createElement('p');
    purposeElement.textContent = `Propósito: ${appInfo.purpose}`;
    introSection.appendChild(purposeElement);

    const featuresElement = document.createElement('ul');
    featuresElement.textContent = "Características:";
    appInfo.features.forEach(feature => {
        const listItem = document.createElement('li');
        listItem.textContent = feature;
        featuresElement.appendChild(listItem);
    });
    introSection.appendChild(featuresElement);

    const usageElement = document.createElement('p');
    usageElement.textContent = `Uso: ${appInfo.usage}`;
    introSection.appendChild(usageElement);

    document.body.appendChild(introSection);
});