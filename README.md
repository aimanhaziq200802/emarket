To run the project in your local machine do follow the steps below:

1. Create virutal environment:
    python -m venv (your_env_name) --windows
    source (your_env_name)/bin/activate --macOS/Linux

2. Activate the virtual environment:
    (your_env_name)\Scripts\activate.bat

3. Change directory to the project:
    cd emarket

4. Install the project dependencies:
    pip install -r requirements.txt

5. Make migrations and migrate:
    python manage.py makemigrations
    python manage.py migrate

6. Create new superuser
    python manage.py createsuperuser

7. Run the project:
    python manage.py runserver

Contact Information:
    Name: Muhammad Aiman Haziq
    Email: 1201101381@student.mmu.edu.my

