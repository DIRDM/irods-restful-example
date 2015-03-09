#!/bin/bash
coll="dac_00001"
centre_admin="du_dccn_admin"
coll_contributor="du_contributor_${coll}"

echo "====> Deleting the collection ..."
./collection_delete.py -u $coll_contributor -c dccn dac_00001

echo "====> Deleting the groups associated to the group ..."
./group_delete.py ${coll}_manager ${coll}_contributor ${coll}_viewer ${coll}_reviewer ${coll}_mdreviewer
