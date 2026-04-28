import os
import sys

from dotenv import load_dotenv
load_dotenv()

from llm_experiment import RunManager
from llm_experiment.utils.read_yaml import read_yaml


def main():
    run_ids = sys.argv[1:] if len(sys.argv) > 1 else []

    config_dir = './configs/'
    
    rm = RunManager(config_dir=config_dir)
    rm.load_all()

    runs_config = read_yaml(config_dir + 'runs.yaml')
    available_runs = {run['id']: run for run in runs_config.get('runs', [])}
    
    if not run_ids:
        print('Available runs:')
        for run_id, run_config in available_runs.items():
            print(f"  - {run_id}: {run_config.get('title', run_id)}")
        print('\nUsage: python main.py <run_id_1> <run_id_2> ...')
        return
    
    for run_id in run_ids:
        if run_id not in available_runs:
            print(f'Run {run_id} not found in configuration.')
            continue
        
        run_config = available_runs[run_id]
        rm.run(run_config)


if __name__ == '__main__':
    main()
