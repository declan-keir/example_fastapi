# Rain Prediction Model Files

## 📁 Required Files

This folder should contain the following files from your experiment repository:

### 1. model.joblib
**What it is**: Your trained rain prediction model (binary classifier)

**How to create it** (in your experiments repo):
```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import joblib

# After training your model
model = LogisticRegression()  # Or RandomForest, XGBoost, etc.
model.fit(X_train_scaled, y_train)

# Save it
joblib.dump(model, 'model.joblib')
```

**Common model types**:
- LogisticRegression (simple, interpretable)
- RandomForestClassifier (good performance)
- GradientBoostingClassifier (often best performance)
- XGBClassifier (advanced)

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

### 3. threshold.txt
**What it is**: Optimal probability threshold for classifying rain/no-rain

**How to find it** (in your experiments repo):
```python
from sklearn.metrics import precision_recall_curve
import numpy as np

# Get predictions on validation set
y_pred_proba = model.predict_proba(X_val_scaled)[:, 1]

# Find optimal threshold (maximize F1 score)
precisions, recalls, thresholds = precision_recall_curve(y_val, y_pred_proba)
f1_scores = 2 * (precisions * recalls) / (precisions + recalls)
optimal_idx = np.argmax(f1_scores)
optimal_threshold = thresholds[optimal_idx]

print(f"Optimal threshold: {optimal_threshold}")

# Save it
with open('threshold.txt', 'w') as f:
    f.write(str(optimal_threshold))
```

**Common threshold values**:
- 0.5 (default, balanced)
- 0.3-0.4 (more sensitive, predict rain more often)
- 0.6-0.7 (more conservative, predict rain less often)

**How to choose**:
- High recall needed (don't miss rain days): lower threshold (0.3-0.4)
- High precision needed (avoid false alarms): higher threshold (0.6-0.7)
- Balanced: use F1-optimal threshold or 0.5

## 📝 Example threshold.txt file

The file should contain just a single number:
```
0.5
```

Or with more precision:
```
0.4827
```

## ✅ Checklist

Before deploying your API, make sure:

- [ ] model.joblib exists and is your trained rain classifier
- [ ] scaler.joblib exists and was fitted on your training data
- [ ] threshold.txt exists and contains a number between 0 and 1
- [ ] All three files are in this folder: `app/models/rain_or_not/`
- [ ] You can load them successfully:
  ```python
  import joblib
  model = joblib.load('model.joblib')
  scaler = joblib.load('scaler.joblib')
  with open('threshold.txt') as f:
      threshold = float(f.read())
  ```

## 🐛 Common Issues

### Issue: "FileNotFoundError: model.joblib not found"
**Solution**: Make sure you've copied model.joblib to this folder

### Issue: "ValueError: X has 10 features, but StandardScaler expected 11"
**Solution**:
- The features you're creating in `model_predictor.py` don't match your training
- Check the feature order in `prepare_rain_features()`
- Make sure it exactly matches your training code

### Issue: Model performs poorly in API
**Possible causes**:
1. Different scaler (fit a new one instead of using training scaler)
2. Different feature engineering (transforms don't match training)
3. Wrong feature order (features in different order than training)
4. Data leakage in training (used test data to fit scaler)

## 📊 Model Performance

Document your model's performance here (from experiments):

**Training Metrics** (example):
- Accuracy: 0.85
- Precision: 0.82
- Recall: 0.78
- F1 Score: 0.80
- AUC-ROC: 0.88

**Validation Metrics** (example):
- Accuracy: 0.83
- Precision: 0.80
- Recall: 0.76
- F1 Score: 0.78
- AUC-ROC: 0.86

**Test Metrics** (example):
- Accuracy: 0.82
- Precision: 0.79
- Recall: 0.75
- F1 Score: 0.77
- AUC-ROC: 0.85

**Model Type**: Logistic Regression with calibration

**Features Used**: 14 features including temperature, wind, solar radiation, seasonal encoding

**Training Data**: Historical Sydney weather 2015-2024 (excluding 2025)
