"""PROFUNBROTE-IA: reglas algebraicas, validación y comparación predictiva.
No incluye datos de emergencia observados ni ajustes preentrenados.
"""
from __future__ import annotations
import io
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

PROFUNDIDADES = (0.5, 1.0, 1.5, 2.0)
SUSTRATOS = ("Tierra vegetal", "Mezcla tierra-arena 1:1")
SEMILLAS_POR_RECIPIENTE = 5
SEMILLA_ALEATORIA = 20261109
CAMPOS = ["recipiente", "profundidad_cm", "sustrato", "repeticion", "semillas_sembradas", "emergidas_dia10", "fecha_siembra", "fecha_revision", "observaciones"]


def plantilla() -> pd.DataFrame:
    """32 unidades experimentales, una fila por recipiente, desenlaces vacíos."""
    filas = []
    idx = 0
    for d in PROFUNDIDADES:
        for s in SUSTRATOS:
            for r in range(1, 5):
                idx += 1
                filas.append(dict(recipient_dummy=0, recipiente=f"R{idx:02d}", profundidad_cm=d,
                                  sustrato=s, repeticion=r, semillas_sembradas=5,
                                  emergidas_dia10="", fecha_siembra="", fecha_revision="",
                                  observaciones=""))
    return pd.DataFrame(filas)[CAMPOS]


def convertir_csv(data: bytes | str | io.BytesIO) -> pd.DataFrame:
    if isinstance(data, bytes):
        data = io.BytesIO(data)
    return pd.read_csv(data, encoding="utf-8-sig")


def validar(df: pd.DataFrame) -> list[str]:
    errores: list[str] = []
    faltan = [c for c in CAMPOS if c not in df.columns]
    if faltan:
        return ["Faltan columnas requeridas: " + ", ".join(faltan)]
    if len(df) != 32:
        errores.append(f"Se requieren 32 recipientes; el archivo contiene {len(df)} filas.")
    if df['recipiente'].isna().any() or df['recipiente'].astype(str).duplicated().any():
        errores.append("Cada recipiente debe tener un código único no vacío.")
    if df['emergidas_dia10'].isna().any() or df['emergidas_dia10'].astype(str).str.strip().eq('').any():
        errores.append("Faltan observaciones del día 10: no se puede entrenar con registros vacíos.")
    claves = []
    for i, row in df.iterrows():
        try:
            d, s, r = float(row['profundidad_cm']), str(row['sustrato']).strip(), int(row['repeticion'])
            n = float(row['semillas_sembradas'])
            if d not in PROFUNDIDADES or s not in SUSTRATOS or r not in (1,2,3,4):
                errores.append(f"Fila {i+2}: tratamiento o repetición no reconocidos.")
            claves.append((d,s,r))
            if n != 5:
                errores.append(f"Fila {i+2}: cada recipiente debe contener exactamente 5 semillas.")
            g = float(row['emergidas_dia10'])
            if not np.isfinite(g) or g < 0 or g > 5 or not g.is_integer():
                errores.append(f"Fila {i+2}: 'emergidas_dia10' debe ser entero entre 0 y 5.")
        except (ValueError, TypeError, OverflowError):
            errores.append(f"Fila {i+2}: hay campos numéricos incompletos o inválidos.")
    if len(claves) == 32:
        if len(set(claves)) != 32:
            errores.append("Hay tratamientos y repeticiones duplicados.")
        requeridos = {(d,s,r) for d in PROFUNDIDADES for s in SUSTRATOS for r in (1,2,3,4)}
        if set(claves) != requeridos:
            errores.append("No están completos los ocho tratamientos con sus cuatro repeticiones.")
    return list(dict.fromkeys(errores))[:16]


def datos_preparados(df: pd.DataFrame) -> pd.DataFrame:
    errores = validar(df)
    if errores:
        raise ValueError(" | ".join(errores))
    out = df.copy()
    out['profundidad_cm'] = out['profundidad_cm'].astype(float)
    out['repeticion'] = out['repeticion'].astype(int)
    out['emergidas_dia10'] = out['emergidas_dia10'].astype(int)
    out['sustrato_cod'] = (out['sustrato'] == SUSTRATOS[1]).astype(int)
    out['emergencia_pct'] = out['emergidas_dia10'] / out['semillas_sembradas'].astype(float) * 100
    out['conjunto'] = np.where(out['repeticion'] == 4, 'Prueba final', 'Entrenamiento')
    return out


def matriz(datos: pd.DataFrame, modelo: str = 'm2') -> np.ndarray:
    d = datos['profundidad_cm'].to_numpy(dtype=float)
    s = datos['sustrato_cod'].to_numpy(dtype=float)
    if modelo == 'm1':
        return np.column_stack((d, d*d, s))
    return np.column_stack((d, s))


class ModeloPromedio:
    def fit(self, x, y):
        self.media = float(np.mean(y))
        return self
    def predict(self, x):
        return np.full(len(x), self.media)


def crear_modelo(nombre: str):
    if nombre == 'M0':
        return ModeloPromedio()
    if nombre == 'M1':
        return LinearRegression()
    if nombre == 'M2':
        return RandomForestRegressor(n_estimators=120, max_depth=3, min_samples_leaf=2,
                                     random_state=SEMILLA_ALEATORIA, n_jobs=1)
    raise ValueError('Modelo no reconocido')


def predecir(modelo, x) -> np.ndarray:
    # Las tasas son porcentajes; la regresión lineal no está naturalmente acotada.
    return np.clip(np.asarray(modelo.predict(x), dtype=float), 0.0, 100.0)


def metricas(y: np.ndarray, pred: np.ndarray) -> dict:
    return {"MAE (p.p.)": float(mean_absolute_error(y, pred)),
            "RMSE (p.p.)": float(np.sqrt(mean_squared_error(y, pred)))}


def particiones_cv(train: pd.DataFrame):
    """Tres folds: en cada fold, un recipiente de cada tratamiento como validación.
    No hay mezcla del recipiente entre ajuste y evaluación; cada fold tiene 16/8 registros.
    """
    train = train.reset_index(drop=True)
    rng = np.random.default_rng(SEMILLA_ALEATORIA)
    folds = np.full(len(train), -1, dtype=int)
    for (_, _), ids in train.groupby(['profundidad_cm','sustrato']).groups.items():
        pos = np.array(list(ids), dtype=int)
        if len(pos) != 3:
            raise ValueError('El entrenamiento requiere 3 repeticiones por tratamiento.')
        rng.shuffle(pos)
        folds[pos] = np.arange(3)
    for fold in range(3):
        a = np.flatnonzero(folds != fold)
        b = np.flatnonzero(folds == fold)
        yield fold+1, a, b


def evaluar_modelos(df: pd.DataFrame):
    """Se calcula a partir de los 32 datos completos de la investigación real.
    No hace uso de la prueba final para selección o ajuste de hiperparámetros.
    """
    clean = datos_preparados(df)
    train = clean[clean['conjunto'] == 'Entrenamiento'].copy().reset_index(drop=True)
    test = clean[clean['conjunto'] == 'Prueba final'].copy().reset_index(drop=True)
    cv = []
    holdout = []
    fitted = {}
    for nombre in ('M0','M1','M2'):
        feats = 'm1' if nombre == 'M1' else 'm2'
        X = matriz(train,feats)
        y = train['emergencia_pct'].to_numpy()
        for fold, idx_fit, idx_eval in particiones_cv(train):
            m = crear_modelo(nombre)
            m.fit(X[idx_fit], y[idx_fit])
            yhat = predecir(m, X[idx_eval])
            cv.append(dict(modelo=nombre, fold=fold, n_entrenamiento=len(idx_fit),
                           n_validacion=len(idx_eval), **metricas(y[idx_eval],yhat)))
        final = crear_modelo(nombre).fit(X,y)
        test_x = matriz(test,feats)
        yh = predecir(final,test_x)
        fitted[nombre] = final
        for i,row in test.iterrows():
            holdout.append(dict(modelo=nombre, recipiente=row['recipiente'],
                                 profundidad_cm=row['profundidad_cm'],sustrato=row['sustrato'],
                                 observado_pct=row['emergencia_pct'],predicho_pct=float(yh[i]),
                                 error_pp=float(abs(yh[i]-row['emergencia_pct']))))
    df_hold = pd.DataFrame(holdout)
    df_metrics = pd.DataFrame([dict(modelo=name, **metricas(
        subset['observado_pct'].to_numpy(),subset['predicho_pct'].to_numpy()))
        for name,subset in df_hold.groupby('modelo',sort=True)])
    return dict(datos=clean, entrenamiento=train, prueba=test, cv=pd.DataFrame(cv),
                predicciones=df_hold, metricas=df_metrics, modelos=fitted)


def predecir_condicion(resultados: dict, d: float, sustrato: str):
    if not (0.5 <= d <= 2.0) or sustrato not in SUSTRATOS:
        raise ValueError('Condición fuera del dominio experimental.')
    sc = int(sustrato == SUSTRATOS[1])
    out={}
    for nombre,m in resultados['modelos'].items():
        x = np.array([[d,d*d,sc]]) if nombre == 'M1' else np.array([[d,sc]])
        out[nombre]=float(predecir(m,x)[0])
    return out


def ejemplo_algebra():
    """Ejemplo ilustrativo explícitamente NO experimental: 3 pares profundidad/porcentaje."""
    d=np.array([0.5,1.0,1.5])
    y=np.array([60.,90.,70.])
    coef=np.polyfit(d,y,2)
    vertex=-coef[1]/(2*coef[0])
    return coef,vertex,float(np.polyval(coef,vertex))
