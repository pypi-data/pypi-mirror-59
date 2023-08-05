from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import collections
import itertools
import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow_core.python.keras.utils import conv_utils
from tensorflow.python.framework import tensor_shape
from tensorflow.python.keras.engine.input_spec import InputSpec
from tensorflow.python.ops import nn_ops
from tensorflow.python.client import device_lib
from .tensorflow_activations import get_activation
from itertools import repeat
import inspect

from ..backend.common import *
from ..backend.tensorflow_backend import *

_tf_data_format= 'channels_last'

__all__ = ['MaxPool1d', 'MaxPool2d','GlobalAvgPool2d','get_pooling']


_session = get_session()

_device='CPU'
for device in device_lib.list_local_devices():
      if tf.DeviceSpec.from_string(device.name).device_type == 'GPU':
          _device='GPU'
          break

_epsilon = _session.epsilon


def _ntuple(n):
    def parse(x):
        if isinstance(x, collections.Iterable):
            return x
        return tuple(repeat(x, n))

    return parse


_single = _ntuple(1)
_pair = _ntuple(2)
_triple = _ntuple(3)
_quadruple = _ntuple(4)

def get_layer_repr(layer):
    # We treat the extra repr like the sub-module, one item per line
    extra_lines = []
    if hasattr( layer, 'extra_repr' ) and callable( layer.extra_repr ):
        extra_repr = layer.extra_repr()
        # empty string will be split into list ['']
        if extra_repr:
            extra_lines = extra_repr.split('\n')
    child_lines = []
    if isinstance(layer,(tf.keras.Model,tf.keras.Sequential)) and layer.layers is not None:
        for module in layer.layers:
            mod_str = repr(module)
            mod_str = addindent(mod_str, 2)
            child_lines.append('(' + module.name + '): ' + mod_str)
    lines = extra_lines + child_lines

    main_str = layer.__class__.__name__ + '('
    if lines:
        # simple one-liner info, which most builtin Modules will use
        if len(extra_lines) == 1 and not child_lines:
            main_str += extra_lines[0]
        else:
            main_str += '\n  ' + '\n  '.join(lines) + '\n'

    main_str += ')'
    return main_str

class MaxPool1d(tf.keras.layers.MaxPool1D):
    def __init__(self,kernel_size=(2,), strides=None, auto_pad=True, **kwargs ):
        kernel_size = _single(kernel_size)
        strides = _single(strides or kernel_size)
        super(MaxPool1d, self).__init__( kernel_size,strides,
                 padding='same' if auto_pad else 'valid', data_format='channels_last', **kwargs)

    @property
    def kernel_size(self):
        return super().pool_size

    @kernel_size.setter
    def kernel_size(self,value):
        self.pool_size=_single(value)

    def __repr__(self):
        return get_layer_repr(self)
    def extra_repr(self):
        s = 'kernel_size={pool_size}, strides={strides}'
        s += ',auto_pad={0}'.format(self.padding == 'same')
        return s.format(**self.__dict__)


class MaxPool2d(tf.keras.layers.MaxPool2D):
    def __init__(self,kernel_size = (2, 2), strides=None, auto_pad=True,padding_mode=PaddingMode.replicate, **kwargs ):
        kernel_size=_pair(kernel_size)
        strides=_pair(strides or kernel_size)
        super(MaxPool2d, self).__init__( kernel_size,strides,
                 padding='same' if auto_pad else 'valid', data_format='channels_last', **kwargs)

    @property
    def kernel_size(self):
        return super().pool_size

    @kernel_size.setter
    def kernel_size(self,value):
        self.pool_size=_pair(value)
    def __repr__(self):
        return get_layer_repr(self)
    def extra_repr(self):
        s = 'kernel_size={pool_size}, strides={strides}'
        s += ',auto_pad={0}'.format(self.padding == 'same')
        return s.format(**self.__dict__)


class GlobalAvgPool2d(tf.keras.layers.GlobalAvgPool2D):
    def __init__(self,name=''):
        super(GlobalAvgPool2d, self).__init__()
    def __repr__(self):
        return get_layer_repr(self)



def get_pooling(fn_name):
    if fn_name is None:
        return None
    fn_modules = ['trident.layers.tensorflow_pooling']
    try:
        if isinstance(fn_name,str) and fn_name in __all__:
            try:
                pooling_class = get_class(fn_name, fn_modules)
                return pooling_class()
            except Exception:
                PrintException()
                return None
        if getattr(fn_name, '__module__', None) == fn_modules[0]:
            if inspect.isfunction(fn_name):
                return fn_name
            elif isinstance(fn_name, tf.keras.layers.Layer):
                return fn_name()
        else:
            if callable(fn_name) :
                result=inspect.getfullargspec(fn_name)
                if 1<=len(result.args)<=2:
                    return fn_name if inspect.isfunction(fn_name) else fn_name()
                else:
                    raise ValueError('Unknown pooling function/ class')
    except Exception:
        return None

