# Ejercicio 2 — A* para encontrar rutas en el mapa de México

Para el desarrollo de este ejercicio, se decidió trabajar con el id en lugar con el nombre de la ciudad, esto para evitar errores de captura y ambigüedades cuando existen ciudades con el mismo nombre. Para esto, se incluye inicialmente la búsqueda de la ciudad para que el usuario pueda saber de antemano el ```id``` para ejecutar la búsqueda. En la versión ```html``` esto se soluciona con el uso de las listas desplegables.

La heurística de **A\*** es la distancia en línea recta (_haversine_) del nodo al destino. Es admisible y consistente porque cada arista del grafo ya es, por construcción, una distancia haversine entre sus dos extremos y por desigualdad del triángulo, ninguna ruta que pase por nodos intermedios puede ser más corta que la línea recta.

Como parte de las pruebas, se realizó el cálculo de la ruta desde Mérida (Yucatán) hasta Caborca (Sonora), de la cual se tuvo una distancia total de 3670.21 km, recorriendo 115 ciudades y 915 nodos expandidos. Las capturas de pantalla de evidencia se encuentran dentro del repositorio.