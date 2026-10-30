# Face Video Analysis API

API REST construida con FastAPI para recibir un video y devolver estadísticas básicas de detección facial mediante OpenCV. Incluye pruebas automatizadas con pytest y un ejemplo de pruebas API con Karate.

## Endpoints

- `GET /health`: verifica que el servicio esté disponible.
- `POST /analyze`: recibe un video `multipart/form-data` y analiza hasta 300 fotogramas.

La API devuelve el número de fotogramas analizados, los fotogramas con al menos una detección y el total de detecciones faciales. No realiza identificación de personas.

## Instalación

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecutar la API

```bash
uvicorn app:app --reload
```

Abre `http://127.0.0.1:8000/docs` para probar los endpoints desde la documentación interactiva de FastAPI.

## Pruebas con pytest

En otra terminal, dentro de esta carpeta:

```bash
pytest -v
```

## Pruebas con Karate

El archivo `karate/face-video-api.feature` muestra escenarios de contrato API. Para ejecutarlo, crea un proyecto de Karate con la versión de Karate Labs que utilices y copia la carpeta `karate` a `src/test/java` de ese proyecto; configura `baseUrl` si el servidor no usa el valor por defecto. Consulta la documentación oficial de Karate para la configuración exacta según la versión elegida.

## Límites y mejoras futuras

- Limita la carga a 50 MB y permite solo extensiones de video conocidas.
- Procesa como máximo 300 fotogramas para mantener acotado el coste de la petición.
- Para producción se necesitarían autenticación, límites de concurrencia, validación de códec, gestión de colas y controles de seguridad adicionales.
- El conteo de detecciones no equivale a contar personas únicas.

## Privacidad

No se guardan permanentemente los videos: el archivo temporal se elimina al terminar la solicitud. Utiliza material propio o autorizado y no subas datos personales al repositorio.
