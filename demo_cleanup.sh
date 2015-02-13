#!/bin/bash
echo "====> Deleting the collection ..."
./collection_create.py dac_00002

echo "====> Deleting the groups associated to the group ..."
./group_delete.py dac_00002_manager dac_00002_contributor dac_00002_user
