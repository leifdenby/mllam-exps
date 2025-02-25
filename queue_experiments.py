import mllam_data_prep as mdp
import isodate
import rich
from loguru import logger
import subprocess


fp_datastore_config = "data/datastore.yaml"


dataset_durations = ["P6M", "P1Y", "P2Y", "P4Y", "P8Y"]

def _queue_experiment(duration=None):
    config = mdp.Config.from_yaml_file(fp_datastore_config)
        
    if duration is not None:
        t_end = isodate.parse_datetime(config.output.splitting.splits["train"].end)
        
        # need to ensure end time stays the same, so we adjust the start time to match the duration
        t_start = t_end - isodate.parse_duration(duration)

        # set the new start time in the config
        config.output.splitting.splits["train"].start = t_start.isoformat()
        
        # also need to set config.output.coord_ranges["time"].start and end
        config.output.coord_ranges["time"].start = t_start.isoformat()
        
        # instead of writing the config back to the file, we can just pass the new
        # values as parameters to dvc to override the existing values in the yaml config file
        
        # convert changes to dvc cli `-S param=value` format
        dvc_params = {
            f"{fp_datastore_config}:output.splitting.splits.train.start": t_start.isoformat(),
            f"{fp_datastore_config}:output.coord_ranges.time.start": t_start.isoformat(),
        }
        
        logger.info(f"Queuing experiment for duration {duration}")
        run_name = duration
    else:
        t_end = isodate.parse_datetime(config.output.splitting.splits["train"].end)
        t_start = isodate.parse_datetime(config.output.splitting.splits["train"].start)
        duration = isodate.duration_isoformat(t_end - t_start)

        logger.info(f"Queueing baseline experiment {duration}")
        dvc_params = {}
        run_name = f"{duration}-baseline"
    
    dvc_params["logger-project"] = "lcd/dataset-duration-study"

    # create cli call to `dvc exp run` with the new parameters
    dvc_args = " ".join([f"-S {key}={value}" for key, value in dvc_params.items()])
    # queue the experiment
    dvc_cmd = f"dvc exp run --queue -n {run_name} {dvc_args}"
    logger.info(f"Running command: {dvc_cmd}")
    
    subprocess.run(dvc_cmd, shell=True)

def main():
    for duration in [None] + dataset_durations:
        _queue_experiment(duration)
    

if __name__ == "__main__":
    main()