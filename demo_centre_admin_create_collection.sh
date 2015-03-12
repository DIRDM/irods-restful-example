#!/bin/bash
new_coll=$1
user_name="du_dccn_admin"
coll_manager="du_manager_${new_coll}"

echo "====> 1. Create demo user '${user_name}'"
read
echo -n "password of new user: "
read -s pass
./user_create.py -p $pass du_dccn_admin

echo "====> 2. Add demo user '${user_name}' into DCCN admin group"
read
./group_adduser.py -u ${user_name} dccn_admin

echo "====> 3. Create the following groups for collection ${new_coll}"
echo "====>    - ${new_coll}_manager"
echo "====>    - ${new_coll}_contributor"
echo "====>    - ${new_coll}_viewer"
echo "====>    - ${new_coll}_reviewer"
echo "====>    - ${new_coll}_mdreviewer"
echo "====>    Note: this step has to be done before the creation of the collection"
read
./group_create.py ${new_coll}_manager ${new_coll}_contributor ${new_coll}_viewer ${new_coll}_reviewer ${new_coll}_mdreviewer 

echo "====> 4. Create new collection '${new_coll}'"
read
./collection_create.py -u ${user_name} ${new_coll}

echo "====> 5. Add user ${coll_manager} as manager of '${new_coll}'"
read
./user_create.py -p $pass ${coll_manager}
./group_adduser.py -u ${coll_manager} ${new_coll}_manager

echo "====> 4. Show group permission of collection ${new_coll}"
read
./collection_getacl.py -u ${coll_manager} ${new_coll}
