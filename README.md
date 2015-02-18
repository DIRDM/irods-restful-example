# Examples to demonstrate the iRODS RESTful interface
This package contains examples written in Python and the [pycurl](http://pycurl.sourceforge.net/) library to demonstrate the [iRODS RESTful](https://github.com/DICE-UNC/irods-rest) interface

## Configuration
The configuration file is located at `etc/config.ini`.  The contents in the file should be self-explained.

## Running the individual python examples
The demo is a composition of several python scripts that can be run standalone. To run them individually, just launch a particular script as follows:

```bash
$ ./server_get_info.py
```

Command-line arguments are available via `-h` option.

## Sequence of running the bash demo scripts
To make the demo easier, several bash scripts with prefix `demo_` are used. An instruction/note is given for the upcoming demonstration step.  Press any key to proceed for the demonstration step.

Those scripts are to be run in the following sequence:

1. make the iRODS instance clean for the demo

    ```bash
    $ ./demo_cleanup.sh
    ```

    __Remarks__:
    
    * The current RESTful API of iRODS does not provide interface for removing iRODS user.  Thus, to really make the instance clean, one needs to use the `iadmin` command to remove the user `demo_user` in addition.

2. initialise a collection `dac_00002` and set up relevant groups for access control

    ```bash
    $ ./demo_init_collection.sh
    ```
    
    __Remark__:
    
    * Access permission inheritance can not be set via the RESTful interface. It's a desired feature.

3. add new user `demo_user` and grant the user with the management permission (role) in the collection

    ```bash
    $ ./demo_init_user.sh
    ```
    
    __Remark__:
    
    * A password needs to be provided when adding new user; while it's not necessary via the `iadmin` command.

4. manage collection metadata with the created user `demo_user` 

    ```bash
    $ ./demo_collection_metadata.sh
    ```

5. upload, download and manage file in the collection with the created user `demo_user` 

    ```bash
    $ ./demo_file_management.sh
    ```
