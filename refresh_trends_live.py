#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Brujula ESER — generador de la cinta en vivo (trends_live.json)

Que hace:
  Lee lo que mas se busca HOY en Google Trends para Argentina, Costa Rica y
  Espana (feed RSS publico, sin API key ni dependencias) y regenera el archivo
  dashboard/trends_live.json que alimenta la cinta de arriba del carrusel.

Como se usa:
  - Manual:            python3 refresh_trends_live.py
  - En la tarea de la Mac (lunes y jueves): correr esta linea ANTES del push, y
    luego  git add dashboard/trends_live.json  junto con radar.json y tendencias.json.

Donde escribe:
  dashboard/trends_live.json  (relativo a la ubicacion de este script; se asume
  que el script vive en la raiz del repo, al lado de la carpeta dashboard/).

Si Google Trends no responde, NO toca el archivo anterior (deja la ultima
version buena) y termina sin error, para no romper la corrida de lun/jue.

Solo usa la libreria estandar de Python 3 (no hay que instalar nada).
"""
import json
import re
import html
import datetime
import os
import sys
import urllib.request

# Paises de la cinta (orden = orden en que aparecen las banderas)
GEOS = ["AR", "CR", "ES"]
MAX_POR_PAIS = 9           # cuantos terminos por pais
TIMEOUT = 25               # segundos por pedido
MES = ["ene", "feb", "mar", "abr", "may", "jun", "jul",
       "ago", "sep", "oct", "nov", "dic"]


def traer(geo):
    """Devuelve la lista de terminos tendencia para un pais (geo)."""
    url = "https://trends.google.com/trending/rss?geo=" + geo
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        xml = r.read().decode("utf-8", "replace")
    terminos = []
    # cada tendencia es un <item>...</item>; su primer <title> es el termino
    for bloque in re.findall(r"<item>(.*?)</item>", xml, re.S):
        m = re.search(r"<title>(.*?)</title>", bloque, re.S)
        if not m:
            continue
        t = re.sub(r"<!\[CDATA\[|\]\]>", "", m.group(1))
        t = html.unescape(t).strip()
        if t:
            terminos.append(t)
    return terminos[:MAX_POR_PAIS]


def destino():
    """Ruta a dashboard/trends_live.json, relativa a este script."""
    base = os.path.dirname(os.path.abspath(__file__))
    d = os.path.join(base, "dashboard", "trends_live.json")
    if os.path.isdir(os.path.join(base, "dashboard")):
        return d
    # fallback: correr desde la raiz del repo
    return os.path.join("dashboard", "trends_live.json")


def main():
    geos = []
    for g in GEOS:
        try:
            items = traer(g)
        except Exception as e:
            print("  aviso: %s fallo (%s)" % (g, type(e).__name__), file=sys.stderr)
            items = []
        if items:
            geos.append({"g": g, "items": items})

    if not geos:
        print("Google Trends no devolvio datos; se deja el trends_live.json anterior.")
        return 0

    hoy = datetime.date.today()
    data = {
        "actualizado": "%d %s %d" % (hoy.day, MES[hoy.month - 1], hoy.year),
        "fuente": "Google Trends - busquedas del dia",
        "geos": geos,
    }

    ruta = destino()
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    total = sum(len(x["items"]) for x in geos)
    print("OK  trends_live.json actualizado: %s  -  %d terminos en %d paises"
          % (data["actualizado"], total, len(geos)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
