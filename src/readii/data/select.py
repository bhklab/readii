from pandas import DataFrame
from typing import Optional

import pandas as pd

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
    


def selectByColumnValue(dataframe:DataFrame, 
                        include_col_values:Optional[dict] = None,
                        exclude_col_values:Optional[dict] = None) -> pd.DataFrame:
    """
    Get rows of pandas DataFrame based on row values in the columns labelled as keys of the include_col_values and not in the keys of the exclude_col_values.
    Include variables will be processed first, then exclude variables, in the order they are provided in the corresponding dictionaries.

    Parameters
    ----------
    dataframeToSubset : pd.DataFrame
        Dataframe to subset.
    include_col_values : dict
        Dictionary of column names and values to include in the subset. ex. {"column_name": ["value1", "value2"]}
    exclude_col_values : dict
        Dictionary of column names and values to exclude from the subset. ex. {"column_name": ["value1", "value2"]}

    Returns
    -------
    pd.DataFrame
        Subset of the input dataframe.

    """
    try:
        if (include_col_values is None) and (exclude_col_values is None):
            raise ValueError("Must provide one of include_col_values or exclude_col_values.")
    
        if include_col_values is not None:
            for key in include_col_values.keys():
                if key in ["Index", "index"]:
                    dataframe = dataframe[dataframe.index.isin(include_col_values[key])]
                else:
                    dataframe = dataframe[dataframe[key].isin(include_col_values[key])]

        if exclude_col_values is not None:
            for key in exclude_col_values.keys():
                if key in ["Index", "index"]:
                    dataframe = dataframe[~dataframe.index.isin(exclude_col_values[key])]
                else:
                    dataframe = dataframe[~dataframe[key].isin(exclude_col_values[key])]
        
        return dataframe

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def getOnlyPyradiomicsFeatures(radiomic_data:DataFrame):
    """ Function to get out just the features from a PyRadiomics output that includes metadata/diagnostics columns before the features.
        Will look for the last diagnostics column or the first PyRadiomics feature column with the word "original" in it
    Parameters
    ----------
    radiomic_data : DataFrame
        Dataframe of Pyradiomics features with diagnostics and other columns before the features
    
    Returns
    -------
    pyradiomic_features_only : DataFrame
        Dataframe with just the radiomic features
    
    """
    # Find all the columns that begin with diagnostics
    diagnostic_data = radiomic_data.filter(regex=r"diagnostics_*")

    if not diagnostic_data.empty:
        # Get the last diagnostics column name - the features begin in the next column
        last_diagnostic_column = diagnostic_data.columns[-1]
        # Drop all the columns before the features start
        pyradiomic_features_only = dropUpToFeature(radiomic_data, last_diagnostic_column, keep_feature_name_column=False)

    else:
        original_feature_data = radiomic_data.filter(regex=r'^original_*')
        if not original_feature_data.empty:
            # Get the first original feature column name - the features begin in this column
            first_pyradiomic_feature_column = original_feature_data.columns[0]
            # Drop all the columns before the features start
            pyradiomic_features_only = dropUpToFeature(radiomic_data, first_pyradiomic_feature_column, keep_feature_name=True)
        else:
            raise ValueError("PyRadiomics file doesn't contain any diagnostics or original feature columns, so can't find beginning of features. Use dropUpToFeature and specify the last non-feature or first PyRadiomic feature column name to get only PyRadiomics features.")

    return pyradiomic_features_only