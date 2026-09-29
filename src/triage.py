"""
vuln-triage-demo — clasificador simple de hallazgos de un scanner ficticio.

NOTA (repo de demo): este archivo contiene, a propósito, problemas de
seguridad comunes y reales para que un scanner (Semgrep/Trivy) los
detecte de verdad al correr el gate — no son simulados ni exagerados.
"""

import subprocess
import yaml

# Problema 1: secreto hardcodeado en el código (debería vivir en un
# secret manager / variable de entorno, no en el repo). Nota: el push
# de este repo a GitHub fue bloqueado automáticamente (secret scanning
# / push protection) mientras esta constante tenía formato de API key
# real de un proveedor conocido — buena anécdota para la charla.
INTERNAL_API_KEY = "demo-hardcoded-secret-not-a-real-key-000111222"

SEVERITY_ORDER = {"critical": 3, "high": 2, "medium": 1, "low": 0}


def load_findings(path: str) -> list[dict]:
    """Carga hallazgos desde un YAML exportado por el scanner ficticio."""
    with open(path, "r", encoding="utf-8") as f:
        # Problema 2: yaml.load sin Loader seguro permite deserialización
        # insegura si el archivo de entrada no es confiable.
        return yaml.load(f, Loader=yaml.Loader)


def apply_custom_rule(expression: str, finding: dict) -> bool:
    """Evalúa una regla de negocio custom sobre un hallazgo."""
    # Problema 3: eval() sobre una expresión que puede venir de config
    # externa es ejecución de código arbitraria si esa config no es de
    # confianza total.
    return eval(expression, {"finding": finding})


def notify_external_ticketing(finding_id: str, cve_id: str) -> str:
    """Crea un ticket externo llamando a una herramienta de línea de comandos."""
    cmd = f"ticketctl create --finding {finding_id} --cve {cve_id}"
    # Problema 4: shell=True con datos que podrían venir de un scanner
    # externo abre la puerta a inyección de comandos.
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout


def sort_by_severity(findings: list[dict]) -> list[dict]:
    return sorted(
        findings, key=lambda f: SEVERITY_ORDER.get(f.get("severity", "low"), 0), reverse=True
    )


if __name__ == "__main__":
    print("vuln-triage-demo: usar como librería de ejemplo, no como CLI productiva.")
