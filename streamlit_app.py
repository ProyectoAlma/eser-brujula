# -*- coding: utf-8 -*-
"""
La Brujula de ESER — playground del modelo de decision de contenido.
El equipo mueve los pesos (alcance / hito / afinidad / grabado) y ve el ranking
recalcularse en vivo, y puede filtrar y explorar el roster.

Lee la planilla de Google Sheets en vivo si hay credenciales en st.secrets;
si no, usa data/snapshot.csv incluido en el repo.
"""
import math
import pandas as pd
import streamlit as st

SHEET_ID = "1Lld0mYgujAi7wvZ2_AwnSZH6Er71JJU6KswAWmNH1bA"
COLS = ["Nombre", "Pais", "Rubro", "Estado episodio", "Instagram",
        "Proximo hito", "Ultima actividad detectada", "Oportunidad de amplificacion",
        "Prioridad", "Seguidores", "Hito (0-3)", "Afinidad (1-5)"]

# ---- paleta ESER ----
AZUL = "#071826"; CARD = "#0f2738"; CREMA = "#eef1ea"
CIAN = "#56c6e6"; DORADO = "#e9b25a"; MUTED = "#9cb3bf"

st.set_page_config(page_title="La Brujula de ESER", page_icon="🧭", layout="wide")


# --------------------------------------------------------------------------- #
# Datos
# --------------------------------------------------------------------------- #
@st.cache_data(ttl=600, show_spinner=False)
def load_data():
    """Devuelve (DataFrame, fuente). Intenta la planilla en vivo; si no, el snapshot."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        if "gcp_service_account" in st.secrets:
            scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
            creds = Credentials.from_service_account_info(
                dict(st.secrets["gcp_service_account"]), scopes=scopes)
            gc = gspread.authorize(creds)
            sid = st.secrets.get("sheet_id", SHEET_ID)
            ws = gc.open_by_key(sid).sheet1
            df = pd.DataFrame(ws.get_all_records())
            # nos quedamos con las columnas que existan
            keep = [c for c in COLS if c in df.columns]
            return df[keep].copy(), "planilla en vivo"
    except Exception as e:  # noqa: BLE001
        st.sidebar.warning(f"No pude leer la planilla en vivo ({e}). Uso el snapshot del repo.")
    df = pd.read_csv("data/snapshot.csv")
    return df, "snapshot del repo"


def to_num(x):
    try:
        return float(str(x).replace(".", "").replace(",", "").strip() or 0)
    except Exception:  # noqa: BLE001
        return 0.0


def prep(df):
    df = df.copy()
    for c in COLS:
        if c not in df.columns:
            df[c] = ""
    df["seg"] = df["Seguidores"].apply(to_num)
    df["hito"] = pd.to_numeric(df["Hito (0-3)"], errors="coerce").fillna(0).clip(0, 3)
    df["afin"] = pd.to_numeric(df["Afinidad (1-5)"], errors="coerce").fillna(1).clip(1, 5)
    df["grabado"] = df["Estado episodio"].astype(str).str.lower().str.contains("grabado")
    # scores 0..1
    df["s_alcance"] = df["seg"].apply(lambda s: min(1.0, math.log10(s + 1) / 6.0))  # 1e6 = tope
    df["s_hito"] = df["hito"] / 3.0
    df["s_afin"] = (df["afin"] - 1) / 4.0
    df["s_grab"] = df["grabado"].astype(float)
    return df


def score(df, wA, wH, wF, wG):
    tot = wA + wH + wF + wG
    if tot == 0:
        tot = 1
    df = df.copy()
    df["Score"] = (wA * df["s_alcance"] + wH * df["s_hito"]
                   + wF * df["s_afin"] + wG * df["s_grab"]) / tot * 100
    return df.sort_values("Score", ascending=False).reset_index(drop=True)


# --------------------------------------------------------------------------- #
# UI
# --------------------------------------------------------------------------- #
raw, fuente = load_data()
data = prep(raw)

st.markdown(
    f"""<div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap">
    <span style="font-family:Georgia,serif;font-size:2rem;font-weight:700;color:{CREMA}">La Brújula de ESER 🧭</span>
    <span style="color:{MUTED};font-size:.95rem">Motor de decisión de contenido · mové los pesos y mirá a quién conviene publicar</span>
    </div>""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("⚖️ El modelo")
    st.caption("El puntaje de cada invitado = combinación ponderada de 4 ingredientes. "
               "Movés los pesos según la estrategia de la semana y el ranking se reordena solo.")
    wA = st.slider("Alcance (seguidores)", 0, 100, 40,
                   help="Cuánto pesa el tamaño de la audiencia del invitado.")
    wH = st.slider("Urgencia del hito", 0, 100, 30,
                   help="Cuánto pesa que tenga un evento/noticia vigente (libro, gala, estreno).")
    wF = st.slider("Afinidad con ESER", 0, 100, 20,
                   help="Cuánto pesa que el tema sea afín al alma/espiritualidad de ESER.")
    wG = st.slider("Episodio grabado", 0, 100, 10,
                   help="Premia a los que ya se pueden publicar (grabados) sobre los que están en dossier.")
    st.divider()
    st.subheader("🔎 Filtros")
    solo_grab = st.checkbox("Solo episodios grabados", value=False)
    paises = sorted([p for p in data["Pais"].unique() if str(p).strip()])
    f_pais = st.multiselect("País", paises, default=[])
    prioridades = sorted([p for p in data["Prioridad"].unique() if str(p).strip()])
    f_prio = st.multiselect("Prioridad base (de la planilla)", prioridades, default=[])
    min_seg = st.slider("Seguidores mínimos", 0, 800000, 0, step=5000, format="%d")
    q = st.text_input("Buscar (nombre, rubro, tema)")
    st.divider()
    st.caption(f"Fuente: {fuente}. El modelo lee la planilla del drive de ESER; "
               "los números (seguidores, hito, afinidad) viven en las columnas P-R de esa planilla.")

# filtros
view = score(data, wA, wH, wF, wG)
if solo_grab:
    view = view[view["grabado"]]
if f_pais:
    view = view[view["Pais"].isin(f_pais)]
if f_prio:
    view = view[view["Prioridad"].isin(f_prio)]
if min_seg:
    view = view[view["seg"] >= min_seg]
if q:
    ql = q.lower()
    mask = (view["Nombre"].astype(str).str.lower().str.contains(ql)
            | view["Rubro"].astype(str).str.lower().str.contains(ql)
            | view["Oportunidad de amplificacion"].astype(str).str.lower().str.contains(ql))
    view = view[mask]
view = view.reset_index(drop=True)
view.index = view.index + 1  # ranking desde 1

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Invitados (en vista)", len(view))
c2.metric("Grabados", int(view["grabado"].sum()))
c3.metric("Con hito vigente", int((view["hito"] >= 2).sum()))
c4.metric("Alcance total", f"{int(view['seg'].sum()):,}".replace(",", "."))

# recomendación de la semana
pub = view[view["grabado"]]
if len(pub):
    top = pub.iloc[0]
    st.markdown(
        f"""<div style="background:{CARD};border:1px solid {DORADO};border-radius:14px;padding:16px 18px;margin:6px 0 2px">
        <div style="color:{DORADO};font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;font-weight:700">
        ✦ Recomendación del modelo · para publicar ya (grabado)</div>
        <div style="color:{CREMA};font-size:1.25rem;font-weight:700;margin-top:4px">{top['Nombre']}
        <span style="color:{CIAN};font-size:1rem">· score {top['Score']:.0f}</span></div>
        <div style="color:{MUTED};margin-top:4px">{top['Oportunidad de amplificacion']}</div>
        </div>""",
        unsafe_allow_html=True,
    )

st.subheader("Ranking del modelo")
tabla = view[["Nombre", "Pais", "Score", "seg", "hito", "afin", "grabado",
              "Prioridad", "Proximo hito", "Oportunidad de amplificacion"]].rename(
    columns={"Pais": "País", "seg": "Seguidores", "hito": "Hito", "afin": "Afinidad",
             "grabado": "Grabado", "Proximo hito": "Próximo hito",
             "Oportunidad de amplificacion": "Oportunidad"})
st.dataframe(
    tabla, use_container_width=True, height=560,
    column_config={
        "Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100,
                                                 format="%.0f"),
        "Seguidores": st.column_config.NumberColumn("Seguidores", format="%d"),
        "Hito": st.column_config.NumberColumn("Hito", help="0-3: urgencia del próximo hito"),
        "Afinidad": st.column_config.NumberColumn("Afinidad", help="1-5: afinidad con ESER"),
        "Grabado": st.column_config.CheckboxColumn("Grabado"),
        "Oportunidad": st.column_config.TextColumn("Oportunidad", width="large"),
    },
)

with st.expander("Ver fichas detalladas (top de la vista)"):
    for _, g in view.head(10).iterrows():
        ig = str(g["Instagram"]).split(" ")[0]
        link = f"[{ig}]({ig})" if ig.startswith("http") else ig
        st.markdown(
            f"**{g['Nombre']}** · {g['Pais']} · score **{g['Score']:.0f}** · "
            f"{'🎬 grabado' if g['grabado'] else '🗂️ en dossier'}  \n"
            f"*{g['Rubro']}*  \n"
            f"📣 **Próximo hito:** {g['Proximo hito'] or '—'}  \n"
            f"🛰️ **Última señal:** {g['Ultima actividad detectada'] or '—'}  \n"
            f"✦ **Oportunidad:** {g['Oportunidad de amplificacion'] or '—'}  \n"
            f"📷 {link}")
        st.divider()

st.caption("La Brújula de ESER · Proyecto Alma. El ranking es una ayuda a la decisión: "
           "el criterio humano manda. Con figuras políticas y temas sensibles, tono humano/espiritual, "
           "nunca partidario ni morboso.")
