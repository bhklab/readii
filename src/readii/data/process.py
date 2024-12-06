from pandas import DataFrame
from typing import Optional

def dropUpToFeature(dataframe:DataFrame,
                    feature_name:str,
                    keep_feature_name_column:Optional[bool] = False
                    ):
    """ Function to drop all columns up to and possibly including the specified feature.

    Parameters
    ----------
    dataframe : DataFrame
        Dataframe to drop columns from.
    feature_name : str
        Name of the feature to drop up to.
    keep_feature_name_column : bool, optional
        Whether to keep the specified feature name column in the dataframe or drop it. The default is False.
        
    Returns
    -------
    dataframe : DataFrame
        Dataframe with all columns up to and including the specified feature dropped.
    """
    try:
        if keep_feature_name_column:
            # Get the column names up to but not including the specified feature
            column_names = dataframe.columns.to_list()[:dataframe.columns.get_loc(feature_name)]
        else:
            # Get the column names up to and including the specified feature
            column_names = dataframe.columns.to_list()[:dataframe.columns.get_loc(feature_name)+1]

        # Drop all columns up to and including the specified feature
        dataframe_dropped_columns = dataframe.drop(columns=column_names)

        return dataframe_dropped_columns
    
    except KeyError:
        print(f"Feature {feature_name} was not found as a column in dataframe. No columns dropped.")
        return dataframe
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None