import numpy
import chainer
from chainer.utils import type_check
from mkldnn.chainer.runtime import Engine
from mkldnn.compute_complex import *
# Most important thing
from mkldnn.api.support import *
import mkldnn.api.memory as m
import mkldnn.api.sum as sum
from mkldnn.mdarray import *

def mkl_sum_enabled(in_data):
    if chainer.should_use_mkldnn('>=auto') \
       and and all(isinstance(xi, numpy.ndarray) or isinstance(xi, mkldnn.mdarray) for xi in in_data):
        return True
    else:
        return False

def _x_format(ndim):
    if ndim == 1:
        return m.memory.x
    if ndim == 2:
        return m.memory.nc
    elif ndim == 4:
        return m.memory.nchw
    else:
        return NotImplemented

def mkl_sum(xs):
    e = Engine()

    xarrays = () # prevent the obj from gc
    xs_arrays = () # prevent the obj from gc
    itm_arr = None #prvent the obj from gc
    xs_mpdl = m.mpd_list()
    xs_pl = ()
    scales = m.vectord()
    pl = primitive_list()
    for i in range(len(xs)):
        xarray = array(xs[i], _x_format(xs[i].ndim), e)
        xmpd = xarray.memory.get_primitive_desc()
        if i == 0:
            xmpd_best = xmpd
        else:
            if m.get_fmt(xmpd) > m.get_fmt(xmpd_best):
                xmpd_best = xmpd
        xs_arrays += (xarray,)
    for x in xs_arrays:
        outputs = reorder_if_must(x, xmpd_best, e, pl)
        if len(outputs) == 2:
            xarray, itm_arr = outputs[:2]
        else:
            xarray = outputs[0]
        xarrays += (xarray,)
        scales.push_back(1.0)
        xs_mpdl.push_back(xarray.memory.get_primitive_desc())
        xs_pl += (at(xarray.memory), )

    cc_pd = sum.primitive_desc(scales, xs_mpdl)
    y = mdarray(cc_pd.dst_primitive_desc())

    pl.push_back(sum.sum(cc_pd, xs_pl, y.memory))
    s = Stream()
    s.submit(pl)
    s.wait()

    return y
