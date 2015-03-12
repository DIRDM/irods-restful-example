#!/bin/bash
coll=$1
coll_manager="du_manager_$coll"
coll_contributor="du_contrib_$coll"
coll_viewer="du_viewer_$coll"
coll_reviewer="du_reviewer_$coll"
coll_mdreviewer="du_mdreviewer_$coll"

echo "!! Adding users into group requires rodsadmin role !!"
echo
echo "====> 1. Add '${coll_contributor}' as contributor of $coll"
read
echo -n "password of new user: "
read -s pass
./user_create.py -p $pass $coll_contributor
./group_adduser.py -u $coll_contributor ${coll}_contributor

echo "====> 2. Add '${coll_viewer}' as viewer of $coll"
read
./user_create.py -p $pass $coll_viewer
./group_adduser.py -u $coll_viewer ${coll}_viewer

echo "====> 3. Add '${coll_reviewer}' as reviewer of $coll"
read
./user_create.py -p $pass $coll_reviewer
./group_adduser.py -u $coll_reviewer ${coll}_reviewer

echo "====> 4. Add '${coll_mdreviewer}' as mdreviewer of $coll"
read
./user_create.py -p $pass $coll_mdreviewer
./group_adduser.py -u $coll_mdreviewer ${coll}_mdreviewer
