#!/usr/bin/env python3
# coding: utf-8


import pandas as pd
import torch
import torch.nn
import numpy as np
import torch.nn.functional as F

from sklearn.metrics import mean_squared_error

from napoleontoolbox.roller import roller

class BaseNeuralNet(torch.nn.Module):
    """ Base object for neural network model with PyTorch.
    Inherits of torch.nn.Module object with some higher level methods.
    Attributes
    ----------
    criterion : torch.nn.modules.loss
        A loss function.
    optimizer : torch.optim
        An optimizer algorithm.
    N, M : int
        Respectively input and output dimension.
    Methods
    -------
    set_optimizer
    train_on
    predict
    set_data
    See Also
    --------
    MultiLayerPerceptron, RollingBasis
    """

    def __init__(self):
        """ Initialize. """
        torch.nn.Module.__init__(self)

    def set_optimizer(self, criterion, optimizer, **kwargs):
        """ Set the optimizer object.
        Set optimizer object with specified `criterion` as loss function and
        any `kwargs` as optional parameters.
        Parameters
        ----------
        criterion : torch.nn.modules.loss
            A loss function.
        optimizer : torch.optim
            An optimizer algorithm.
        **kwargs
            Keyword arguments of `optimizer`, cf PyTorch documentation [1]_.
        Returns
        -------
        BaseNeuralNet
            Self object model.
        References
        ----------
        .. [1] https://pytorch.org/docs/stable/optim.html
        """
        self.criterion = criterion()
        self.optimizer = optimizer(self.parameters(), **kwargs)

        return self

    @torch.enable_grad()
    def train_on(self, X, y):
        """ Trains the neural network model.
        Parameters
        ----------
        X, y : torch.Tensor
            Respectively inputs and outputs to train model.
        Returns
        -------
        torch.nn.modules.loss
            Loss outputs.
        """
        self.optimizer.zero_grad()
        outputs = self(X)
        loss = self.criterion(outputs, y)
        loss.backward()
        self.optimizer.step()
        return loss.item()

    @torch.no_grad()
    def predict(self, X):
        """ Predicts outputs of neural network model.
        Parameters
        ----------
        X : torch.Tensor
           Inputs to compute prediction.
        Returns
        -------
        torch.Tensor
           Outputs prediction.
        """
        return self(X).detach()

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
        self.T, self.N = self.X.size()
        T_veri, self.M = self.y.size()

        if self.T != T_veri:
            raise ValueError('{} time periods in X differents of {} time \
                             periods in y'.format(self.T, T_veri))

        return self

    def _set_data(self, X, dtype=None):
        """ Convert array-like data to tensor. """
        # TODO : Verify dtype of data torch tensor
        if isinstance(X, np.ndarray):

            return torch.from_numpy(X)

        elif isinstance(X, pd.DataFrame):
            # TODO : Verify memory efficiancy
            return torch.from_numpy(X.values)

        elif isinstance(X, torch.Tensor):

            return X

        else:
            raise ValueError('Unkwnown data type: {}'.format(type(X)))


class MultiLayerPerceptron(BaseNeuralNet):
    r""" Neural network with MultiLayer Perceptron architecture.
    Refered as vanilla neural network model, with `n` hidden layers s.t
    n :math:`\geq` 1, with each one a specified number of neurons.
    Parameters
    ----------
    X, y : array-like
        Respectively inputs and outputs data.
    layers : list of int
        List of number of neurons in each hidden layer.
    activation : torch.nn.Module
        Activation function of layers.
    drop : float, optional
        Probability of an element to be zeroed.
    Attributes
    ----------
    criterion : torch.nn.modules.loss
        A loss function.
    optimizer : torch.optim
        An optimizer algorithm.
    n : int
        Number of hidden layers.
    layers : list of int
        List with the number of neurons for each hidden layer.
    f : torch.nn.Module
        Activation function.
    Methods
    -------
    set_optimizer
    train_on
    predict
    set_data
    See Also
    --------
    BaseNeuralNet, RollMultiLayerPerceptron
    """

    def __init__(self, X, y, layers=[], activation=None, drop=None,
                 x_type=None, y_type=None, bias=True, activation_kwargs={}):
        """ Initialize object. """
        BaseNeuralNet.__init__(self)

        self.set_data(X=X, y=y, x_type=x_type, y_type=y_type)
        layers_list = []
        self.n_layers =  len(layers)
        # Set input layer
        input_size = self.N
        for output_size in layers:
            # Set hidden layers
            layers_list += [torch.nn.Linear(
                input_size,
                output_size,
                bias=bias
            )]
            input_size = output_size

        # Set output layer
        layers_list += [torch.nn.Linear(input_size, self.M, bias=bias)]
        self.layers = torch.nn.ModuleList(layers_list)


        # Set activation functions
        # Set activation functions
        if activation is None:
            self.activation = lambda x: x
        else:
            self.activation = activation

        # Set dropout parameters
        if drop is not None:
            self.drop = torch.nn.Dropout(p=drop)

        else:
            self.drop = lambda x: x

    def forward(self, x):
        """ Forward computation. """
        x = self.drop(x)
        for name, layer in enumerate(self.layers):
            if name == (self.n_layers) and self.activation.__name__ == F.relu.__name__:
                x = layer(x)
            else:
                x = self.activation(layer(x))

        return x


def _type_convert(dtype):
    if dtype is np.float64 or dtype is np.float or dtype is np.double:
        return torch.float64

    elif dtype is np.float32:
        return torch.float32

    elif dtype is np.float16:
        return torch.float16

    elif dtype is np.uint8:
        return torch.uint8

    elif dtype is np.int8:
        return torch.int8

    elif dtype is np.int16 or dtype is np.short:
        return torch.int16

    elif dtype is np.int32:
        return torch.int32

    elif dtype is np.int64 or dtype is np.int or dtype is np.long:
        return torch.int64

    else:
        raise ValueError('Unkwnown type: {}'.format(str(dtype)))
#
# class _RollingBasis:
#     """ Base object to roll a neural network model.
#     Rolling over a time axis with a train period from `t - n` to `t` and a
#     testing period from `t` to `t + s`.
#     Parameters
#     ----------
#     X, y : array_like
#         Respectively input and output data.
#     f : callable, optional
#         Function to transform target, e.g. ``torch.sign`` function.
#     index : array_like, optional
#         Time index of data.
#     Methods
#     -------
#     __call__
#     Attributes
#     ----------
#     n, s, r : int
#         Respectively size of training, testing and rolling period.
#     b, e, T : int
#         Respectively batch size, number of epochs and size of entire dataset.
#     t : int
#         The current time period.
#     y_eval, y_test : np.ndarray[ndim=1 or 2, dtype=np.float64]
#         Respectively evaluating (or training) and testing predictions.
#     """
#
#     # TODO : other methods
#     def __init__(self, X, y, f=None, index=None):
#         """ Initialize shape of target. """
#         self.T = X.shape[0]
#         self.y_shape = y.shape
#
#         if f is None:
#             self.f = lambda x: x
#
#         else:
#             self.f = f
#
#         if index is None:
#             self.idx = np.arange(self.T)
#
#         else:
#             self.idx = index
#
#     # TODO : fix callable method to overwritten problem with torch.nn.Module
#     def __call__(self, train_period, test_period, start=0, end=None,  epochs=1):
#         """ Callable method to set target features data, and model.
#         Parameters
#         ----------
#         train_period, test_period : int
#             Size of respectively training and testing sub-periods.
#         start : int, optional
#             Starting observation, default is first observation.
#         end : int, optional
#             Ending observation, default is last observation.
#         roll_period : int, optional
#             Size of the rolling period, default is the same size of the
#             testing sub-period.
#         eval_period : int, optional
#             Size of the evaluating period, default is the same size of the
#             testing sub-period if training sub-period is large enough.
#         batch_size : int, optional
#             Size of a training batch, default is 64.
#         epochs : int, optional
#             Number of epochs on the same subperiod, default is 1.
#         Returns
#         -------
#         _RollingBasis
#             The rolling basis model.
#         """
#         # Set size of subperiods
#         self.n = train_period
#         self.s = test_period
#         self.e = epochs
#
#         # Set boundary of period
#         self.T = self.T if end is None else min(self.T, end)
#         self.t = max(self.n - self.s, start)
#
#         return self
#
#     def __iter__(self):
#         """ Set iterative method. """
#         self.y_eval = np.zeros(self.y_shape)
#         self.y_test = np.zeros(self.y_shape)
#         self.loss_train = []
#         self.loss_eval = []
#         self.loss_test = []
#
#         return self
#
#     def __next__(self):
#         """ Incrementing method. """
#         # TODO : to finish
#         # Time forward incrementation
#         self.t += self.s
#
#         if self.t > (self.T-1):
#             raise StopIteration
#
#         if self.t + self.s > self.T:
#             # output to train would need the future : we do not retrain the networl
#             return slice(self.t - self.n, self.t), slice(self.t, self.T)
#
#         # TODO : Set training part in an other method
#         # Run epochs
#         for epoch in range(self.e):
#             train_slice = slice(self.t - self.n, self.t-self.s)
#             lo = self._train(
#                 X=self.X[train_slice],
#                 y=self.f(self.y[train_slice]),
#             )
#             self.loss_train += [lo.item()]
#         # Set eval and test periods
#         return slice(self.t - self.n, self.t), slice(self.t, self.t + self.s)
#




class RollMultiLayerPerceptron(MultiLayerPerceptron, roller._RollingBasis):
    """ Rolling version of the vanilla neural network model.
    TODO:
    - fix train and predict methods
    - finish docstring
    - finish methods
    """

    def __init__(self, X, y, layers=[], activation=None, drop=None, bias=True,
                 x_type=None, y_type=None, activation_kwargs={}, **kwargs):
        """ Initialize rolling multi-layer perceptron model. """
        roller._RollingBasis.__init__(self, X, y, **kwargs)
        MultiLayerPerceptron.__init__(self, X, y, layers=layers, bias=bias,
                                      activation=activation, drop=drop,
                                      x_type=x_type, y_type=y_type,
                                      activation_kwargs=activation_kwargs)


    def set_roll_period(self, train_period, test_period, start=0, end=None,epochs=1):
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
            start=start, end=end, epochs=epochs
        )

    def _train(self, X, y):
        return self.train_on(X=X, y=y)

    def sub_predict(self, X):
        """ Predict. """
        return self.predict(X=X)

    def eval_predictor_importance(self, features, features_names):
        explainer_shap = shap.GradientExplainer(model=self,
                                            data=features)
        # Fit the explainer on a subset of the data (you can try all but then gets slower)

        shap_values = explainer_shap.shap_values(X=features,nsamples = 100, ranked_outputs=True,output_rank_order='max',rseed=None, return_variances=False)
        #shap_values = explainer_shap.shap_values(X=features,
        #                                         ranked_outputs=True)

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

    def unroll(self):
        for eval_slice, test_slice in self:
            # Compute prediction on eval and test set
            self.y_eval[eval_slice] = self.sub_predict(self.X[eval_slice])
            test_prediction = self.sub_predict(self.X[test_slice])
            if abs(test_prediction.numpy().sum())<= 1e-6:
                print('null prediction, investigate')
            self.y_test[test_slice] = test_prediction

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

    def unroll_features(self,dates, feature_names):
        rows_list = []
        dates_list = []
        for eval_slice, test_slice in self:
            # Compute prediction on eval and test set
            self.y_eval[eval_slice] = self.sub_predict(self.X[eval_slice])
            test_prediction = self.sub_predict(self.X[test_slice])
            self.y_test[test_slice] = test_prediction
            # getting the features importance
            features_dico = self.eval_predictor_importance(self.X[test_slice], feature_names)

            rows_list.append(features_dico)
            dates_list.append(dates[test_slice.start])

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

        features_df = pd.DataFrame(rows_list)
        features_df.index = list(dates_list)

        return features_df



