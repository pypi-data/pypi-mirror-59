import os
import warnings
import numpy as np
import tensorflow as tf

from ..backend.common import get_function,get_class,snake2camel
from ..backend.tensorflow_backend import to_numpy
from ..misc.callbacks import AdjustLRCallback
__all__ = ['get_lr_scheduler','ReduceLROnPlateau','reduce_lr_on_plateau']


class ReduceLROnPlateau(AdjustLRCallback):
    """Reduce learning rate when a metric has stopped improving.
    Models often benefit from reducing the learning rate by a factor
    of 2-10 once learning stagnates. This callback monitors a
    quantity and if no improvement is seen for a 'patience' number
    of epochs, the learning rate is reduced.
    # Example
    ```python
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2,
                                  patience=5, min_lr=0.001)
    model.fit(X_train, Y_train, callbacks=[reduce_lr])
    ```
    # Arguments
        monitor: quantity to be monitored.
        factor: factor by which the learning rate will
            be reduced. new_lr = lr * factor
        patience: number of epochs that produced the monitored
            quantity with no improvement after which training will
            be stopped.
            Validation quantities may not be produced for every
            epoch, if the validation frequency
            (`model.fit(validation_freq=5)`) is greater than one.
        verbose: int. 0: quiet, 1: update messages.
        mode: one of {auto, min, max}. In `min` mode,
            lr will be reduced when the quantity
            monitored has stopped decreasing; in `max`
            mode it will be reduced when the quantity
            monitored has stopped increasing; in `auto`
            mode, the direction is automatically inferred
            from the name of the monitored quantity.
        min_delta: threshold for measuring the new optimum,
            to only focus on significant changes.
        cooldown: number of epochs to wait before resuming
            normal operation after lr has been reduced.
        min_lr: lower bound on the learning rate.
    """

    def __init__(self, monitor='total_losses', factor=0.1, patience=10,
                 verbose=0, mode='auto', min_delta=1e-4, cooldown=0, min_lr=0,
                 **kwargs):
        super(ReduceLROnPlateau, self).__init__()

        self.monitor = monitor
        if factor >= 1.0:
            raise ValueError('ReduceLROnPlateau '
                             'does not support a factor >= 1.0.')
        if 'epsilon' in kwargs:
            min_delta = kwargs.pop('epsilon')
            warnings.warn('`epsilon` argument is deprecated and '
                          'will be removed, use `min_delta` instead.')
        self.factor = factor
        self.min_lr = min_lr
        self.min_delta = min_delta
        self.patience = patience
        self.verbose = verbose
        self.cooldown = cooldown
        self.cooldown_counter = 0  # Cooldown counter.
        self.wait = 0
        self.best = 0
        self.mode = mode
        self.monitor_op = None
        self._reset()

    def _reset(self):
        """Resets wait counter and cooldown counter.
        """
        if self.mode not in ['auto', 'min', 'max']:
            warnings.warn('Learning Rate Plateau Reducing mode %s is unknown, '
                          'fallback to auto mode.' % (self.mode),
                          RuntimeWarning)
            self.mode = 'auto'
        if (self.mode == 'min' or
           (self.mode == 'auto' and 'acc' not in self.monitor)):
            self.monitor_op = lambda a, b: np.less(a, b - self.min_delta)
            self.best = np.Inf
        else:
            self.monitor_op = lambda a, b: np.greater(a, b + self.min_delta)
            self.best = -np.Inf
        self.cooldown_counter = 0
        self.wait = 0

    def on_train_begin(self, training_context):
        self._reset()

    def on_epoch_end(self, training_context):
        training_context['current_lr']=training_context['optimizer'].lr
        current =to_numpy(training_context['losses'].get(self.monitor,training_context['metrics'].get(self.monitor,training_context['losses']['total_losses']))).mean()
        if current is None:
            warnings.warn(
                'Reduce LR on plateau conditioned on metric `%s` '
                'which is not available. Available metrics are: %s' %
                (self.monitor, ','.join(training_context['metrics'].keys_list)), RuntimeWarning
            )

        else:
            if self.in_cooldown():
                self.cooldown_counter -= 1
                self.wait = 0

            if self.monitor_op(current, self.best):
                self.best = current
                self.wait = 0
            elif not self.in_cooldown():
                self.wait += 1
                print(self.wait )
                if self.wait >= self.patience:
                    old_lr = float(training_context['optimizer'].lr)
                    if old_lr > self.min_lr:
                        new_lr = old_lr * self.factor
                        new_lr = max(new_lr, self.min_lr)
                        training_context['optimizer'].adjust_learning_rate(new_lr,True)

                        if self.verbose > 0:
                            print('\nEpoch %05d: ReduceLROnPlateau reducing '
                                  'learning rate to %s.' % (training_context['current_epoch'] + 1, new_lr))
                        self.cooldown_counter = self.cooldown
                        self.wait = 0

    def in_cooldown(self):
        return self.cooldown_counter > 0

def reduce_lr_on_plateau(monitor='total_loss',base_lr=0.001 ,verbose=True, mode='min', factor=0.5, patience=5, threshold=1e-4, threshold_mode='rel', cooldown=0, min_lr=1e-8, eps=1e-9):
   return ReduceLROnPlateau(monitor=monitor,mode=mode,factor=factor,patience=patience,verbose=int(verbose),min_delta=threshold,threshold_mode=threshold_mode,cooldown=cooldown,min_lr=min_lr)

def get_lr_scheduler(lr_scheduler_name):
    if lr_scheduler_name is None:
        return None
    lr_scheduler_modules = ['trident.optims.tensorflow_lr_schedulers']
    lr_scheduler_fn=None
    if isinstance(lr_scheduler_name,str):
        if lr_scheduler_name in __all__:
            lr_scheduler_fn=get_function(lr_scheduler_name,lr_scheduler_modules)
    else:
        try:
            lr_scheduler_fn = get_function(lr_scheduler_name, lr_scheduler_modules)
        except Exception :
            lr_scheduler_fn = get_function(snake2camel(lr_scheduler_name), lr_scheduler_modules)
    return lr_scheduler_fn


