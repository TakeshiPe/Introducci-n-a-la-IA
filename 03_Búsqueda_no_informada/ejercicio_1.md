# Ejercicio 1 — Comparar BFS, UCS, DFS, DLS e IDS en el mapa de Rumania

Para la pareja origen-destino elegida **Hirsova-Timisoara**, al ejecutar los 5 algoritmos se obtuvieron los siguientes resultados:

|Algoritmo| Status | Path | Depth | Cost | Expanded | Generated |
| --- | --- | --- | --- | --- | --- | --- |
| BFS | success | Hirsova → Urziceni → Bucharest → Fagaras → Sibiu → Arad → Timisoara | 6 roads | 751 km | 14 nodes | 34 nodes |
| UCS | success | Hirsova → Urziceni → Bucharest → Pitesti → Rimnicu Vilcea → Sibiu → Arad → Timisoara | 7 roads | 719 km | 19 nodes | 45 nodes |
| DFS | success | Hirsova → Urziceni → Bucharest → Fagaras → Sibiu → Arad → Timisoara | 6 roads | 751 km | 7 nodes | 20 nodes |
| DLS (```limit=2```) | cutoff | --- | --- | --- | 3 nodes | 7 nodes |
| DLS (```limit=6```) | success | Hirsova → Urziceni → Bucharest → Fagaras → Sibiu → Arad → Timisoara | 6 roads  | 751 km | 7 nodes | 11 nodes |
| IDS | success | Hirsova → Urziceni → Bucharest → Fagaras → Sibiu → Arad → Timisoara | 6 roads  | 751 km | 38 nodes | 88 nodes |



De los resultados se observa que todos los algoritmos, con excepción de **UCS**, encuentran la misma ruta (_Hirsova → Urziceni → Bucharest → Fagaras → Sibiu → Arad → Timisoara_), con 6 carreteras, mientras que UCS encuentra una ruta con más carreteras (7: _Hirsova → Urziceni → Bucharest → Pitesti → Rimnicu Vilcea → Sibiu → Arad → Timisoara_), pero con **el menor costo en kilómetros** (719 km en comparación de 751 km de los otros algoritmos). Es decir, **BFS sí encuentra el camino con el menor número de carreteras**.

En este caso todos los algoritmos distintos a **UCS** coinciden en ruta, sin embargo, el DFS pudo haber devuelto camino más largo dado que explora un camino más profundo posible antes de retroceder, devolviendo la primer ruta encontrada que llegue a la meta. 

Para el algoritmo **DLS** no se encuentra solución, es decir, el resultado es ```cutoff```, cuando ```limit``` se establece en 2, 3, 4 y 5. Es a partir de ```limit = 6``` que se encuentra la solución, lo cual está relacionado con la profundidad con la que el algoritmo **BFS** encuentra su solución, ya que dicho modelo encuentra el modelo a la profundidad más óptima, proporcionarle a **DLS** un límite inferior a la profundidad encontrada provoca que el algoritmo no baje hasta el nivel donde está el objetivo. Por otro lado, dado que el algoritmo **IDS** ejecuta **DLS** incrementando en 1 el límite, tiene sentido que la profundidad en la que encuentra la solución coincida con la profundidad de **BFS** y el primer límite en el que **DLS** encuentra solución. 

El algoritmo que más nodos expandió es el **IDS**, situación que está alineada con su naturaleza de algoritmo iterativo. Por otro lado, los algoritmos (que sí encuentran una solución), que menos nodos expanden son los **DFS** y **DLS** (con ```limit = 6```), con 7 nodos cada uno, lo cual está relacionado de igual manera con la forma en la que operan estos algoritmos (búsqueda hacia abajo/en profundidad).