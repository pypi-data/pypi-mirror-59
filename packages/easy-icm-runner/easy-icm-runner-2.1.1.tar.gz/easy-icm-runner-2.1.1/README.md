# easy-icm-runner
Simplified Job Execution for Varicent's ICM v10 using REST APIs

## Installation
```
pip install easy-icm-runner
```

## Usage
This project can be used as a module within your custom program, or standalone from the command line.  Below we demonstrate sample usage:

#### Python Usage:

The snippet below demonstrates running a job _syncronously_ in python code.  Such a method will be desirable for incorporating an ICM job step into a more complex application, or such tasks as integrating your own secret and configuration management.
```python
"""
API Call to ICM v10 that runs a specified scheduler root/main process
"""

from easy_icm_runner.icm_runner import Runner
from easy_icm_runner.icm_runner import exec_runner


USERNAME = 'username'
PASSWORD = 'password'
MODEL_NAME = 'model'
PROCESS_NAME = 'scheduler job name'
API_KEY = 'api_key/token'

# run using instance
JOB_RUNNER = Runner(API_KEY)
JOB_RUNNER.run_process_by_name(model_name=MODEL_NAME, process_name=PROCESS_NAME)

# run using exec runners
# using api key
exec_runner(model_name=MODEL_NAME, process_name=PROCESS_NAME, api_key=API_KEY)
# using username and password
exec_runner(username=USERNAME, password=PASSWORD, model_name=MODEL_NAME,
            process_name=PROCESS_NAME)

```

#### Command Line Usage:
For those of you who are not budding pythonistas, or just looking for a simple solution to job scheduling we also allow a command line entrypoint.
```text
$ python -m easy_icm_runner.icm_runner -u "icm username" -p "icm password" -m "model name" -j "process name"
```
```text
$ python -m easy_icm_runner.icm_runner -m "model name" -j "process name" -a "api key"
```

------------
##### Updates in this version
- Project description was updated
