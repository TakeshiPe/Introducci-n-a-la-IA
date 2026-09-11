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

Los cuales fueron elegidos de tal manera que se encuentren lo suficientemente separados. Sin embargo, al ejecutar el modelo de K-medias y revisar los valores de las inercias y de la silueta, se tienen los siguientes resultados:

```intertias
Inercias

[19052.99, 12339.62, 4257.04, 2353.93, 872.95, 792.89, 644.97, 550.08, 510.54]
```

| k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| inercia | 19052.99 | 12339.62 | 4257.04 | 2353.93 | 872.95 | 792.89 | 644.97 | 550.08 | 510.54 |
| diferencia neta | - | 6713.37 | 8082.58 | 1903.11 | 1480.98 | 80.06 | 147.92 | 94.89 | 39.54 |
| diferencia porcentual | - | 35% | 66% | 45% | 63% | 9% | 19% | 15% | 7% |

![Gráfico de codo](./3.%20Codo%20modificado.png) 

De las inercias y observando el gráfico de codo, a simple vista se aprecia que el punto donde se encuentra el codo es en ```k=3```, sin embargo, revisando las diferencias porcentuales, el número de clústers podría situarse entre 3 y 5.

Las puntuaciones de siluetas son las siguientes:

```silhouette_scores
Puntuación de siluetas
[0.4, 0.6, 0.66, 0.75, 0.66, 0.63, 0.63, 0.61]
```

De lo anterior, queda claro que el valor en ```k=5``` se tiene la mejor puntuación, con 0.75.

---

Para análizar el origen de la diferencia entre los resultados de los dos métodos, se realiza el ejercicio reduciendo la desviación de los _blobs_ a 0.01 para todos, a pesar de esto, a simple vista se observa que las ```k``` propuestas por los métodos mencionados anteriormente siguen siendo los mismos (```k=3``` para **codo** y ```k=5``` para **silueta**). Sin embargo, al analizar los resultados de manera numérica, puede verse que las inercias llegan al punto más óptimo en ```k=5```, teniendo una disminución del 100% respecto a ```k=4```, por lo tanto, 5 es el número de clústers a elegir.

| k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Inercia | 18171.48 | 11419.29 | 3653.23 | 1477.59 | 0.39 | 0.37 | 0.34 | 0.32 | 0.3 |
| Diferencia neta | - | 6752.19 | 7766.06 | 2175.64 | 1477.2 | 0.02 | 0.03 | 0.02 | 0.02 |
| Diferencia porcentual | - | 37% | 68% | 60% | 100% | 5% | 8% | 6% | 6% |

Finalmente, se realiza nuevamente el ejercicio, con centroides más dispersos, con las posiciones

```
[ -200.9,  100.9],
[-100.78 ,  -100.3],
[0.1,  300],
[100.23,  -200.65],
[200.75,  200.4]
```

Conservando las desviaciones de la primera modificación. Al hacer estos cambios, se observa que el gráfico de codo, podría definirse entre 3 y 5, siendo que después de 5 es el punto de inflexión en el que la curva se aplana por completo y deja de caer de forma significativa, sin embargo, nuevamente es a partir de 3 es que empieza a tomar la forma del codo de manera visual. Numéricamente los resultados se presentan a continuación, de los cuales se observa de forma más clara que el número de clústers ```k=5``` es donde se tiene la mejor disminución de inercias, por lo que, ésta debe ser la cantidad de grupos elegida.

| k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Inercia | 109395223.83 | 74346888.57 | 20127543.65 | 10037318.78 | 904.76 | 842.02 | 693.34 | 608.02 | 585.86 |
| Diferencia neta | - | 35048335.26 | 54219344.92 | 10090224.87 | 10036414.02 | 62.74 | 148.68 | 85.32 | 22.16 |
| Diferencia porcentual | - | 32% | 73% | 50% | 100% | 7% | 18% | 12% | 4% |

Por otro lado, el criterio de las siluetas siempre mantuvo la misma tendencia, y en todas las iteraciones propuso el valor de ```k=5```. Por lo que al medir si está más cerca del centroide que de la frontera, resulta ser un mejor criterio para determinar el número de centroides, al no caer en una observación subjetiva. En todos los casos, determinar el valor de ```k``` utilizando el gráfico de codo, puede resultar confuso y sujeto a errores si se hace a simple vista, esto porque las escalas de los datos entran en juego respecto a cómo se presenta la información de manera visual, ya que revisando las tablas es que se determina que el mejor valor de ```k``` puede ser distinto al observado como punto de codo.