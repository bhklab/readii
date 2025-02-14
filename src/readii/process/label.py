import re
from typing import Optional

import numpy as np
from pandas import DataFrame, Series

from readii.process.split import replaceColumnValues
from readii.utils import logger


def getPatientIdentifierLabel(dataframe_to_search:DataFrame) -> str:
    r"""Find a column in a dataframe that contains some form of patient ID or case ID (case-insensitive). If multiple found, will return the first match.

       Current regex is: '(pat)?(ient)?(case)?(\s|.)?(id|#)'

    Parameters
    ----------
    dataframe_to_search : DataFrame
        Dataframe to look for a patient ID column in.

    Returns
    -------
    str
        Label for patient identifier column from the dataframe.
    """
    # regex to get patient identifier column name in the dataframes
    # catches case-insensitive variations of patient_id, patid, pat id, case_id, case id, caseid, id
    id_search_term = re.compile(pattern= r'(pat)?(ient)?(case)?(\s|.)?(id|#)', flags=re.IGNORECASE)

    # Get any columns from the dataframe based on the regex
    patient_identifier = dataframe_to_search.filter(regex=id_search_term).columns.to_list()

    if len(patient_identifier) > 1:
        logger.debug(f"Multiple patient identifier labels found. Using {patient_identifier[0]}.")
    
    elif len(patient_identifier) == 0:
        msg = "Dataframe doesn't have a recognizeable patient ID column. Must contain patient or case ID."
        logger.exception(msg)
        raise ValueError()

    return patient_identifier[0]



def setPatientIdAsIndex(dataframe_to_index:DataFrame,
                        patient_id_col:str = None
                        ) -> DataFrame:
    """Set the patient ID column as the index of a dataframe.

    Parameters
    ----------
    dataframe : DataFrame
        Dataframe to set the patient ID column as the index.
    patient_id_col : str, optional
        Name of the patient ID column to use as the index. If not provided, will find the patient ID column with getPatientIdentifierLabel.
    """
    if not patient_id_col:
        patient_id_col = getPatientIdentifierLabel(dataframe_to_index)
        
    pat_indexed_dataframe = dataframe_to_index.set_index(patient_id_col)
    return pat_indexed_dataframe



def convertDaysToYears(dataframe_with_outcome:DataFrame,
                       time_column_label:str,
                       divide_by:int = 365
                       ) -> DataFrame:
    """Create a copy of a time outcome column mesaured in days and convert it to years.

    Parameters
    ----------
    dataframe_with_outcome : DataFrame
        Dataframe containing the outcome column to convert.
    time_column_label : str
        Label for the time column to convert in the dataframe.
    divide_by : int, optional
        Value to divide the time column by. The default is 365.

    Returns
    -------
    dataframe_with_outcome : DataFrame
        Dataframe with a copy of the specified time column converted to years.
    """
    # Set up the new column name for the converted time column
    years_column_label = time_column_label + "_years"
    # Make a copy of the time column with the values converted from days to years and add suffic _years to the column name
    dataframe_with_outcome[years_column_label] = dataframe_with_outcome[time_column_label] / divide_by

    return dataframe_with_outcome



def timeOutcomeColumnSetup(dataframe_with_outcome:DataFrame,
                            outcome_column_label:str,
                            standard_column_label:str,
                            convert_to_years:bool = False,
                            ) -> DataFrame:
    """Set up a time outcome column in a dataframe. Makes a copy of the specified outcome column with a standardized column name and converts it to years if specified.

    Parameters
    ----------
    dataframe_with_outcome : DataFrame
        Dataframe containing the outcome column to convert.
    outcome_column_label : str
        Label for the outcome column to convert in the dataframe.
    standard_column_label : str
        Name of the column to save the standardized outcome column as.
    convert_to_years : bool, optional
        Whether to convert the time column to years. The default is False.

    Returns
    -------
    dataframe_with_outcome : DataFrame
        Dataframe with a copy of the specified outcome column converted to years.    
    """
    # Check if the outcome column is numeric
    if not np.issubdtype(dataframe_with_outcome[outcome_column_label].dtype, np.number):
        msg = f"{outcome_column_label} is not numeric. Please confirm outcome_column_label is the correct column or convert the column in the dataframe to numeric."
        logger.exception(msg)
        raise ValueError()
        
    else:
        # Make a copy of the dataframe to work on
        dataframe_with_standardized_outcome = dataframe_with_outcome.copy()

        if convert_to_years:
            logger.debug("Converting outcome column to years by dividing by 365.")
            # Create a copy of the outcome column and convert it to years
            dataframe_with_standardized_outcome = convertDaysToYears(dataframe_with_standardized_outcome, outcome_column_label)

            # Rename the converted column with the standardized name
            dataframe_with_standardized_outcome.rename(columns={f"{outcome_column_label}_years": standard_column_label}, inplace=True)
        else:

            # Make a copy of the outcome column with the standardized name
            dataframe_with_standardized_outcome[standard_column_label] = dataframe_with_standardized_outcome[outcome_column_label]
    
    return dataframe_with_standardized_outcome



def survivalStatusToNumericMapping(event_outcome_column:Series) -> dict:
    """Convert a survival status column to a numeric column by iterating over unique values and assigning a numeric value to each.
    
    Alive values will be assigned a value of 0, and dead values will be assigned a value of 1.
    If "alive" is present, next event value index will start at 1. If "dead" is present, next event value index will start at 2.
    Any NaN values will be assigned the value "unknown", then converted to a numeric value.

    Parameters
    ----------
    event_outcome_column : Series
        Series containing the survival status values.

    Returns
    -------
    event_column_value_mapping : dict
        Dictionary mapping the survival status values to numeric values.
    """
    # Create a dictionary to map event values to numeric values
    event_column_value_mapping = {}
    # Get a list of all unique event values, set NaN values to unknown, set remaining values to lower case
    existing_event_values = event_outcome_column.fillna("unknown").str.lower().unique()

    # Set the conversion value for the first event value to 0
    other_event_num_value = 0

    # See if alive is present, and set the conversion value for alive to 0
    if "alive" in existing_event_values:
        event_column_value_mapping['alive'] = 0
        # Remove alive from the list of existing event values
        existing_event_values.remove("alive")
        # Update starting value for other event values
        other_event_num_value = 1

    # See if dead is present, and set the conversion value for dead to 1
    if "dead" in existing_event_values:
        event_column_value_mapping['dead'] = 1
        # Remove dead from the list of existing event values
        existing_event_values.remove("dead")
        # Update starting value for other event values
        other_event_num_value = 2

    # Set the conversion value for the other event values to the next available value
    for other_event_value in existing_event_values:
        event_column_value_mapping[other_event_value] = other_event_num_value
        other_event_num_value += 1


    return event_column_value_mapping



def eventOutcomeColumnSetup(dataframe_with_outcome:DataFrame,
                            outcome_column_label:str,
                            standard_column_label:str,
                            event_column_value_mapping:Optional[dict]=None
                            ) -> DataFrame:
    """Set up an event outcome column in a dataframe.

    Parameters
    ----------
    dataframe_with_outcome : DataFrame
        Dataframe containing the outcome column to convert.
    outcome_column_label : str
        Label for the outcome column to convert in the dataframe.
    standard_column_label : str
        Name of the column to save the standardized outcome column as.
    event_column_value_mapping : dict, optional
        Dictionary of event values to convert to numeric values. Keys are the event values, values are the numeric values. If provided, all event values in the outcome column must be handled by the dictionary.
        If not provided, will attempt to convert based on the values in the outcome column. By default alive and dead will be converted to 0 and 1, respectively, if present in the outcome column.
        The default is an empty dictionary.
    
    Returns
    -------
    dataframe_with_standardized_outcome : DataFrame
        Dataframe with a copy of the specified outcome column converted to numeric values.
    """
    # Get the type of the existing event column
    event_variable_type = dataframe_with_outcome[outcome_column_label].dtype

    # Make a copy of the dataframe to work on 
    dataframe_with_standardized_outcome = dataframe_with_outcome.copy()

    # Handle numeric event column
    if np.issubdtype(event_variable_type, np.number):
        dataframe_with_standardized_outcome[standard_column_label] = dataframe_with_outcome[outcome_column_label]

    # Handle boolean event column
    elif np.issubdtype(event_variable_type, np.bool_):
        dataframe_with_standardized_outcome[standard_column_label] = dataframe_with_outcome[outcome_column_label].astype(int)

    # Handle string event column
    elif np.issubdtype(event_variable_type, np.object_):
        try:
            # Make values of outcome column lowercase
            dataframe_with_standardized_outcome[outcome_column_label] = dataframe_with_outcome[outcome_column_label].str.lower()
        except Exception as e:
            msg = f"Error converting string event column {outcome_column_label} to lowercase. Please check the column is a string type and try again."
            logger.exception(msg)
            raise e
        
        # Get the existing event values in the provided dataframe and and sort them
        existing_event_values = sorted(dataframe_with_standardized_outcome[outcome_column_label].unique())

        if not event_column_value_mapping:
            # Create a dictionary to map event values to numeric values
            event_column_value_mapping = survivalStatusToNumericMapping(event_outcome_column=dataframe_with_standardized_outcome[outcome_column_label])

        else:
            # Convert all dictionary keys in provided mapping to lowercase
            event_column_value_mapping = {status.lower():value for status, value in event_column_value_mapping.items()}

            # Check if user provided dictionary handles all event values in the outcome column
            if set(existing_event_values) != set(event_column_value_mapping.keys()):
                msg = f"Not all event values in {outcome_column_label} are handled by the provided event_column_value_mapping dictionary."
                logger.exception(msg)
                raise ValueError()
        
                # TODO: add handling for values not in the dictionary
        
        # Set up the new column name for the converted event column
        dataframe_with_standardized_outcome[standard_column_label] = dataframe_with_standardized_outcome[outcome_column_label]

        # Swap the keys and values in the mapping dictionary to use the replaceColumnValues function
        # So the numeric values will be the keys and the string event values will be the values
        replacement_value_data = dict([num_event, str_event] for str_event, num_event in event_column_value_mapping.items())

        # Replace the string event values in the standardized column with the numeric event values
        dataframe_with_standardized_outcome = replaceColumnValues(dataframe_with_standardized_outcome,
                                                                  column_to_change=standard_column_label,
                                                                  replacement_value_data=replacement_value_data)
    
    # end string handling
    else:
        msg = f"Event column {outcome_column_label} is not a valid type. Must be a string, boolean, or numeric."
        logger.exception(msg)
        raise TypeError()


    return dataframe_with_standardized_outcome



def addOutcomeLabels(feature_data_to_label:DataFrame,
                     clinical_data:DataFrame,
                     outcome_labels:Optional[list] = None
                     ) -> DataFrame:
    """Add survival labels to a feature dataframe based on a clinical dataframe.

    Parameters
    ----------
    feature_data_to_label : DataFrame
        Dataframe containing the feature data to add survival labels to.
    clinical_data : DataFrame
        Dataframe containing the clinical data to use for survival labels.
    outcome_labels : list, optional
        List of outcome labels to extract from the clinical dataframe. The default is ["survival_time_in_years", "survival_event_binary"].

    Returns
    -------
    outcome_labelled_feature_data : DataFrame
        Dataframe containing the feature data with survival labels added.
    """
    if outcome_labels is None:
        outcome_labels = ["survival_time_in_years", "survival_event_binary"]

    # Get the survival time and event columns as a dataframe
    outcome_label_columns = clinical_data[outcome_labels]

    # Join the outcome label dataframe to the feature data dataframe
    outcome_labelled_feature_data = outcome_label_columns.join(feature_data_to_label)
    return outcome_labelled_feature_data