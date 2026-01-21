# Predicting Coronary Diseases

Welcome to our final project!

In this repository you will find how we develop an API for a robust and accurate
**predictive model for use in coronary disease diagnosis** based on specific
markers or features.

## Table of Contents

1. [Repository Structure](#repository-structure)
2. [Stages of the Project](#stages-of-the-project)
3. [Per Stage Notes](#per-stage-notes)
4. [Collaborators](#collaborators)

## Repository Structure

This repository has been organized by grouping content in dedicated
directories.

- The `APP/` directory holds all the files required to use the model API. For
  a complete overview of the `APP/` directory, please refer to its own
  [README][docs_api].
- The `DATA/` directory holds all the dataframes used and created during the
  whole process:
    - [`coronary_disease.csv`][raw_data]. The raw dataframe
    - [`first_cleaned_df.csv`][first_data]. The first modified dataframe;
      obtained after the data cleaning step.
    - [`feat_engineered_df.csv`][feat_data]. The dataframe with the engineered
      features; obtained after the feature engineering and exploratory data
      analysis step.
    - [`cleaned_df.csv`][clean_df]. Final version of the dataframe; obtained
      after the normalization and correlation step.
- The `MODEL/` directory holds the [final model][final_model] and the
  JSON with the [feature schema][feature_schema] obtained in the validation
  and model selection step.
- The `NOTEBOOKS/` directory holds one reproducible jupyter notebook for each
  of the stages.
- The `SCRIPTS/` directory holds the script that merges all the steps done
  in the different notebooks into a single executable script. Please, read
  the script documentation for a detailed explanation.

In addition, the root directory contains the README you are reading, the
project [final report][report], and a [configuration file][pytest] for `pytest`
to be able to perform the API tests.

The structure of this repository can be seen in the tree below:

```console
coronary_disease_SP
├── app
│   ├── model
│   ├── static
│   ├── templates
│   ├── tests
│   ├── Dockerfile
│   ├── main.py
│   ├── preprocessing.py
│   ├── README.md
│   └── requirements.txt
├── data
│   ├── cleaned_df.csv
│   ├── coronary_disease.csv
│   ├── feat_engineered_df.csv
│   └── first_cleaned_df.csv
├── model
│   ├── feature_schema.json
│   └── final_model.pkl
├── notebooks
│   ├── 0_data_cleaning.ipynb
│   ├── 1_feat_engineering_and_eda.ipynb
│   ├── 2_normalization_correlation.ipynb
│   ├── 3_model_development.ipynb
│   └── 4_validation_and_model_selection.ipynb
├── scripts
│   └── train_and_export.py
├── pytest.ini
├── README.md
├── requirements.txt
└── project_report.pdf
```

## Stages of the Project

We decided to divide this project in 8 different stages. See the
[Collaborators](#collaborators) section to see who did what.

### Data Understanding and Cleaning

> Timeline: Dec 16 - Dec 18

The goal in this stage is to take the raw dataframe and turn it into a usable
and trustworthy one. To do so, the different tasks are:

- Inspect the fields, their types and ranges
- Rename the fields to consistent, readable names
- Detect missing values and decide how to handle them
- Check impossible values
- Identify obvious outliers

In addition, a short written summary of data quality and possible issues would
also be provided.

### Feature Engineering and Exploratory Data Analysis (EDA)

> Timeline: Dec 18 - Dec 21

The goal in this stage is to turn raw variables into model-ready features and
understand patterns. To do so, the different tasks are:

- Encode categorical variables
- Decide whether ordinal variables need special handling
- Create derived features
- Produce some plots
- Check separability between control and cases

The final output on this stage is going to be a feature-engineered dataframe
and EDA plots with brief observations.

### Normalization and Correlation

> Timeline: Dec 21 - Dec 24

The goal in this stage is to prepare features for stable and interpretable
modeling. To do so, the different tasks are:

- Normalize numerical variables
- Compute correlation matrix
- Identify highly correlated features
- Propose which features to keep or remove
- Finalize clean feature list

The final output on this stage is going to be a normalized dataset, a
correlation analysis summary and a final feature set recommendation.

### Model Development

> Timeline: Dec 24 - Dec 29

The goal in this stage is to train multiple predictive models for coronary
heart disease. To do so, the different tasks are:

- Split data into training and testing sets
- Train a Logistic Regression model
- Train a KNN model
- Train one tree-based model
- Address class imbalance (if needed)
- Record performance metrics

The final output on this stage is going to be a set of trained models and
initial performance metrics.

### Validation and Model Selection

> Timeline: Dec 29 - Jan 2

The goal in this stage is to objectively select the best model. To do so, the
different tasks are:

- Perform cross-validation or repeated train/test evaluation
- Compare the different models using accuracy, recall, and ROC-AUC
- Select the final model for deployment
- Define exact input feature schema

The final output on this stage is a validation report and the feature schema
of the selected final model.

### API Development

> Timeline: Jan 2 - Jan 8

The goal on this stage is to turn the model into a usable diagnostic API. To
do so, the different tasks are:

- Build an API (using FastAPI or similar)
- Create endpoint accepting patient markers
- Load the trained model and return prediction
- Return probability and coronary heart disease class
- Add input validation and documentation
- Write simple test requests

The final output on this stage is a functional API with documentation and test
examples.


### Deployment

> Timeline: Jan 6 - Jan 12

The goal on this stage is to make the API runnable anywhere. To do so, the
different tasks are:

- Write a Dockerfile
- Containerize the API
- Run and test locally or on a server
- Document the deployment steps

The final output on this stage is a Docker image with deployment instructions,
and a running deployed API.

### Final Integration

> Timeline: Jan 12 - Jan 16

The goal in this final stage is to deliver a complete, polished project. To do
so, the different tasks are:

- Improve the model (if needed)
- Ensure the API and model work together
- Write the final report
- Record the demo or presentation video

The final output is going to be a complete report with a demo video, and the
end-to-end predictive system.

## Per Stage Notes

### Data Understanding and Cleaning

We loaded the [coronary dataset][raw_data], which contains 4,238 rows and 16
columns, and observed that the **target variable is imbalanced**, with
approximately 15% positive cases. To improve clarity and avoid
misunderstandings among collaborators, we renamed the variables using more
descriptive names. We then removed around 500 rows containing missing values.
After cleaning the data, we checked for negative values in variables where
they are not physiologically plausible. Finally, we explored the presence of
outliers using boxplots and interquartile range (IQR) calculations.

### Feature Engineering and EDA

Two derived features were created to capture clinically meaningful information
beyond the raw variables. **Smoker intensity** was defined as the product of
current smoking status and the number of cigarettes smoked per day, allowing
differentiation between non-smokers, light smokers, and heavy smokers, while
assigning zero exposure to non-smokers. **Pulse pressure** was computed as the
difference between systolic and diastolic blood pressure and serves as an
indicator of arterial stiffness and cardiovascular risk. These engineered
features aim to incorporate interaction effects and physiological relationships
that may not be fully captured by individual variables alone.

The data frame was saved as [`feat_engineered_df.csv`][feat_data].

Exploratory data analysis was conducted to examine the relationship between
baseline characteristics and ten-year coronary heart disease (CHD) status. Age,
pulse pressure and systolic blood pressure show the strongest univariate
associations with CHD, with distributions for CHD cases shifted toward higher
values compared to non-CHD cases. However, substantial overlap remains,
indicating only moderate separability when these variables are considered
individually. Other continuous variables, including diastolic blood pressure,
body mass index, glucose, and total cholesterol, exhibit weaker differences
and considerable overlap between groups. Categorical variables such as sex,
prevalent hypertension, blood pressure medication use, and diabetes suggest
associations with CHD risk, although small subgroup sizes and class imbalance
limit their standalone discriminatory power. Overall, no single variable
clearly separates CHD from non-CHD cases, highlighting the need for
multivariable modeling to capture combined effects.

### Normalization and Correlation

The **continuous variables were standardized** using z‑score normalization to
ensure that all features operated on a comparable scale (mean $\approx$ 0,
standard deviation $\approx$ 1). This step stabilizes distance‑based
relationships, prevents scale‑driven dominance in correlation analysis, and
prepares the dataset for interpretable modeling. A pre‑normalization summary
confirmed the heterogeneity of the original scales, while post‑normalization
checks validated that the transformation was applied correctly across all
numerical variables.

A **full correlation matrix and heatmap** were computed to identify linear
dependencies between predictors. Several moderate correlations were observed,
and one strong relationship emerged between systolic blood pressure and pulse
pressure ($r = 0.86$). This association is clinically expected, as pulse
pressure is derived from systolic and diastolic blood pressure. Beyond this
physiological dependency, no additional pairs exceeded the high‑correlation
threshold ($|r| \geq 0.8$), indicating limited multicollinearity in the dataset.

**Feature selection** was focused on removing redundant or overlapping
predictors while preserving clinically meaningful information. The variable
`cigs_per_day` was dropped because its information was fully captured by the
engineered feature `smoker_intensity`, which better represents smoking
exposure. All remaining variables were retained, including both systolic
blood pressure and pulse pressure, as they provide complementary insights into
cardiovascular physiology. The [final cleaned dataset][clean_df] contains 17
well‑defined features, free from unnecessary redundancy and ready for downstream
modeling.

Overall, this section delivers a normalized dataset, a clear correlation
analysis, and a transparent, clinically grounded feature‑selection process
that ensures stability, interpretability, and reproducibility for subsequent
modeling steps.

### Model Development

In this section 4 different architectures have been used to develop different
models in order to predict the coronary heart disease.

To obtain the metrics for each model, the dataset has been split into two
datasets in a 0.8/0.2 proportion, so no cross-validation has been done, and
the metrics might be optimistic. Class unbalanced has been addressed, and
different models changing hyperparameters have been tested to try to obtain the
best results. The trained models are saved in dictionaries for each
architecture and the results for each model are displayed. These results include
accuracy, recall and other important statistics.

The results obtained show that none of the models used is perfect and some more
advanced and complex models might be needed in order to obtain the best results.

### Validation and Model Selection

A total of 16 candidate models across four families were defined and assessed:
- 4 logistic regressions (varying regularization and class weights)
- 4 random forests (varying depth and balancing)
- 4 four SVMs (different kernels and regularisation)
- 4 four KNeighbour’s classifiers (varying neighbours and algorithms)

For all of them, a consistent 5-fold stratified cross-validation strategy was
applied to ensure fair comparisons, computing accuracy, recall, precision,
F1-score, and ROC-AUC for each configuration. Given the preventive nature of
CHD risk prediction, recall was prioritised to minimise missed high-risk cases,
while maintaining acceptable F1-score and ROC-AUC to control false positives.

Models were first evaluated grouped by families, resulting in logistic
regression as the strongest contender. SVM and KNN showed very low recall
(<0.13), making them unsuitable, and therefore discard, while random forests
offered moderate performance (best RF recall ~0.56).

Among logistic models, LR_Hard_Penalization (`class_weight={0:1, 1:10}`)
achieved the highest recall (0.85), with F1-score = 0.34 and ROC-AUC = 0.73.
Comparative bar plots were used to make more visible the differences across
the finalists (LR_C01, LR_C10, LR_Hard_Penalization, RF_Limited_Depth).

The final model was trained on the full dataset and exported as
[`final_model.pkl`][final_model] for deployment.

### API Development

The API development has been detailed in it dedicated [README][docs_api]. In
general, a scikit-learn `Pipeline` was generated by integrating all the
previous work on a single Python [script][script], and the API was created
using FastAPI with a user interface in order to ease the user's input process.

### Deployment

To make sure the application is both accessible and easy to reproduce, we 
containerized the API using **Docker**. By creating a dedicated `Dockerfile`, 
we bundled the entire environment, dependencies, and our model pipeline into 
a single package. This guarantees that the tool performs consistently, 
no matter where it's running.

For the final step, we deployed the containerized app to the cloud using 
**Render**. This moves the predictive model from a local setup to a public 
web interface, allowing anyone to interact with it in real-time without 
needing to install anything locally.

**Note**  
For a deeper dive into the technical setup or cloud configuration, 
feel free to check out the **[(Deployed) API][docs_deploy]** section in 
the App documentation.


## Collaborators

- [Pol Jardí Yanes][pol] | Data understanding and cleaning | Final integration
- [Johanna Albers][johanna] | Feature engineering and EDA | Final integration
- [Miguel González González][miguel] | Normalization and correlation | Final integration
- [César Merino Fidalgo][cesar] | Model development | Final integration
- [Miriam Cegarra Cuquerella][miriam] | Validation and model selection | Final integration
- [Iris Mestres Pascual][iris] | API Development | Final integration
- [Jan Carreras Boada][jan] | Deployment | Final integration

[cesar]: <cesar.merino@estudiants.urv.cat>
[clean_df]: ./data/cleaned_df.csv
[docs_api]: ./app/README.md
[feat_data]: ./data/feat_engineered_df.csv
[feature_schema]: ./model/feature_schema.json
[final_model]: ./model/final_model.pkl
[first_data]: ./data/first_cleaned_df.csv
[iris]: <iris.mestres@estudiants.urv.cat>
[jan]: <jan.carreras@estudiants.urv.cat>
[johanna]: <johanna.albers@estudiants.urv.cat>
[miguel]: <miguel.gonzalez@estudiants.urv.cat>
[miriam]: <miriam.cegarra@estudiants.urv.cat>
[pol]: <pol.jardi@estudiants.urv.cat>
[pytest]: pytest.ini
[raw_data]: ./data/coronary_disease.csv
[report]: project_report.pdf
[script]: ./scripts/train_and_export.py
[docs_deploy]: ./app/README.md#4-deployed-api
