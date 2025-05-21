def construir_prompt_mcp(idea: str) -> str:
    return f"""
[ROL]
Eres un diseñador de experiencia de usuario especializado en aplicaciones móviles.

[OBJETIVO]
A partir de la siguiente idea de aplicación, genera un flujo de pantallas representado como una lista JSON. 
Cada pantalla debe contener:
- "pantalla": nombre breve de la pantalla,
- "descripcion": qué función cumple la pantalla,
- "elementos": lista de componentes UI visibles (botones, campos, texto, etc.)

El resultado debe estar contenido **únicamente** dentro de un objeto JSON con una clave `"flujo"`.

**No uses markdown, no incluyas explicaciones, ni comillas triples. Responde exclusivamente con el objeto JSON.**

Ejemplo del formato esperado (el contenido debe adaptarse a la nueva idea):

{{
  "flujo": [
    {{
      "pantalla": "Inicio",
      "descripcion": "Pantalla de bienvenida con opciones para login y registro.",
      "elementos": ["Logo", "Botón Login", "Botón Registro"]
    }},
    {{
      "pantalla": "Login",
      "descripcion": "Pantalla para ingresar credenciales.",
      "elementos": ["Campo Email", "Campo Contraseña", "Botón Ingresar"]
    }}
  ]
}}

[INPUT]
{idea}

[OUTPUT]
"flujo": [
    {{
      "pantalla": "Inicio",
      "descripcion": "Pantalla de bienvenida con opciones para login y registro.",
      "elementos": ["Logo", "Botón Login", "Botón Registro"]
    }},
    {{
      "pantalla": "Login",
      "descripcion": "Pantalla para ingresar credenciales.",
      "elementos": ["Campo Email", "Campo Contraseña", "Botón Ingresar"]
    }}
  ]
""".strip()