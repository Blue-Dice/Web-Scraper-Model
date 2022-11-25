Web scraper (Flask + Selenium + Celery)
==============================


# Getting Started


Create Environment
------------
```
python3 -m venv venv
```

Activate environment
------------
```
On Linux: source venv/bin/activate
On Windows: venv\Scripts\activate
```

Install dependencies
------------
```
pip install - r requirements.txt
```

Create .env file
------------
```
create a file named ".env"
copy all the content from .env.txt into the .env file
make changes according to your requirements
delete .env.txt file
```

Python run command
------------
```
python setup.py
```

Celery run command
------------
```
Help command: python scraper/celery_config/worker.py --help
Run command: python scraper/celery_config/worker.py start
Purge command: python scraper/celery_config/worker.py purge
Force purge command: python scraper/celery_config/worker.py purge -f
```

Project Organization
------------

    ├── README.md             <- The top-level README for developers using this project.
    ├── scraper
    │   ├── celery_config     <- Celery configuration
    │   ├── helpers           <- Helper functions for the project
    │   ├── static            <- Static file, contains css and assets
    │   ├── templates         <- Template file
    │   └── main.py           <- The original, immutable data dump
    │
    ├── setup.py              <- main run file
    │
    ├── LICENSE               <- License information
    │
    ├── .env.txt              <- .env file sample
    │
    ├── runtime.txt           <- python version
    │
    ├── requirements.txt      <- The requirements file for reproducing the analysis environment
    │
    └── tests                 <- Project test cases
        │
        ├── test_1            <- Test 1
        │   └── test.py
        │
        ├── test_2            <- Test 2
        │   └── test.py
        │
        └── test_3            <- Test 3
            └── test.py

------------