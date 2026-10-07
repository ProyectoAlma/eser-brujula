# Pipeline interno — lectura de videos + matching

> Estado: **roadmap / scaffold** (todavía no implementado). Este documento define el plan
> para que, cuando lo construyamos, sepamos exactamente qué hace cada etapa.

## Objetivo
Leer los videos y audios de las entrevistas de ESER, entender su contenido, y **matchear**
los mejores momentos de cada entrevista con la oportunidad de amplificación vigente de ese
invitado. Resultado: ante una ola (ej. Tati presenta su libro), el sistema propone **el clip
exacto** a publicar — con timestamp, la frase textual, un copy y a quién etiquetar.

## Etapas

1. **Ingesta** — Listar los videos del drive de ESER (carpeta de edición). Registrar por
   episodio: invitado, archivo, duración, estado.
2. **Audio** — Extraer la pista de audio de cada video (ffmpeg).
3. **Transcripción** — Audio → texto con marcas de tiempo (p. ej. Whisper). Guardar por
   episodio en `pipeline/transcripts/` (no se versiona).
4. **Análisis de contenido** — Segmentar la charla en "momentos". Por cada momento: tema,
   frase/quote potente, emoción, duración apta para reel (~20–60 s), timestamp inicio–fin.
5. **Indexación** — Guardar por invitado una colección de momentos (quote + timestamps +
   temas + embedding). Esto es la "memoria" del contenido de ESER.
6. **Matching** — Cruzar la **última señal / próximo hito** del radar (lo que el invitado está
   haciendo ahora) con los momentos indexados de su entrevista, por similitud semántica
   (embeddings) + reglas. Elegir el mejor clip para esa ola.
7. **Salida** — Para cada 🔥/👀: una tarjeta de **"clip sugerido"** (timestamp, frase, copy,
   hashtags, a quién etiquetar) en el dashboard y en el resumen semanal.

## Decisiones a tomar al construirlo
- Motor de transcripción (local vs. API) y costo por hora de video.
- Modelo de embeddings para el matching.
- Dónde corre la corrida (tarea programada interna) y cada cuánto.
- Cómo se revisa/aprueba un clip sugerido antes de publicar.

## Carpetas (ignoradas en git por peso)
- `pipeline/audio/`         audios extraídos
- `pipeline/transcripts/`   transcripciones
- `pipeline/work/`          artefactos intermedios
