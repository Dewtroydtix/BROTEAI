"""PROFUNBROTE-IA — investigación escolar de emergencia de rabanito.
No contiene resultados reales predeterminados. Se entrena solo con 32 registros validados.
"""
import hashlib
import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from modelos.funciones import (
    PROFUNDIDADES, SUSTRATOS, SEMILLA_ALEATORIA,
    plantilla, validar, convertir_csv, datos_preparados, evaluar_modelos,
    predecir_condicion, ejemplo_algebra, matriz,
)

st.set_page_config(page_title='PROFUNBROTE-IA | EXPOMATE 2026', page_icon='🌱', layout='wide')
st.markdown('''<style>
.block-container{padding-top:1.4rem; max-width:1200px}
h1,h2,h3{letter-spacing:-.025em}
div[data-testid="stMetric"]{border:1px solid #dce8df;border-radius:12px;padding:10px}
.caption{color:#56736a}
</style>''', unsafe_allow_html=True)
st.title('PROFUNBROTE-IA')
st.caption('EXPOMATEMÁTICA JUANPABLINA 2026 · Categoría B · Álgebra aplicada a la agricultura')

PAGES = ['Inicio','Diseño experimental','Registro y validación','Álgebra aplicada',
         'Entrenamiento y comparación','Simulador de escenarios','Pruebas técnicas','Referencias']
with st.sidebar:
    st.subheader('Navegación')
    page = st.radio('Secciones', PAGES, label_visibility='collapsed')
    st.divider()
    st.markdown('**Datos experimentales propios**')
    upload = st.file_uploader('Cargar CSV completo (32 recipientes)',type=['csv'],key='datos_csv')
    st.download_button('Descargar plantilla vacía', data=plantilla().to_csv(index=False).encode('utf-8-sig'),
                       file_name='plantilla_PROFUNBROTE_32.csv',mime='text/csv',key='descargar_plantilla')
    certificado = st.checkbox('Confirmo que los 32 resultados proceden de observaciones reales del día 10.',key='confirmacion')
    st.caption('No suba nombres de estudiantes ni fotografías. No hay datos de emergencia preinstalados.')
    st.divider()
    st.caption('Rango experimental: 0,5–2,0 cm · Cinco semillas por recipiente · 2 sustratos')

df_raw=None; errors=[]; sha=None
if upload is not None:
    raw=upload.getvalue(); sha=hashlib.sha256(raw).hexdigest()
    try:
        df_raw=convertir_csv(raw)
        errors=validar(df_raw)
    except Exception as exc:
        errors=[f'El CSV no pudo interpretarse: {type(exc).__name__}: {exc}']
    if st.session_state.get('ultima_firma')!=sha:
        st.session_state.pop('entrenamiento_real',None)
        st.session_state['ultima_firma']=sha
res=st.session_state.get('entrenamiento_real')

def not_ready():
    st.info('Para obtener resultados del modelo, cargue los 32 registros reales, confirme su procedencia y pulse «Entrenar y evaluar» en la sección correspondiente. No se emplean datos ficticios.')

def show_csv(df,name, key):
    st.download_button('Descargar CSV: '+name, df.to_csv(index=False).encode('utf-8-sig'),
        file_name=name+'.csv',mime='text/csv',key=key)

if page=='Inicio':
    st.markdown('## ¿Qué investigaremos?')
    st.write('**Pregunta:** ¿la profundidad de siembra y el tipo de sustrato ayudan a estimar el porcentaje de plántulas de rabanito que emergen al décimo día?')
    a,b,c=st.columns(3)
    a.metric('Tratamientos', '8')
    b.metric('Recipientes', '32')
    c.metric('Semillas previstas','160')
    st.markdown('''### Dos caminos para investigar
- **Álgebra:** calcula el porcentaje de emergencia y ajusta una función cuadrática con términos de sustrato.
- **IA real:** entrena RandomForestRegressor con datos propios y compara sus predicciones con modelos más sencillos.

**Estado:** los registros experimentales se introducen por CSV; ningún resultado de emergencia está precargado.''')
    st.warning('Las predicciones no son recomendaciones agrícolas generales. Muestra pequeña, condiciones escolares y rango de profundidad limitado.')
    st.markdown('### Etapas de la investigación')
    st.code('Siembra → Registro día 10 → Validación CSV → Entrenar (24) → Prueba reservada (8) → Interpretar errores')

elif page=='Diseño experimental':
    st.header('Diseño factorial y control de variables')
    st.latex(r'4\text{ profundidades}\times2\text{ sustratos}\times4\text{ repeticiones}=32\text{ recipientes}')
    st.latex(r'32\text{ recipientes}\times5\text{ semillas}=160\text{ semillas}')
    st.write('Profundidades (cm): **0,5; 1,0; 1,5; 2,0**. Sustratos: **tierra vegetal** y **mezcla de tierra y arena 1:1 por volumen**.')
    plan=plantilla()[['recipiente','profundidad_cm','sustrato','repeticion','semillas_sembradas']]
    st.dataframe(plan, hide_index=True, use_container_width=True)
    st.markdown('''**Unidades experimentales:** cada recipiente, no cada semilla; las cinco semillas de un recipiente comparten condiciones.

**Separación predefinida:** repetición 4 = **prueba final** para cada uno de los ocho tratamientos; repeticiones 1–3 = **entrenamiento**. La elección se fija antes de conocer resultados.

**Controles del experimento:** mismo lote de semillas, recipientes comparables con drenaje, distribución aleatorizada en el espacio de cultivo, condiciones de exposición semejantes, riego siguiendo un procedimiento uniforme y registro de incidencias. El asesor supervisará la actividad y la higiene de los materiales.''')
    st.info('Se registra la emergencia visible en el décimo día, no la germinación interna ni el rendimiento final del cultivo.')

elif page=='Registro y validación':
    st.header('Revisión de datos experimentales')
    if df_raw is None:
        st.warning('Todavía no se ha cargado un CSV. La plantilla contiene 32 filas y **la columna de resultados está vacía**.')
        st.dataframe(plantilla().head(12),hide_index=True,use_container_width=True)
    else:
        st.dataframe(df_raw,hide_index=True,use_container_width=True)
        if errors:
            st.error('El archivo no es apto para entrenar:')
            for e in errors: st.write('• '+e)
        else:
            st.success('CSV estructuralmente válido: 32 filas, 8 tratamientos y 4 repeticiones por tratamiento.')
            clean=datos_preparados(df_raw)
            a,b,c=st.columns(3)
            a.metric('Registros para entrenar', len(clean[clean['conjunto']=='Entrenamiento']))
            b.metric('Registros reservados', len(clean[clean['conjunto']=='Prueba final']))
            c.metric('Rango de emergencia observado', f"{clean['emergencia_pct'].min():.0f}–{clean['emergencia_pct'].max():.0f} %")
            st.dataframe(clean[['recipiente','profundidad_cm','sustrato','emergidas_dia10','emergencia_pct','conjunto']],hide_index=True,use_container_width=True)
            show_csv(clean[['recipiente','profundidad_cm','sustrato','repeticion','emergencia_pct','conjunto']], 'datos_validados',key='descargar_validados')
        if not certificado:
            st.warning('Para entrenar es obligatorio confirmar que los valores son observaciones reales del día 10.')

elif page=='Álgebra aplicada':
    st.header('De la observación a la función algebraica')
    st.latex(r'E=\frac{g}{n}\cdot100\%')
    st.latex(r'\widehat E(d,s)=\beta_0+\beta_1d+\beta_2d^2+\beta_3s')
    st.caption('d en centímetros, s = 0 para tierra vegetal y 1 para mezcla 1:1; E es porcentaje de emergencia.')
    st.subheader('Ejemplo numérico — completamente hipotético')
    st.warning('Los puntos siguientes son didácticos y **no corresponden a recipientes reales**.')
    toy=pd.DataFrame({'Profundidad (cm)':[0.5,1.0,1.5], 'Emergencia (%)':[60.,90.,70.]})
    st.dataframe(toy, hide_index=True, use_container_width=True)
    cf, vertex, peak=ejemplo_algebra()
    st.latex(r'E(d)=-100d^2+210d-20')
    st.write(f'Vertice de la parábola: **{vertex:.2f} cm**, valor modelado: **{peak:.2f} %** (solo para este ejemplo).')
    x=np.linspace(0.5,1.5,120)
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=x,y=np.polyval(cf,x),name='Función ilustrativa', mode='lines'))
    fig.add_trace(go.Scatter(x=toy['Profundidad (cm)'],y=toy['Emergencia (%)'], mode='markers', name='Tres valores hipotéticos',marker={'size':10}))
    fig.update_layout(xaxis_title='Profundidad (cm)',yaxis_title='Emergencia (%)',height=350)
    st.plotly_chart(fig,use_container_width=True,key='fig_algebra_hipotetica')
    if res is not None:
        m1=res['modelos']['M1']
        cs=m1.coef_
        st.subheader('Función M1 ajustada a las 24 observaciones reales')
        st.code(f'E_pred = {m1.intercept_:+.4f} {cs[0]:+.4f}*d {cs[1]:+.4f}*d² {cs[2]:+.4f}*s\n(Se limita la salida al rango 0–100 %.)',language='text')
        st.caption('La estimación en escenarios no medidos no constituye una recomendación de profundidad ideal.')

elif page=='Entrenamiento y comparación':
    st.header('Entrenamiento real de M0, M1 y M2')
    st.markdown('**M0:** promedio general de los 24 registros de entrenamiento. **M1:** regresión lineal en d, d² y s. **M2:** RandomForestRegressor con 120 árboles, profundidad máxima 3, mínimo 2 observaciones por hoja y semilla fija.')
    st.markdown('**Validación interna:** tres particiones, cada una con 16 recipientes para ajustar y 8 para validar. **Prueba final:** los ocho recipientes de repetición 4; no intervienen en los ajustes.')
    can_train=df_raw is not None and not errors and certificado
    if st.button('Entrenar y evaluar sobre datos reales',type='primary',disabled=not can_train,key='btn_entrenar'):
        with st.spinner('Ajustando los modelos y calculando errores...'):
            st.session_state['entrenamiento_real']=evaluar_modelos(df_raw)
            res=st.session_state['entrenamiento_real']
    if not can_train:
        not_ready()
    if res is not None:
        st.success('Modelos calculados con los registros cargados en esta sesión.')
        cv=res['cv']; metrics=res['metricas']; pred=res['predicciones']
        st.subheader('Validación cruzada: 3 particiones del entrenamiento')
        st.dataframe(cv.style.format({'MAE (p.p.)':'{:.2f}','RMSE (p.p.)':'{:.2f}'}),hide_index=True,use_container_width=True)
        st.subheader('Prueba final: 8 recipientes reservados')
        st.dataframe(metrics.style.format({'MAE (p.p.)':'{:.2f}','RMSE (p.p.)':'{:.2f}'}),hide_index=True,use_container_width=True)
        fig=px.bar(metrics,x='modelo',y=['MAE (p.p.)','RMSE (p.p.)'],barmode='group',title='Errores sobre la prueba final')
        fig.update_layout(height=340,yaxis_title='Puntos porcentuales')
        st.plotly_chart(fig,use_container_width=True,key='fig_errores_reservados')
        fig2=px.scatter(pred,x='observado_pct',y='predicho_pct',color='modelo',
                         hover_data=['recipiente','profundidad_cm','sustrato'],title='Observado frente a predicho')
        fig2.add_trace(go.Scatter(x=[0,100],y=[0,100],mode='lines',name='Predicción exacta',line={'dash':'dash','color':'gray'}))
        fig2.update_layout(xaxis_title='Observado (%)',yaxis_title='Predicho (%)',height=360)
        st.plotly_chart(fig2,use_container_width=True,key='fig_obs_pred')
        mm={r['modelo']:r['MAE (p.p.)'] for _,r in metrics.iterrows()}
        delta=mm['M0']-mm['M2']
        st.metric('Reducción MAE M0 − M2',f'{delta:.2f} puntos porcentuales')
        st.info('Hipótesis descriptiva H1: reducción ≥ 5 puntos porcentuales. Muestra final de solo 8 recipientes: interpretar con cautela.')
        c1,c2,c3=st.columns(3)
        with c1:show_csv(cv,'validacion_cruzada_M0_M1_M2',key='desc_cv')
        with c2:show_csv(metrics,'metricas_prueba_final',key='desc_metrics')
        with c3:show_csv(pred,'predicciones_ocho_recipientes',key='desc_preds')

elif page=='Simulador de escenarios':
    st.header('Simulador de estimaciones')
    st.warning('Las predicciones solo son válidas como exploración del experimento. No representan recomendaciones agronómicas ni sustituyen nuevas mediciones.')
    d=st.slider('Profundidad (cm)', min_value=0.5,max_value=2.0,value=1.0,step=0.1,key='prof_sim')
    s=st.selectbox('Sustrato',SUSTRATOS,key='suelo_sim')
    if res is None:
        not_ready()
    else:
        try:
            pred=predecir_condicion(res,round(d,2),s)
            cols=st.columns(3)
            for c,(k,label) in zip(cols,[('M0','Promedio M0'),('M1','Función M1'),('M2','IA M2')]):
                c.metric(label,f'{pred[k]:.1f} %')
            st.caption('Predicción entre 0 y 100 %. Las medidas originales son discretas de 20 puntos porcentuales por recipiente de cinco semillas.')
            st.download_button('Exportar predicción del escenario',pd.DataFrame([dict(profundidad_cm=d,sustrato=s,**pred)]).to_csv(index=False).encode('utf-8-sig'),
                               file_name='escenario_predicho.csv',mime='text/csv',key='desc_escenario')
        except ValueError as exc:
            st.error(str(exc))

elif page=='Pruebas técnicas':
    st.header('Comprobaciones matemáticas independientes')
    respuestas=[]
    p=plantilla()
    respuestas.append(('32 recipientes en la plantilla',len(p)==32))
    respuestas.append(('8 tratamientos únicos',len(p.groupby(['profundidad_cm','sustrato']))==8))
    respuestas.append(('4 repeticiones por tratamiento',(p.groupby(['profundidad_cm','sustrato']).size()==4).all()))
    respuestas.append(('160 semillas en el diseño',int(p['semillas_sembradas'].sum())==160))
    respuestas.append(('Un archivo vacío NO es entrenable',len(validar(p))>0))
    co,vert,peak=ejemplo_algebra()
    respuestas.append(('Ejemplo algebraico: coeficientes correctos',np.allclose(co,[-100,210,-20])))
    respuestas.append(('Ejemplo algebraico: máximo en 1,05 cm',np.isclose(vert,1.05)))
    respuestas.append(('Ejemplo algebraico: máximo 90,25 %',np.isclose(peak,90.25)))
    for name,ok in respuestas:
        st.write(('✅ ' if ok else '❌ ')+name)
    st.caption('Estas son comprobaciones de código y aritmética, no resultados de emergencia observada. También se incluye pytest en la carpeta pruebas/.')

elif page=='Referencias':
    st.header('Bibliografía y reproducibilidad')
    st.markdown('''1. I.E.P. Juan Pablo Peregrino (2026). *Bases EXPOMATE 2026*. Documento institucional.
2. University of Delaware Cooperative Extension. *Radishes*. https://www.udel.edu/academics/colleges/canr/cooperative-extension/fact-sheets/radishes/
3. scikit-learn. *RandomForestRegressor*. https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
4. scikit-learn. *LinearRegression*. https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
5. Streamlit. *App dependencies for Community Cloud*. https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
6. Streamlit. *Deploy your app on Community Cloud*. https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

El código usa una semilla fija (`20261109`) para reproducibilidad y declara explícitamente cuáles filas son de entrenamiento y cuáles son de prueba.''')

st.divider()
st.caption('PROFUNBROTE-IA · Proyecto escolar exploratorio · Los resultados de los estudiantes no se inventan.')
