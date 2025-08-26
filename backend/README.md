### Framework

I used `Django` as a reputable and widely-used framework for backend. Although this project is small, having a well-organized backend that can easily be extended in the future is nice. The `sqlite3` database is being used for our structured data. The project itsef is named `wave_engine` but the single **_app_** that I'm using here is named `payroll`. You can see their corresponding directories under `/backend`.

### Structure

- **models:** defines our data models.
- **exceptions:** contains our application-specific exceptions and a related message for it.
- **migrations:** Django creates it, just added a migration to store the default job rate for group `A` and `B`.
- **repositores:** it has all our database interaction functions in it, in an ideal scenario, if we want to change the database in the future, we should be concered about this directory only.
- **services** contains our core logic and services.

### Setup and Run

This project has been tested on Ubuntu 24.04 and it should be fine on other versions.

1. clone the repository and change your working directory to `backend`.

2. I used a virtual environment to make it more standard `(e.g. python3 -m venv .venv)`. It doesn't have too many requirements right now, probably if you have an updated `Django` installed on your machine it should be fine. But if needed, you can make your own virtual environmet and use `requirements.txt` to install dependencies, make sure you activate your virtual environment prior to run.

3. Run the migration for the database `python manage.py migrate`.

4. Run the app on port `8000` using `python manage.py runserver 8000`
