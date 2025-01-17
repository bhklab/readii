from pandas import DataFrame

def replaceColumnValues(dataframe:DataFrame,
                       column_to_change:str,
                       replacement_value_data:dict
                       ):
    """Function to replace specified values in a column with a new value.

    Parameters
    ----------
    dataframe : DataFrame
        Dataframe to replace values in.
    column_to_change : str
        Name of the column to replace values in.
    replacement_value_data : dict
        Dictionary of values to replace in the column. Key is the new value, value is the old value(s) to replace.
        Can be a single value or a list of values.
    
    Returns
    -------
    dataframe : DataFrame
        Dataframe with values replaced.
    """

    # Check if the column name is a valid column in the dataframe
    if column_to_change not in dataframe.columns:
        raise ValueError(f"Column {column_to_change} not found in dataframe.")
    
    for new_value in replacement_value_data.keys():
        # Check if the replacement value is a valid value in the column
        old_values = replacement_value_data[new_value]
        values_not_found_in_column = set(old_values).difference(set(dataframe[column_to_change].unique()))
        if values_not_found_in_column == set(old_values):
            raise ValueError(f"All values in {values_not_found_in_column} are not found to be replaced in column {column_to_change}.")
        # Replace the old values with the new value
        dataframe = dataframe.replace(to_replace=replacement_value_data[new_value], 
                                      value=new_value)
        
    return dataframe


def splitDataByColumnValue(dataframe:DataFrame,
                           split_col_data:dict[str,list],
                           impute_value = None,
                           ):
    """Function to split a dataframe into multiple dataframes based on the values in a specified column. Optionally, impute values in the split columns.

    Parameters
    ----------
    dataframe : DataFrame
        Dataframe to split.
    split_col_data : dict[str,list]
        Dictionary of a column name and values to split the dataframe by. Key is the column name, value is the list of values to split by.
    impute_value (Optional)
        If set, will impute any non-specified split values in the split column with this value. The default is None.
    
    Returns
    -------
    split_dataframes : dict
        Dictionary of dataframes, where the key is the split value and the value is the dataframe for that split value.
    """
    
    # Initialize dictionary to store the split dataframes
    split_dataframes = {}

    for split_column_name in split_col_data.keys():
        # Check if the column name is a valid column in the dataframe
        if split_column_name not in dataframe.columns:
            raise ValueError(f"Column {split_column_name} not found in dataframe.")
    
        # Get split column values for this column
        split_col_values = split_col_data[split_column_name]
        
        if impute_value is not None:
            # Get all values in the column that are not one of the split_col_values
            column_value_set = set(dataframe[split_column_name].unique())
            split_value_set = set(split_col_values)
            non_split_values = list(column_value_set - split_value_set)

            # Replace all values not specified in the split_col_data with the impute_value specified for this column
            dataframe = replaceColumnValues(dataframe,
                                            column_to_change=split_column_name,
                                            replacement_value_data={impute_value: non_split_values})
            
        # End imputation
        
        # Split dataframe by the specified split_col_values
        for split_value in split_col_values:
            # Check if the split_value is a valid value in the column
            if split_value not in dataframe[split_column_name].unique():
                raise ValueError(f"Split value {split_value} not found in column {split_column_name}.")
            
            # Split the dataframe by the specified split_value
            split_dataframe = dataframe[dataframe[split_column_name] == split_value]

            split_dataframe.reset_index(inplace=True, drop=True)

            # Save the split dataframe to the dictionary
            split_dataframes[split_value] = split_dataframe

        # End dataframe splitting
    
    return split_dataframes
