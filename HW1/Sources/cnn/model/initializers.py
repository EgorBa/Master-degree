import numpy as np


def get_fans(shape):
    fan_in = shape[0] if len(shape) == 2 else np.prod(shape[1:])
    fan_out = shape[1] if len(shape) == 2 else shape[0]
    return fan_in, fan_out


def normal(shape, scale=0.05):
    return np.random.normal(0, scale, size=shape)


def uniform(shape, scale=0.05):
    return np.random.uniform(-scale, scale, size=shape)


def he_normal(shape):
    fan_in, fan_out = get_fans(shape)
    scale = np.sqrt(2. / fan_in)
    shape = (fan_out, fan_in) if len(shape) == 2 else shape
    bias_shape = (fan_out, 1) if len(shape) == 2 else (
        1, 1, 1, shape[3])
    return normal(shape, scale), uniform(bias_shape)


def glorot_uniform(shape):
    fan_in, fan_out = get_fans(shape)
    scale = np.sqrt(6. / (fan_in + fan_out))
    shape = (fan_out, fan_in) if len(shape) == 2 else shape
    bias_shape = (fan_out, 1) if len(shape) == 2 else (
        1, 1, 1, shape[3])
    return uniform(shape, scale), uniform(shape=bias_shape)
