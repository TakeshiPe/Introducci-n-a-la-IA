# Ejercicio 1 — Separar los blobs y volver a elegir \(k\)

Posterior a la ejecución del ejercicio de K-medias, se observa que, durante la corrida original (datos de Gerón), el codo prefiere ```k=4``` a pesar de que ```make_blobs``` utilizó 5 centros porque dos de los _blobs_ están muy cerca, con las posiciones [-2.8,1.3] y [-2.8,1.8] y cada uno con desviación 0.1, pues como comparten eje x y al crear los blobs de manera aleatoria, los datos se concentran en la misma área. Desde el inicio prácticamente puede verse que los datos pueden agruparse en tan sólo 4 grupos y el modelo, al no conocer el origen de los datos, considera que el número de grupos más óptimo es 4.

Al separar los centros de los _blobs_ con las siguientes posiciones:
```
    [ -2.9,  1.9],
    [-1.78 ,  -1.3],
    [0.1,  3],
    [1.23,  -2.65],
    [2.75,  2.4]
```

Y con desviaciones: ```[0.3, 0.8, 0.1, 0.5, 0.4]```

Los cuales fueron elegidos de tal manera que se encuentren lo suficientemente separados. Sin embargo, al ejecutar el modelo de K-medias y revisar los valores de las inercias y de la silueta, así como sus respectivos gráficos, se observa que, el valor de ```k``` donde se encuentra el **codo** es ```k=3```, mientras que, en el gráfico de **siluetas**, el valor de k es ```5```.

Para análizar el origen de la diferencia entre los resultados de los dos métodos, se realiza el ejercicio reduciendo la desviación de los _blobs_ a 0.01 para todos, a pesar de esto, se observa que las ```k``` propuestas por los métodos mencionados anteriormente siguen siendo los mismos (```k=3``` para **codo** y ```k=5``` para **silueta**). Por lo que, se determina que la desviación no es el factor determinante en la discrepancia entre los dos métodos.

Se realiza nuevamente el ejercicio, con centroides más dispersos, con las posiciones
```
    [ -200.9,  100.9],
    [-100.78 ,  -100.3],
    [0.1,  300],
    [100.23,  -200.65],
    [200.75,  200.4]
```
Conservando las desviaciones de la primera modificación. Al hacer estos cambios, se observa que el gráfico de codo, podría definirse entre 3 y 5, siendo que después de 5 es el punto de inflexión en el que la curva se aplana por completo y deja de caer de forma significativa, sin embargo, a partir de 3 es que empieza a tomar la forma del codo de manera visual. Por otro lado, el criterio de las siluetas siempre mantuvo la misma tendencia, y en todas las iteraciones propuso el valor de ```k=5```, por lo que al medir si está más cerca del centroide que de la frontera, resulta ser un mejor criterio para determinar el número de centroides, al no caer en una observación subjetiva.  