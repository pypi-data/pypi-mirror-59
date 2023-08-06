create-pypkg
============

Python Package Scaffold Builder

[![wercker status](https://app.wercker.com/status/92f0cf6945529d93502debb6d9edfe73/s/master "wercker status")](https://app.wercker.com/project/byKey/92f0cf6945529d93502debb6d9edfe73)

Installation
------------

```sh
$ pip install -U create-pypkg
```

Docker image
------------

The image is available at [Docker Hub](https://hub.docker.com/r/dceoy/create-pypkg/).

```sh
$ docker pull dceoy/create-pypkg
```

Usage
-----

1.  Create a new package.

    Replace `newpackage` below with your package's name.

    ```sh
    $ mkdir newpackage
    $ create-pypkg ./newpackage
    ```

2.  Test the command-line interface of the package. (optional)

    ```sh
    $ python -m venv venv
    $ source venv/bin/activate
    $ pip install -U ./newpackage
    $ newpackage --help
    $ newpackage --debug foo bar
    ```
