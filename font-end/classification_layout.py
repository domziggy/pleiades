from explainerdashboard.custom import *

class CustomPredictionsTab(ExplainerComponent):
    def __init__(self, explainer):
        super().__init__(explainer, title="Predictions")

        self.index = ClassifierRandomIndexComponent(explainer,
                                                    hide_title=True, hide_index=False,
                                                    hide_slider=True, hide_labels=True,
                                                    hide_pred_or_perc=True,
                                                    hide_selector=True, hide_button=False)

        self.contributions = ShapContributionsGraphComponent(explainer,
                                                            hide_title=True, hide_index=True,
                                                            hide_depth=True, hide_sort=True,
                                                            hide_orientation=True, hide_cats=True,
                                                            hide_selector=True,
                                                            sort='importance')

        self.trees = DecisionTreesComponent(explainer,
                                            hide_title=True, hide_index=True,
                                            hide_highlight=True, hide_selector=True)


        self.connector = IndexConnector(self.index, [self.contributions, self.trees])

        self.register_components()

    def layout(self):
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H3("Enter name:"),
                    self.index.layout()
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.H3("Contributions to prediction:"),
                    self.contributions.layout()
                ]),

            ]),
            dbc.Row([

                dbc.Col([
                    html.H3("Every tree in the Random Forest:"),
                    self.trees.layout()
                ]),
            ])
        ])
