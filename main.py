import os
import yaml
import numpy as np
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

from llm_experiment import RunManager


def read_yaml(filename):
    with open(filename, 'r') as f:
        d = yaml.safe_load(f)
    return d


if __name__ == '__main__':
    experiments_config = read_yaml(os.getenv('CONFIGS_FOLDER') + 'experiments.yaml')
    models_config = read_yaml(os.getenv('CONFIGS_FOLDER') + 'models.yaml')
    participants_config = read_yaml(os.getenv('CONFIGS_FOLDER') + 'participants.yaml')
    runs_config = read_yaml(os.getenv('CONFIGS_FOLDER') + 'runs.yaml')

    rm = RunManager()
    rm.load_experiments(experiments_config)
    rm.load_models(models_config)
    rm.load_participants(participants_config)

    for run_config in runs_config['runs']:
        rm.run(run_config)
