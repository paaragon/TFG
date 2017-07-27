import argparse
import json

class Predict(object):

    data_set_file_name = None
    normalization_info = None
    model_path = None
    score = None
    n_samples = None
    samples_step = None
    target_time_step = None
    target_column = None
    map_target = None

    def __init__(self, data_set_file_name, normalization_info, model_path, score, n_samples, samples_step, target_time_step, target_column, map_target):
        self.data_set_file_name = data_set_file_name
        self.normalization_info = normalization_info
        self.model_path = model_path
        self.score = score
        self.n_samples = n_samples
        self.samples_step = samples_step
        self.target_time_step = target_time_step
        self.target_column = target_column
        self.map_target = map_target

def main():
    """main function of module"""

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config-file", nargs="?", action="store", \
                        dest="config_file", help="File with the parameters.")

    arguments = parser.parse_args()

    config_file = arguments.config_file

    with open(config_file) as data_file:
        config_data = json.load(data_file)

    data_set_file_name = config_data["data_set_file_name"]
    normalization_info = config_data["normalization_info"]
    model_path = config_data["model_path"]
    score = config_data["score"]
    n_samples = config_data["n_samples"]
    samples_step = config_data["samples_step"]
    target_time_step = config_data["target_time_step"]
    target_column = config_data["target_column"]
    map_target = config_data["map_target"]

    predic = Predict(data_set_file_name, normalization_info, model_path, score, n_samples, samples_step, target_time_step, target_column, map_target)

if __name__ == "__main__":
    main()