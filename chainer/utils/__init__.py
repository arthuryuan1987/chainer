import numpy

import chainer.walker_alias

WalkerAlias = chainer.walker_alias.WalkerAlias


def force_array(x):
    # numpy returns a float value (scalar) when a return value of an operator
    # is a 0-dimension array.
    # We need to convert such a value to a 0-dimension array because `Function`
    # object needs to return an `numpy.ndarray`.
    if numpy.isscalar(x):
        return numpy.array(x, x.dtype)
    else:
        return x
