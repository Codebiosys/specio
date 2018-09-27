# Specio.app

*A programmatic continuous validation service for humans.*


# Running Specio

In order to install Specio, clone this repo and run the following command to boot the system.

Assuming you have a working Docker machine, simply run the following:

```bash
docker-compose up -d --build
```

Once the containers build, you can see the logging output by using the command:

```bash
docker-compose logs -f
```


# Usage

Specio's pipeline can be run as a complete unit, or you can choose to run the pieces of the pipeline separately.

**IMPORTANT** Only the hosts `customers` directory is mounted inside the running containers, so be sure to put anything you need exposed to the containers in that directory.


## Running the Complete Pipeline

Given that you have a properly configured test config YAML file, and you've put it into the customers volume mounted in the container, you can run the pipeline as follows:


```bash
docker-compose run --rm specio forrest /opt/customers/path/to/config.yml
```

Once it finishes, you should be able to see the report at the location specified in the configuration YAML.


## Running the Pieces

Running the pipeline in pieces does result in more work having to be done by the user, but can be very useful for testing and development.


#### Running Validation Tests

The first step is to tell behave to run the tests and collect the results into the `cucumber.json`. To do this, run the following.

```bash
docker-compose run --rm specio behave \
  -o /opt/customers/path/to/cucumber.json \
  /opt/customers/path/to/features
```


#### Converting Results to the Specio file format

Once you have a completed `cucumber.json` file, you can convert it into the format expected by the reports generator with the following command:

```bash
docker-compose run --rm specio veripy2specio \
  -o /opt/customers/path/to/specio.json \
  -i /opt/customers/path/to/cucumber.json \
```


#### Generating the Report PDF

Once you have a converted Specio JSON file, you can generate a report from it like so:

```bash
docker-compose run --rm specio pydf \
  --source /opt/customers/path/to/template \
  --params /opt/customers/path/to/specio.json \
  --target /opt/customers/path/to/report.pdf
```

You should now see a `report.pdf` in the customers directory.


# Watching the Tests Run

As with any dockerized selenium suite you can watch the tests run in the browser using VNC. On macOS, open Safari and enter `vnc://<docker machine IP>`.


# Monitoring Pipeline Progress

There are two systems in place to help users monitor the progress of tasks as they run.


#### Kibana

If you visit `http://<docker-machine-ip>:5601/` you will find a Kibana logging stack which will give you real-time access to the logs from the containers as they run.


#### Celery Flower

If you're running the entire Specio pipeline at once, using the `forrest` application, you can monitor the progress of each piece using celery flower. This app is available at `http://<docker-machine-ip>:5555/`.


#### CLI logs

Although they're not the most readable thing, the apps do emit logs from the CLI in case you need to see task progress as they go.
