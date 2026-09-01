# Ejercicio 2 — Descripción PEAS de agentes inteligentes


### 1. **Asistente virtual de voz** (p. ej. Siri, Alexa o Google Assistant en un altavoz inteligente).

- **Performance:** Precisión en tareas ejecutadas, número de correcciones solicitadas por el usuario.
- **Environment:** Sistema operativo del dispositivo. _Entorno es totalmente observable, determinista, episódico y discreto_
- **Actuators:** Capacidad de abrir aplicaciones, reproducir o pausar contenido multimedia, enviar mensajes o hacer llamadas.
- **Sensors:** Micrófono, bocina, botón de encendido y de acción.


### 2. **Robot aspirador doméstico** (p. ej. Roomba u otro robot que limpia pisos de un departamento).

- **Performance:** Porcentaje de área limpia, número de _choques_ en paredes u objetos, cantidad de intervenciones humanas, tiempo total de recorrido.
- **Environment:** Habitación para limpiar, suelo, muebles, personas o mascotas. _Entorno es parcialmente observable, determinista, episódico, dinámico y discreto._
- **Actuators:** Llantas, motor, filtros, mangueras o tuberías.
- **Sensors:** Sensor de movimiento y de objetos cercanos, cámaras, GPS.


### 3. **Sistema de recomendación de streaming** (p. ej. Netflix o Spotify que sugiere películas o canciones).

- **Performance:** Cantidad de clics realizados en la recomendación, minutos de reproducción del contenido sugerido, valoración de la sugerencia por parte del usuario.
- **Environment:** Pantalla de inicio e interfaz de reproducción de la plataforma, catálogo disponible. _Entorno es totalmente observable, estocástico, episódico, estático y discreto_
- **Actuators:** Notificaciones, vista previa de reproducción, reproducción automática al finalizar un contenido.
- **Sensors:** Historial de reproducción, calificaciones de otros usuarios con comportamiento similar, tendencias.

### 4. **Vehículo autónomo en ciudad** (conducción sin conductor en calles urbanas con tráfico y peatones).

- **Performance:** Tiepo de traslado, costo de viaje respecto a otros medios de transporte.
- **Environment:** Calles de la ciudad, semáforos, reglamento vial, condiciones climáticas, peatones y otros conductores. _Entorno es parcialmente observable, estocástico, secuencial, dinámico y continuo._
- **Actuators:** Volante, freno, acelerador, seguros de puertas.
- **Sensors:** Cámara, velocímetro, GPS.



### 5. **Agente de trading algorítmico en bolsa** (compra y venta automática de acciones en mercados financieros).

- **Performance:** Número de acciones compradas y vendidas, monto gastado, rendimiento ganado.
- **Environment:** Plataformas de _trading_, páginas web de índices de precios y cotizaciones. _Entorno es totalmente observable, estocástico, episódico, dinámico y discreto_
- **Actuators:** Botón de compra, venta y subasta de acciones.
- **Sensors:** Lista de precios y acciones, variación en los precios, horas de inciio y fin de operaciones en diferentes mercados.



### 6. **Sistema de diagnóstico médico asistido por IA** (apoya a un médico a interpretar síntomas e imágenes clínicas).

- **Performance:** Precisión del diagnóstico realizado, tiempo de respuesta, costo total del tratamiento.
- **Environment:** Paciente, síntomas descritos, médico usario del sistema. _Entorno es parcialmente observable, estocástico, secuencial, dinámico y continuo._
- **Actuators:** Emitir diagnósticos, recetas y alertas al médico.
- **Sensors:** Información proporcionada por el paciente, historial de diagnósticos previos, retroalimentación del médico.


### 7. **Dron de inspección de infraestructura** (revisa grietas, corrosión o fugas en puentes, tuberías o líneas eléctricas).

- **Performance:** Número de deficiencias detectadas, tiempo total del recorrido, exactitud en la ubicación reportada.
- **Environment:** Vía pública, edificio o infraestructura a revisar. _Entorno es parcialmente observable, estocástico, secuencial, dinámico y continuo._
- **Actuators:** Envío de notificaciones, alarma.
- **Sensors:** Cámara, termómetro, giroscopio, GPS.


### 8. **Agente jugador de ajedrez** (programa que compite contra un humano u otro agente en partidas completas).

- **Performance:** Puntos ganados por partida, cantidad de partidas ganadas, número de turnos hasta el jaque mate, nivel Elio alcanazado, piezas ganadas y perdidas.
- **Environment:** Tablero virtual, piezas del juego y oponente. _Entorno es totalmente observable, determinista, secuencial, estático y discreto._
- **Actuators:** Mover cada pieza de acuerdo con las piezas del juego.
- **Sensors:** Movimiento del oponente en tiempos anteriores, tiempo transcurrido.
