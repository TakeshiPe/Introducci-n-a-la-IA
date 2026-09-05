# Ejercicio 1 - Comparar Greedy y A* en el mapa de Rumania

Con la pareja elegida: **Vaslui - Zerind** y al ejecutar los algoritmos Greedy y A*, se obtienen los siguientes resultados:

| Algoritmo | Path | Depth | Cost | Expanded | Heuristica utilizada |
| --- | --- | --- | --- | --- | --- |
| Greedy | Vaslui → Urziceni → Bucharest → Faragas → Sibiu → Arad → Zerind | 6 roads | 752 km | 8 nodes | Euclidean distance to Zerind (map coordinates) |
| A* | Vaslui → Urziceni → Bucharest → Pitesti → Rimnicu Vilcea → Sibiu → Arad → Zerind | 7 roads | 720 km | 13 nodes | Euclidean distance to Zerind (map coordinates) |

De la tabla puede verse que **A\* encontró la ruta con menor costo en km** con 720 km en comparación con la ruta encontrada por Greedy, la cual consta de 752 km, a pesar de la profundidad de Greedy es menor (6 carreteras vs 7 carreteras de A*). 

Esto se debe a que el algoritmo Greedy no toma en cuenta el costo acumulado asociado a los caminos tomados, teniendo en cuenta únicamente en la distancia o heurística faltante hasta el estado meta. Es decir, que aunque la heurística sea admisible, Greedy no optimiza considerando costos pasados, únicamente costos futuros. 

Por otro lado, tras la ejecución de **A\*** se aprecia que el valor de ```f``` incrementa a lo largo de la ruta, esto es una señal de que la heurística utilizada es consistente, es decir, que el costo estimado para llegar a la meta desde un nodo ```n``` no es mayor que el costo real de ir de ```n``` más la heurística de ```n'``` hasta la meta.

Similarmente, se ejecutó el algoritmo **UCS** (Uniform Cost Search) de búsqueda no informada, el cual encontró la misma ruta que el algoritmo **A\***, sin embargo, éste último lo logra expandiendo menos nodos (13 nodos de A* vs 17 nodos de UCS).

En la carpeta del repositorio se pueden ver los subgrafos utilizados para los algoritmos Greedy y A*.
