### Aplicación:
Programa de reproducción de musica con gestión de carpeta para guardar fav o lista de reproducción (v1 sin interfaz gráfica)

### Librerias a instalar:
pip install pygame
pip install keyboard

### Tecnologias
python, archivos json, API Jamendo

### Patrones de diseño:
1. Command
2. Facade
3. Inyección de dependencias

### Controles para manejar:
i : reproducir
r : repetir
d : detener
f : detener y pregunar si agregar a fav/lista de reproducción/ambas opciones/ninguna
p : pausar la musica

## Variables de entorno
Crea un archivo .env en la raíz con:
JAMENDO_API_KEY=tu_api_key_aqui
Puedes obtener tu API key gratis en: jamendo.com/developers

## ¿Cómo ejecutarlo?
1. Contar con conexión a internet
2. Correr: python Principal.py


## Estado del proyecto
En desarrollo - v1 sin interfaz gráfica
v2 planeada con interfaz gráfica

## Aprendizajes
Implementación de patrones Command, Facade e Inyección de dependencias en Python
