#!/bin/bash
echo "====> 1. Upload file 'data/fzero.100mb' to collection dac_00002/raw_data/fzero.100mb.1 ..."
read

echo "======> 1-1. create directory 'raw_data' in dac_00002 ..."
read
./collection_create.py -u demo_user dac_00002/raw_data

echo "======> 1-2. upload local file 'data/fzero.100mb' to path 'raw_data/fzero.100mb.1' ..."
read
./file_upload.py -u demo_user -p raw_data/fzero.100mb.1 data/fzero.100mb dac_00002

echo "======> 1-3. upload annotation 'data/README' to collection 'dac_00002' ..."
read
./file_upload.py -u demo_user data/README dac_00002

echo "====> 2. List file 'raw_data/fzero.100mb.1' in collection dac_00002 ..."
read
./file_list.py -u demo_user -p raw_data/fzero.100mb.1 dac_00002

echo "====> 3. Download file 'raw_data/fzero.100mb.1' from collection dac_00002 ..."
read
./file_download.py -u demo_user -p raw_data/fzero.100mb.1 dac_00002

echo "====> 4. Delete file 'raw_data/fzero.100mb.1' from collection dac_00002 ..."
read
./file_delete.py -u demo_user -p raw_data/fzero.100mb.1 dac_00002
