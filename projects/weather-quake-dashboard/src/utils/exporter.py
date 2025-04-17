import pandas as pd
import io
import geopandas as gpd


def export_dataframe_as_excel(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()


def export_dataframe_as_csv(df: pd.DataFrame) -> str:
    return df.to_csv(index=False)


def export_dataframe_as_html(df: pd.DataFrame) -> str:
    return df.to_html(index=False)


def export_quakes_and_boundaries_geojson(quake_df: pd.DataFrame, boundary_gdf: gpd.GeoDataFrame) -> str:
    """
    Merge earthquake points and tectonic boundary lines into a single GeoJSON FeatureCollection.
    """
    features = []

    if not quake_df.empty:
        quake_gdf = gpd.GeoDataFrame(
            quake_df.copy(),
            geometry=gpd.points_from_xy(quake_df['Longitude'], quake_df['Latitude']),
            crs="EPSG:4326"
        )
        features.extend(quake_gdf.__geo_interface__["features"])

    if boundary_gdf is not None and not boundary_gdf.empty:
        features.extend(boundary_gdf.__geo_interface__["features"])

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return io.StringIO(str(pd.io.json.dumps(geojson))).getvalue()
