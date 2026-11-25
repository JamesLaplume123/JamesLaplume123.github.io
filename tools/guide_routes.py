#!/usr/bin/env python3
"""Routes réelles du guide de voyage (onglet « Guide » de Mobilité).

Usage : python3 tools/guide_routes.py

Calcule une fois, sur le réseau routier réel (OSRM de FOSSGIS, données OpenStreetMap), la route
de chaque idée d'exemple du guide, puis l'enregistre dans src/demos/mobilite_guide.json
(points [lat, lon] simplifiés, distance en km, durée en minutes). Le site ne contacte donc
aucun service de routage pour les exemples. À relancer seulement si une idée change.
"""
import json
import math
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
OSRM = "https://routing.openstreetmap.de/routed-car/route/v1/driving/"


def simplifie(pts, tol):
    """Douglas-Peucker sur [lat, lon] (tolérance en degrés)."""
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    def dist(p):
        x0, y0, x1, y1, x, y = a[1], a[0], b[1], b[0], p[1], p[0]
        dx, dy = x1 - x0, y1 - y0
        if dx == dy == 0:
            return math.hypot(x - x0, y - y0)
        t = max(0, min(1, ((x - x0) * dx + (y - y0) * dy) / (dx * dx + dy * dy)))
        return math.hypot(x - x0 - t * dx, y - y0 - t * dy)
    i, dmax = 0, 0
    for k in range(1, len(pts) - 1):
        d = dist(pts[k])
        if d > dmax:
            i, dmax = k, d
    if dmax <= tol:
        return [a, b]
    return simplifie(pts[:i + 1], tol)[:-1] + simplifie(pts[i:], tol)


def route(points):
    chemin = ";".join(f"{p['lng']},{p['lat']}" for p in points)
    req = urllib.request.Request(OSRM + chemin + "?overview=full&geometries=geojson&steps=false",
                                 headers={"User-Agent": "jarvisprivatesystems.com guide (calcul unique)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    assert d.get("code") == "Ok", d
    rt = d["routes"][0]
    ll = [[round(c[1], 4), round(c[0], 4)] for c in rt["geometry"]["coordinates"]]
    ll = simplifie(ll, .004)
    ecarts = [round(w.get("distance", 0)) for w in d["waypoints"]]
    # Les repères se posent là où la route arrive vraiment (point le plus proche sur le réseau).
    arrets = [[round(w["location"][1], 4), round(w["location"][0], 4)] for w in d["waypoints"]]
    return {"pts": ll, "km": round(rt["distance"] / 1000), "min": round(rt["duration"] / 60),
            "jambes": [round(l["distance"] / 1000) for l in rt["legs"]], "arrets": arrets}, ecarts


def main():
    from demos.mobilite import GUIDE
    dep = GUIDE["depart"]
    out = {}
    for k, idee in enumerate(GUIDE["idees"]):
        if idee.get("itineraire"):
            r, ec = route([dep] + idee["lieux"])
            out[str(k)] = [r]
            print(k, "itinéraire", r["km"], "km", r["jambes"], "points", len(r["pts"]), "écarts au réseau (m)", ec)
        else:
            out[str(k)] = []
            for l in idee["lieux"]:
                r, ec = route([dep, l])
                out[str(k)].append(r)
                print(k, l["nom"], r["km"], "km", "points", len(r["pts"]), "écarts au réseau (m)", ec)
    (ROOT / "src" / "demos" / "mobilite_guide.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    main()
