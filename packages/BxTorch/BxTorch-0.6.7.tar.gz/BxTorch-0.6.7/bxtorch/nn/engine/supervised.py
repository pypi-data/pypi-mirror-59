#
#  supervised.py
#  bxtorch
#
#  Created by Oliver Borchert on 09/04/19.
#  Copyright (c) 2019 Oliver Borchert. All rights reserved.
#

import copy
from .base import BaseEngine

class SupervisedEngine(BaseEngine):
    """
    Trainer to be used in a supervised learning setting.

    A dataset supplied to the `train` or `evaluate` method must supply tuples 
    with the following items:

    * x: input to the model
    * y: correct output

    For the `predict method, the data must be supplied as follows:

    * x: input to the model

    Further, the `train` method requires the following parameters:

    - optimizer: torch.optim.Optimizer or str
        The optimizer to use for optimizing the model's weights. If a string is 
        given, the corresponding optimizer is used with default 
        hyperparameters. Be aware that this optimizer is kept in memory as long 
        as the trainer exists.
    - loss: func (torch.Tensor, torch.Tensor) -> float
        The loss function to use.
    - gradient_accumulation_steps: int, default: 1
        The number of batches which should be used for a single update step.
        Gradient accumulation can be useful if your GPU can only fit a small
        batch size but model convergence is hindered by that.
    """

    def __init__(self, model):
        super().__init__(model)
        self._grad_accum_cache = {}

    # MARK: Callback Overrides
    def before_epoch(self, current, num_iterations):
        self._grad_accum_cache['num_iterations'] = num_iterations
        self._grad_accum_cache['current_iteration'] = 0

    def after_batch(self, *args):
        if 'current_iteration' in self._grad_accum_cache:
            self._grad_accum_cache['current_iteration'] += 1

    def after_epoch(self, metrics):
        self._grad_accum_cache = {}
    
    # MARK: Private Methods
    def train_batch(self, data, optimizer=None, loss=None,
                    gradient_accumulation_steps=1):
        if isinstance(optimizer, str):
            if optimizer not in self._cache:
                self._cache[optimizer] = self.optimizer(optimizer)
            optimizer = self._cache[optimizer]

        it = self._grad_accum_cache['current_iteration']
        if it == 0:
            optimizer.zero_grad()

        loss_func = loss

        y_pred, y_true = self.forward_train_batch(*data)
        loss = loss_func(y_pred, y_true) / gradient_accumulation_steps

        loss.backward()

        it_is_last = it == self._grad_accum_cache['num_iterations'] - 1
        if it % gradient_accumulation_steps == 0 or it_is_last:
            optimizer.step()
            optimizer.zero_grad()

        return loss.item()

    def eval_batch(self, data):
        x, y_true = data
        y_pred = self._forward(x)
        return y_pred, y_true

    def forward_train_batch(self, x, y_true):
        y_pred = self._forward(x)
        return y_pred, y_true
