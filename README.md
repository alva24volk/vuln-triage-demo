# vuln-triage-demo

> ⚠️ **Repositorio de demostración** para una charla técnica (Ekoparty 2026, "DSOMM: midiendo la madurez que tu DevSecOps solo declara"). No es un proyecto productivo — está construido a propósito para ilustrar la diferencia entre un pipeline que *declara* buenas prácticas de DevSecOps y uno que las *mide* de verdad con [OWASP DSOMM](https://dsomm.owasp.org/).

## Qué es esto

Un mini-servicio de triage de vulnerabilidades (clasifica hallazgos de un scanner ficticio por severidad). Tiene:

- Un pipeline de CI (`.github/workflows/ci.yml`) que **corre tests y build** — es decir, "en el papel" el proyecto tiene CI/CD, como cualquier repo que diría "hacemos DevSecOps".
- **Sin ningún paso de escaneo de seguridad por commit** todavía — a propósito. Ese es el estado inicial ("declara, no mide") que la charla usa como punto de partida.
- Código con un par de problemas de seguridad reales y comunes (nada exótico), para que un scanner (Semgrep/Trivy) encuentre hallazgos genuinos al agregarlo — no simulados.

## Uso

```bash
pip install -r requirements.txt
pytest
python -m src.triage
```

## Contexto para la charla

Este repo se usa para:
1. Autoevaluar con el heatmap de DSOMM (dimensiones *Build and Deployment* y *Test and Verification*) el estado inicial.
2. Agregar un gate mínimo de escaneo por commit (Trivy/Semgrep) y volver a evaluar.
3. Comparar qué hallazgos aparecen "tarde" si el escaneo se hiciera solo una vez por semana en vez de por commit.
