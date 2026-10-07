# ESER · Radar de Entrevistados

Radar vivo de los invitados del podcast **ESER** (una creación de René Boiero × Osmos Global).
Detecta, semana a semana, **qué invitado está en auge** (un libro, una gala, una nota, un
lanzamiento) para que ESER **suba su fragmento en el momento justo y surfee esa ola**:
republicar el clip de la entrevista cuando esa persona está en boca de todos, etiquetarla y
multiplicar el alcance de ambos.

## Las 3 piezas del sistema

1. **Planilla** (fuente editable) — Google Sheet en el drive compartido de ESER. Una fila por
   invitado: datos, redes, última señal, próximo hito, **oportunidad de amplificación** y
   **prioridad** (🔥 ola fuerte · 👀 seguir · 💤 sin novedades).
2. **Dashboard** (`/dashboard`) — página con la identidad de ESER (azul petróleo, crema,
   dorado, cian + logo). Muestra el radar priorizado y las oportunidades. Se alimenta de
   `dashboard/radar.json` (datos) y es estática (hosteable en cualquier lado).
3. **Automatización** — tarea programada que corre **lunes y jueves**: investiga novedades de
   cada invitado (prensa, webs, Instagram, YouTube, Spotify), actualiza la planilla, refresca
   `radar.json` y envía un resumen con las oportunidades de la semana.

## Estructura del repo

```
dashboard/     Fuente del dashboard (index.html + radar.json + eser.png). Estático.
data/          roster.csv — export semilla de la planilla (30 invitados).
pipeline/      Corrida interna (lectura de videos + matching). Ver pipeline/PLAN.md. [roadmap]
```

## Cómo se actualiza el dashboard

El dashboard lee `dashboard/radar.json` ({ fecha, guests[] }). Para actualizarlo, se
regenera ese archivo desde la planilla y se vuelve a publicar. El HTML no necesita tocarse.

## Roadmap — la corrida interna de videos

El próximo gran paso: **leer los videos de las entrevistas y su contenido** para **matchear**
cada momento potente con la oportunidad de amplificación de cada invitado. Así, cuando Tati
presenta su libro, el sistema no solo avisa "subí a Tati": sugiere **el clip exacto** de su
entrevista (timestamp, frase, copy y a quién etiquetar). Detalle en `pipeline/PLAN.md`.

## Enlaces
- Planilla: https://docs.google.com/spreadsheets/d/1Lld0mYgujAi7wvZ2_AwnSZH6Er71JJU6KswAWmNH1bA/edit
- Dashboard: https://claude.ai/artifact/1D7VMHRwNNF5NM3udo3H23
