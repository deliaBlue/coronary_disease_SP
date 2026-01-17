# Predicting Coronary Diseases

Welcome to our final project!

In this repository you will find how we develop an API for a robust and accurate
**predictive model for use in coronary disease diagnosis** based on specific
markers or features.

## Table of Contents

1. [Stages of the Project](#stages-of-the-project)
2. [Collaborators](#collaborators)

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

## Collaborators

- [Pol Jardí Yanes][pol] | Data understanding and cleaning | Final integration
- [Johanna Albers][johanna] | Feature engineering and EDA | Final integration
- [Miguel González González][miguel] | Normalization and correlation | Final integration
- [César Merino Fidalgo][cesar] | Model development | Final integration
- [Miriam Cegarra Cuquerella][miriam] | Validation and model selection | Final integration
- [Iris Mestres Pascual][iris] | API Development | Final integration
- [Jan Carreras Boada][jan] | Deployment | Final integration



[cesar]: <cesar.merino@estudiants.urv.cat>
[iris]: <iris.mestres@estudiants.urv.cat>
[jan]: <jan.carreras@estudiants.urv.cat>
[johanna]: <johanna.albers@estudiants.urv.cat>
[miguel]: <miguel.gonzalez@estudiants.urv.cat>
[miriam]: <miriam.cegarra@estudiants.urv.cat>
[pol]: <pol.jardi@estudiants.urv.cat>

## Collaborators notes
Collaborator 1: We loaded the coronary dataset, which contains 4,238 rows and 16 columns, and observed that the target variable is imbalanced, with approximately 15% positive cases. To improve clarity and avoid misunderstandings among collaborators, we renamed the variables using more descriptive names. We then removed around 500 rows containing missing values. After cleaning the data, we checked for negative values in variables where they are not physiologically plausible. Finally, we explored the presence of outliers using boxplots and interquartile range (IQR) calculations.

Collaborator 2: 
Two derived features were created to capture clinically meaningful information beyond the raw variables. Smoker intensity was defined as the product of current smoking status and the number of cigarettes smoked per day, allowing differentiation between non-smokers, light smokers, and heavy smokers, while assigning zero exposure to non-smokers. Pulse pressure was computed as the difference between systolic and diastolic blood pressure and serves as an indicator of arterial stiffness and cardiovascular risk. These engineered features aim to incorporate interaction effects and physiological relationships that may not be fully captured by individual variables alone.
The data frame was saved as engineered_df.csv.

Exploratory data analysis was conducted to examine the relationship between baseline characteristics and ten-year coronary heart disease (CHD) status. Age, pulse pressure and systolic blood pressure show the strongest univariate associations with CHD, with distributions for CHD cases shifted toward higher values compared to non-CHD cases. However, substantial overlap remains, indicating only moderate separability when these variables are considered individually. Other continuous variables, including diastolic blood pressure, body mass index, glucose, and total cholesterol, exhibit weaker differences and considerable overlap between groups. Categorical variables such as sex, prevalent hypertension, blood pressure medication use, and diabetes suggest associations with CHD risk, although small subgroup sizes and class imbalance limit their standalone discriminatory power. Overall, no single variable clearly separates CHD from non-CHD cases, highlighting the need for multivariable modeling to capture combined effects.

Collaborator 3: The continuous variables were standardized using z‑score normalization to ensure that all features operated on a comparable scale (mean ≈ 0, standard deviation ≈ 1). This step stabilizes distance‑based relationships, prevents scale‑driven dominance in correlation analysis, and prepares the dataset for interpretable modeling. A pre‑normalization summary confirmed the heterogeneity of the original scales, while post‑normalization checks validated that the transformation was applied correctly across all numerical variables.

A full correlation matrix and heatmap were computed to identify linear dependencies between predictors. Several moderate correlations were observed, and one strong relationship emerged between systolic blood pressure and pulse pressure (r = 0.86). This association is clinically expected, as pulse pressure is derived from systolic and diastolic blood pressure. Beyond this physiological dependency, no additional pairs exceeded the high‑correlation threshold (|r| ≥ 0.8), indicating limited multicollinearity in the dataset.

Feature selection focused on removing redundant or overlapping predictors while preserving clinically meaningful information. The variable *cigs_per_day* was dropped because its information was fully captured by the engineered feature *smoker_intensity*, which better represents smoking exposure. All remaining variables were retained, including both systolic blood pressure and pulse pressure, as they provide complementary insights into cardiovascular physiology. The final cleaned dataset contains 17 well‑defined features, free from unnecessary redundancy and ready for downstream modeling.

Overall, this section delivers a normalized dataset, a clear correlation analysis, and a transparent, clinically grounded feature‑selection process that ensures stability, interpretability, and reproducibility for subsequent modeling steps.

Collaborator 5: A total of 16 candidate models across four families were defined and assessed: four logistic regressions (varying regularisation and class weights), four random forests (varying depth and balancing), four SVMs (different kernels and regularisation), and four KNeighbour’s classifiers (varying neighbours and algorithms). For all of them, a consistent 5-fold stratified cross-validation strategy was applied to ensure fair comparisons, computing accuracy, recall, precision, F1-score, and ROC-AUC for each configuration. Given the preventive nature of CHD risk prediction, recall was prioritised to minimise missed high-risk cases, while maintaining acceptable F1-score and ROC-AUC to control false positives.
Models were first evaluated grouped by families, resulting in logistic regression as the strongest contender. SVM and KNN showed very low recall (<0.13), making them unsuitable, and therefore discard, while random forests offered moderate performance (best RF recall ~0.56). Among logistic models, LR_Hard_Penalization (class_weight={0:1, 1:10}) achieved the highest recall (0.85), with F1-score 0.34 and ROC-AUC 0.73. Comparative bar plots were used to make more visible the differences across the finalists (LR_C01, LR_C10, LR_Hard_Penalization, RF_Limited_Depth). The final model was trained on the full dataset and exported as final_model.pkl for deployment.
