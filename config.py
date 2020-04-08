import yaml
from Utils import flags
FLAGS = flags.FLAGS


def load_config(config_path):
    ''' Loads config file.
    Args:
        config_path (str): path to config file
        default_path (bool): whether to use default path
    '''
    # Load configuration from file itself
    with open(config_path, 'r') as f:
        cfg_special = yaml.load(f, Loader=yaml.FullLoader)
    with open("./configs/0default.yaml", 'r') as f:
        default = yaml.load(f, Loader=yaml.FullLoader)

    input_arguments = []
    # Include main configuration
    for k in cfg_special:
        if k in default and FLAGS.__getattr__(k) != default[k]:
            if k not in ['key', 'gpu', 'data']:
                input_arguments.append(k)
            tmp = "Default of {} is {}, config gives {}."
            tmp += "but we follow the args {}"
            print(
                tmp.format(k, default[k], cfg_special[k],
                           FLAGS.__getattr__(k)))
            continue
        v = cfg_special[k]
        FLAGS.__setattr__(k, v)
    return input_arguments


with open("./configs/0default.yaml", 'r') as f:
    default = yaml.load(f, Loader=yaml.FullLoader)

flags.DEFINE_argument('config_file', type=str, help='Path to config file.')
for k in default:
    v = default[k]
    if type(v) == bool:
        flags.DEFINE_boolean("-" + k, "--" + k, default=v)
    else:
        if v is None:
            flags.DEFINE_argument("-" + k, "--" + k, default=None)
        else:
            flags.DEFINE_argument("-" + k, "--" + k, default=v, type=type(v))
