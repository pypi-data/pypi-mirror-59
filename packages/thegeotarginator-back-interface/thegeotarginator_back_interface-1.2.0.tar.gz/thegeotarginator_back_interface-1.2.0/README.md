# Geotargeting backend (Repository overview)

The goal of this system is to store and retrieve geotargeting information in a format that can be consumed by the front-end.

This project is part of the [Geotargeting domain](/doc/Geotargeting.md).

Please read the [house rules](/doc/House-rules.md) before contributing.

# Implementation

## Design considerations

The system was developed with three main design considerations:

- high compatibility with existing systems (Portal, UniversityAdmin)
- optimizing availability of geotargeting information for CloudSearch
- batching operations to provide an economical way to persist data

## Technologies used

- Python
- AWS Lambda
- AWS DynamoDB
- AWS SNS
- AWS SQS

## Exposed interfaces
See: [Exposed interfaces](doc/Exposed-interfaces.md).

# Getting Started

## Prerequisites
To run the project, ensure [Python 3](https://www.python.org/download/releases/3.0/) is installed, as well as [pip](https://pip.pypa.io/en/stable/installing/).

Optionally: create a virtual environent for this project. For the PyCharm IDE
you can find an explanation [here](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html).

Next, run the following command to install the necessary dependencies

```
pip install -r requirements.txt
```

## Deploy
This service is deployed on 2 stages: test and production

Deployment is executed through serverless via AWS CodePipeline. 
Create and merge a pull request to the `develop` branch to deploy to the test. 
Merge to `master` to deploy to production.

## Test

Unit:
```
python -m pytest tests/unit/
```

Unit test Coverage:
```
python -m pytest --cov-report term-missing --cov=src tests/unit/
```

Integration
```
python -m pytest tests/integration/
```

