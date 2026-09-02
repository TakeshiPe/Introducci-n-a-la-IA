# Ejercicio 2 — Descripción PEAS de agentes inteligentes


### 1. **Asistente virtual de voz** (p. ej. Siri, Alexa o Google Assistant en un altavoz inteligente).

- **Performance:** Precisión en tareas ejecutadas, número de correcciones solicitadas por el usuario.
- **Environment:** Sistema operativo del dispositivo, aplicaciones de reproducción de video o música. _Entorno es totalmente observable, determinista, episódico, estático y discreto_
- **Actuators:** Capacidad de abrir aplicaciones, reproducir o pausar contenido multimedia, enviar mensajes o hacer llamadas.
- **Sensors:** Micrófono, bocina, botón de encendido y de acción.

Se clasifica al entorno como totalmente observable, porque el asistente conoce por completo al sistema operativo y a las aplicaciones a las que accede, determinista porque su única acción es realizar lo que el usuario pida, episódico porque la acción que ejecute no repercute en eventos futuros, estático porque no cambia mientras se decide qué acción realizar y discreto porque el número de acciones que puede ejecutar, aunque es grande, es limitado.

### 2. **Robot aspirador doméstico** (p. ej. Roomba u otro robot que limpia pisos de un departamento).

- **Performance:** Porcentaje de área limpia, número de _choques_ en paredes u objetos, cantidad de intervenciones humanas, tiempo total de recorrido.
- **Environment:** Habitación para limpiar, suelo, muebles, personas o mascotas. _Entorno es parcialmente observable, determinista, episódico, estático y discreto._
- **Actuators:** Llantas, motor, filtros, mangueras o tuberías.
- **Sensors:** Sensor de movimiento y de objetos cercanos, cámaras, GPS.

Se clasifica al entorno como parcialmente observable porque el agente no observa la totalidad de la habitación al mismo tiempo, determinista porque del agente depende si se limpia o no, episódico porque el hecho de limpiar no afecta el estado futuro de la habitación, estático porque el entorno no cambia mientras el agente decide su acción y discreto porque la cantidad de acciones que puede ejecutar es limitada.

### 3. **Sistema de recomendación de streaming** (p. ej. Netflix o Spotify que sugiere películas o canciones).

- **Performance:** Cantidad de clics realizados en la recomendación, minutos de reproducción del contenido sugerido, valoración de la sugerencia por parte del usuario.
- **Environment:** Pantalla de inicio e interfaz de reproducción de la plataforma, catálogo disponible. _Entorno es totalmente observable, estocástico, secuencial, dinámico y discreto_
- **Actuators:** Notificaciones, vista previa de reproducción, reproducción automática al finalizar un contenido.
- **Sensors:** Historial de reproducción, calificaciones de otros usuarios con comportamiento similar, tendencias.

Se clasifica al entorno como totalmente observable porque el agente conoce en su totalidad el catálogo de la plataforma, estocástico porque basado la recomendación hecha puede o no ser seleccionada, secuencial porque con base en la interacción que tenga el usuario con la recomendación se puede cambiar recomendaciones futuras, dinámico porque conforme el usuario elige, las tendencias o listas pueden dejar de estar disponibles y discreto porque las recomendaciones que puede hacer son limitadas.

### 4. **Vehículo autónomo en ciudad** (conducción sin conductor en calles urbanas con tráfico y peatones).

- **Performance:** Tiepo de traslado, costo de viaje respecto a otros medios de transporte.
- **Environment:** Calles de la ciudad, semáforos, reglamento vial, condiciones climáticas, peatones y otros conductores. _Entorno es parcialmente observable, estocástico, secuencial, dinámico y continuo._
- **Actuators:** Volante, freno, acelerador, seguros de puertas.
- **Sensors:** Cámara, velocímetro, GPS.

Se clasifica al entorno como parcialmente observable porque el vehículo sólo puede percibir lo que tiene en sus inmediaciones, estocástico porque no existe certeza en el resultado que se tendrá dadas las decisiones que tome el agente, secuencial porque cada una de las acciones impactan en el entorno futuro, dinámico porque los partícipes del entorno no esperan a que el agente actúe y continuo porque las acciones no pueden medirse en un número finito (velocidad, por ejemplo).


### 5. **Agente de trading algorítmico en bolsa** (compra y venta automática de acciones en mercados financieros).

- **Performance:** Número de acciones compradas y vendidas, monto gastado, rendimiento ganado.
- **Environment:** Plataformas de _trading_, páginas web de índices de precios y cotizaciones. _Entorno es totalmente observable, estocástico, secuencial, dinámico y continuo_
- **Actuators:** Botón de compra, venta y subasta de acciones.
- **Sensors:** Lista de precios y acciones, variación en los precios, horas de inciio y fin de operaciones en diferentes mercados.

Se clasifica al entorno como totalmente observable porque el agente tiene a su disposición la totalidad de sitios web y acciones que pueden comprarse y venderse, estocástico porque el comprar o no cierta acción está asociada a la probabilidad de que se tenga una ganancia o una pérdida, secuencial porque la decisión de compra puede afectar en el volumen disponible y en los precios de compraventa, dinámico porque el valor de las acciones cambia prácticamente cada segundo por factores no atribuibles al agente y continuo porque el rendimiento y las variaciones en los precios son medibles con números fraccionados. 


### 6. **Sistema de diagnóstico médico asistido por IA** (apoya a un médico a interpretar síntomas e imágenes clínicas).

- **Performance:** Precisión del diagnóstico realizado, tiempo de respuesta, costo total del tratamiento.
- **Environment:** Paciente, síntomas descritos, médico usario del sistema. _Entorno es parcialmente observable, estocástico, secuencial, dinámico y continuo._
- **Actuators:** Emitir diagnósticos, recetas y alertas al médico.
- **Sensors:** Información proporcionada por el paciente, historial de diagnósticos previos, retroalimentación del médico.

Se clasifica al entorno como parcialmente observable porque el agente se limita a conocer los síntomas que le proporcionan médico y paciente, pero no puede conocer la totalidad del organismo del paciente, estocástico porque no existe certeza en que los síntomas correspondan al diagnóstico realizado, secuencial porque el tratamiento afecta al estado de salud futuro del paciente, dinámico porque la salud del paciente mejora o empeora independientemente de las acciones que haga el agente y continuo porque el agente opera con rangos de precisión.

### 7. **Dron de inspección de infraestructura** (revisa grietas, corrosión o fugas en puentes, tuberías o líneas eléctricas).

- **Performance:** Número de deficiencias detectadas, tiempo total del recorrido, exactitud en la ubicación reportada.
- **Environment:** Vía pública, edificio o infraestructura a revisar. _Entorno es parcialmente observable, estocástico, secuencial, dinámico y continuo._
- **Actuators:** Envío de notificaciones, alarma.
- **Sensors:** Cámara, termómetro, giroscopio, GPS.

Se clasifica al entorno como parcialmente observable porque la visión del dron se limita a lo que tenga en su alrededor inmediato, estocástico porque puede dar lugar a falsos positivos o confusión en las alertas, secuencial porque las acciones del agente pueden detonar en el estado futuro de la edificación (una alerta provoca que se hagan las reparaciones pertinentes, por ejemplo). Dinámico porque el edificio se deteriora independientemente de que el agente actúe o no y continuo porque el agente maneja coordenadas y proporciones que requieren de una mayor proporción.

### 8. **Agente jugador de ajedrez** (programa que compite contra un humano u otro agente en partidas completas).

- **Performance:** Puntos ganados por partida, cantidad de partidas ganadas, número de turnos hasta el jaque mate, nivel Elio alcanazado, piezas ganadas y perdidas.
- **Environment:** Tablero virtual, piezas del juego y oponente. _Entorno es totalmente observable, determinista, secuencial, estático y discreto._
- **Actuators:** Mover cada pieza de acuerdo con las piezas del juego.
- **Sensors:** Movimiento del oponente en tiempos anteriores, tiempo transcurrido.

Se clasifica al entorno como totalmente observable porque el agente en todo momento ve cómo está el tablero, determinista porque el siguiente estado depende del actual y del movimiento que haga el agente, secuencial porque el movimiento afecta el desarrollo futuro del juego, estático porque (en partidas sin tiempo), el tablero no se ve afectado hasta que el jugador haga su movimiento y discreto porque, a pesar de existir millones de combinaciones de partidas y movimientos, el número es discreto y finito. 