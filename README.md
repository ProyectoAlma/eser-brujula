# La Brújula de ESER 🧭

> **El motor de decisión de contenido de ESER.** Marca **qué publicar y cuándo**: qué episodio
> sacar, qué reel editar y de qué invitado — según lo que está pasando en el mundo y lo que hay
> dentro de las entrevistas. (ESER es una creación de René Boiero × Osmos Global.)

## La lógica de la brújula
La decisión nace de cruzar tres señales:

1. **Quién está en auge** — el *Radar de entrevistados*: qué invitado tiene un momento caliente
   ahora (un libro, una gala, una nota, un lanzamiento).
2. **Qué hay dentro de las entrevistas** — la *lectura de videos*: los mejores momentos y frases
   de cada episodio grabado.
3. **El match** — se unen las dos: «esta semana publicá el episodio de X / este reel con esta
   frase, porque la persona está en boca de todos». Eso es lo que apunta la brújula.

## Componentes
1. **Planilla** (fuente editable) — Google Sheet en el drive de ESER. Una fila por invitado:
   datos, redes, última señal, próximo hito, **oportunidad de amplificación** y **prioridad**.
2. **Dashboard** (`/dashboard`) — la vista del radar, con la identidad de ESER. Se alimenta de
   `dashboard/radar.json`. Estático y hosteable.
3. **Automatización** — corre **lunes y jueves**: investiga novedades de cada invitado, actualiza
   la planilla, refresca el dashboard y manda un resumen con las oportunidades de la semana.
4. **Pipeline de videos** (`/pipeline`) — lee los videos, transcribe, extrae momentos potentes y
   **matchea** cada momento con la oportunidad del invitado → sugiere el clip exacto. [roadmap]

## Estructura del repo
```
dashboard/            Vista del radar (index.html + radar.json + eser.png). Estático.
data/
  entrevistados.csv   Lista maestra (export de la planilla).
  fichas/             Una ficha .md por invitado — acá vamos agregando info de cada uno.
episodios/            Info por episodio/video (metadatos; luego transcripciones y clips).
pipeline/             Lectura de videos + matching. Ver pipeline/PLAN.md. [roadmap]
```

## La web (publicación)
La web **es la carpeta `dashboard/`** (estática). Se publica con **GitHub Pages** mediante el
workflow `.github/workflows/pages.yml`: cada push a `main` que toque `dashboard/` reconstruye y
publica el sitio solo. No hay build.

Puesta en marcha (una vez): en GitHub → **Settings → Pages → Build and deployment → Source:
GitHub Actions**. Con eso, la URL pública queda en `https://proyectoalma.github.io/eser-brujula/`.
(La app de Streamlit — `streamlit_app.py` — queda como herramienta interna de playground del modelo,
no como la web pública.)

Alternativa: Netlify (import del repo, publish directory `dashboard`). Equivale a lo mismo.

## Cómo se actualiza el dashboard
Lee `dashboard/radar.json` ({ fecha, guests[] }). La automatización de lunes y jueves investiga
las novedades, regenera `radar.json` y lo **commitea al repo**; el push dispara el workflow y la web
se actualiza sola. El HTML no se toca. Para un arreglo puntual se puede editar `dashboard/radar.json`
directo desde la web de GitHub.

## Enlaces
- Planilla: https://docs.google.com/spreadsheets/d/1Lld0mYgujAi7wvZ2_AwnSZH6Er71JJU6KswAWmNH1bA/edit
- Web (GitHub Pages, una vez habilitada): https://proyectoalma.github.io/eser-brujula/
- Dashboard (artifact, versión previa): https://claude.ai/artifact/1D7VMHRwNNF5NM3udo3H23
