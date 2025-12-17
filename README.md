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
- Create simple derived features (if/when useful)
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
