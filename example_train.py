import os
import shutil
import time
import copy

import torch
import numpy as np

from Utils.checkpoints import save_context, Logger
from Utils import flags
from Utils import config

import Torture
from Torture.utils import distributions
from Torture import shortcuts

import library
from library import training_control as training

FILES_TO_BE_SAVED = ["./", "./GAN"]
FLAGS = flags.FLAGS
KEY_ARGUMENTS = config.load_config(FLAGS.config_file)
text_logger, MODELS_FOLDER, SUMMARIES_FOLDER = save_context(__file__, KEY_ARGUMENTS)

torch.manual_seed(1234)
torch.cuda.manual_seed(1235)
np.random.seed(1236)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# torch.autograd.set_detect_anomaly(True)

generator, discriminator = library.inputs.get_Gen_Dis()
generator = generator.to(device)
discriminator = discriminator.to(device)
generator_test = copy.deepcopy(generator)
opt_G, opt_D = library.inputs.get_optimizer(generator, discriminator)

checkpoint_io = Torture.utils.checkpoint.CheckpointIO(checkpoint_dir=MODELS_FOLDER)
checkpoint_io.register_modules(
    generator=generator, generator_test=generator_test, discriminator=discriminator
)
logger = Logger(log_dir=SUMMARIES_FOLDER)
itr = library.inputs.get_data()