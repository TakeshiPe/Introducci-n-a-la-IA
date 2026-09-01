# Reporte del Ejercicio 01 (Cambiar la ubicación del Wumpus y los pits)

Posterior al cambio de mapa en el que el oro se encuentra en las coordenadas **[3,4]**, el Wumpus en las coordenadas **[3,3]** y los pits en **[1,4]**, **[4,2]** y **[4,4]**, se observa lo siguiente:

El agente 1 **(de reflejo simple)** no logró salir con el oro, se queda estancado en la primera fila, logrando llegar hasta la última casilla, pero al tener arriba a un _pit_, no logra avanzar y se queda dando vueltas. Este agente siempre tendrá el mismo resultado dado que no tiene una memoria y como únicamente depende de la percepción de la casilla en la que se encuentra, al percibir un peligro en las casillas adyacentes, se queda dando vueltas a la derecha.

El agente 2 **(basado en modelo)** tampoco logra salir con el oro sólo que éste agente sí logra subir en las columnas, llegando hasta la columna 3, sin embargo, al tener un _pit_ arriba, nuevamente entra en un bucle en el que da vueltas, puesto que éste modelo ya no tiene registro de casillas seguras, lo cual provoca que siempre esté dando vueltas a la izquierda. Se realizó el ejercicio de cambiar de lugar un _pit_ y acercarlo a la entrada, de lo cual se observa que, si el _pit_ se coloca junto a la entrada, ya sea arriba o a la derecha, el jugador se queda dando vueltas a la izquierda, esto por lo mismo de que no detecta ninguna casilla como segura.

El agente 3 **(basado en metas)** tampoco logró salir con el oro, y parece repetir el mismo patrón del agente anterior, pues se detuvo en la misma casilla (3,1) y terminó en un bucle de vueltas a la izquierda. 

El agente 4 **(basado en utilidad)** sí logró salir con el oro en 34 pasos, llegando incluso a matar al Wumpus.

El agente 5 **(de aprendizaje)** inicialmente no logró salir con el oro, pues inicia la partida e inmediatamente después escala la cueva (sin el oro), sin embargo, al incrementar el número de episodios a 3000, sí logra salir con el oro en 18 pasos y sin matar al Wumpus.

 
### Resumen
Los agentes de reflejo simple, basado en modelo y basado en metas, no logran salir con el oro. Por otro lado, los modelos basados en utilidad y de aprendizaje sí logran el objetivo, éste último lo logra al incrementar el número de episodios de entrenamiento.