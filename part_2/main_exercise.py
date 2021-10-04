import argparse
import cartoframes
import geopandas as gpd
import pandas as pd


from cartoframes.utils import decode_geometry

cartoframes.auth.set_default_credentials('creds.json')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--table-name", required=True, help="name of the table to upload data")
    file_type = parser.add_mutually_exclusive_group(required=True)
    file_type.add_argument("--csv-url-upload", help="csv url to upload")
    file_type.add_argument("--geojson-url-upload", help="geojson url to upload")
    parser.add_argument("--row-size", nargs='?', help="Number of rows to read and upload. Default 10 rows")
    args = parser.parse_args()

    table_name = args.table_name
    csv_url = args.csv_url_upload
    geojson_url = args.geojson_url_upload
    row_size = args.row_size

    if not row_size:
        row_size = 10

    if geojson_url:
        gdf = get_geojson(geojson_url, row_size)
        upload_data_chunks(table_name, gdf, row_size)
    elif csv_url:
        gdf = get_csv(csv_url, row_size)
        upload_data_chunks(table_name, gdf, row_size)


def get_geojson(geojson_url, row_size):
    gdf = gpd.read_file(geojson_url, rows=int(row_size))
    return gdf


def get_csv(csv_url, row_size):
    with pd.read_csv(csv_url, iterator=True) as reader:
        df = reader.get_chunk(int(row_size))
        gdf = dataframe_to_geodataframe(df)
        return gdf


def upload_data_chunks(table_name, gdf, row_size):
    cartoframes.to_carto(
        gdf, table_name, if_exists='replace'
    )
    print(
        'uploaded {row_size} rows successful ✅\nto {table_name}'.format(
            row_size=row_size,
            table_name=table_name
        )
    )


def dataframe_to_geodataframe(df):
    gdf = gpd.GeoDataFrame(df, geometry=decode_geometry(df['the_geom']))
    gdf = gdf.set_crs('epsg:4326')
    return gdf


if __name__ == "__main__":
    main()
