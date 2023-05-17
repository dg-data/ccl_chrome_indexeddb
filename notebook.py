import json
import logging as log
import sys
import ccl_chromium_indexeddb
from ccl_blink_value_deserializer import BlinkV8Deserializer
from ccl_v8_value_deserializer import Deserializer
# reading IPython notebook content from IndexedDB (and saving to disk)
save_content = False
log.basicConfig(stream=sys.stdout, level=log.DEBUG)
profile_path = r'C:\Users\DG\Desktop\Opera\profile\data\IndexedDB\\'
url = 'https://hub.gke2.mybinder.org'
# paths to the .leveldb and .blob folders
leveldb_folder_path = profile_path + url.replace('://', '_', 1) + '_0.indexeddb.leveldb'
blob_folder_path = profile_path + url.replace('://', '_', 1) + '_0.indexeddb.blob'
# open indexedDB
wrapper = ccl_chromium_indexeddb.WrappedIndexDB(leveldb_folder_path, blob_folder_path)
log.debug(f'found {wrapper.database_count} database(s)')
db = wrapper[1]
log.debug(f'In {db.name} found {db[1].name}')

for record in db[1].iterate_records(
    errors_to_stdout=True, 
        bad_deserializer_data_handler=lambda k,v: log.error(f"error: {k}, {v}")):
    try:
        log.debug(f'{record.key} has {len(record.value["content"]["cells"])} cell(s)')
    except:
        log.debug(f'{record.key} has no content')
        continue
    value = record.value
    if save_content:
        try:
            with open(value['name'], 'w') as j:
                json.dump(value['content'], j)
            log.debug(f'{value["name"]} saved')
        except:
            log.error(f'Error dumping {value["name"]}')
            
