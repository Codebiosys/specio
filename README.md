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

Using Specio locally is easy, all you need is a report template, some feature files, and a configuration YML file. Refer to the `customers/codebiosys/codebiosys.yml` for an example Specio configuration.

**TODO:** Add more docs about the configuration format.

Once you've assembled the files needed, (or if you just want to test Specio, you can use the sample file in the `codebiosys` directory), simply drag and drop your `.yml` config file into the `dropzone` directory.


## Watching the Tests Run

As with any dockerized selenium suite you can watch the tests run in the browser using VNC. On macOS, open Safari and enter `vnc://<docker machine IP>`.


## Remote Usage

Specio can also be run on an external machine and automatically configures SFTP to allow you to drop files in the dropzone remotely.

**TODO:** Finish FTP support before adding instructions.
