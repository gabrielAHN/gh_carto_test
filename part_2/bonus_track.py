import argparse
import cartoframes
import geopandas as gpd
import pandas as pd


from cartoframes.utils import decode_geometry

cartoframes.auth.set_default_credentials('creds.json')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--table-name", required=True, help="Name of the Carto table to upload data")
    parser.add_argument("--csv-upload", help="Csv url/file to upload to Carto")
    parser.add_argument("--chunk-size", nargs='?', help="MB chunk size to upload data. Default 100 MB")
    args = parser.parse_args()

    table_name = args.table_name
    csv_file = args.csv_upload
    chunk_size = args.chunk_size

    upload_csv(csv_file, table_name, chunk_size)


def upload_csv(csv_url, table_name, chunk_size):
    chunk_size = get_chunk_size(csv_url, chunk_size)

    for df in pd.read_csv(csv_url, iterator=True, chunksize=chunk_size):
        gdf = dataframe_to_geodataframe(df)
        upload_data_chunks(table_name, gdf)
    print(
        'uploaded all data successfully ✅\nto {table_name}'.format(
            table_name=table_name
        )
    )


def get_chunk_size(csv_url, chunk_size):
    if chunk_size:
        chunk_size = int(chunk_size)*1000000
    if not chunk_size:
        chunk_size = 100000000

    df_sample = pd.read_csv(csv_url, nrows=10)
    gdf_sample = dataframe_to_geodataframe(df_sample)
    df_sample_size = gdf_sample.memory_usage(index=True).sum()
    my_chunk = (chunk_size // df_sample_size) / 10
    my_chunk = int(my_chunk // 1)
    return my_chunk


def upload_data_chunks(table_name, gdf):
    try:
        cartoframes.to_carto(
            gdf, table_name, if_exists='append',
            max_upload_size=100, retry_times=3
        )
    except:
        raise Exception("Sorry, upload failed too many upload requests")

    print('uploaded chunk successfully')


def dataframe_to_geodataframe(df):
    gdf = gpd.GeoDataFrame(df, geometry=decode_geometry(df['the_geom']))
    gdf = gdf.set_crs('epsg:4326')
    return gdf


if __name__ == "__main__":
    main()
