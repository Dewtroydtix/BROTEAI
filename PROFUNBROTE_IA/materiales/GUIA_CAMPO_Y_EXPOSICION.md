# Guía de campo, comprobación y exposición — PROFUNBROTE-IA

## Antes de la siembra

1. Solicitar aprobación institucional. Confirmar presupuesto ≤ S/ 50 y cuatro a seis integrantes.
2. Conseguir un lote homogéneo de semillas de rabanito, 32 recipientes comparables con drenaje, tierra vegetal y mezcla tierra-arena 1:1.
3. Etiquetar R01–R32 con la plantilla CSV. Definir día 0 y día 10. Fijar las repeticiones 4 como prueba final antes de conocer el desenlace.
4. Distribuir aleatoriamente los recipientes en el espacio; mantener comparables las condiciones ambientales y registrar incidencias. La tarea se realiza con supervisión docente.

## Registro de campo

- Cada recipiente: 5 semillas.
- Contar plántulas visibles diariamente, pero usar **solo el dato del día 10** como variable objetivo.
- Ingresar en `emergidas_dia10` un número entero de 0 a 5. No completar celdas sin observar.
- No cambiar los códigos ni los sustratos después de la siembra.
- Guardar CSV original, una copia fechada y fotografías del trabajo solo si están autorizadas.

## Verificación previa

- ¿Hay 32 recipientes, 4 profundidades, 2 sustratos y 4 repeticiones?
- ¿La columna de emergencia contiene únicamente enteros 0–5?
- ¿Las repeticiones 4 quedaron reservadas y se cumple la separación 24/8?
- ¿El entorno de desarrollo no ha utilizado datos de prueba para escoger el algoritmo?
- ¿Se distinguen las ilustraciones hipotéticas de los registros del día 10?

## Guion recomendado para 10 minutos

| Tiempo | Expositor | Contenido / demostración |
|---|---|---|
| 0:00–1:00 | Integrante 1 | Problema real: profundidad, sustrato y emergencia visible |
| 1:00–2:30 | Integrante 2 | Diseño 4 × 2 × 4 × 5; explicar la unidad experimental |
| 2:30–4:00 | Integrante 3 | E = g/n × 100 y función cuadrática de ejemplo, con rótulo HIPOTÉTICO |
| 4:00–6:00 | Integrante 4 | Mostrar Streamlit, cargar CSV real y comparar M0, M1, M2 si se obtuvieron datos |
| 6:00–7:30 | Integrante 5 (si lo hay) | Mostrar MAE, RMSE, prueba reservada y posibles errores |
| 7:30–9:00 | Integrante 6 (si lo hay) | Limitaciones, ausencia de causalidad/generalización y próximos pasos |
| 9:00–10:00 | Todo el equipo | Preguntas y evidencia documental |

Si solo hay cuatro estudiantes, distribuir las tareas adicionales entre los cuatro.

**Importante:** si al día de exposición faltan registros reales, no simulen una tabla de resultados agrícolas. Demuestren el funcionamiento del programa con las pruebas técnicas claramente etiquetadas y expliquen lo que sigue pendiente.

## Preguntas que podría formular el jurado

- ¿Por qué usar una función cuadrática y no una recta? ¿Cómo se estiman sus coeficientes?
- ¿Cuál es la diferencia entre germinación interna y emergencia visible?
- ¿Por qué 160 semillas no equivalen a 160 réplicas independientes?
- ¿Qué significa un error medio de diez puntos porcentuales?
- ¿Qué sucedería si M1 obtiene menor MAE que Random Forest?
- ¿Por qué hay ocho recipientes reservados? ¿Puede modificarse su selección después de conocer resultados?
- ¿Puede utilizarse una predicción para recomendar una profundidad de siembra en otros cultivos?

## Aportación genuina de la IA

Random Forest aprende cómo cambia el porcentaje de emergencia observado según las dos entradas, mediante árboles entrenados en Python. No existe un modelo entrenado antes de cargar los datos reales. El valor de la investigación es contrastarlo con métodos más sencillos, no demostrar forzosamente una ventaja.
