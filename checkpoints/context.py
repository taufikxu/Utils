import os
import shutil
import time
import socket

from Utils.checkpoints.logger import build_logger


def save_context(filename, FLAGS, config):
    FILES_TO_BE_SAVED = config['FILES_TO_BE_SAVED']
    KEY_ARGUMENTS = config['KEY_ARGUMENTS']

    # Start to figure out the environment of the experiments, including path, etc.
    if FLAGS.gpu.lower() not in ['-1', 'none']:
        # print(FLAGS.gpu)
        os.environ["CUDA_VISIBLE_DEVICES"] = str(FLAGS.gpu)
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

    default_key = ''
    for item in KEY_ARGUMENTS:
        default_key += item + "_" + str(FLAGS.__getattr__(item)) + "_"

    if FLAGS.results_folder == "Not Valid":
        FLAGS.results_folder = os.path.join(
            "./results/",
            "({dirname})({file}_{data})_({time})_({default_key})_({user_key})".
            format(dirname=os.path.basename(os.getcwd()),
                   file=filename.replace("/", "_"),
                   data=FLAGS.data,
                   time=time.strftime("%Y-%m-%d-%H-%M"),
                   default_key=default_key,
                   user_key=FLAGS.key))

    if os.path.exists(FLAGS.results_folder):
        folder, i = FLAGS.results_folder, 0
        FLAGS.results_folder = "{}_{}".format(folder, i)
        while os.path.exists(FLAGS.results_folder):
            i += 1
            FLAGS.results_folder = "{}_{}".format(folder, i)

    MODELS_FOLDER = FLAGS.results_folder + "/models/"
    SUMMARIES_FOLDER = FLAGS.results_folder + "/summary/"
    SOURCE_FOLDER = FLAGS.results_folder + "/source/"

    # creating result directories
    os.makedirs(FLAGS.results_folder)
    os.makedirs(MODELS_FOLDER)
    os.makedirs(SUMMARIES_FOLDER)
    os.makedirs(SOURCE_FOLDER)
    logger = build_logger(FLAGS.results_folder, FLAGS.get_dict())
    for folder in FILES_TO_BE_SAVED:
        destination = SOURCE_FOLDER
        if folder != "./":
            destination += folder
            os.makedirs(destination)
        for file in [f for f in os.listdir(folder) if f.endswith(".py")]:
            shutil.copy(os.path.join(folder, file),
                        os.path.join(destination, file))
    # Figure finished
    return logger, MODELS_FOLDER, SUMMARIES_FOLDER
