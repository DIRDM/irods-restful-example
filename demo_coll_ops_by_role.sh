#!/bin/bash
coll="dac_00001"
coll_manager="du_manager_$coll"
coll_contributor="du_contrib_$coll"
coll_viewer="du_viewer_$coll"
coll_reviewer="du_reviewer_$coll"
coll_mdreviewer="du_mdreviewer_$coll"

echo "====> 1. create folder 'raw_data' in $coll by $coll_contributor"
read
./collection_create.py -u $coll_contributor ${coll}/raw_data

echo "====> 2. upload 'data/fzero.100mb' in ${coll}/raw_data by $coll_contributor"
read
./file_upload.py -u $coll_contributor -p raw_data/fzero.100mb data/fzero.100mb $coll

echo "====> 3. Add the following metadata to collection $coll by $coll_contributor ..."
echo "====>    * projectId: 3010000.01"
echo "====>    * projectOwner: Hurng-Chun Lee"
echo "====>    * projectOwnerEmail: h.lee@donders.ru.nl"
echo "====>    * projectMgmtURL: http://projects.fcdonders.nl/index.php/projects/view/3010000.01"
read
./collection_metadata_add.py -u $coll_contributor -m 'projectId|3010000.01++projectMgmtURL|http://projects.fcdonders.nl/index.php/projects/view/3010000.01++projectOwner|Hurng-Chun Lee++projectOwnerEmail|h.lee@donders.ru.nl' $coll
 
echo "====> 4. Ops of collection viewer"
echo "====> 4.1 View the metadata of $coll by $coll_viewer"
read
./collection_metadata_get.py -u $coll_viewer $coll 
echo "====> 4.2 Download the data 'raw_data/fzero.100mb' from $coll by $coll_viewer"
read
rm -f fzero.100mb
./file_download.py -u $coll_viewer -p raw_data/fzero.100mb $coll
ls -lt fzero.100mb

echo "====> 5. Ops of collection reviewer"
echo "====> 5.1 View the metadata of $coll by $coll_reviewer"
read
./collection_metadata_get.py -u $coll_reviewer $coll 
echo "====> 5.2 Download the data 'raw_data/fzero.100mb' from $coll by $coll_reviewer"
read
rm -f fzero.100mb
./file_download.py -u $coll_reviewer -p raw_data/fzero.100mb $coll
ls -lt fzero.100mb

echo "====> 6. Ops of collection mdreviewer (Note: file download should not be allowed)"
echo "====> 6.1 View the metadata of $coll by $coll_mdreviewer"
read
./collection_metadata_get.py -u $coll_mdreviewer $coll 
echo "====> 6.2 Download the data 'raw_data/fzero.100mb' from $coll by $coll_mdreviewer"
read
rm -f fzero.100mb
./file_download.py -u $coll_mdreviewer -p raw_data/fzero.100mb $coll
ls -lt fzero.100mb
