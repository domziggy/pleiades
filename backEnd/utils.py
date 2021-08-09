from sklearn.linear_model import LogisticRegression
from explainerdashboard.datasets import titanic_survive
from explainerdashboard import *

X_train, y_train, X_test, y_test = titanic_survive()
model = LogisticRegression()
model.fit(X_train, y_train)
model1 = LogisticRegression()
model1.fit(X_train+1, y_train)
explainer = ClassifierExplainer(model, X_test, y_test, 
                                    shap='linear', 
                                    X_background=X_train, 
                                    model_output='logodds',
                                    cats=['Sex', 'Deck', 'Embarked'])
explainer1 = ClassifierExplainer(model1, X_test, y_test, 
                                    shap='linear', 
                                    X_background=X_train, 
                                    model_output='logodds',
                                    cats=['Sex', 'Deck', 'Embarked'])
db1 = ExplainerDashboard(explainer)
db2 = ExplainerDashboard(explainer1)
hub = ExplainerHub([db1, db2])
hub.run()