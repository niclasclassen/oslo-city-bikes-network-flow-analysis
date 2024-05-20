import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString


def create_stations_gdf(df: pd.DataFrame, crs_out: int = 3857) -> gpd.GeoDataFrame:
    # Create unique dataframes for start and end stations
    start_stations = df[
        [
            "start_station_id",
            "start_station_name",
            "start_station_description",
            "start_station_latitude",
            "start_station_longitude",
            # "month",
            # "year",
        ]
    ].drop_duplicates()
    end_stations = df[
        [
            "end_station_id",
            "end_station_name",
            "end_station_description",
            "end_station_latitude",
            "end_station_longitude",
            # "month",
            # "year",
        ]
    ].drop_duplicates()

    # Rename columns for uniformity
    start_stations.columns = [
        "station_id",
        "station_name",
        "station_description",
        "latitude",
        "longitude",
        # "month",
        # "year",
    ]
    end_stations.columns = [
        "station_id",
        "station_name",
        "station_description",
        "latitude",
        "longitude",
        # "month",
        # "year",
    ]

    # Concatenate the dataframes
    stations = pd.concat([start_stations, end_stations]).drop_duplicates()

    # Create GeoDataFrame
    gdf_stations = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations.longitude, stations.latitude),
        crs=crs_out,
    )
    return gdf_stations


def create_rides_gdf(df: pd.DataFrame, crs_out: int = 3857) -> gpd.GeoDataFrame:
    # Create a new DataFrame with necessary columns
    df_rides = df[
        [
            "start_station_id",
            "end_station_id",
            "started_at",
            "ended_at",
            "duration",
            "start_station_name",
            "start_station_description",
            "start_station_latitude",
            "start_station_longitude",
            "end_station_name",
            "end_station_description",
            "end_station_latitude",
            "end_station_longitude",
            # "month",
            # "year",
        ]
    ]

    # Create LineString objects
    df_rides["geometry"] = df_rides.apply(
        lambda row: LineString(
            [
                (row["start_station_longitude"], row["start_station_latitude"]),
                (row["end_station_longitude"], row["end_station_latitude"]),
            ]
        ),
        axis=1,
    )

    # Create GeoDataFrame
    gdf_rides = gpd.GeoDataFrame(df_rides, geometry="geometry", crs=crs_out)
    return gdf_rides


def create_oslo_districts_gdf(
    data_path: str = "data/Oslo_Kommuner.geojson",
    crs_in: int = 32633,
    crs_out: int = 3857,
) -> gpd.GeoDataFrame:
    gdf_oslo_kommuner = gpd.read_file(data_path)
    # Set the correct CRS
    gdf_oslo_kommuner.set_crs(crs_in, inplace=True, allow_override=True)

    # Reproject the data
    gdf_oslo_kommuner = gdf_oslo_kommuner.to_crs(epsg=crs_out)

    # rename columns
    gdf_oslo_kommuner = gdf_oslo_kommuner.rename(columns={"bydelnavn": "district"})

    return gdf_oslo_kommuner
