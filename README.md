# TICKETS HelpDesk

Este proyecto es una base para una aplicación de seguimiento de tickets de soporte.

## Requisitos
- Python 3.9+
- Dependencias en `requirements.txt`

## Instalación
```bash
pip install -r requirements.txt
```

## Uso
Configura las variables de entorno en un archivo `.env` (ver `tickets_app/config.py`).
Luego ejecuta la interfaz básica de ejemplo:

```bash
python -m tickets_app.ui.main
```

Este proyecto solo contiene una estructura inicial y debe ser ampliado para soportar
la descarga de correos, el análisis por IA y la gestión completa de tickets.
