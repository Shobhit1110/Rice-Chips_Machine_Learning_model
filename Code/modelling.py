# -*- coding: utf-8 -*-
"""Modelling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GTng_ov1fl-30xGgYZUehdkz3Y0wno7a

# 5 Modelling

***The conf_matrix function evaluates and visualizes the performance of a binary classification model. It calculates and prints training and test accuracies using the predicted labels (X_train_predicted and X_test_predicted) compared to the true labels (Y_train and Y_test). The confusion matrices for the training and test sets are then displayed using seaborn's heatmap, offering insights into the model's classification performance for each class.***
"""

def conf_matrix(X_train_predicted,X_test_predicted):
  train_accuracy = accuracy_score(Y_train, X_train_predicted)
  test_accuracy = accuracy_score(Y_test, X_test_predicted)

  print('Training Accuracy:\t', train_accuracy)
  print('Test  Accuracy:\t', test_accuracy)

  conf_matrix_train = confusion_matrix(Y_train,X_train_predicted)
  conf_matrix_test = confusion_matrix(Y_test, X_test_predicted)
  plt.figure(figsize=(12, 5))

  plt.subplot(1, 2, 1)
  sns.heatmap(conf_matrix_train, annot=True, fmt="d", cmap="Blues", xticklabels=['Class 0', 'Class 1'], yticklabels=['Class 0', 'Class 1'])
  plt.title('Confusion Matrix - Training Set')

  plt.subplot(1, 2, 2)
  sns.heatmap(conf_matrix_test, annot=True, fmt="d", cmap="Blues", xticklabels=['Class 0', 'Class 1'], yticklabels=['Class 0', 'Class 1'])
  plt.title('Confusion Matrix - Test Set')

  plt.show()

"""***The code includes seven machine learning algorithms. Each algorithm is individually initialized, trained on the given datasets, and its accuracy is evaluated on both the training and test sets.***

#Logistic Regression
"""

LR_model = make_pipeline(StandardScaler(), LogisticRegression(penalty='l2', C=10))
LR_model.fit(X_train_smote, Y_train_smote)
LR_X_train_predicted = LR_model.predict(X_train_fn)
LR_X_test_predicted = LR_model.predict(X_test_fn)

conf_matrix(LR_X_train_predicted, LR_X_test_predicted)

"""#Support Vector Classifier"""

SVC_model = LinearSVC(C=0.5)
SVC_model.fit(X_train_smote, Y_train_smote)
SVC_X_train_predicted = SVC_model.predict(X_train_fn)
SVC_X_test_predicted = SVC_model.predict(X_test_fn)

conf_matrix(SVC_X_train_predicted,SVC_X_test_predicted)

"""#Decision Tree"""

DT_model = DecisionTreeClassifier(max_depth=20, random_state=42)
DT_model.fit(X_train_smote, Y_train_smote)

DT_X_train_predicted =  DT_model.predict(X_train_fn)
DT_X_test_predicted = DT_model.predict(X_test_fn)

conf_matrix(DT_X_train_predicted,DT_X_test_predicted)

"""#Random Forest"""

RF_model = RandomForestClassifier(n_estimators=26, max_depth=14, random_state=42)
RF_model.fit(X_train_smote, Y_train_smote)

RF_X_train_predicted = RF_model.predict(X_train_fn)
RF_X_test_predicted = RF_model.predict(X_test_fn)
conf_matrix(RF_X_train_predicted,RF_X_test_predicted)

"""#Gradiant Boost"""

class_priors_original = np.bincount(Y_train) / len(Y_train)

NB_model = GaussianNB(priors=class_priors_original)
NB_model.fit(X_train_smote, Y_train_smote)

NB_X_train_predicted = NB_model.predict(X_train_fn)
NB_X_test_predicted = NB_model.predict(X_test_fn)
conf_matrix(NB_X_train_predicted,NB_X_test_predicted)

"""#XGBoost"""

dtrain_smote = xgb.DMatrix(X_train_smote, label=Y_train_smote)
dtrain = xgb.DMatrix(X_train_fn, label=Y_train)
dtest = xgb.DMatrix(X_test_fn, label=Y_test)

params = {
    'objective': 'binary:logistic',
    'eval_metric': 'logloss',
    'max_depth': 20,
    'learning_rate': 0.2,
    'subsample': 1,
    'colsample_bytree': 1,
    'seed': 42
}

num_rounds = 13
xgb_model = xgb.train(params, dtrain_smote, num_rounds)

Y_pred_probs = xgb_model.predict(dtest)
xgb_X_test_predicted = [1 if prob > 0.5 else 0 for prob in Y_pred_probs]
X_pred_probs = xgb_model.predict(dtrain)
xgb_X_train_predicted = [1 if prob > 0.5 else 0 for prob in X_pred_probs]
conf_matrix(xgb_X_train_predicted,xgb_X_test_predicted)

"""#KNeighborsClassifier"""

knn_model = KNeighborsClassifier(n_neighbors=1)

knn_model.fit(X_train_smote, Y_train_smote)

knn_X_train_predicted = knn_model.predict(X_train_fn)
knn_X_test_predicted = knn_model.predict(X_test_fn)

conf_matrix(knn_X_train_predicted,knn_X_test_predicted)