"""Pruebas informáticas con datos sintéticos de verificación, jamás resultados agrícolas."""
import numpy as np
import pandas as pd
import pytest
from modelos.funciones import (
    plantilla, validar, datos_preparados, evaluar_modelos, predecir_condicion,
    ejemplo_algebra, particiones_cv, metricas, PROFUNDIDADES, SUSTRATOS,
)


def ejemplo_sintetico_verificacion():
    df=plantilla()
    # VALORES TOTALMENTE SINTÉTICOS para probar el código, no observaciones reales.
    for ix,row in df.iterrows():
        d=float(row['profundidad_cm']); s=row['sustrato']; r=int(row['repeticion'])
        g=3 + int(d in (1.0,1.5)) - int(s==SUSTRATOS[1]) + (r%3-1)
        df.at[ix,'emergidas_dia10']=int(np.clip(g,0,5))
    return df


def test_plantilla_sin_resultados():
    df=plantilla()
    assert len(df)==32
    assert df['emergidas_dia10'].astype(str).str.len().eq(0).all()
    assert int(df['semillas_sembradas'].sum())==160
    assert validar(df)


def test_restricciones_y_duplicados():
    df=ejemplo_sintetico_verificacion()
    assert not validar(df)
    df.loc[0,'emergidas_dia10']=6
    assert validar(df)
    df=ejemplo_sintetico_verificacion()
    df.loc[0,'repeticion']=2
    assert validar(df)


def test_separacion_y_dominio():
    df=datos_preparados(ejemplo_sintetico_verificacion())
    assert len(df[df['conjunto']=='Entrenamiento'])==24
    assert len(df[df['conjunto']=='Prueba final'])==8
    assert set(df['emergencia_pct'].unique()).issubset({0.,20.,40.,60.,80.,100.})
    assert (df.groupby(['profundidad_cm','sustrato']).size()==4).all()


def test_cv_sin_fuga_de_recipientes():
    df=datos_preparados(ejemplo_sintetico_verificacion())
    tr=df[df['conjunto']=='Entrenamiento'].reset_index(drop=True)
    seen=[]
    for fold,fi,vi in particiones_cv(tr):
        assert len(fi)==16 and len(vi)==8
        assert set(fi).isdisjoint(set(vi))
        assert len(tr.iloc[vi].groupby(['profundidad_cm','sustrato']))==8
        seen.extend(vi)
    assert sorted(seen)==list(range(24))


def test_ejemplo_cuadratico_verificado():
    co,x,y=ejemplo_algebra()
    assert np.allclose(co,[-100.,210.,-20.])
    assert np.isclose(x,1.05) and np.isclose(y,90.25)
    assert np.isclose(np.polyval(co,1),90)


def test_entrenamiento_se_hace_solo_al_llamar_con_datos_completos():
    data=ejemplo_sintetico_verificacion()
    results=evaluar_modelos(data)
    assert set(results['modelos'])=={'M0','M1','M2'}
    assert len(results['cv'])==9
    assert len(results['predicciones'])==24
    assert len(results['metricas'])==3
    assert (results['predicciones']['predicho_pct'].between(0,100)).all()
    assert (results['metricas']['MAE (p.p.)']>=0).all()
    assert len(results['prueba'])==8


def test_simulador_restringe_dominio():
    res=evaluar_modelos(ejemplo_sintetico_verificacion())
    v=predecir_condicion(res,1.2,SUSTRATOS[0])
    assert set(v)=={'M0','M1','M2'}
    assert all(0<=x<=100 for x in v.values())
    with pytest.raises(ValueError):predecir_condicion(res,3.0,SUSTRATOS[0])


def test_mae_rmse():
    m=metricas(np.array([20.,60.]),np.array([30.,50.]))
    assert np.isclose(m['MAE (p.p.)'],10.)
    assert np.isclose(m['RMSE (p.p.)'],10.)
