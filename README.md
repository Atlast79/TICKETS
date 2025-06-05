# TICKETS HelpDesk

Aplicación de ejemplo para gestionar tickets de soporte descargados desde
Outlook y analizados mediante OpenAI.
Incluye una interfaz mínima para listar y revisar tickets almacenados en una base
de datos. Esta base puede ampliarse para un helpdesk completo.

## Requisitos
- Python 3.9+
- Dependencias en `requirements.txt`

## Instalación
```bash
pip install -r requirements.txt
```

## Uso
Configura las variables de entorno en un archivo `.env` (ver `tickets_app/config.py`).
Luego ejecuta la interfaz principal:

```bash
python -m tickets_app.ui.main
```

Al pulsar "Refrescar" la aplicación descarga los correos nuevos de la carpeta
configurada en Outlook, los envía a OpenAI para extraer la información del
ticket y guarda las observaciones. Se pueden añadir adjuntos manualmente y
registrar observaciones personales por ticket. El listado permite filtrar por
número de ticket y colorea cada fila según el estado.

Variables de entorno destacadas:
- `OUTLOOK_FOLDER`: carpeta de Outlook donde leer los correos.
- `ATTACHMENTS_DIR`: directorio para almacenar adjuntos.
- `DB_URL`: cadena de conexión de la base de datos.
- `OPENAI_API_KEY`: clave de la API de OpenAI.
- `MAX_EMAILS`: límite de correos a procesar en cada refresco.
