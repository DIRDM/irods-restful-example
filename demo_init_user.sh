#!/bin/bash

echo "====> 1. Creating a new user ..."
echo -n "password of new user: "
read -s pass
./user_create.py -p $pass demo_user
read

echo "====> 2. Adding user to donders_user group ..."
./group_adduser.py -u demo_user donders_user
read

echo "====> 2. Giving user the manager permission of dac_00002 ..."
./group_adduser.py -u demo_user dac_00002_manager
read

echo "====> 3. Getting the user information ..."
./user_get_info.py demo_user
