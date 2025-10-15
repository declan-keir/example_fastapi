# Precipitation Prediction Model Files

## 📁 Required Files

This folder should contain the following files from your experiment repository:

### 1. model.joblib
**What it is**: Your trained precipitation prediction model (regression)

**How to create it** (in your experiments repo):
```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from lightgbm import LGBMRegressor
import joblib

# After training your model
model = LGBMRegressor()  # Or LinearRegression, RandomForest, etc.
model.fit(X_train_scaled, y_train)

# Save it
joblib.dump(model, 'model.joblib')
```

**Common model types for regression**:
- LinearRegression (simple, fast)
- Ridge (linear with regularization)
- RandomForestRegressor (good performance)
- GradientBoostingRegressor (often best)
- LGBMRegressor (fast and accurate)
- XGBRegressor (advanced)

### 2. scaler.joblib
**What it is**: StandardScaler fitted on your training data

**How to create it** (in your experiments repo):
```python
from sklearn.preprocessing import StandardScaler
import joblib

# Create and fit scaler on training data
scaler = StandardScaler()
scaler.fit(X_train)  # Fit on TRAINING data only (not test!)

# Use it to transform
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save it
joblib.dump(scaler, 'scaler.joblib')
```

**CRITICAL**:
- Fit the scaler ONLY on training data
- Never fit on test data (that's data leakage!)
- Use the same scaler for train, validation, and test

## ✅ Checklist

Before deploying your API, make sure:

- [ ] model.joblib exists and is your trained precipitation regressor
- [ ] scaler.joblib exists and was fitted on your training data
- [ ] Both files are in this folder: `app/models/precipitation_fall/`
- [ ] You can load them successfully:
  ```python
  import joblib
  model = joblib.load('model.joblib')
  scaler = joblib.load('scaler.joblib')
  ```

## 🐛 Common Issues

### Issue: "FileNotFoundError: model.joblib not found"
**Solution**: Make sure you've copied model.joblib to this folder

### Issue: "ValueError: X has 11 features, but StandardScaler expected 13"
**Solution**:
- The features you're creating in `model_predictor.py` don't match your training
- Check the feature order in `prepare_precipitation_features()`
- Make sure it exactly matches your training code

### Issue: Model predicts negative precipitation
**Solution**:
- The API already handles this with `max(0, prediction)`
- But consider:
  - Using a model that can't predict negative (e.g., with log transform)
  - Training with non-negative constraints
  - Checking for data quality issues

### Issue: Model predictions are very different from training
**Possible causes**:
1. Different scaler (fit a new one instead of using training scaler)
2. Different feature engineering (transforms don't match training)
3. Wrong feature order (features in different order than training)
4. Data leakage in training (used future data)

## 📊 Model Performance

Document your model's performance here (from experiments):

**Training Metrics** (example):
- MAE (Mean Absolute Error): 2.5 mm
- RMSE (Root Mean Squared Error): 4.2 mm
- R² Score: 0.72
- MAPE (Mean Absolute Percentage Error): 18%

**Validation Metrics** (example):
- MAE: 2.8 mm
- RMSE: 4.6 mm
- R² Score: 0.68
- MAPE: 20%

**Test Metrics** (example):
- MAE: 2.9 mm
- RMSE: 4.8 mm
- R² Score: 0.66
- MAPE: 21%

**Model Type**: LightGBM Regressor

**Features Used**: 13 features including precipitation history, temperature, sunshine, wind, seasonal encoding

**Training Data**: Historical Sydney weather 2015-2024 (excluding 2025)

## 🎯 Interpreting Results

**MAE (Mean Absolute Error)**:
- Average difference between predicted and actual precipitation
- Example: MAE=2.5mm means predictions are off by 2.5mm on average
- Lower is better

**RMSE (Root Mean Squared Error)**:
- Similar to MAE but penalizes large errors more
- Always >= MAE
- Lower is better

**R² Score**:
- How much variance in the data is explained by the model
- Range: -∞ to 1
- 1.0 = perfect predictions
- 0.0 = predicting the mean
- Negative = worse than predicting the mean
- Typical good value: 0.6-0.9

**MAPE (Mean Absolute Percentage Error)**:
- Average percentage error
- Example: MAPE=20% means predictions are off by 20% on average
- Lower is better
- Note: Can be very high when actual values are close to 0

## 💡 Tips for Better Models

1. **Feature Engineering**:
   - Include precipitation from previous days
   - Add seasonal features (month, season)
   - Try circular encoding for cyclical features (wind direction, month)
   - Add interaction features (temp * humidity)

2. **Model Selection**:
   - Start simple (LinearRegression)
   - Try ensemble methods (RandomForest, GradientBoosting)
   - Use LightGBM or XGBoost for best performance
   - Compare multiple models

3. **Hyperparameter Tuning**:
   - Use GridSearchCV or RandomizedSearchCV
   - Tune on validation set, not test set
   - Important hyperparameters:
     - For RandomForest: n_estimators, max_depth, min_samples_split
     - For GradientBoosting: n_estimators, learning_rate, max_depth
     - For LightGBM: n_estimators, learning_rate, num_leaves

4. **Validation Strategy**:
   - Use time-based splits (don't shuffle time series data!)
   - Train on earlier dates, validate on later dates
   - Use cross-validation with TimeSeriesSplit

5. **Handling Zeros**:
   - Many days have 0mm precipitation
   - Consider two-stage model:
     - Stage 1: Will it rain? (classification)
     - Stage 2: How much? (regression on rainy days only)
   - Or use models that handle zero-inflated data
