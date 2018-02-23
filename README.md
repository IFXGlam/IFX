# 🎥 IFX 🎥
Israeli film archive

# Development Setup Instructions

## Requirements

* Python 3.6.x
* [postgres](https://github.com/nonZero/setups/blob/master/postgres-setup.md)
* [pipenv](http://pipenv.readthedocs.io/en/latest/)
* Optional: [RabbitMQ](https://www.rabbitmq.com/)


## Setup

* Clone this repo.
* Add an `IFX/ifx/local_settings.py` file with:

        DEBUG = True
        SECRET_KEY = "kukuriku"

        CELERY_TASK_ALWAYS_EAGER = True

* To install all the requirements and get into the virtual environment:

       pipenv install
       pipenv shell

* Assuming your user can create DBs:

        python manage.py sqlcreate

* Create tables:

        python manage.py migrate

* Import data from dump (not published yet on github):

        python manage.py loaddata all_data.json

* Run your server:

        python manage.py runserver

* Enjoy: 
        
        http://localhost:8000/

# Tips

* Linux/Mac: add to your `.bashrc` or `.bash_profile`:

        alias m='python manage.py'
        alias sp='python manage.py shell_plus'
