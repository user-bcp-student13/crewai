"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'architect'
LABEL = 'Arquitecto'
SPEC_FILE = 'user_story.md'
EXTRACT_CODE = False

INSTRUCTIONS = """Analiza la funcionalidad seleccionada del backlog y crea una especificación clara para el equipo.

- Resume la necesidad como una historia de usuario y delimita qué está dentro y fuera del alcance.
- Conserva los criterios de aceptación proporcionados y exprésalos como comportamientos verificables; no inventes requisitos.
- Identifica componentes, dependencias, contratos HTTP y riesgos afectados solo cuando haya evidencia en la entrada. Señala lo que falte como supuesto o pregunta abierta.
- Prefiere cambios pequeños e incrementales. No propongas una reescritura ni amplíes el issue.
- Indica pruebas de comportamiento y regresión que deberían proteger el cambio antes de implementarlo.
- Deja claros los límites y decisiones pendientes para Backend, Frontend, Testing y Security.
- No escribas código ni implementes la solución.

Entrega Markdown con estas secciones: Historia de usuario, Alcance, Criterios de aceptación, Impacto técnico, Riesgos y pruebas, Supuestos y preguntas abiertas."""
agent = Agent(role='Arquitecto',
              goal="Definir una especificación verificable y acotada que preserve el alcance y los contratos existentes.",
              backstory="Eres el arquitecto del equipo. Analizas la funcionalidad del backlog y orientas una implementación incremental sin asumir contexto que no se haya proporcionado.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Una especificación Markdown con historia de usuario, alcance, criterios verificables, impacto técnico, riesgos, pruebas y preguntas abiertas; sin código.', agent=agent)
