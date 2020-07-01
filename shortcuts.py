import math
import sys
import logging
from tqdm import tqdm
from tqdm import trange
import numpy as np


def get_logger(logger_name=None):
    if logger_name is not None:
        logger = logging.getLogger(logger_name)
        logger.propagate = 0
    else:
        logger = logging.getLogger("taufikxu")
    return logger


def xrange(iters, prefix=None, Epoch=None, **kwargs):
    if Epoch is not None and prefix is None:
        prefix = "Epoch " + str(Epoch)
    return trange(
        int(iters),
        file=sys.stdout,
        leave=False,
        dynamic_ncols=True,
        desc=prefix,
        **kwargs
    )


def range_iterator(iters, prefix=None, Epoch=None, **kwargs):
    if Epoch is not None and prefix is None:
        prefix = "Epoch " + str(Epoch)
    return tqdm(
        iters, file=sys.stdout, leave=False, dynamic_ncols=True, desc=prefix, **kwargs
    )


def weight_init(m):
    if hasattr(m, "reset_parameters"):
        m.reset_parameters()


def toggle_grad(model, requires_grad):
    for p in model.parameters():
        p.requires_grad_(requires_grad)


def update_average(model_tgt, model_src, beta=0.999):
    param_dict_src = dict(model_src.named_parameters())
    for p_name, p_tgt in model_tgt.named_parameters():
        p_src = param_dict_src[p_name]
        assert p_src is not p_tgt

        p_tgt.data.mul_(beta).add_((1 - beta) * p_src.data)
