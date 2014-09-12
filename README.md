Germinal
========

Website / Catalog develop in Django

Installation / Usage
--------------------

1. Clone the project

    ``` sh
    $ git clone https://github.com/laborautonomo/germinal.git
    $ cd germinal
    ``` 

2. Create and active [vitualenv](http://pypi.python.org/pypi/virtualenv)

    ``` sh
    $ virtualenv venv
    $ source venv/bin/activate
    ``` 

3. Download and install requirements with [pip](http://pypi.python.org/pypi/pip)

    ``` sh
    $ pip install -r requirements.txt
    ```

4. Configure the project in `germinal/settings.py` file

5. Syncronize database with `$ python manage.py syncdb`

6. Collect static files with `$ python manage.py collectstatic`

7. Finally, run `$ python manage.py runserver`


References
----------

* [Django documentation](https://docs.djangoproject.com/en/1.6/)
* [aprendendo-django](https://github.com/marinho/aprendendo-django)