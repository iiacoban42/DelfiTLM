# DelfiTLM

[![Django CI](https://github.com/iiacoban42/DelfiTLM/actions/workflows/django.yml/badge.svg?branch=main)](https://github.com/iiacoban42/DelfiTLM/actions/workflows/django.yml)
[![Pylint](https://github.com/iiacoban42/DelfiTLM/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/iiacoban42/DelfiTLM/actions/workflows/pylint.yml)

## Requirements

- Python3 and Java 8 or higher
- For local running/development: The postgres client library (For apt users: `apt install libpq-dev`)
- Docker and docker-compose if running the system or the database from a container
- For running without docker: Set up a Postgres instance on port 5432

## Setup (Run locally/on host machine)

1. Create a python environment (one time instruction):
`python3 -m venv env`

2. Activate it using:
`source env/bin/activate`

3. Install the requirements (one time instruction):
`pip install -r requirements.txt`

4. Set up the database via docker or connect your own Postgres instance
`docker-compose up db`

5. Run the migrations from the root folder:
`python src/manage.py migrate`

6. Run the server from the root folder:
`python src/manage.py runserver` The server runs on http://127.0.0.1:8000/

7. To run the tests:
`python src/manage.py test`

8. To run pylint:
`find src -name "*.py" | xargs pylint`

## Setup (Run via docker)

This method should be sufficient for most development tasks as any (file) changes you make are monitored by StatReloader. To start the environment, run:
`docker-compose up --build`

Note: remove `--build` to skip building the container, will use the cached one (last build)

After this, you can access the application on http://127.0.0.1:8000/ and a pgAdmin instance on http://127.0.0.1:5050/ with `admin@admin.com:admin` for username:password. From pgAdmin add a new server by giving it a name and the following database credentials:

![image](https://user-images.githubusercontent.com/15870306/145728488-ada8aacf-ec53-42d1-8e4d-b7198c70cc77.png)

InfluxDB can accessed at http://localhost:8086/, username:admin, password:adminpwd.

Grafana runs on http://localhost:3000/, username:admin, password:adminpwd with the following InfluxDB datasource config:
![image](https://user-images.githubusercontent.com/43474282/179267387-554aeb2e-b789-408f-ad24-74f1afd281e2.png)

The datasource and dashboards confing for Grafana can be changed from `grafana/provisioning/grafana-datasources.yml` and `grafana/dashboards/grafana-dashboard.yml` respectively. New dashboards can also be created in Grafana and exported as json, then added to `grafana/dashboards`, to be loaded when the container restarts.

To reset the containers and remove the volumes run the `./reset_docker.sh` script.

## Deployment

1. In case SSL certificates are used, create a volume named delfitlm\_certificates [example](https://github.com/moby/moby/issues/25245#issuecomment-365980572) and copy inside _server.pem_ and _server.key_. Ensure they are owned by root and that permissions are 644 before copying them.

2. Set up the firewall bouncer for CrowdSec, instructions in `crowdsec/README.md`.

3. Build and run Docker deployment script (runs on port 80 - default web port):
`docker-compose -f docker-compose.yml -f docker-compose-deploy.yml up --build`

3. Access the container to initialize Django (only required the first time):
`docker exec -it delfitlm_app_1 /bin/bash`

4. Run the database migration to create the tables (only required the first time):
`python manage.py migrate`

Note: remove `--build` to skip building the container, will use the cached one (last build)

## Testing

1. To run the unit tests execute `python manage.py test` from within the `src` folder

2. To compile the coverage report run the `./run_coverage.sh` script and the report will appear in `src/htmlcov/index.html`


## Backup and restore Postgres database

### Backup

To backup the database run: `docker exec -t your-db-container pg_dumpall -c -U your-db-user > dump.sql`

For this project: `docker exec -t delfitlm_db_1 pg_dumpall -c -U postgres > dump.sql`

### Restore

To restore the database run: `cat dump.sql | docker exec -i your-db-container psql -U your-db-user -d your-db-name`

For this project: `cat dump.sql | docker exec -i delfitlm_db_1 psql -U postgres -d delfitlm`
