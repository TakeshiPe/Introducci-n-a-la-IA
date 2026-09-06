#!/usr/bin/env python3
"""Encuentra la ruta más corta entre dos ciudades del grafo de México usando A*.

Uso
---
    # 1) Buscar el id de una ciudad por nombre

    # 2) Calcular la ruta entre dos ids y pintarla en un HTML nuevo
    python

    # 3) Elegir dónde se guarda el HTML de salida (por defecto mexico_route.html)
    python
"""

from __future__ import annotations

import argparse
import heapq
import json
import math
import sys
from pathlib import Path

import generate_mexico_graph as gg  # reutiliza la misma plantilla HTML del mapa

ROOT = Path(__file__).resolve().parent
DEFAULT_GRAPH = ROOT / "mexico_cities_graph.json"
DEFAULT_OUTPUT = ROOT / "mexico_route.html"
EARTH_KM = 6371.0


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distancia en línea recta (km) sobre la esfera terrestre."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * EARTH_KM * math.asin(math.sqrt(min(1.0, a)))


def load_graph(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_adjacency(graph: dict) -> dict[int, list[tuple[int, float]]]:
    """Lista de adyacencia {id_ciudad: [(id_vecino, km), ...]}.

    Se utiliza el id numérico de cada nodo como identificador, no el
    nombre para evitar ambigüedad.
    """
    adj: dict[int, list[tuple[int, float]]] = {n["id"]: [] for n in graph["nodes"]}
    for e in graph["edges"]:
        a, b, km = e["source"], e["target"], e["km"]
        adj[a].append((b, km))
        adj[b].append((a, km))
    return adj


class RouteNotFound(Exception):
    pass


def a_star(graph: dict, start_id: int, goal_id: int) -> dict:
    """A*.

    h(n) = distancia en línea recta (haversine) de n al destino.
    Es admisible y consistente porque cada arista del grafo YA es una
    distancia haversine entre sus dos extremos: por desigualdad del triángulo, ninguna ruta que
    pase por nodos intermedios puede ser más corta que la línea recta.
    """
    nodes = {n["id"]: n for n in graph["nodes"]}
    adj = build_adjacency(graph)
    goal = nodes[goal_id]

    def h(node_id: int) -> float:
        n = nodes[node_id]
        return haversine(n["lat"], n["lon"], goal["lat"], goal["lon"])

    counter = 0  # desempata nodos con el mismo f
    frontier: list[tuple[float, int, int]] = [(h(start_id), counter, start_id)]
    came_from: dict[int, int] = {}
    best_g: dict[int, float] = {start_id: 0.0}
    explored: set[int] = set()
    expanded = 0
    generated = 1
    max_frontier = 1

    while frontier:
        _f, _i, node_id = heapq.heappop(frontier)
        if node_id in explored:
            continue
        if node_id == goal_id:
            return {
                "path": _reconstruct(came_from, start_id, goal_id),
                "total_km": best_g[goal_id],
                "nodes_expanded": expanded,
                "nodes_generated": generated,
                "max_frontier": max_frontier,
            }

        explored.add(node_id)
        expanded += 1
        g = best_g[node_id]
        for neighbor_id, km in adj[node_id]:
            if neighbor_id in explored:
                continue
            tentative_g = g + km
            generated += 1
            if neighbor_id not in best_g or tentative_g < best_g[neighbor_id]:
                best_g[neighbor_id] = tentative_g
                came_from[neighbor_id] = node_id
                counter += 1
                heapq.heappush(frontier, (tentative_g + h(neighbor_id), counter, neighbor_id))
                max_frontier = max(max_frontier, len(frontier))

    raise RouteNotFound(f"No hay ruta conectada entre el id {start_id} y el id {goal_id}.")


def _reconstruct(came_from: dict[int, int], start_id: int, goal_id: int) -> list[int]:
    path = [goal_id]
    while path[-1] != start_id:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


def find_by_name(graph: dict, query: str) -> list[dict]:
    q = query.strip().lower()
    return [n for n in graph["nodes"] if q in n["name"].lower()]


def print_matches(matches: list[dict]) -> None:
    if not matches:
        print("No se encontraron ciudades con ese nombre.")
        return
    print(f"{'id':>5}  {'Ciudad':<28} {'Estado':<20} Población")
    for n in sorted(matches, key=lambda n: -n["population"]):
        print(f"{n['id']:>5}  {n['name']:<28} {n['state']:<20} {n['population']:,}")


def write_route_html(
    graph: dict, result: dict, start_id: int, goal_id: int, output_path: Path
) -> None:
    """Genera un HTML igual al mapa interactivo, pero con la ruta pintada.

    """
    if "__ROUTE_JSON__" not in gg.HTML_TEMPLATE:
        raise RuntimeError(
            "generate_mexico_graph.py no tiene el marcador "
            "__ROUTE_JSON__ en HTML_TEMPLATE: es una versión anterior a la "
            "que incluye el planeador de rutas. Reemplaza ese archivo por "
            "la versión más reciente y vuelve a intentarlo."
        )

    nodes = {n["id"]: n for n in graph["nodes"]}
    path = result["path"]
    route_payload = {
        "path": path,
        "edges": [[path[i], path[i + 1]] for i in range(len(path) - 1)],
        "total_km": round(result["total_km"], 2),
        "from": nodes[start_id],
        "to": nodes[goal_id],
        "nodes_expanded": result["nodes_expanded"],
        "nodes_generated": result["nodes_generated"],
        "stops": [nodes[i] for i in path],
    }
    graph_payload = {
        "meta": graph["meta"],
        "outline": graph["outline"],
        "nodes": graph["nodes"],
        "edges": graph["edges"],
    }
    html = (
        gg.HTML_TEMPLATE.replace(
            "__GRAPH_JSON__", json.dumps(graph_payload, ensure_ascii=False, separators=(",", ":"))
        ).replace(
            "__ROUTE_JSON__", json.dumps(route_payload, ensure_ascii=False, separators=(",", ":"))
        )
    )
    Path(output_path).write_text(html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--from", dest="start_id", type=int, help="id de la ciudad de origen")
    parser.add_argument("--to", dest="goal_id", type=int, help="id de la ciudad de destino")
    parser.add_argument("--graph", default=str(DEFAULT_GRAPH), help="ruta al JSON del grafo")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="archivo HTML de salida")
    parser.add_argument("--list", dest="query", help='buscar ciudades por nombre, ej. --list "puebla"')
    args = parser.parse_args()

    graph = load_graph(Path(args.graph))

    if args.query:
        print_matches(find_by_name(graph, args.query))
        return

    if args.start_id is None or args.goal_id is None:
        parser.error('debes indicar --from y --to (usa --list "nombre" para encontrar los ids)')

    nodes = {n["id"]: n for n in graph["nodes"]}
    for label, node_id in (("--from", args.start_id), ("--to", args.goal_id)):
        if node_id not in nodes:
            parser.error(f"{label} {node_id} no existe en el grafo")

    if args.start_id == args.goal_id:
        parser.error("--from y --to no pueden ser la misma ciudad")

    try:
        result = a_star(graph, args.start_id, args.goal_id)
    except RouteNotFound as exc:
        print(exc)
        sys.exit(1)

    origin, dest = nodes[args.start_id], nodes[args.goal_id]
    print(f"Ruta: {origin['name']} ({origin['state']}) -> {dest['name']} ({dest['state']})")
    print(
        f"Distancia total: {result['total_km']:.2f} km | "
        f"{len(result['path'])} ciudades | nodos expandidos: {result['nodes_expanded']}"
    )
    print()

    adj = build_adjacency(graph)
    acc = 0.0
    prev = None
    for node_id in result["path"]:
        n = nodes[node_id]
        if prev is not None:
            acc += next(km for nb, km in adj[prev] if nb == node_id)
        print(f"  {acc:8.1f} km  {n['name']} ({n['state']})")
        prev = node_id

    output_path = Path(args.output)
    write_route_html(graph, result, args.start_id, args.goal_id, output_path)
    print(f"\nMapa con la ruta pintada: {output_path}")


if __name__ == "__main__":
    main()
