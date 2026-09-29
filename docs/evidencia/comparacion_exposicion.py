"""
Genera el gráfico de comparación "escaneo semanal vs. por commit" para la
charla de Ekoparty.

IMPORTANTE — honestidad de los datos:
- El número "por commit" (~10s) es REAL: promedio medido de las 2 corridas
  reales de security-gate.yml que llegaron a ejecutar Bandit+pip-audit sobre
  el código con los hallazgos (commits 5ac8c20 y a2166d1): 11s y 8s.
- Los "días de exposición" bajo escaneo semanal son un MODELO ILUSTRATIVO,
  no el historial real del repo (todos los commits de la demo se hicieron
  en una sola sesión). Es aritmética simple: si el escaneo corre una vez
  por semana (viernes), un hallazgo introducido el día D queda expuesto
  (viernes - D) mod 7 días antes de detectarse. Esto se declara explícitamente
  en el gráfico y en las notas — no se presenta como dato observado.
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Paleta (dataviz skill) — un solo hue secuencial (azul) + status "good" (verde)
BLUE = "#256abf"       # sequential hue, step 500
GREEN_GOOD = "#0ca30c" # status: good
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
SURFACE = "#fcfcfb"

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
# (viernes=4 - D) mod 7
exposicion = [(4 - d) % 7 for d in range(7)]  # [4,3,2,1,0,6,5]

fig, ax = plt.subplots(figsize=(9.5, 6), dpi=200)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)

bars = ax.bar(dias, exposicion, width=0.6, color=BLUE, zorder=3)
for rect, val in zip(bars, exposicion):
    rect.set_capstyle("round")
    ax.text(
        rect.get_x() + rect.get_width() / 2,
        val + 0.18,
        f"{val} día{'s' if val != 1 else ''}",
        ha="center", va="bottom",
        fontsize=10.5, color=INK_PRIMARY, fontweight="medium",
    )

# Línea de referencia: escaneo por commit (real, medido)
ax.axhline(0.08, color=GREEN_GOOD, linewidth=2.5, zorder=4)

ax.set_ylim(0, 7.6)
ax.set_ylabel("Días de exposición hasta el escaneo", fontsize=10.5, color=INK_SECONDARY)

# Título y subtítulo como texto de figura, con separación clara (evita choque)
fig.text(0.06, 0.965, "¿Cuánto tarda en detectarse el mismo hallazgo?",
          fontsize=15.5, color=INK_PRIMARY, fontweight="bold", ha="left", va="top")
fig.text(0.06, 0.925, "Modelo ilustrativo — escaneo semanal (viernes) vs. escaneo real por commit de este repo",
          fontsize=10.5, color=INK_MUTED, ha="left", va="top")

# Leyenda de la línea verde, como caja aparte arriba a la derecha (no pisa barras)
ax.text(
    6.7, 7.0,
    "Escaneo por commit\n(real, medido): ~10 s",
    ha="right", va="top", fontsize=10, color=GREEN_GOOD, fontweight="bold",
    linespacing=1.4,
)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_color(BASELINE)
ax.tick_params(axis="x", length=0, labelsize=10.5, colors=INK_SECONDARY)
ax.tick_params(axis="y", length=0, labelsize=9.5, colors=INK_MUTED)
ax.yaxis.grid(True, color=GRID, linewidth=1, zorder=0)
ax.set_axisbelow(True)

ax.text(
    0, -0.13,
    "Día en que se introduce el hallazgo en el código (día de la semana, hipotético)",
    transform=ax.transAxes, fontsize=9.5, color=INK_MUTED, ha="left",
)

plt.tight_layout(rect=[0, 0.02, 1, 0.885])
plt.savefig("/tmp/claude-0/-home-claude-vuln-triage-demo/b8b037b5-0e08-5f02-be3b-39d89265ee30/scratchpad/comparacion-exposicion.png", facecolor=SURFACE, bbox_inches="tight")
print("OK")
