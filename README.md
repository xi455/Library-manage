# Django Library Manage System

## Want to use this project?

1. Fork/Clone

1. Create and activate a virtual environment:

    ```sh
    $ python3.11 -m venv env && source venv/bin/activate
    ```

1. Install the requirements:

    ```sh
    (venv)$ pip install -r requirements.txt
    ```

1. Apply the migrations:

    ```sh
    (env)$ python manage.py migrate
    ```

1. Create a superuser and populate the database:

    ```sh
    (env)$ python manage.py createsuperuser
    ```

1. Run the development server:

    ```sh
    (env)$ python manage.py runserver
    ```

1. Your Django admin site should be accessible at [http://localhost:8000/secretadmin/](http://localhost:8000/secretadmin/).