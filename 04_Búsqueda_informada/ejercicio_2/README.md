# Rutas óptimas en el grafo de ciudades de México (A*)

## Archivos utilizados para el ejercicio

| Archivo | Qué es |
|---|---|
| `mexico_cities_graph.json` | Grafo: 1000 ciudades (`nodes`, `id` único) y `edges` con su costo en km. |
| `generate_mexico_graph.py` | Genera `mexico_map.html` a partir del JSON. Aquí se encuentra el planeador de rutas con A*. |
| `mexico_map.html` | El mapa interactivo (salida de `generate_mexico_graph.py`). |
| `find_route.py` | CLI: calcula la ruta óptima entre dos ciudades con A* y genera un HTML con la ruta pintada. |


---

## 1. Funcionamiento del CLI

### Buscar el `id` de una ciudad por nombre

Como hay nombres repetidos (ej. "Puebla" existe en el estado de Puebla y en Baja California), el identificador único es el `id`, no el nombre:

```bash
python find_route.py --list "puebla"
```

```
   id  Ciudad                       Estado               Población
    4  Puebla                       Puebla               1,434,062
  580  Puebla                       Baja California      15,168
```

### Calcular una ruta

```bash
python find_route.py --from 4 --to 580
```

Esto imprime en la terminal la distancia total, el número de ciudades y, paso a paso, cada parada con su distancia acumulada. Al final genera `mexico_route.html` (el mapa con la ruta ya pintada).

Para elegir dónde se guarda el HTML:

```bash
python find_route.py --from 4 --to 580 --output mi_ruta.html
```

Argumentos disponibles: `--from`, `--to` (ids, obligatorios), `--graph` (ruta al JSON, por defecto `mexico_cities_graph.json`), `--output` (por defecto `mexico_route.html`), `--list "texto"` (buscar ids por nombre).

---

## 2. Usar el planeador de rutas interactivo dentro del mapa

Con el fin de hacer el mapa más interactivo, se replicó el algoritmo **A\*** en la plantilla HTML, con el fin de que el usuario pueda introducir las ciudades origen y destino y ver la ruta en el mapa. La selección de ciudades se hace mediante listas desplegables, con el fin de evitar ambigüedades con las ciudades duplicadas. Para utilizar esta versión se siguen los siguientes pasos:

1. Abre `mexico_map.html` en tu navegador.
2. En el panel izquierdo, en **"Planear ruta (A\*)"**, escribe en **Origen** el nombre de una ciudad. Aparece una lista de sugerencias mostrando también el estado y el `id`, para que se pueda distinguir ciudades con el mismo nombre. Haz clic en la que quieras.
3. Repite lo mismo en **Destino**.
4. Haz clic en **"Calcular ruta (A*)"**. El propio navegador calcula la ruta y la pinta en el mapa: los nodos y aristas del camino óptimo se resaltan en naranja fuerte, el resto se atenúa, y el mapa hace zoom automático a la zona de la ruta. El panel derecho muestra la distancia total y la lista de paradas (si son más de 10 ciudades, solo se listan las primeras 5 y las últimas 5, para que el resumen sea legible).
5. **"Limpiar ruta"** regresa el mapa a su vista normal de exploración.
