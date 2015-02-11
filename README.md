# irods-restful-example
Example python scripts to demonstrate the irods-restful interface

## configuration file
The configuration file is located at `etc/config.ini`.  The contents in the file should be self-explained.

## run the script
Simply run the script as follows:

```Bash
$ ./server_get_info.py
```

## Notes on the workflow

For the demonstration purpose, resources are hard-coded in various scripts.  Therefore, one should be aware of the
following dependencies between scripts.

1. One should firstly run `collection_create.py` to create a collection called `dac_00002` hard-coded in the script so that
the script `collection_getacl.py`, `collection_setacl.py` and `collection_delete.py` will work.

2. Before running `collection_setacl.py`, one should firstly create the group `dac_00002_manager` using the script
`user_group_create.py`.  Also the `user_group_delete.py` works only the group `dac_00002_manager` has been created.

3. The script `collection_setacl.py` add the group `dac_00002_manager` as owner of the collection `dac_00002`.
