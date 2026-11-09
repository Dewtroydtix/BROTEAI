# Verificaciones del proyecto PROFUNBROTE-IA

**Estado final de esta entrega:** programa y diseño experimental preparados; no hay observaciones agrícolas.

## Comprobaciones realmente ejecutadas

- `python -m pytest pruebas -q`: **8 pruebas aprobadas**.
- `python -m compileall -q app.py modelos pruebas`: compilación sintáctica sin errores.
- Ejemplo numérico algebraico comprobado con `numpy.polyfit`: coeficientes **−100, 210, −20**, máximo **1,05 cm y 90,25 %**; el ejemplo es *hipotético*.
- Comprobación de plantilla: 32 recipientes, ocho tratamientos, cuatro repeticiones por tratamiento y 160 semillas.
- Separación fijada antes del resultado: repeticiones 1–3 (24 recipientes) entrenamiento; repetición 4 (ocho recipientes) prueba.
- Tres folds con 16 recipientes de ajuste y ocho de validación cada uno; sin solapamientos y con representación de los ocho tratamientos.
- Pruebas de entrenamiento M0/M1/M2 realizadas **solo con datos sintéticos técnicos creados por los tests**. Esos resultados no son agrícolas ni se incluyen en la plantilla real.
- Validación de porcentajes, enteros 0–5, duplicados y sustratos, dominio del simulador [0,5; 2,0] cm y salidas acotadas a 0–100 %.
- Documento Word renderizado a once páginas para revisión visual.

## Verificación no realizada en este entorno

No fue posible instalar el paquete `streamlit` en el entorno de ejecución disponible, por lo que **no se ha probado la interfaz gráfica en un navegador ni se ha desplegado en Streamlit Cloud**. El código `app.py` fue comprobado sintácticamente y las funciones de cálculo se probaron con `pytest`. El README especifica cómo desplegarlo. Tras instalar dependencias, se debe realizar una comprobación manual de las ocho pantallas y botones de descarga.

## Verificaciones pendientes tras la siembra

- CSV con 32 valores reales de emergencia al día 10.
- Ajustes finales de M0, M1, M2 y resultados MAE/RMSE sobre ocho recipientes reservados.
- Determinación de la hipótesis H1 (reducción de MAE de al menos cinco puntos porcentuales).
- Sustentación del equipo y evidencia de campo.

Ningún resultado académico de emergencia debe reportarse como real antes de observarlo.
