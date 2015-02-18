#!/bin/bash

echo "====> 1. Create a new collection dac_00002 ..."
read
./collection_create.py dac_00002

echo "====> 2. Create user groups associated with the colleciton dac_00002 ..."
read
./group_create.py dac_00002_manager dac_00002_contributor dac_00002_user

echo "====> 3. Set group permission for collection dac_00002 ..."
read
./collection_setacl.py dac_00002

echo "====> 4. Show group permission of collection dac_00002 ..."
read
./collection_getacl.py dac_00002
