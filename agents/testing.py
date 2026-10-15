"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'testing'
LABEL = 'Ingeniero de pruebas'
SPEC_FILE = 'testing_report.md'
EXTRACT_CODE = True

INSTRUCTIONS = """
Define y prepara la estrategia de pruebas para el cambio seleccionado. Usa el issue,
sus criterios de aceptación y el contexto aprobado de arquitectura, backend y frontend
como fuentes de verdad. Prueba únicamente el alcance de esta funcionalidad y conserva
los contratos existentes; no implementes cambios de producto ni amplíes el issue.

Entrega un informe en español con estas secciones:
1. Alcance y supuestos: distingue hechos del contexto de aquello que no está definido.
2. Matriz de trazabilidad: relaciona cada criterio de aceptación con uno o más casos,
   su tipo (positivo, negativo, límite o regresión) y el resultado esperado.
3. Riesgos, cobertura pendiente y casos manuales necesarios, explicando por qué no
   pueden automatizarse con la información o dependencias disponibles.
4. Ejecución: indica el comando de prueba aplicable (por ejemplo, `mvn test` desde
   `output/backend-quarkus`) y deja el resultado como `PENDIENTE DE EJECUCIÓN`.
   No afirmes haber ejecutado tests, no inventes resultados ni porcentajes de cobertura.

Incluye pruebas automatizadas Java con JUnit 5 solo cuando las clases, métodos y
contratos necesarios estén respaldados por el contexto aprobado. No inventes APIs,
fixtures, dependencias ni comportamientos para forzar que una prueba parezca completa.
Si falta información para una prueba fiable, regístrala como bloqueada o pendiente en
el informe en vez de generar código especulativo. No alteres código de producción.

Para cada clase de prueba generada, entrega un bloque `java` independiente. En las
primeras líneas del bloque incluye `// NombreTest.java` y declara el package que
corresponda al código probado (`pe.bcp.login` si el contexto no permite determinar
uno más específico). Las pruebas deben ser deterministas, aisladas y comprobar
resultados observables, incluyendo errores y límites relevantes cuando estén definidos.
""".strip()
agent = Agent(role='Ingeniero de pruebas',
              goal="Diseñar pruebas trazables y verificables sin inventar resultados.",
              backstory=("Eres responsable de calidad. Proteges los criterios de aceptación "
                         "y contratos existentes con pruebas basadas en evidencia; separas "
                         "claramente lo verificado de lo pendiente."),
              llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output=('Informe testing_report.md con matriz de trazabilidad y '
                                 'estado de ejecución honesto, más bloques Java JUnit 5 '
                                 'extraíbles cuando haya contexto suficiente.'),
                agent=agent)
