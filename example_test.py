import glob
import os
import pickle

import matplotlib
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

import torchvision
from matplotlib import pyplot as plt

import ESM
from ESM import inputs
from ESM.sampling_mdsm import Annealed_Langevin_E, SS_denoise

import Utils
from Utils import config, flags


def main():
    matplotlib.use("Agg")
    FLAGS = flags.FLAGS
    config.load_config(FLAGS.config_file)
    if FLAGS.gpu.lower() not in ["-1", "none", Utils.config.notValid.lower()]:
        os.environ["CUDA_VISIBLE_DEVICES"] = str(FLAGS.gpu)

    torch.manual_seed(1234)
    torch.cuda.manual_seed(1235)
    np.random.seed(1236)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = FLAGS.old_model
    dirname = os.path.dirname(model)
    basename = os.path.basename(model)
    config_path = os.path.join(dirname, "..", "source", "configs_dict.pkl")
    summary_path = os.path.join(dirname, "..", "summary")
    with open(config_path, "rb") as f:
        new_dict = pickle.load(f)
    FLAGS.set_dict(new_dict)

if __name__ == "__main__":
    main()