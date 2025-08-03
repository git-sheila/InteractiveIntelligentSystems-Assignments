import logging
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier, HistGradientBoostingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, make_scorer, f1_score

# Set logging level
logging.getLogger().setLevel(logging.WARNING)

# Load augmented dataset
data = pd.read_csv("augmented_dataset.csv")
labels = data["emotion"].values
features = data.drop(columns=["emotion"]).values

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    features,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels #test train bhaag korle, jei ratio te pura data ase, shei ratio tei test train split hobe 
)

# Define models
models = {
    "KNN": KNeighborsClassifier(),
    "Radius Neighbors": RadiusNeighborsClassifier(),
    "SVC": SVC(),
    "Linear SVC": LinearSVC(),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(random_state=42, class_weight='balanced'), 
    "Extra Trees": ExtraTreesClassifier(random_state=42),
    "AdaBoost": AdaBoostClassifier(algorithm="SAMME", random_state=42),
    "Hist Gradient Boosting": HistGradientBoostingClassifier(random_state=42),
    "XGBoost": XGBClassifier(eval_metric='logloss', random_state=42),
    "LightGBM": LGBMClassifier(force_col_wise=True, random_state=42, verbose=-1),
    "MLP Classifier": MLPClassifier(max_iter=2000, random_state=42),
    "Naive Bayes": GaussianNB()
}

# Define parameter grids for hyperparameter tuning
param_grids = {
    "KNN": {
        "n_neighbors": [3, 5, 10],
        "weights": ["uniform", "distance"]
    },
    "Radius Neighbors": {
        "radius": [1.0, 1.5, 2.0]
    },
    "SVC": {
        "C": [0.1, 1, 10],
        "kernel": ["linear", "rbf"],
        "gamma": ["scale", "auto"]
    },
    "Linear SVC": {
        "C": [0.1, 1, 10]
    },
    "Decision Tree": {
        "max_depth": [5, 10, 20],
        "min_samples_split": [2, 5, 10]
    },
    "Random Forest": {
        "n_estimators": [50, 100, 200],
        "max_depth": [5, 10, None],
        "min_samples_split": [2, 5]
    },
    "Extra Trees": {
        "n_estimators": [50, 100, 200],
        "max_depth": [5, 10, None]
    },
    "AdaBoost": {
        "n_estimators": [50, 100, 200],
        "learning_rate": [0.01, 0.1, 1]
    },
    "Hist Gradient Boosting": {
        "max_iter": [100, 200],
        "learning_rate": [0.01, 0.1, 0.2]
    },
    "XGBoost": {
        "n_estimators": [50, 100, 200],
        "max_depth": [3, 6, 10],
        "learning_rate": [0.01, 0.1, 0.3]
    },
    "LightGBM": {
        "n_estimators": [50, 100, 200],
        "learning_rate": [0.01, 0.1, 0.3]
    },
    "MLP Classifier": {
        "hidden_layer_sizes": [(100,), (100, 50), (50, 25)],
        "alpha": [0.0001, 0.001]
    },
    "Naive Bayes": {
        "var_smoothing": [1e-9, 1e-8, 1e-7]
    }
}

# Function for hyperparameter tuning
def hyperparameter_tuning(model, param_grid, X_train, y_train):
    f1_scorer = make_scorer(f1_score, average='weighted') #imbalance ke balance kore
    grid_search = GridSearchCV(
        model,
        param_grid,
        cv=5, #cross validation e koy fold hobe
        scoring=f1_scorer,
        verbose=1, #kototuk detailed output dibe
        n_jobs=-1 
    )
    grid_search.fit(X_train, y_train) #shob rokom comb chalabe taking from the param grid 
    return grid_search.best_params_, grid_search.best_score_, grid_search.best_estimator_

# Train, tune, and evaluate each model
for name, model in models.items():
    print(f"\nPerforming hyperparameter tuning for {name}...")
    param_grid = param_grids.get(name, None)
    if param_grid:
        best_params, best_score, best_model = hyperparameter_tuning(model, param_grid, X_train, y_train)
        print(f"Best Parameters for {name}: {best_params}")
        print(f"Best Cross-Validation Score for {name}: {best_score}")
        
        # Evaluate on test data
        y_pred = best_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, zero_division=0)
        
        print(f"{name} Test Accuracy: {accuracy}")
        print(f"{name} Test Classification Report:\n{report}")
        
        # Save the best model
        model_filename = f"best_{name.lower().replace(' ', '_')}_model.pkl"
        joblib.dump(best_model, model_filename)
        print(f"Best {name} model saved to {model_filename}")
    else:
        print(f"No parameter grid defined for {name}.")
