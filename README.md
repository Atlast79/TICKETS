# TICKETS HelpDesk

Aplicación de ejemplo para gestionar tickets de soporte descargados desde
Outlook y analizados mediante OpenAI.

## Requisitos
- Python 3.9+
- Dependencias en `requirements.txt`

## Instalación
```bash
pip install -r requirements.txt
```

## Uso
Configura las variables de entorno en un archivo `.env` (ver
`tickets_app/config.py`). Después ejecuta la interfaz principal:

```bash
python -m tickets_app.ui.main
```

Al pulsar "Refrescar" la aplicación descarga los correos nuevos de la carpeta
configurada en Outlook, los envía a OpenAI para extraer la información del
ticket y guarda las observaciones. Se pueden añadir adjuntos manualmente y
registrar observaciones personales por ticket.
