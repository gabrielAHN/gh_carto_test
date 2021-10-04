# 2. Python Support Engineer Test - Sample creation

Below are two scripts for uploading data to CARTO excerise.

    main_exercise.py
    bonus_track.py


## Setup

### Add Creds
In `creds.json` file add your Carto `username` and `api_key`

### Installs
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## main_exercise.py

### Use

#### Command
You can use the script below with these config flags.

- `--table-name`: The name of table that will be created once you upload the file. *This is a required field*
- `--geojson-url-upload`: Url of the geojson file you want to upload.
- `--csv-url-upload`: Url of the csv file you want to upload.
- `--row-size`: The number of rows read and uploaded to the Carto database.

```
python  main_exercise.py [-h] --table-name TABLE_NAME (--csv-url-upload CSV_URL_UPLOAD | --geojson-url-upload GEOJSON_URL_UPLOAD) [--row-size [ROW_SIZE]]
```

#### Example
```
 # Here we are creating a table named test to the Carto database and uploading a file found from this [url](https://data.cityofnewyork.us/api/views/bntt-wmh5/rows.csv\?accessType\=DOWNLOAD) to it. Also, we will be reading and uploading the files by 10 rows.

 python  main_exercise.py --table-name test --csv-url-upload https://data.cityofnewyork.us/api/views/bntt-wmh5/rows.csv\?accessType\=DOWNLOAD --row-size 10

 # Here we are creating a table named test_2 to the Carto database and uploading a file found from this [url](https://data.cityofnewyork.us/api/geospatial/p5vh-vm7p?method=export&format=GeoJSON) to it. Also, we will be reading and uploading the files by 15 rows.

python  main_exercise.py --table-name test --geojson-url-upload https://data.cityofnewyork.us/api/geospatial/p5vh-vm7p?method=export&format=GeoJSON --row-size 15
```

## bonus_track.py

### Use

#### Command
You can use the script below with these config flags.

- `--table-name`: The name of table that will be created once you upload the file. *This is a required field*
- `--csv-upload`: Csv url/file to upload
- `--chunk-size`: MB chunk size to upload file. Default 100 MB.

```
python bonus_track.py --table-name TABLE_NAME [--csv-upload CSV_UPLOAD][--chunk-size [CHUNK_SIZE]]
```

#### Example
```
 # Here we create a table named test_3 to the Carto database and uploading a file found from this [url](https://data.cityofnewyork.us/api/views/bntt-wmh5/rows.csv\?accessType\=DOWNLOAD) to it. We will be downloading and uploading in 1 MB size chunks.

python bonus_track.py --table-name test_3 --csv-upload https://data.cityofnewyork.us/api/views/bntt-wmh5/rows.csv\?accessType\=DOWNLOAD --chunk-size 1

