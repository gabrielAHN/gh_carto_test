import argparse
import cartoframes
import pandas as pd


from cartoframes.utils import decode_geometry
from geopandas import GeoDataFrame


cartoframes.auth.set_default_credentials('creds.json')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--table-name", required=True, help="name of the table to be uploaded")
    parser.add_argument("--url-upload", nargs='?', help="csv url to upload")
    parser.add_argument("--file-chunk", nargs='?', help="chunk size to download in MB if not given 100MB would be default")
    args = parser.parse_args()

    table_name = args.table_name
    url_upload = args.url_upload
    file_chunk_size = args.file_chunk

    if url_upload and file_chunk_size:
        upload_data_chunks(table_name, url_upload, file_chunk_size)
    elif url_upload and not file_chunk_size:
        upload_data_chunks(table_name, url_upload)
    else:
        raise Exception('You need to pick a command.\nTo see them type: python data_upload.py -h')


def upload_data_chunks(table_name, url, chunksize=100):
    chunksize = int(chunksize)
    data_chunks = pd.read_csv(url, iterator=True, chunksize=chunksize)
    for idx, chunk in enumerate(data_chunks, 1):
        geo_df = dataframe_geo_converstion(chunk)
        cartoframes.to_carto(
            geo_df, table_name, if_exists='append', max_upload_size=chunksize
        )
        print('Uploaded chunk {}'.format(idx))
    print('uploaded all file chunks successful ✅\nto {}\nfrom\n{}'.format(table_name, url))


def dataframe_geo_converstion(df):
    gdf = GeoDataFrame(df, geometry=decode_geometry(df['the_geom']))
    gdf = gdf.set_crs('epsg:4326')
    return gdf


if __name__ == "__main__":
    main()
