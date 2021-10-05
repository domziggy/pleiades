import pandas as pd
from backEnd import plots
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import shap
import xgboost as xgb
from sklearn import preprocessing as prep

shap.initjs()

df = pd.read_csv('fetal_health.csv')
'''
dictionary for this data
    radiomic like features
    fetal health outcome
        1 = normal
        2 = suspect
        3 = pathological
'''
df.loc[df['fetal_health']==2] = 0
df.loc[df['fetal_health']==3] = 0
features = df.drop(['fetal_health'], axis=1)
outcomes = df['fetal_health']


# here would precede logic that accommodates feature sets and multiple outcome variables
x_train, x_val, y_train, y_val = train_test_split(features, outcomes, test_size=0.3)
train_data = xgb.DMatrix(x_train, label=y_train.values)
val_data = xgb.DMatrix(x_val, label=y_val.values)

params = {
    'eta': 0.5,
    'max_depth': 5,
    'objective': 'binary:logistic',
    'base_score': np.mean(y_train),
    'learning_rate': 0.1,
    'alpha': 10
    'eval_metric': ['logloss',]
}

model = xgb.train(params, train_data, 200, [(train_data,'train'),(val_data,'valid')], early_stopping_rounds=10, verbose_eval=25)

xgb_train = xgb.cv(params, train_data, 100, 5, metrics=('auc','logloss'), early_stopping_rounds=10, verbose_eval=20, seed=7)
xgb_val = xgb.cv(params, val_data, 200, 5, metrics=('auc','logloss'), early_stopping_rounds=10, verbose_eval=20, seed=7)

print(xgb_val.head())

explainer = shap.TreeExplainer(model)
xgb_shap_vals = explainer.shap_values(x_val)

#summary plot
shap.summary_plot(xgb_shap_vals, x_val)

#sort features by importance and display dependence plots
top_feats = np.argsort(-np.sum(np.abs(xgb_shap_vals), 0))

for i in range(len(features.columns)):
    shap.dependence_plot(top_feats[i], xgb_shap_vals, x_val)
    