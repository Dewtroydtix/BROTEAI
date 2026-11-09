# PROFUNBROTE-IA — Resumen institucional (para una página)

**Categoría B.** Álgebra aplicada. **Modalidad:** Modelización y optimización. **Integrantes:** cuatro a seis estudiantes. **Presupuesto:** S/ 40 de materiales base; máximo estimado S/ 48.

**Problema.** La profundidad de siembra y la composición del sustrato pueden modificar la proporción de semillas de rabanito que llegan a producir plántulas visibles. Se investigará si la IA puede estimar esa proporción a partir de un experimento escolar con mejores resultados que un promedio general.

**Pregunta.** ¿Random Forest reduce al menos cinco puntos porcentuales el MAE respecto del promedio de entrenamiento sobre ocho recipientes reservados?

**Fundamentación matemática.** E = (plántulas emergidas / semillas sembradas) × 100 %. M1 será una función Ê(d,s) = β₀ + β₁d + β₂d² + β₃s. Se comparará con el promedio M0 y el bosque aleatorio de regresión M2 mediante MAE y RMSE.

**Metodología.** Cuatro profundidades (0,5; 1,0; 1,5; 2,0 cm), dos sustratos y cuatro repeticiones: 32 recipientes con cinco semillas cada uno (160 semillas). Las repeticiones 1–3 de cada tratamiento formarán el conjunto de entrenamiento (24); la repetición 4 quedará como prueba final (8). La variable objetivo será la emergencia visible al décimo día, registrada en un CSV.

**Producto.** Aplicación Streamlit Cloud con registro, validación, modelos, gráficos, simulación de escenarios y exportación CSV. No entrena mientras falten resultados reales completos.

**Estado:** herramienta y diseño preparados, resultados experimentales **pendientes**. No se incluyen mediciones ficticias.
