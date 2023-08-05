#
#  nn/callbacks/schedule.py
#  bxtorch
#
#  Created by Oliver Borchert on May 21, 2019.
#  Copyright (c) 2019 Oliver Borchert. All rights reserved.
#  

import torch
from .base import TrainingCallback

class ParameterScheduler(TrainingCallback):
    """
    The parameter scheduler is able to change the value of a variable
    over the course of the training. The scheduler modifies parameters
    **in-place**, hence, you must pass tensors to be modified and you must
    never pass them to the CPU.
    """

    # MARK: Initialization
    def __init__(self, parameter, schedule, after_batch=False):
        """
        Initalizes a new scheduler for the given parameter.

        Parameters:
        -----------
        - parameter: torch.Tensor
            The parameter which should be modified over the course of the
            training.
        - schedule: func (float, int) -> float
            Function which should update the parameter (given as first
            argument) based on itself and the current epoch (second argument).
            The function must return the updated parameter. The scheduler
            function is called after every epoch.
        - after_batch: bool, default: False
            Whether to call the scheduler after every batch instead of after
            every epoch. The schedule function is then passed as second
            parameter the current iteration (number of all batches) instead of
            the epoch.
        """
        self.parameter = parameter
        self.schedule = schedule
        self.exec_after_batch = after_batch
        self.epoch = None
        self.iterations = None

    # MARK: Instance Methods
    def before_training(self, model, num_epochs):
        self.iterations = 0

    def before_epoch(self, current, num_iterations):
        self.epoch = current

    def after_batch(self, train_loss):
        self.iterations += 1
        self._update(True)

    def after_epoch(self, metrics):
        self._update(False)

    def after_training(self):
        self.epoch = None
        self.iterations = None

    # MARK: Private Methods
    def _update(self, is_batch_update):
        if is_batch_update != self.exec_after_batch:
            return
        if self.exec_after_batch:
            update = self.schedule(self.parameter.item(), self.iterations)
        else:
            update = self.schedule(self.parameter.item(), self.epoch)
        self.parameter.set_(torch.tensor(update))
