#!/bin/bash
echo "====> Deleting the collection ..."
./collection_delete.py -u demo_user dac_00002/raw_data
./collection_delete.py dac_00002

echo "====> Deleting the groups associated to the group ..."
./group_delete.py dac_00002_manager dac_00002_contributor dac_00002_viewer dac_00002_reviewer dac_00002_mdreviewer
