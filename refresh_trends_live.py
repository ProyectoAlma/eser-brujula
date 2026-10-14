#!/usr/bin/env python3
# Refresca dashboard/trends_live.json con lo que mas se busca hoy en Google Trends (AR, CR, ES).
# Lo corre la tarea de lunes y jueves, junto con radar.json y tendencias.json.
import json, re, html, datetime, urllib.request, os

GEOS = ["AR", "CR", "ES"]
MES = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]

def fetch(geo):
    url = "https://trends.google.com/trending/rss?geo=" + geo
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        xml = r.read().decode("utf-8", "replace")
    items = re.findall(r"<item>(.*?)</item>", xml, re.S)
    out = []
    for it in items:
        m = re.search(r"<title>(.*?)</title>", it, re.S)
        if m:
            t = html.unescape(re.sub(r"<!\[CDATA\[|\]\]>", "", m.group(1))).strip()
            if t:
                out.append(t)
    return out[:9]

geos = []
for g in GEOS:
    try:
        items = fetch(g)
    except Exception:
        items = []
    if items:
        geos.append({"g": g, "items": items})

if geos:
    hoy = datetime.date.today()
    data = {
        "actualizado": f"{hoy.day} {MES[hoy.month-1]} {hoy.year}",
        "fuente": "Google Trends — busquedas del dia",
        "geos": geos,
    }
    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard", "trends_live.json")
    # si se corre desde la raiz del repo:
    if not os.path.isdir(os.path.dirname(dest)):
        dest = os.path.join("dashboard", "trends_live.json")
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("trends_live.json actualizado:", data["actualizado"], "·", sum(len(x["items"]) for x in geos), "terminos")
else:
    print("Google Trends no devolvio datos; se deja el trends_live.json anterior.")
