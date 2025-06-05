"""Send email content to OpenAI API and parse structured response."""

import openai
import logging
import json
from typing import Dict, Any

from . import config

logger = logging.getLogger(__name__)
openai.api_key = config.OPENAI_API_KEY

PROMPT = (
    "Eres un asistente que analiza correos de soporte y extrae la siguiente \n"
    "información en formato JSON: numero_de_ticket, resumen, proximo_paso, \n"
    "urgencia (alta/media/baja), cerrado (true/false). Si no es un ticket, \n"
    "indica 'es_ticket': false."
)


def analyze_email(body: str) -> Dict[str, Any]:
    """Send body to OpenAI and return parsed JSON."""
    if not config.OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY is not configured")
        return {}
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": PROMPT + "\n" + body}],
    )
    content = response.choices[0].message["content"]
    try:
        data = json.loads(content)
    except Exception as exc:
        logger.error("Error parsing OpenAI response: %s", exc)
        data = {}
    return data
