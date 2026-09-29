# vuln-triage-demo

> ⚠️ **Repositorio de demostración** para una charla técnica (Ekoparty 2026, "DSOMM: midiendo la madurez que tu DevSecOps solo declara"). No es un proyecto productivo — está construido a propósito para ilustrar la diferencia entre un pipeline que *declara* buenas prácticas de DevSecOps y uno que las *mide* de verdad con [OWASP DSOMM](https://dsomm.owasp.org/).

## Qué es esto

Un mini-servicio de triage de vulnerabilidades (clasifica hallazgos de un scanner ficticio por severidad). Tiene:

- Un pipeline de CI (`.github/workflows/ci.yml`) que **corre tests y build** — es decir, "en el papel" el proyecto tiene CI/CD, como cualquier repo que diría "hacemos DevSecOps".
- **Sin ningún paso de escaneo de seguridad por commit** todavía — a propósito. Ese es el estado inicial ("declara, no mide") que la charla usa como punto de partida.
- Código con un par de problemas de seguridad reales y comunes (nada exótico), para que un scanner (Bandit + pip-audit) encuentre hallazgos genuinos al agregarlo — no simulados.

## Uso

```bash
pip install -r requirements.txt
pytest
python -m src.triage
```

## Contexto para la charla

Este repo se usa para:
1. Autoevaluar con el heatmap de DSOMM (sub-dimensiones *Build*, *Verification* y *Static depth for applications*) el estado inicial — sin ningún gate corriendo, la autoevaluación honesta es "Not implemented" en todas las actividades relevantes.
2. Agregar un gate mínimo de escaneo por commit (Bandit + pip-audit, `.github/workflows/security-gate.yml`) y volver a evaluar.
3. Comparar qué hallazgos aparecen "tarde" si el escaneo se hiciera solo una vez por semana en vez de por commit.

### Mapeo de actividades DSOMM usadas en la charla

| Hallazgo real del repo | Actividad DSOMM | Sub-dimensión | Nivel |
|---|---|---|---|
| pip-audit: 16 CVEs en dependencias (pyyaml, requests, pytest) | **Software Composition Analysis (server side)** | Static depth for applications | 2 |
| Bandit: 4 hallazgos (shell=True, yaml.load inseguro, eval, subprocess) | **Static analysis for important server side components** | Static depth for applications | 3 |

Nota: "SBOM of components" (Build) **no** se usa como mapeo — un SBOM es un inventario de componentes, no un escaneo de vulnerabilidades; pip-audit hace SCA, no genera SBOM. Usar esa actividad sería una afirmación inexacta sobre lo que el repo realmente prueba.
