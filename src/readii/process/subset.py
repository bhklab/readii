from typing import Optional

from pandas import DataFrame

from readii.utils import logger

from .label import setPatientIdAsIndex


def dropUpToFeature(dataframe:DataFrame,
                    feature_name:str,
                    keep_feature_name_column:Optional[bool] = False
                    ) -> DataFrame:
    """Drop all columns up to and possibly including the specified feature.

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
        logger.warning(f"Feature {feature_name} was not found as a column in dataframe. No columns dropped.")
        return dataframe
    
    except Exception as e:
        logger.exception(f"An error occurred in dropUpToFeature: {e}")
        raise e
    


def selectByColumnValue(dataframe:DataFrame, 
                        include_col_values:Optional[dict] = None,
                        exclude_col_values:Optional[dict] = None
                        ) -> DataFrame:
    """
    Get rows of pandas DataFrame based on row values in the columns labelled as keys of the include_col_values and not in the keys of the exclude_col_values. Include variables will be processed first, then exclude variables, in the order they are provided in the corresponding dictionaries.

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
            msg = "Must provide one of include_col_values or exclude_col_values."
            logger.exception(msg)
            raise ValueError(msg)
    
        if include_col_values is not None:
            for key in include_col_values:
                if key in ["Index", "index"]:
                    dataframe = dataframe[dataframe.index.isin(include_col_values[key])]
                else:
                    dataframe = dataframe[dataframe[key].isin(include_col_values[key])]

        if exclude_col_values is not None:
            for key in exclude_col_values:
                if key in ["Index", "index"]:
                    dataframe = dataframe[~dataframe.index.isin(exclude_col_values[key])]
                else:
                    dataframe = dataframe[~dataframe[key].isin(exclude_col_values[key])]
        
        return dataframe

    except Exception as e:
        logger.exception(f"An error occurred in selectByColumnValue: {e}")
        raise e
    

def getOnlyPyradiomicsFeatures(radiomic_data:DataFrame) -> DataFrame:
    """Get out just the features from a PyRadiomics output that includes metadata/diagnostics columns before the features. Will look for the last diagnostics column or the first PyRadiomics feature column with the word "original" in it.

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
            pyradiomic_features_only = dropUpToFeature(radiomic_data, first_pyradiomic_feature_column, keep_feature_name_column=True)
        else:
            msg = "PyRadiomics file doesn't contain any diagnostics or original feature columns, so can't find beginning of features. Use dropUpToFeature and specify the last non-feature or first PyRadiomic feature column name to get only PyRadiomics features."
            logger.exception(msg)
            raise ValueError(msg)

    return pyradiomic_features_only



def getPatientIntersectionDataframes(dataframe_A:DataFrame, 
                                     dataframe_B:DataFrame,
                                     need_pat_index_A:bool = True,
                                     need_pat_index_B:bool = True
                                     ) -> DataFrame: 
    """Get the subset of two dataframes based on the intersection of their indices. Intersection will be based on the index of dataframe A.

    Parameters
    ----------
    dataframe_A : DataFrame
        Dataframe A to get the intersection of based on the index.
    dataframe_B : DataFrame
        Dataframe B to get the intersection of based on the index.
    need_pat_index_A : bool, optional
        Whether to run setPatientIdAsIndex on dataframe A. If False, assumes the patient ID column is already set as the index. The default is True.
    need_pat_index_B : bool, optional
        Whether to run setPatientIdAsIndex on dataframe B. If False, assumes the patient ID column is already set as the index. The default is True.

    Returns
    -------
    intersection_index_dataframeA : DataFrame
        Dataframe containing the rows of dataframe A that are in the intersection of the indices of dataframe A and dataframe B.
    intersection_index_dataframeB : DataFrame
        Dataframe containing the rows of dataframe B that are in the intersection of the indices of dataframe A and dataframe B.
    """
    # Set the patient ID column as the index for dataframe A if needed
    if need_pat_index_A:
        dataframe_A = setPatientIdAsIndex(dataframe_A)

    # Set the patient ID column as the index for dataframe B if needed
    if need_pat_index_B:
        dataframe_B = setPatientIdAsIndex(dataframe_B)

    # Get patients in common between dataframe A and dataframe B
    intersection_index = dataframe_A.index.intersection(dataframe_B.index)

    # Select common patient rows from each dataframe
    intersection_index_dataframeA = dataframe_A.loc[intersection_index]
    intersection_index_dataframeB = dataframe_B.loc[intersection_index]

    return intersection_index_dataframeA, intersection_index_dataframeB


# Katy (Jan 2025): I think I wrote this function for the correlation functions, but I don't think it's used.
# def validateDataframeSubsetSelection(dataframe:DataFrame,
#                                      num_rows:Optional[int] = None,
#                                      num_cols:Optional[int] = None
#                                      ) -> None:
    
#     # Check if dataframe is a DataFrame
#     if not isinstance(dataframe, DataFrame):
#         msg = f"dataframe must be a pandas DataFrame, got {type(dataframe)}"
#         logger.error(msg)
#         raise TypeError(msg)
    
#     if num_rows is not None:
#         # Check if num_rows is an integer
#         if not isinstance(num_rows, int):
#             msg = f"num_rows must be an integer, got {type(num_rows)}"
#             logger.error(msg)
#             raise TypeError(msg)
        
#         if num_rows > dataframe.shape[0]:
#             msg = f"num_rows ({num_rows}) is greater than the number of rows in the dataframe ({dataframe.shape[0]})"
#             logger.error(msg)
#             raise ValueError()
#     else:
#         logger.debug("Number of rows is within the size of the dataframe.")    
    
        
#     if num_cols is not None:
#         # Check if num_cols is an integer
#         if not isinstance(num_cols, int):
#             msg = f"num_cols must be an integer, got {type(num_cols)}"
#             logger.error(msg)
#             raise TypeError(msg)
        
#         if num_cols > dataframe.shape[1]:
#             msg = f"num_cols ({num_cols}) is greater than the number of columns in the dataframe ({dataframe.shape[1]})"
#             logger.error(msg)
#             raise ValueError()
#     else:
#         logger.debug("Number of columns is within the size of the dataframe.")




