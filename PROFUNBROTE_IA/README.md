# PROFUNBROTE-IA — EXPOMATEMÁTICA JUANPABLINA 2026

**Categoría B · Álgebra aplicada · Modelización y optimización · Presupuesto máximo S/ 50.**

## Estado y principio de integridad científica

Este paquete es un **instrumento preparado para la investigación real**. No contiene porcentajes de emergencia observados ni modelos entrenados con datos agrícolas reales. La plantilla CSV tiene 32 recipientes y el campo `emergidas_dia10` vacío. El programa no permitirá entrenar sin cargar las 32 observaciones completas y declarar su procedencia experimental.

El gráfico parabólico de tres puntos del informe y la pantalla «Álgebra aplicada» son **ejemplos hipotéticos**. Los resultados de pruebas unitarias con datos sintéticos son **verificaciones de software**, no resultados de emergencia ni evidencia de H1.

## 1. Archivos principales

```
PROFUNBROTE_IA/
├── app.py                               # aplicación Streamlit
├── requirements.txt                     # dependencias Python
├── README.md                            # estas instrucciones
├── PROFUNBROTE_IA_INFORME_15_APARTADOS_EDITABLE.docx
├── modelos/
│   ├── __init__.py
│   └── funciones.py                      # validación, M0/M1/M2, CV, métricas
├── datos/
│   └── plantilla_experimental_32_recipientes.csv
├── pruebas/
│   └── test_modelos.py                  # casos sintéticos de verificación
└── materiales/
    ├── GUIA_CAMPO_Y_EXPOSICION.md
    ├── RESUMEN_1_PAGINA.md
    ├── MATERIAL_STAND_A4.html
    └── GRAFICO_EJEMPLO_HIPOTETICO.png
```

## 2. Ejecutar localmente (opcional)

Se requiere Python compatible con los paquetes de requirements.txt.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

El navegador abrirá una dirección local, habitualmente `http://localhost:8501`.

## 3. Desplegar en Streamlit Community Cloud

La aplicación no necesita claves de API ni servicios externos de IA.

1. Cree un repositorio en GitHub (puede ser privado si su configuración de Streamlit lo permite) y suba los archivos desde **el interior de la carpeta** `PROFUNBROTE_IA` a la raíz del repositorio, conservando la carpeta `modelos/`.
2. Compruebe que `app.py` y `requirements.txt` están juntos en la raíz.
3. Acceda a https://share.streamlit.io y seleccione **Create app**.
4. Elija **Yup, I have an app**, su repositorio, rama y ruta `app.py`.
5. Despliegue. Streamlit instalará las dependencias declaradas.
6. Abra la aplicación y descargue la plantilla de CSV. La app mostrará que no existen observaciones hasta que se carguen.

Documentación oficial: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## 4. Recolectar los datos

- Ocho tratamientos: 4 profundidades (0,5; 1,0; 1,5; 2,0 cm) × 2 sustratos (tierra vegetal, mezcla tierra-arena 1:1).
- Cuatro repeticiones por tratamiento: **32 recipientes**.
- Cinco semillas por recipiente: **160 semillas**.
- Día 0: siembra. **Día 10: cuenta de plántulas visibles**, un entero de 0 a 5 por recipiente.
- Registren fechas e incidencias, no nombres personales. Mantengan comparables el origen de semillas, recipientes, iluminación y manejo de humedad; organicen las ubicaciones aleatoriamente y supervisen el procedimiento.
- Se reservan **las repeticiones 4** de cada tratamiento para la prueba final. No miren ni utilicen sus resultados para escoger el algoritmo.

**No introduzcan valores simulados en el CSV de los resultados reales.**

## 5. Comparación de modelos y métricas

- M0: media del entrenamiento.
- M1: regresión lineal con variables `d`, `d²`, `s` (función cuadrática en la profundidad).
- M2: bosque aleatorio de regresión; 120 árboles, profundidad máxima 3, mínimo 2 recipientes por hoja, semilla 20261109.
- Ajuste: 24 recipientes (repeticiones 1–3 de cada tratamiento). Validación cruzada: tres folds, con 16 recipientes para ajustar y ocho para validar por fold, balanceados por tratamiento.
- Prueba independiente: ocho recipientes de repetición 4.
- Métricas: error absoluto medio (MAE) y raíz del error cuadrático medio (RMSE), ambos en **puntos porcentuales**.
- H1 se apoya descriptivamente si `MAE(M0) − MAE(M2) ≥ 5 p.p.` en el conjunto reservado. Una muestra de ocho unidades puede ser inestable: el criterio no demuestra superioridad general.

## 6. Pruebas informáticas

```bash
python -m pytest pruebas -q
python -m compileall -q app.py modelos pruebas
```

Las pruebas crean un conjunto **sintético y claramente señalado como técnico**, no se exporta como si fuera un registro de estudiantes o de una cosecha real.

## 7. Limitaciones importantes

- Con cinco semillas por recipiente, los porcentajes observados son múltiplos de 20. Las predicciones pueden ser intermedias.
- Los ocho registros de prueba constituyen una muestra muy pequeña.
- La predicción no valida recomendaciones de siembra ni generaliza a otros cultivos, sustratos, variedades o temporadas.
- Los datos de los CSV subidos a Streamlit Cloud se procesan en el servidor; eviten nombres personales y datos sensibles.
- Las imágenes del ejemplo hipotético deben conservar dicha indicación durante la exposición.

## 8. Presupuesto

S/ 40 de materiales base y hasta S/ 8 de contingencia; total máximo estimado S/ 48 (dentro de S/ 50). Precios pendientes de cotización. No comprar antes de la aprobación del comité.

## 9. Fuentes

- Bases institucionales EXPOMATE 2026 (archivo proporcionado).
- https://www.udel.edu/academics/colleges/canr/cooperative-extension/fact-sheets/radishes/
- https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
