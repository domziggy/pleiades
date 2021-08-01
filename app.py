from explainerdashboard import ExplainerDashboard


ExplainerDashboard(explainer, [CustomModelTab, CustomPredictionsTab], 
                        title='Titanic Explainer', header_hide_selector=True,
                        bootstrap=FLATLY).run()