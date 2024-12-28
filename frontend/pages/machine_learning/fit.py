import asyncio
import streamlit as st
from tools.api import client

st.header("Обучение модели")
payload = {}

payload["type"] = st.radio("Выберите модель", ["LogisticRegression", "SVC"])

st.subheader("Выберите гиперпараметры модели")
params = {}
params["C"] = st.slider("C", 0.0, 10.0, step=0.001, value=1.0, format="%.3f")
params["tol"] = st.slider("tol", 1e-6, 1e-3, step=0.000001, format="%.6f", value=1e-4)

if payload["type"] == "LogisticRegression":

    params["penalty"] = st.radio("penalty", ["l2", None, "l1", "elasticnet"])

    if params["penalty"] == "l2":
        params["solver"] = st.radio("solver", 
                      ["lbfgs", 
                       "liblinear", 
                       "newton-cg", 
                       "newton-cholesky", 
                       "sag", 
                       "saga"])
    if params["penalty"] is None:
        params["solver"] = st.radio("solver", 
                      ["lbfgs", 
                       "newton-cg", 
                       "newton-cholesky", 
                       "sag", 
                       "saga"])
    if params["penalty"] == "l1":
        params["solver"] = st.radio("solver", 
                      ["liblinear", 
                       "saga"])
    if params["penalty"] == "elasticnet":
        params["solver"] = "saga"

    if params["penalty"] == "l2" and params["solver"] == "liblinear":
        params["dual"] = st.radio("dual", [False, True])


        
    params["max_iter"] = st.slider("max_iter", 100, 1000, step=1, value=100)

    if params["solver"] == "liblinear":
        params["warm_start"] = st.radio("warm_start", [False, True])

    if params["penalty"] == "elasticnet":
        params["l1_ratio"] = st.slider("l1_ratio", 0.0, 1.0, step=0.01, value=0.5)
else:
    params["kernel"] = st.radio("kernel", ["rbf", "linear", "poly", "sigmoid"])
    if params["kernel"] == "poly":
        params["degree"] = st.slider("degree", 1, 5, step=1, value=3)
    if params["kernel"] != "linear":
        params["gamma"] = st.radio("gamma", ["scale", "auto"])
    if params["kernel"] in set(["poly", "sigmoid"]):
        params["coef0"] = st.slider("coef0", -1.0, 1.0, step=0.01, value=0.0)
    params["shrinking"] = st.radio("shrinking", [False, True])
    params["probability"] = True

payload["hyperparameters"] = params

payload["model_id"] = st.text_input("Введите id модели")

payload["description"] = st.text_input("Введите описание модели")

if st.button("Обучить модель"):
    if not payload["model_id"]:
        st.error("Введите id модели")
    else:
        response = asyncio.run(
            client.fit('/fit', payload)
        )
        st.warning(response["status"])