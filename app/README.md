# 10-Year Coronary Heart Disease Predictor

Greetings from the more technical side of the project!

In this README you will find a detailed explanation of the development of the
[FastAPI][docs_fastapi] coronary heart disease (CHD) predictor.

## Table of Contents

- [1. Overview](#1-overview)
- [2. Artifacts](#2-artifacts)
- [3. (Local) API](#3-local-api)
- [4. (Deployed) API](#4-deployed-api)
- [5. User Interface](#5-ui)
- [6. Testing](#6-testing)
- [7. Limitations and Intended Use](#7-limitations-and-intended-use)

## 1. Overview

This section of the repository exposes a machine-learning model for predicting
**10-year CHD risk.** It provides:

- A FastAPI JSON inference API (`POST /predict`)
- A lightweight browser user interface (UI) for interactive input (`GET /`)
- Automatic interactive API documentation, including two alternative user
interfaces: [Swagger UI][docs_swagger] (`GET /docs`) and [ReDoc][docs_redoc]
  (`GET /redoc`)
- A health endpoint (`GET /healthz`)

### Design Principles

The three different design principles our API is built upon are:

1. **Raw inputs in, predictions out**. The user provides raw, not normalized
   values

2. **Training/serving parity via a single persisted Pipeline**. The saved model
   artifact (`model/model_pipeline.pkl`) is a [scikit-learn][docs_scikit]
   `Pipeline` to ensure the same transformations are applied at training and
   inference time.

3. **No data leakage**. Data-driven pre-processing (scaling, imputing,
   encoding) must be fit on training data only

### Final Train and Export

All the steps performed in the [different notebooks][dir_notebook] had been
merged in a single [Python script][file_script] that:

1. **Loads** the raw dataframe
2. **Cleans and pre-processes** the data (renames fields, transforms binary
variables, and drops missing values)
3. **Splits data** into train and test datasets
4. **Fits** a scikit-learn `Pipeline` (see [Model Pipeline](#model-pipeline)
   section for a detailed explanation)
5. **Evaluates basic metrics** (accuracy, recall, precision, F1-score, and
   ROC-AUC)
6. **Exports artifacts** to `model/`

To run the script on new data, and re-generate the API artifacts, from the
repository's root directory:

```bash
python3 ./scripts/train_and_export.py
```

## 2. Artifacts

This project uses two artifacts.

### Model Pipeline

We decided to store the feature engineering and normalization steps alongside
the final model in a [joblib][docs_joblib] persisted `Pipeline` containing:

- Feature engineering transformer (`FeatureEngineer`)
- Pre-processing ( `ColumTransformer` using `StandardScaler`)
- Model (the classifier)

As a consequence, the FastAPI app does not have to call `fit`, `fit_transform`,
or compute scaling parameters at runtime; it just have to pass raw inputs into
the pipeline and call `predict_proba`.

The two engineered features in `FeatureEngineer` are:
- `smoker_intensity`. The intensity is computed as product of `current_smoker`
  (which takes as values `1` if the patient smokes, and `0` otherwise) and
  `cigs_per_day`. This product ensures that even if a non-smoker is set to
  smoke any amount of cigarettes per day (an incongruence) the intensity is
  going to be 0.
- `pulse_pressure`. The pulse pressure is computed as the difference between
  systolic and diastolic blood pressure. It represents the force that the heart
  generates each time it contracts.

The pre-processing is made using `ColumTransformer` which applies the
transformer `StandardScaler` to numeric columns, leaves the rest "_as-is_",
and concatenates the results into a single feature space. The `StandardScaler`
transformer computes scaling parameters (mean and standard deviation) on the
training set during `fit()` and stores them for later use in.

For a detailed explanation on the model development, validation and selection,
please refer to the dedicated section in the [main README][file_readme].

### Model Metadata

The model metadata (`model/metadata.json`) exports the current model contract
and evaluation summary. We created and kept this file not only because it
establishes a stable API contract, but also because it makes the UI generation
and configuration straightforward, and helps reproduce and audit predictions.

The current metadata schema contains:

- `version`. Artifact version string (date of creation)
- `target`. The target column name (`ten_year_chd`)
- `raw_features`. Required API request keys (`sex`, `age`, `education_level`,
  `current_smoker`, `cigs_per_day`. `bp_meds`, `prevalent_stroke`,
  `prevalent_hypertension`, `diabetes`, `total_cholesterol`, `systolic_bp`,
  `diastolic_bp`, `bmi`, `heart_rate`, and `glucose`)
- `engineered_features`. Derived columns computed inside the pipeline
  (`smoker_intensity` and `pulse_pressure`)
- `model_features_scaled`. Numeric columns scaled (`age`, `bmi`, `systolic_bp`,
  `diastolic_bp`, `total_cholesterol`, `glucose`, `heart_rate`,
  `pulse_pressure`, and `smoker_intensity`)
- `model_features_passthrough`. Non-scaled passthrough columns (`sex`,
  `education_level`, `current_smoker`, `bp_meds`, `prevalent_stroke`,
  `prevalent_hypertension` and `diabetes`)
- `threshold`. Decision threshold (set to 0.5)
- `metrics`. Evaluation metrics dictionary (`accuracy`, `recall`, `precision`,
  `F1-score`, and `ROC-AUC`)
- `notes`. Free-text notes

## 3. (Local) API

First, all the required packages have to be installed. From the repository's
root directory run:

```bash
pip3 install -r requirements.txt
```

In order to start the server locally, from the `app/` directory run:

```bash
fastapi dev main.py
```

The different access points are:

- UI: `http://127.0.0.1:8000/`
- Documentation via Swagger UI: `http://127.0.0.1:8000/docs`
- Documentation via ReDoc: `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/healthz`
- OpenAPI schema JSON: `http://127.0.0.1:8000/openapi.json`

### API Endpoints

#### `GET /`

Interactive user interface.

For a detailed description of the UI, refer to its [dedicated section](#5-UI).

#### `GET /healthz`

Health/readiness endpoint.

If the API is up and running, and the model has been correctly loaded, the
expected response is

```json
{
  "status": "ok",
  "model_loaded": true,
  "model_version": "2026-01-18"
}
```

#### `POST /predict`

Runs inference.

> NOTE: the endpoint `GET /predict` returns **405 Method Not Allowed** because
> inference is **POST**.

The API accepts raw values (not normalized). The list is the contract exported
in `model/metadata.json`.

A `curl` example would be:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "sex": 1,
  "age": 5,
  "education_level": 2,
  "current_smoker": 1,
  "cigs_per_day": 10,
  "bp_meds": 0,
  "prevalent_stroke": 0,
  "prevalent_hypertension": 1,
  "diabetes": 0,
  "total_cholesterol": 20,
  "systolic_bp": 135,
  "diastolic_bp": 85,
  "bmi": 26.5,
  "heart_rate": 72,
  "glucose": 90
}'
```

The response body that this would generate is:

```json
{
  "prediction": 0,
  "probability": 0.05812722137703385,
  "threshold": 0.5,
  "model_version": "2026-01-18",
  "roc_auc": 0.73
}
```

Missing request fields (for example `glucose`) would return
`422 Error: Unprocessable Content` with the following details:

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "glucose"
      ],
      "msg": "Field required",
      "input": {
        "sex": 1,
        "age": 5,
        "education_level": 2,
        "current_smoker": 1,
        "cigs_per_day": 10,
        "bp_meds": 0,
        "prevalent_stroke": 0,
        "prevalent_hypertension": 1,
        "diabetes": 0,
        "total_cholesterol": 20,
        "systolic_bp": 135,
        "diastolic_bp": 85,
        "bmi": 26.5,
        "heart_rate": 72
      }
    }
  ]
}
```

In the scenario of extra request fields (for example `FIELD`), the response
would be `422 Error: Unprocessable Content` with the following details:

```json
{
  "detail": [
    {
      "type": "extra_forbidden",
      "loc": [
        "body",
        "FIELD"
      ],
      "msg": "Extra inputs are not permitted",
      "input": 2
    }
  ]
}
```

## 4. (Deployed) API

We wanted to make this tool as accessible as possible without forcing anyone 
to deal with local installations. To achieve this, and to make sure the app 
runs exactly the same for everyone, we containerized the entire project and 
moved it to the cloud.

### Docker Containerization

To dodge the classic "it works on my machine" headache, we used **Docker**. 
By creating a `Dockerfile`, we bundled everything the app needs to run, 
operating system dependencies, the Python environment and the trained 
model artifacts, into one isolated image.

Here is the breakdown of our build process:
1.  **Base Image**: We use `python:3.9-slim` to keep the image lightweight.
2.  **Dependencies**: We copy `requirements.txt` and install packages.
3.  **App & Model**: We copy the `app/` code and the trained `model/` 
directory into the container.
4.  **Entrypoint**: The container launches the server using 
`uvicorn app.main:app --host 0.0.0.0 --port 80`.

If you want to test the production environment locally, you can build and run 
it with these commands:
```bash
# Build the image
docker build -t coronary-api .

# Run the container (mapping port 80 inside to 8000 outside)
docker run -p 8000:80 coronary-api
```

### Cloud Hosting (Render)

For hosting, we chose Render because of how well it handles automation. 
We set up a Continuous Deployment (CD) pipeline that works seamlessly 
with our workflow:

1. **Automatic Sync:** Render keeps an eye on the `main` branch of this
   repository. 
2. **Smart Updates:** Whenever we merge a new commit, Render automatically
    pulls the changes.
3. **Zero Downtime:** It builds the new Docker image and swaps the old version
   for the new one without the API ever going offline.

### Live Access

The API is publicly available at:

- <https://api-coronary-disease-sp.onrender.com/>

You can interact with it exactly as you would locally:

- **Interactive UI**: Open the URL in your browser.
- **Documentation**: Go to `/docs` or `/redoc`.
- **Inference**: Send `POST` requests to `/predict`.

> **Important Note on Cold Starts**  
> Since we are using the free tier of Render, the server *sleeps* after 15 minutes of inactivity.  
> The first request after a period of inactivity may take up to **50 seconds** to process while the container wakes up.  
> Subsequent requests will be instant.


## 5. UI

The UI provides an interactive way for users to submit input values using
sliders, drop-down menus, and/or the keyboard, without requiring `curl`.

<img width="2558" height="1337" alt="UI" src="https://github.com/user-attachments/assets/fc2e960a-4bd3-43eb-b79a-edefad972ed7" />

By clicking `Predict` a call to `POST /predict` is done, and the JSON response
is viewed in a formatted table with a risk-based styling.

<img width="655" height="474" alt="Image" src="https://github.com/user-attachments/assets/849cb68b-d360-47d9-a49e-1a03b974e42d" />

### UI Customization

The UI customization is divided in three different files:

1. [**UI configuration**][file_ui_conf]. This file holds the UI configuration
   for the labels, descriptions, colors, risk bands, variables types and their
   accepted range, and the result formatting.
2. [**UI rendering and API calls**][file_ui_render]. This file holds all the
   functions involved in the page rendering and the API calls.
3. [**UI styling**][file_ui_style]. This file holds the UI styling.

The page shell can be found in the [HTML index file][file_ui_html].

## 6. Testing

FastAPI lifespan is best tested by using `TestClient` as a context manager so
startup/shutdown runs properly.

To run the tests, from the repository's root directory:

```bash
pytest -q
```

The two tests (in the `tests/` directory) cover:

1. Health endpoint returns `"ok"` and the model has been loaded
2. Predict endpoint returns a probability in [0, 1]

## 7. Limitations and Intended Use

- This project is intended for educational purposes.
- Predictions depend on the quality and representativeness of the training
  dataset, feature definitions, and model training.
- Output probabilities are model estimates and **should not** be interpreted
  as medical advice.

[dir_notebook]: ../notebooks
[docs_fastapi]: <https://fastapi.tiangolo.com/>
[docs_joblib]: <https://joblib.readthedocs.io/en/stable/>
[docs_redoc]: <https://redocly.com/docs/redoc>
[docs_scikit]: <https://scikit-learn.org/stable/index.html>
[docs_swagger]: <https://swagger.io/tools/swagger-ui/>
[file_readme]: ../README.md
[file_script]: ../scripts/train_and_export.py
[file_ui_conf]: ./static/ui_config.js
[file_ui_html]: ./templates/index.html
[file_ui_render]: ./static/app.js
[file_ui_style]: ./static/style.css
