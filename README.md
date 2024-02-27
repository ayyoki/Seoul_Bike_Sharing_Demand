# Seoul Bike Sharing Demand Prediction Project + EDA + Deploy to a web page

# Demonstration
![Demonstration](https://img.youtube.com/vi/K4Ryf1VRX0E/0.jpg)



## Project Overview
The core objective of this project is to forecast the number of bicycles rented in Seoul using supervised machine learning techniques. By employing a regression algorithm, the project aims to predict bicycle rental counts based on a range of factors including temporal elements and environmental conditions.


## Model programming environment
The project used Google Colab as an environment for developing and training the model, providing access to free computing resources.

## Libraries Utilized
In this project, the following libraries are integral to our analysis and model development:

- `pandas`: For data manipulation and analysis.
- `numpy`: For numerical computing.
- `matplotlib.pyplot`: For creating static, interactive, and animated visualizations.
- `seaborn`: For statistical data visualization.
- `missingno`: For visualizing missing data.
- `xgboost`: For optimized gradient boosting machine learning algorithms.
- `sklearn`: For machine learning tools.
- `joblib`: For saving and loading models.

## Data Source
The dataset for this project can be accessed on Kaggle: [Seoul Bike Sharing Demand Prediction Dataset](https://www.kaggle.com/datasets/saurabhshahane/seoul-bike-sharing-demand-prediction/data).

### Data Set Details
- **Training Set**: Comprises 7,260 entries with 15 distinct columns.

### Attribute Information
- **Id**: Unique identifier for each entry.
- **Date**: Date (dd/mm/yyyy).
- **Hour**: Hour of the day (integer).
- **Temperature**: In degrees Celsius.
- **Humidity**: Percentage of humidity.
- **Wind Speed**: In meters per second.
- **Visibility**: In a 10-meter range.
- **Dew Point**: Dew point temperature in degrees Celsius.
- **Solar Radiation**: In MJ/m^2.
- **Rainfall**: In millimeters.
- **Snowfall**: In millimeters.

#### Categorical Columns
- **Season**: Winter, Spring, Summer, Autumn.
- **IsHoliday**: Indicates public holidays (1 for holiday, 0 for non-holiday).
- **IsFunctioningDay**: Indicates whether the hour is within working hours (1 for yes, 0 for no).

#### Target Column
- **Bikes_Rented**: The count of bikes rented during the specified hour and conditions.

## Model Building

### Model Used
- **XGBoost Regressor**

### Features Used
- Hour
- Temperature (°C)
- Humidity (%)
- Solar Radiation (MJ/m^2)
- Rainfall (mm)
- Snowfall (cm)
- Day
- Month
- Holiday_Holiday
- Holiday_No Holiday

### Model Selection
Hyperparameter tuning was carried out using `GridsearchCV` to identify the optimal model for regression.

### Metrics
The model's performance was evaluated using the following metrics:
- r2_score
- RMSE (Root Mean Square Error)
- MSE (Mean Square Error)
- MAE (Mean Absolute Error)

## Model Deployment
The model was deployed using the `Flask` web framework, facilitating interaction with the predictive model via a web interface.

The model itself is in '.pkl' format and is located at the following path:
\Seoul Bike Rental Prediction\Web Application\static\model