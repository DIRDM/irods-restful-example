#!/bin/bash

echo "====> 1. Creating a new collection ..."
./collection_create.py dac_00002
read

echo "====> 2. Creating user groups associated with the colleciton ..."
./group_create.py dac_00002_manager dac_00002_contributor dac_00002_user
read

echo "====> 3. Setting the group permission for the collection ..."
./collection_setacl.py dac_00002
read

echo "====> 4. Showing the group permission for the collection ..."
./collection_getacl.py dac_00002

