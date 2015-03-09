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
    
    __Remark__:
    
    * File transfer via interface is based on the file streaming mechanism, which is not on the equal footing with the `iput/iget` command in terms of functionality and performance. As a consequence, policy enforcement points in the rule engine, e.g. `acPostProcForPut`, is not triggered as expected. More details on this issue can be traced [here](https://github.com/irods/irods/issues/2055) and [here](https://github.com/EUDAT-B2SAFE/B2SAFE-core/issues/18).

## demo for access control
The following three demo scripts are meant for demonstrating the access control for the "mdreviewer" roles which are only allowed to access the metadata but not the content of the collection.

1. create a new user that becomes the centre admin, and create a new collection by the centre admin.

    ```bash
    $ ./demo_centre_admin_create_collection.sh
    ```
    
2. add a demo user to each of the following roles of a collection: "contributor", "viewer", "reviewer", "mdreviewer"

    ```bash
    $ ./demo_coll_manager_addusers_to_collection.sh
    ```
    
    __Remark__:
    
    * since we use the iRODS group to implement the RDM role associated to access right, giving an access right to a user for a collection is done by adding the user in a corresponding iRODS user group.  For example, adding user `du_contributor_dac_00001` into group `dac_00001_contributor` gives the user the "contributor" right of the collection `dac_00001`.
    
    * since adding users into iRODS group can only be done by `rodsadmin` (on behalf of the collection "manager"). This is the consequence of using group-based ACL instead of user-based ACL.  However, user-based ACL requires to map the iRODS access rights onto RDM roles (and vice-versa) on the application layer.
    
3. show the access right in action for different RDM roles.

    ```bash
    $ ./demo_coll_ops_by_role.sh
    ```
    
    * contributor creates folder in collection
    * contributor uploads file into the created folder
    * contributor adds metadata to the collection
    * viewer/reviewer/mdreviewer retrieves metadata of the collection
    * viewer/reviewer/mdreviewer downloads the file in the collection
    
    In the above operations, only "mdrvewer downloads the file in the collection" will fail. It shows that the "mdreviewer" can only retrieve collection metadata.  Neither listing collection content nor downloading files is allowed.