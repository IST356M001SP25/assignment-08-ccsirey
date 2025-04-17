import pandas as pd
import streamlit as st 


def top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    grouped = violations_df.groupby('location', as_index=False)['amount'].sum()
    filtered = grouped[grouped['amount'] >= threshold]
    return filtered # TODO implement this function


def top_locations_mappable(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    top_locs = top_locations(violations_df, threshold)
    
    # Get representative lat/lon per location
    location_coords = violations_df.groupby('location', as_index=False)[['lat', 'lon']].first()
    
    # Merge top locations with their lat/lon
    merged = pd.merge(top_locs, location_coords, on='location', how='left')
    
    # Reorder columns
    return merged[['location', 'lat', 'lon', 'amount']]  # TODO implement this function


def tickets_in_top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    top_locations_df = top_locations(violations_df)
    merged_df = pd.merge(top_locations_df[['location']], violations_df, on='location')
    return merged_df

if __name__ == '__main__':
  if __name__ == '__main__':
    import pandas as pd
    violations_df = pd.read_csv('./cache/final_cuse_parking_violations.csv')

    top_locs_df = top_locations(violations_df)

    top_locs_df.to_csv('./cache/top_locations.csv', index=False)

    top_mappable_df = top_locations_mappable(violations_df)

    top_mappable_df.to_csv('./cache/top_locations_mappable.csv', index=False)

    tickets_in_top_locations_df = tickets_in_top_locations(violations_df, top_locs_df)

    tickets_in_top_locations_df.to_csv('./cache/tickets_in_top_locations.csv', index=False)