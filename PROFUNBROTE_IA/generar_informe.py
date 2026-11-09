"""Genera el informe académico editable de quince apartados. Requiere python-docx y matplotlib."""
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'PROFUNBROTE_IA_INFORME_15_APARTADOS_EDITABLE.docx'
D=Document()
sec=D.sections[0]
sec.page_width,sec.page_height=Cm(21),Cm(29.7)
sec.top_margin=Cm(2.1); sec.bottom_margin=Cm(2.1); sec.left_margin=Cm(2.65); sec.right_margin=Cm(2.45)
sec.header_distance=Cm(.9); sec.footer_distance=Cm(.9)
styles=D.styles
normal=styles['Normal']; normal.font.name='Times New Roman'; normal.font.size=Pt(12); normal.font.color.rgb=RGBColor(34,44,40)
normal.paragraph_format.line_spacing=2.0
normal.paragraph_format.space_after=Pt(5)
normal.paragraph_format.first_line_indent=Cm(.6)
for name,size in [('Title',18),('Heading 1',13),('Heading 2',12)]:
    s=styles[name]; s.font.name='Times New Roman'; s.font.size=Pt(size); s.font.bold=True; s.font.color.rgb=RGBColor(19,76,63)
    s.paragraph_format.space_before=Pt(14 if name=='Heading 1' else 8)
    s.paragraph_format.space_after=Pt(5)
    s.paragraph_format.keep_with_next=True
    s.paragraph_format.line_spacing=1.2
header=sec.header.paragraphs[0]; header.text='IEP JUAN PABLO PEREGRINO   ·   EXPOMATEMÁTICA JUANPABLINA 2026'
header.style='Normal'; header.alignment=WD_ALIGN_PARAGRAPH.CENTER
header.paragraph_format.first_line_indent=Cm(0); header.paragraph_format.line_spacing=1
for run in header.runs: run.font.size=Pt(8); run.font.bold=True; run.font.color.rgb=RGBColor(66,98,90)
foot=sec.footer.paragraphs[0]; foot.text='PROFUNBROTE-IA  |  Investigación escolar con datos reales por recolectar  |  '
foot.paragraph_format.first_line_indent=Cm(0); foot.paragraph_format.line_spacing=1
foot.alignment=WD_ALIGN_PARAGRAPH.RIGHT
for run in foot.runs: run.font.size=Pt(8); run.font.color.rgb=RGBColor(96,96,96)
fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); foot._p.append(fld)

def paragraph(text='',style=None,indent=True):
    p=D.add_paragraph(style=style)
    p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
    if not indent: p.paragraph_format.first_line_indent=Cm(0)
    p.add_run(str(text))
    return p

def h(number,title):
    D.add_heading(f'{number}. {title}',level=1)

def sub(title):D.add_heading(title,level=2)

def bullets(items):
    for t in items:
        p=D.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent=Cm(.7)
        p.paragraph_format.first_line_indent=Cm(-.3)
        p.paragraph_format.line_spacing=1.5
        p.add_run(t)

def table(headers, rows, widths=None):
    t=D.add_table(rows=1,cols=len(headers)); t.style='Table Grid';t.alignment=WD_TABLE_ALIGNMENT.CENTER
    for i,v in enumerate(headers):t.rows[0].cells[i].text=str(v)
    for values in rows:
        cells=t.add_row().cells
        for i,v in enumerate(values):cells[i].text=str(v)
    for ridx,row in enumerate(t.rows):
        for cell in row.cells:
            cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing=1.05;p.paragraph_format.space_after=Pt(2);p.paragraph_format.space_before=Pt(2);p.paragraph_format.first_line_indent=Cm(0)
                for r in p.runs:
                    r.font.name='Times New Roman';r.font.size=Pt(9.5)
                    if ridx==0:r.font.bold=True;r.font.color.rgb=RGBColor(255,255,255)
            if ridx==0:
                tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),'185847'); tcPr.append(shd)
    return t

def eq(t):
    p=D.add_paragraph()
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent=Cm(0);p.paragraph_format.line_spacing=1.2;p.paragraph_format.space_before=Pt(6);p.paragraph_format.space_after=Pt(6)
    r=p.add_run(t);r.font.name='Cambria Math';r.font.size=Pt(12);r.bold=True
    return p

# Portada sin numeración de apartado adicional
p=D.add_paragraph();p.style='Title';p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.first_line_indent=Cm(0);p.add_run('PROFUNBROTE-IA')
p=D.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.first_line_indent=Cm(0);r=p.add_run('Predicción de la emergencia temprana del rabanito mediante funciones cuadráticas y aprendizaje automático');r.bold=True;r.font.size=Pt(13)
p=D.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.first_line_indent=Cm(0);p.add_run('INFORME ACADÉMICO · 15 APARTADOS OFICIALES · EDICIÓN PARA COMPLETAR CON DATOS REALES')
table(['Institución','Categoría / modalidad','Área','Presupuesto'],[['I.E.P. Juan Pablo Peregrino','B · Modelización y optimización','Álgebra aplicada','Hasta S/ 50']])
paragraph('ESTADO DEL PROYECTO: software y metodología preparados; la emergencia al décimo día debe observarse experimentalmente. Ningún porcentaje de plántulas emergidas se considera medido antes del registro de campo.',indent=False)

h(1,'Título del proyecto e integrantes')
paragraph('Título: PROFUNBROTE-IA: Modelación algebraica y predicción de la emergencia de semillas de rabanito según profundidad de siembra y sustrato.')
paragraph('Institución: I.E.P. Juan Pablo Peregrino. Categoría: B (3.º–5.º de secundaria). Modalidad: Modelización y optimización. Competencia matemática principal: Resuelve problemas de regularidad, equivalencia y cambio.')
table(['Integrante','Apellidos y nombres','Grado / sección'],[(str(i),'.............................................................','.......................') for i in range(1,7)])
paragraph('Participan entre cuatro y seis estudiantes bajo asesoría docente. Completar únicamente las filas correspondientes a integrantes reales.')
paragraph('Asesor: ...................................................... Fecha de entrega: ...................................')

h(2,'Planteamiento del problema y justificación')
paragraph('En una siembra experimental, no todas las semillas producen plántulas visibles sobre la superficie. La profundidad y la composición del sustrato pueden influir en esta emergencia. En contextos escolares suele explicarse el fenómeno con afirmaciones cualitativas, sin construir una función ni medir el error de sus predicciones.')
paragraph('Problema investigable: estimar el porcentaje de emergencia visible al décimo día de semillas de rabanito, utilizando profundidad de siembra (0,5; 1,0; 1,5; 2,0 cm) y tipo de sustrato (tierra vegetal o mezcla 1:1 de tierra y arena). El proyecto limita el análisis a estas condiciones: no pretende predecir cosecha ni rendimiento comercial.')
paragraph('Pregunta principal: ¿el modelo Random Forest (M2) reduce el error absoluto medio respecto del promedio de entrenamiento (M0) al estimar el porcentaje de emergencia en ocho recipientes reservados?')
paragraph('Hipótesis H1: el MAE de M2 será al menos cinco puntos porcentuales menor que el MAE de M0. Hipótesis H0: la reducción será inferior a cinco puntos porcentuales. Se comparará además con la regresión cuadrática M1, sin presuponer superioridad de la IA.')
paragraph('Justificación: el proyecto hace observable la relación entre sistemas de ecuaciones, funciones cuadráticas, mínimos cuadrados, toma de datos, predicción y evaluación crítica de algoritmos, mediante una experiencia agrícola escolar de bajo costo.')

h(3,'Objetivo general y objetivos específicos')
paragraph('Objetivo general: construir y evaluar modelos algebraicos y de aprendizaje automático que estimen la emergencia visible de rabanito al décimo día, a partir de datos experimentales obtenidos por estudiantes.')
bullets(['Diseñar ocho tratamientos y cuatro repeticiones independientes por tratamiento.','Registrar número de semillas sembradas y plántulas emergidas para cada recipiente.','Calcular porcentajes y formular modelos de regresión algebraica cuadrática.','Entrenar RandomForestRegressor únicamente con observaciones reales completas.','Comparar M0, M1 y M2 mediante MAE y RMSE en una prueba reservada.','Construir un simulador Streamlit que explique fórmulas, errores y limitaciones.','Comunicar los resultados sin inventar datos ni extrapolar fuera del intervalo observado.'])

h(4,'Competencia principal')
paragraph('Competencia principal CNEB: «Resuelve problemas de regularidad, equivalencia y cambio». El estudiante traduce variables a expresiones algebraicas, comunica relaciones de cambio, utiliza métodos para resolver sistemas y justifica afirmaciones a partir del comportamiento de funciones.')
paragraph('Competencia complementaria: «Resuelve problemas de gestión de datos e incertidumbre», presente en la organización de registros, lectura de gráficos, cálculo e interpretación de medidas de error y consideración de la variabilidad experimental.')
paragraph('Evidencias esperadas: funciones editables, ejemplo resuelto, matriz de datos completa, pruebas matemáticas, comparación de predicciones con observaciones y sustentación oral de errores y límites del modelo.')

h(5,'Fundamentación teórica y matemática')
sub('Variables y unidades')
table(['Símbolo','Definición','Unidad / dominio'],[
('d','Profundidad de siembra','cm; 0,5 / 1,0 / 1,5 / 2,0'),('s','Sustrato codificado','0 = tierra; 1 = mezcla'),
('n','Semillas sembradas por recipiente','5 unidades'),('g','Plántulas emergidas al día 10','entero de 0 a 5'),
('E','Emergencia observada','%'),('Ê','Emergencia predicha','%')])
sub('Porcentaje de emergencia')
eq('E = (g / n) × 100 %')
paragraph('Cada recipiente contiene cinco semillas. Por eso, los valores observados por recipiente solo podrán ser 0 %, 20 %, 40 %, 60 %, 80 % o 100 %. La predicción de los modelos puede ser intermedia porque estima un promedio. Un porcentaje de emergencia visible no equivale a germinación interna.')
sub('Función algebraica M1')
eq('Ê(d,s) = β₀ + β₁d + β₂d² + β₃s')
paragraph('Los parámetros β se estimarán por mínimos cuadrados usando exclusivamente los 24 recipientes de entrenamiento. La suma de cuadrados a minimizar es Σ(Eᵢ − Êᵢ)². Para interpretar físicamente las salidas, se limitarán las predicciones al intervalo [0, 100] %.')
sub('Ejemplo resuelto, estrictamente hipotético')
table(['Profundidad (cm)','Emergencia ilustrativa (%)'],[('0,5','60'),('1,0','90'),('1,5','70')])
paragraph('Los tres pares son ejemplos inventados, no datos de los 32 recipientes del proyecto. Sea E(d) = ad² + bd + c. Se plantea: 0,25a + 0,5b + c = 60; a + b + c = 90; 2,25a + 1,5b + c = 70. Al resolver, a = −100, b = 210 y c = −20.')
eq('E(d) = −100d² + 210d − 20')
paragraph('El vértice está en d* = −b/(2a) = 1,05 cm. Su valor es E(1,05) = 90,25 %. Esta conclusión pertenece solo a la función ilustrativa y no representa la profundidad agronómica recomendada para el rabanito.')
# toy graph
x=np.linspace(0.5,1.5,151);y=-100*x*x+210*x-20
fig,ax=plt.subplots(figsize=(6.9,3.0));ax.plot(x,y,label='Curva didáctica hipotética');ax.scatter([.5,1,1.5],[60,90,70],label='Tres valores inventados');ax.set_xlabel('Profundidad (cm)');ax.set_ylabel('Porcentaje de emergencia (%)');ax.set_ylim(50,100);ax.grid(alpha=.23);ax.legend(fontsize=8)
fig.text(0.5,.98,'EJEMPLO HIPOTÉTICO — NO SON DATOS DEL EXPERIMENTO',ha='center',va='top',fontsize=9)
fig.tight_layout(rect=[0,0,1,.93]);art=ROOT/'materiales'/'GRAFICO_EJEMPLO_HIPOTETICO.png';fig.savefig(art,dpi=160);plt.close(fig)
p=D.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.first_line_indent=Cm(0);p.add_run().add_picture(str(art),width=Cm(14.7))

h(6,'Aplicación de inteligencia artificial')
paragraph('El modelo M2 utiliza RandomForestRegressor de scikit-learn: un conjunto de árboles de regresión entrenados con pares (profundidad, sustrato) y porcentajes observados. Cada árbol predice un valor y el bosque promedia las salidas. No se trata de una IA generativa, y no se dispone de un modelo preentrenado hasta recolectar observaciones.')
eq('Ê_RF(d,s) = (1 / B) × Σ T_b(d,s)')
paragraph('Parámetros prefijados: B = 120 árboles, profundidad máxima 3, mínimo 2 recipientes por hoja, semilla aleatoria 20261109. Se limitan la complejidad y la extrapolación. No se utilizará el conjunto de prueba final para seleccionar parámetros.')
table(['Modelo','Naturaleza','Entradas','Resultado'],[
('M0','Promedio del entrenamiento','Ninguna variable explicativa','Porcentaje medio'),
('M1','Regresión cuadrática','d, d², s','Porcentaje estimado'),
('M2','Bosque aleatorio','d, s','Porcentaje estimado')])
paragraph('Diferencia entre datos y simulación: la aplicación usa datos reales únicamente cuando el usuario carga las 32 observaciones completas y confirma su procedencia. Los ejemplos hipotéticos están separados en la pantalla Álgebra; nunca se emplean para entrenar el modelo destinado a evaluar H1.')

h(7,'Metodología y procedimientos')
sub('Diseño factorial')
paragraph('Variables explicativas: profundidad de siembra con cuatro niveles (0,5; 1,0; 1,5; 2,0 cm) y sustrato con dos niveles (tierra vegetal y mezcla de tierra y arena 1:1 por volumen). Se usarán cuatro repeticiones por tratamiento: 4 × 2 × 4 = 32 recipientes. Se sembrarán cinco semillas por recipiente: 160 semillas.')
table(['Profundidad (cm)','Tierra vegetal','Mezcla tierra-arena 1:1'],[(str(d).replace('.',','),'4 recipientes × 5 semillas','4 recipientes × 5 semillas') for d in [.5,1.,1.5,2.]])
sub('Procedimiento de campo')
bullets(['Solicitar aprobación del comité y asesor antes de comprar o plantar.','Rotular los 32 recipientes R01–R32 según la plantilla; prever drenaje y recipientes comparables.','Distribuir los recipientes aleatoriamente dentro del espacio de cultivo, registrando su ubicación sin datos personales.','Utilizar un solo lote de semillas, un criterio uniforme de observación y un procedimiento de humedad comparable. Registrar incidencias, sin cambiar las etiquetas de tratamientos.','Anotar fecha de siembra (día 0). Registrar observaciones diarias; al décimo día contar las plántulas visibles por recipiente.','Transcribir g = 0…5 al CSV, confirmar exactitud y mantener un respaldo local fechado.','Reservar de antemano la repetición 4 de cada tratamiento (8 recipientes) para prueba final. Las otras 24 se emplearán en entrenamiento y validación interna.'])
sub('Validación interna y externa')
paragraph('En el entrenamiento se ejecutarán tres folds balanceados por tratamiento: cada fold ajusta modelos con 16 recipientes y los valida en los ocho restantes, uno por tratamiento. Después se ajustan los tres modelos con los 24 recipientes completos y se obtienen predicciones sobre los ocho recipientes reservados, nunca usados en entrenamiento.')
paragraph('Los cinco granos de un mismo recipiente no se considerarán observaciones independientes. La unidad experimental es el recipiente.')

h(8,'Materiales, recursos y presupuesto')
table(['Material / recurso','Procedencia prevista','Costo estimado'],[
('Semillas de rabanito (≥160)','Vivero o comercio agrícola','S/ 8'),
('Tierra vegetal','Vivero','S/ 12'),('Arena lavada','Proveedor local','S/ 5'),
('32 recipientes reutilizados','Hogar/colegio','S/ 0'),
('Etiquetas y cinta','Librería','S/ 3'),('Cartulinas','Librería','S/ 6'),
('Impresión de gráficos','Imprenta local','S/ 6'),
('Python / Streamlit / scikit-learn','Software gratuito','S/ 0'),
('Subtotal','','S/ 40'),('Contingencia opcional','','Hasta S/ 8'),('Máximo previsto','','S/ 48')])
paragraph('El presupuesto no incluye compra de computadora ni acceso de datos móviles; se presupone equipo escolar y acceso existente para desplegar en Streamlit Community Cloud. Los precios son estimados y deben cotizarse. Las bases requieren autorización del comité antes de la compra de materiales.')

h(9,'Desarrollo e implementación del proyecto')
paragraph('El producto se entregará como una aplicación Python desplegable en Streamlit Cloud, con archivos app.py, requirements.txt, modelos/funciones.py, datos/plantilla_experimental_32_recipientes.csv, pruebas/test_modelos.py, README.md y recursos para la exposición.')
paragraph('Secciones de la interfaz: Inicio, Diseño experimental, Registro y validación, Álgebra aplicada, Entrenamiento y comparación, Simulador de escenarios, Pruebas técnicas y Referencias. La plantilla contiene cuatro profundidades, dos tipos de sustrato y cuatro repeticiones sin resultados precargados.')
paragraph('El archivo CSV no se entrena si faltan resultados del día 10, si hay recipientes duplicados, profundidades fuera de dominio, sustratos erróneos, recuentos no enteros o combinaciones incompletas. El operador debe confirmar que las observaciones proceden de la experimentación. Cuando el archivo cambia, los modelos de la sesión se invalidan y deben volver a entrenarse.')
paragraph('Los tres modelos se evalúan con la misma separación de datos. Los archivos CSV exportados incluyen resultados calculados a partir de las observaciones realmente cargadas. La aplicación no guarda automáticamente información de participantes en una base externa; los datos subidos permanecen en la sesión del servidor.')

h(10,'Resultados y análisis matemático')
sub('Resultados técnicos obtenidos — no agrícolas')
paragraph('Se ejecutó la batería de ocho pruebas automatizadas del proyecto con el comando python -m pytest pruebas -q. Las ocho pruebas pasaron: plantilla vacía, restricciones, 32 recipientes y 160 semillas, separación 24/8, validación interna sin recipientes compartidos, ejemplo cuadrático, entrenamiento únicamente tras pasar datos completos de prueba técnica y predicción restringida al dominio.')
paragraph('El ensayo de ejecución del entrenador se realizó con un conjunto SINTÉTICO construido para comprobación del código. Sus valores no representan emergencia real ni evidencia de la hipótesis agrícola. Los resultados de ese ensayo no se incorporan como observaciones experimentales.')
sub('Resultados agrícolas pendientes')
table(['Indicador','M0','M1','M2'],[
('MAE en 8 recipientes','PENDIENTE','PENDIENTE','PENDIENTE'),
('RMSE en 8 recipientes','PENDIENTE','PENDIENTE','PENDIENTE'),
('Reducción de MAE frente a M0','—','PENDIENTE','PENDIENTE')])
paragraph('La tabla solo se completará después de la observación del décimo día, la carga del CSV y el entrenamiento real. No se incluyen porcentajes de emergencia ni conclusiones predictivas no observadas.')

h(11,'Comprobación y validación de resultados')
eq('MAE = (1/n) × Σ |Eᵢ − Êᵢ|')
eq('RMSE = √[(1/n) × Σ (Eᵢ − Êᵢ)²]')
paragraph('Ambas métricas se expresan en puntos porcentuales. Cada predicción se compara con el resultado observado en su mismo recipiente. La variable principal de H1 es R = MAE(M0) − MAE(M2); el criterio predefinido es R ≥ 5 puntos porcentuales sobre los ocho recipientes de prueba final.')
paragraph('Se reportarán también MAE(M1), errores por recipiente, las tres particiones de validación interna, el código de la semilla aleatoria y las diferencias por tratamiento. La prueba de ocho recipientes es pequeña y no autoriza a generalizar la eficacia del modelo a otras semillas, sustratos o temporadas.')
sub('Controles metodológicos')
bullets(['No usar datos del conjunto de prueba en el ajuste, la selección de variables ni la elección de hiperparámetros.','Mantener fija la repetición 4 de cada tratamiento como prueba, con decisión previa a las observaciones.','Documentar todos los datos faltantes o incidencias; no completar con estimaciones ni reemplazar sin constancia.','Corroborar resultados aritméticos con cálculos manuales o independientes y mantener las unidades visibles.','Evitar usar la predicción máxima de una función como recomendación agronómica fuera del dominio experimental.'])

h(12,'Limitaciones y propuestas de mejora')
paragraph('La variable de respuesta tiene resolución de 20 puntos porcentuales, pues cada recipiente tiene cinco semillas; ello genera incertidumbre considerable. Treinta y dos recipientes y ocho observaciones de prueba son adecuados como exploración escolar, pero insuficientes para conclusiones agrícolas generales.')
paragraph('Las condiciones de luz, temperatura, humedad, heterogeneidad del sustrato y calidad de las semillas pueden afectar la emergencia y no están incluidas en el modelo. La función cuadrática puede predecir valores fuera de 0–100 %, por eso se acota la visualización. Random Forest puede sobreajustar y tampoco extrapola de forma confiable.')
paragraph('Mejoras futuras: repetir el experimento en diferentes fechas, ampliar la cantidad de recipientes por tratamiento, medir variables ambientales con instrumentos apropiados y evaluar tasas de emergencia por día, conservando registros de replicación.')

h(13,'Conclusiones y recomendaciones')
paragraph('Conclusiones que sí se sustentan en la etapa actual: (i) el diseño experimental comprende ocho tratamientos, 32 recipientes y 160 semillas; (ii) el porcentaje de emergencia y la regresión cuadrática pueden calcularse y representarse matemáticamente; (iii) los módulos informáticos superaron las pruebas unitarias ejecutadas; (iv) la comparación M0/M1/M2 está programada con entrenamiento y prueba separados.')
paragraph('Conclusión que permanece pendiente: determinar si Random Forest mejora el MAE en al menos cinco puntos porcentuales respecto del promedio. No se ha demostrado ni refutado sin observaciones reales del día 10.')
paragraph('Se recomienda que el equipo conserve el CSV original, documente el procedimiento, describa cualquier incidencia, muestre la limitación de la muestra y explique ante el jurado cómo una función algebraica y una IA pueden llegar a resultados diferentes.')

h(14,'Referencias bibliográficas')
refs=[
'I.E.P. Juan Pablo Peregrino. (2026). Bases EXPOMATE 2026. Documento institucional proporcionado.',
'University of Delaware Cooperative Extension. (s. f.). Radishes. https://www.udel.edu/academics/colleges/canr/cooperative-extension/fact-sheets/radishes/',
'scikit-learn. (consulta 2026). RandomForestRegressor. https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html',
'scikit-learn. (consulta 2026). LinearRegression. https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html',
'Streamlit. (consulta 2026). App dependencies for your Community Cloud app. https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies',
'Streamlit. (consulta 2026). Deploy your app on Community Cloud. https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy'
]
for r in refs:paragraph(r,indent=False)

h(15,'Anexos y evidencias del proyecto')
table(['Anexo','Archivo / evidencia','Estado'],[
('A','app.py y requirements.txt','Implementados'),
('B','modelos/funciones.py','Implementado, con validación y algoritmos'),
('C','datos/plantilla_experimental_32_recipientes.csv','32 filas y respuestas vacías'),
('D','pruebas/test_modelos.py','8 verificaciones aprobadas'),
('E','GUIA_CAMPO_Y_EXPOSICION.md','Guía para el equipo'),
('F','MATERIAL_STAND_A4.html','Material imprimible'),
('G','RESUMEN_1_PAGINA.md','Síntesis institucional'),
('H','CSV con observaciones del día 10','PENDIENTE'),
('I','Gráficos y errores con datos reales','PENDIENTE')])
paragraph('Cronograma: 11 de noviembre, inscripción y aprobación; 13, resumen y boceto; 16, primer avance; 19, segunda revisión; 23, informe y producto terminado; 25–26, ensayo ante asesor; 27, exposición de la feria. El inicio de la siembra debe permitir completar la observación del décimo día antes del cierre, sin fabricar registros.')
paragraph('Este informe es editable. Completar integrantes, fechas de siembra, observaciones agrícolas, resultados cuantitativos, conclusiones basadas en evidencia y fotografías autorizadas después de ejecutar el experimento.')

D.save(OUT)
print('Generado:',OUT,OUT.stat().st_size,'bytes')
