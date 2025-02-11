- to use `uv` need:
    # use local pypi server
    - export UV_INDEX=https://nexus.gefion.dcai.dk/repository/pypi/simple/
    # use local root certificate
    - export UV_NATIVE_TLS=true
    # limit number of concurrent threads in download/build/install
    - export UV_CONCURRENT_BUILDS=1
    - export UV_CONCURRENT_INSTALLS=1
    - export UV_CONCURRENT_DOWNLOADS=1
    
- `params.yaml` can be used as baseline experiment
- creation of parameter study can be done by creating script e.g. `queue_experiments.sh` that execute `dvc exp run --queue -S parameter={value}` for each value of parameter in script