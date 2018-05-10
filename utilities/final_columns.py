import pandas as pd


def user_cols(user_def_column_name, final_aoi_df, merged, analysis_names):
    # to keep columns from getting too long:
    new_cols = []

    # if ID in shapefile, rename it otherwise join will fail
    if 'ID' in final_aoi_df.columns:
        final_aoi_df = final_aoi_df.rename(columns={'ID': 'user_ID'})
        new_cols.append('user_ID')

    new_cols.append(user_def_column_name)

    print('assigning rows to user-def column values \n')

    # make new column equal to index number bc this is the join
    final_aoi_df['aoi_ID'] = final_aoi_df.index
    new_cols.append('aoi_ID')

    final_aoi_df = final_aoi_df[new_cols]

    # join zstats to shapefile
    joined = pd.merge(merged, final_aoi_df, left_on='ID', right_on='aoi_ID')

    columns_to_keep = [user_def_column_name]
    columns_to_keep.extend(['tcd', 'year'])
    columns_to_keep.extend(analysis_names)

    return joined[columns_to_keep]