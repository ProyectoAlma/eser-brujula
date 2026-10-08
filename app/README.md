# La Brújula de ESER — app Streamlit (playground del modelo)

App interactiva para que el equipo **juegue con el modelo de decisión**: mueve los pesos
(alcance / urgencia del hito / afinidad con ESER / episodio grabado) y ve el ranking de
invitados recalcularse en vivo, con filtros y fichas.

- Código: [`streamlit_app.py`](../streamlit_app.py) (en la raíz del repo).
- Datos: lee la planilla de Google Sheets en vivo; si no hay credenciales, usa
  [`data/snapshot.csv`](../data/snapshot.csv) (respaldo incluido en el repo).

## Correr en local
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
Sin credenciales ya funciona con el snapshot.

## Deploy en Streamlit Community Cloud (gratis)
1. Entrá a https://share.streamlit.io con la cuenta de GitHub que tiene acceso a
   `ProyectoAlma/eser-brujula`.
2. **New app** → repo `ProyectoAlma/eser-brujula`, branch `main`, main file
   `streamlit_app.py`.
3. **Deploy**. En minutos queda una URL pública que podés pasarle al equipo.

### Para que lea la planilla EN VIVO (recomendado)
La planilla es privada, así que la app entra con una **cuenta de servicio** de Google:
1. En Google Cloud Console creá un proyecto y una *service account*; generá una **key JSON**.
   Habilitá la **Google Sheets API**.
2. Compartí la planilla de ESER (solo lectura) con el email de esa service account
   (`...@...iam.gserviceaccount.com`).
3. En Streamlit Cloud → tu app → **Settings → Secrets**, pegá:
   ```toml
   sheet_id = "1Lld0mYgujAi7wvZ2_AwnSZH6Er71JJU6KswAWmNH1bA"

   [gcp_service_account]
   type = "service_account"
   project_id = "..."
   private_key_id = "..."
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "...@....iam.gserviceaccount.com"
   client_id = "..."
   token_uri = "https://oauth2.googleapis.com/token"
   ```
4. Guardá: la app se reinicia y ya muestra los datos en vivo (se refrescan solos con la
   tarea de lunes y jueves). Sin secrets, usa el snapshot del repo.

## Cómo funciona el puntaje
`score = (wA·alcance + wH·hito + wF·afinidad + wG·grabado) / (wA+wH+wF+wG) · 100`
- **alcance** = log10(seguidores) normalizado (columna P de la planilla).
- **hito** = columna Q (0-3): urgencia del próximo hito.
- **afinidad** = columna R (1-5): qué tan afín es el tema a ESER.
- **grabado** = 1 si el episodio está grabado, 0 si está en dossier.

El modelo es una ayuda a la decisión; el criterio humano manda.
