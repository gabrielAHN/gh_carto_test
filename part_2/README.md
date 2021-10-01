# 2. Python Support Engineer Test - Sample creation

Below is a script to download csv from urls and upload them to CARTO by chunks.

## Setup

### Add Creds
In `creds.json` file add your Carto `username` and `api_key`

### Installs
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Use

### Command
You can use the script below with these config flags.

- `--table-name`: The name of table that will be created once you upload the file. *This is a required field*
- `--url-upload`: Url of the csv file you want to upload.
- `--file-chunk`: The size of the chunks to upload to the online Carto database.

```
python data_uploader.py --table-name TABLE_NAME [--url-upload [URL_UPLOAD]] [--file-chunk [FILE_CHUNK]]
```

### Example
```
 # Here we create a table named test to the Carto database and uploading a file found from this [url](https://data.cityofnewyork.us/api/views/bntt-wmh5/rows.csv\?accessType\=DOWNLOAD) to it. Also, we will be downloading and uploading in 1 MB size chunks.

 python data_uploader.py --table-name test --url-upload https://data.cityofnewyork.us/api/views/bntt-wmh5/rows.csv\?accessType\=DOWNLOAD --file-chunk 1

```