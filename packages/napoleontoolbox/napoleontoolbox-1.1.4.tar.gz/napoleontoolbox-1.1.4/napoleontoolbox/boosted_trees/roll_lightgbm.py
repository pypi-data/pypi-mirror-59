#!/usr/bin/env python3
# coding: utf-8

from matplotlib import pyplot as plt
import torch

from sklearn.metrics import mean_squared_error
import lightgbm as lgb
from sklearn.multioutput import MultiOutputRegressor
import xgboost as xgb
import numpy as np

import shap
from napoleontoolbox.roller import roller

class RollLightGbm(roller._RollingBasis):
    def __init__(self, X, y, num_boost_round = 50, early_stopping_rounds = 50, x_type = None, y_type = None):
        """ Initialize rolling multi-layer perceptron model. """
        roller._RollingBasis.__init__(self, X, y)
        self.set_data(X=X, y=y, x_type=x_type, y_type=y_type)
        self.num_boost_round = num_boost_round
        self.early_stopping_rounds = early_stopping_rounds
        self.models = [None] * y.shape[1]
        # fitting
        self.multioutputregressor = MultiOutputRegressor(xgb.XGBRegressor(objective='reg:squarederror'))

    def set_roll_period(self, train_period, test_period, start=0, end=None,
                        roll_period=None, eval_period=None):
        """ Callable method to set target features data, and model.
        Parameters
        ----------
        train_period, test_period : int
            Size of respectively training and testing sub-periods.
        start : int, optional
            Starting observation, default is first observation.
        end : int, optional
            Ending observation, default is last observation.
        roll_period : int, optional
            Size of the rolling period, default is the same size of the
            testing sub-period.
        eval_period : int, optional
            Size of the evaluating period, default is the same size of the
            testing sub-period if training sub-period is large enough.
        batch_size : int, optional
            Size of a training batch, default is 64.
        epochs : int, optional
            Number of epochs, default is 1.
        Returns
        -------
        _RollingBasis
            The rolling basis model.
        """
        return roller._RollingBasis.set_roll_period(
            self, train_period=train_period, test_period=test_period,
            start=start, end=end, roll_period=roll_period,
            eval_period=eval_period
        )

    def _train(self, X, y):
        # predicting
        self.multioutputregressor.fit(X,y)


    def sub_predict(self, X):
        """ Predict. """
        preds = self.multioutputregressor.predict(X)
        return preds

    def set_data(self, X, y, x_type=None, y_type=None):
        """ Set data inputs and outputs.
        Parameters
        ----------
        X, y : array-like
            Respectively input and output data.
        x_type, y_type : torch.dtype
            Respectively input and ouput data types. Default is `None`.
        """
        if hasattr(self, 'N') and self.N != X.size(1):
            raise ValueError('X must have {} input columns'.foramt(self.N))

        if hasattr(self, 'M') and self.M != y.size(1):
            raise ValueError('y must have {} output columns'.format(self.M))

        self.X = self._set_data(X, dtype=x_type)
        self.y = self._set_data(y, dtype=y_type)
        self.T, self.N = self.X.shape
        T_veri, self.M = self.y.shape

        if self.T != T_veri:
            raise ValueError('{} time periods in X differents of {} time \
                             periods in y'.format(self.T, T_veri))

        return self

    def _set_data(self, X, dtype=None):
        """ Convert array-like data to tensor. """
        # TODO : Verify dtype of data torch tensor
        if isinstance(X, np.ndarray):

            return X

        elif isinstance(X, pd.DataFrame):
            # TODO : Verify memory efficiancy
            return X.values
        else:
            raise ValueError('Unkwnown data type: {}'.format(type(X)))



    def unroll(self):
        for eval_slice, test_slice in self:
            # Compute prediction on eval and test set
            self.y_eval[eval_slice] = self.sub_predict(self.X[eval_slice])
            test_prediction = self.sub_predict(self.X[test_slice])
            self.y_test[test_slice] = test_prediction

            # Update loss function of eval set and test set
            ev = self.y_eval[eval_slice]
            ev_true = self.y[eval_slice]

            tt = self.y_test[test_slice]
            tt_true = self.y[test_slice]

            self.loss_eval += [mean_squared_error(ev, ev_true)]
            self.loss_test += [mean_squared_error(tt, tt_true)]

            # Print loss on current eval and test set
            pct = (self.t - self.n - self.s) / (self.T - self.n - self.T % self.s)
            txt = '{:5.2%} is done | '.format(pct)
            txt += 'Eval loss is {:5.2} | '.format(self.loss_eval[-1])
            txt += 'Test loss is {:5.2} | '.format(self.loss_test[-1])
            if np.random.rand()>=0.8:
                print(txt)

    def eval_predictor_importance(self, features, features_names):
            explainer_shap = shap.GradientExplainer(model=self,
                                                data=features)
            # Fit the explainer on a subset of the data (you can try all but then gets slower)
            shap_values = explainer_shap.shap_values(X=features,
                                                     ranked_outputs=True)

            predictors_shap_values = shap_values[0]
            predictors_feature_order = np.argsort(np.sum(np.mean(np.abs(predictors_shap_values), axis=0), axis=0))

            predictors_left_pos = np.zeros(len(predictors_feature_order))

            predictors_class_inds = np.argsort([-np.abs(predictors_shap_values[i]).mean() for i in range(len(predictors_shap_values))])
            for i, ind in enumerate(predictors_class_inds):
                predictors_global_shap_values = np.abs(predictors_shap_values[ind]).mean(0)
                predictors_left_pos += predictors_global_shap_values[predictors_feature_order]

            predictors_ds = {}
            predictors_ds['features'] = np.asarray(features_names)[predictors_feature_order]
            predictors_ds['values'] = predictors_left_pos
            predictors_features_df = pd.DataFrame.from_dict(predictors_ds)
            values = {}
            for index, row in predictors_features_df.iterrows():
                values[row['features']]=row['values']

            return values



