# Ejercicio 1 — Más capas en el perceptrón multicapa (Iris)

Posterior a la implementación de dos capas extra en los modelos 'a mano' y Kreras, se presenta un resumen de los prinipales resultados obtenidos.

| Modelo | Topologia | Tiempo de ejecución | Error al final |
| --- | --- | --- | --- |
| A mano (NumPy) | $ 4 \times 3 \times 3 $| 14s | 0.0565 |
| A mano (NumPy) | $ 4 \times 3 \times 3 \times 3 \times 3 $| 14s | 0.0620 |
| Keras | $ 4 \times 3 \times 3 $| 49s | 0.1549 |
| Keras | $ 4 \times 3 \times 3 \times 3 \times 3 $| 43s | 0.2222 |

De lo anterior puede verse que, para el modelo _a mano_ (NumPy), al implementar dos capas adicionales, el error es más grande, mientras que el tiempo de ejecución fue el mismo. Gráficamente, el modelo con más capas parece llegar más rápido a la solución, puesto que el error disminuye más rápidamente. 

La situación se repite con el modelo Keras, sin embargo, el modelo con más capas se ejecuta en menor tiempo (6 segundos menos), pero el error es mayor a la versión con menos capas, esto se debe a que la base de datos es pequeña, al contar sólo con 4 características, por lo que, al tener tantas capas el modelo empieza a aprender información que no le es útil. 

Al realizar la comparación entre modelos, se aprecia que tienen la misma tendencia pero no el mismo comportamiento, la disminución en Keras es mucho más rápida y pronunciada, mientras que en el modelo a mano la caída es un poco más lenta, observándose un pequeño estancamiento al inicio de las iteraciones. De igual forma, se aprecia que el modelo a mano inicia con un error más grande, pero finaliza con uno más bajo que el modelo Keras. 
La diferencia en las curvas de error se explica con la diferencia en inicialización de pesos, ya que el modelo manual lo hace de manera aleatoria mientras que Keras utiliza un método llamado inicializador uniforme de Glorot. Por otro lado, Keras organiza los datos antes de cada época, mientras que NumPy no hace esto. Adicionalmente, Keras optimiza las operaciones en función del hardware, mientras que NumPy hace la vectorización de forma matemática.

En conclusión, tiene sentido que utilizar redes más profundas no aprenda mejor que una red simple, principalmente porque el conjunto de datos Iris es muy pequeño, es decir, linealmente separable, lo cual produce un sobreajuste provocando resultados menos certeros que con el modelo más sencillo. De igual manera, existe un término llamado Desvanecimiento del Gradiente, en el que al momento de la retropropagación se multipliquen números muy pequeños (activaciones de la sigmoide) y al contar con una gran cantidad de capas, la multiplicación de todas las activaciones hace que el resultado sea cercano a cero, de modo que las capas iniciales de la red aprendan muy poco.
