from ConfigParser import SafeConfigParser


def read_config(config):

    parser = SafeConfigParser()
    parser.read(config)

    config_dict = {}

    for section in parser.sections():
        config_dict[section] = {}
        
        for option in parser.options(section):
            config_dict[section][option] = parser.get(section, option)

    return config_dict['inputs']