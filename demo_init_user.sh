#!/bin/bash
echo "====> 1. Create a new user 'demo_user' ..."
read
echo -n "password of new user: "
read -s pass
./user_create.py -p $pass demo_user

echo "====> 2. Add user 'demo_user' to 'donders_user' group ..."
read
./group_adduser.py -u demo_user donders_user

echo "====> 2. Give user 'demo_user' the manager permission of collection 'dac_00002' ..."
echo "====>    This is done by adding user to group 'dac_00002_manager'."
read
./group_adduser.py -u demo_user dac_00002_manager

echo "====> 3. Get information of user 'demo_user' ..."
read
./user_get_info.py demo_user
