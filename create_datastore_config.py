from mllam_data_prep import Config

from loguru import logger
import copy
import isodate
import argparse
import datetime


BASE_DATASTORE_CONFIG_PATH = 'configs/base_datastore.yaml'
DATASTORE_CONFIG_PATH = 'configs/datastore.yaml'


def main(input_path: str, output_path: str, train_duration: datetime.timedelta):
    datastore_base_config = Config.from_yaml_file(input_path)
    
    datastore_config = copy.deepcopy(datastore_base_config)
    # modify the datastore config
    
    orig_splits = datastore_config.output.splitting.splits
    t_start_train = isodate.parse_datetime(orig_splits["train"].start)
    t_end_train = t_start_train + train_duration
    
    datastore_config.output.splitting.splits["train"].start = t_start_train.isoformat()
    datastore_config.output.splitting.splits["train"].end = t_end_train.isoformat()
    
    # save the modified datastore config
    datastore_config.to_yaml_file(output_path)
    logger.info(f'Saved datastore config to {output_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str)
    parser.add_argument('--output_path', type=str)
    parser.add_argument('--train_duration', type=isodate.parse_duration)
    
    args = parser.parse_args()

    main(input_path=args.input_path, output_path=args.output_path, train_duration=args.train_duration)
    
