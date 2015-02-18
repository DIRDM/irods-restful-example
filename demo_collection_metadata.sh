#!/bin/bash
echo "====> 1. Add metadata to collection dac_00002 for linking to project 3010000.01 ..."
echo "====>    * projectId: 3010000.01"
echo "====>    * projectOwner: Hurng-Chun Lee"
echo "====>    * projectOwnerEmail: h.lee@donders.ru.nl"
echo "====>    * projectMgmtURL: http://projects.fcdonders.nl/index.php/projects/view/3010000.01"
read
./collection_metadata_add.py -u demo_user -m 'projectId|3010000.01,projectMgmtURL|http://projects.fcdonders.nl/index.php/projects/view/3010000.01,projectOwner|Hurng-Chun Lee,projectOwnerEmail|h.lee@donders.ru.nl' dac_00002

echo "====> 2. Get metadata of collection dac_00002 ..."
read
./collection_metadata_get.py -u demo_user dac_00002

echo "====> 3. Delete metadata 'projectOwner' from collection dac_00002 ..."
read
./collection_metadata_del.py -u demo_user -m 'projectOwner|Hurng-Chun Lee' dac_00002

echo "====> 4. Get metadata of collection dac_00002 ..."
read
./collection_metadata_get.py -u demo_user dac_00002
