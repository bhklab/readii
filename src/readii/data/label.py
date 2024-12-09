import re
from pandas import DataFrame
import numpy as np

def getPatientIdentifierLabel(dataframe_to_search:DataFrame) -> str:
    """Function to find a column in a dataframe that contains some form of patient ID or case ID (case-insensitive). 
       If multiple found, will return the first match.

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
        print(f"Multiple patient identifier labels found. Using {patient_identifier[0]}.")
    
    elif len(patient_identifier) == 0:
        raise ValueError("Dataframe doesn't have a recognizeable patient ID column. Must contain patient or case ID.")

    return patient_identifier[0]



def convertDaysToYears(dataframe_with_outcome:DataFrame,
                       time_column_label:str,
                       divide_by:int = 365):
    """ Function to create a copy of a time outcome column mesaured in days and convert it to years.

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
                            ):
    """ Function to set up a time outcome column in a dataframe. Makes a copy of the specified outcome column with a standardized column name and converts it to years if specified.

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
        raise ValueError(f"{outcome_column_label} is not numeric. Please confirm outcome_column_label is the correct column or convert the column in the dataframe to numeric.")
    else:
        # Make a copy of the dataframe to work on
        dataframe_with_standardized_outcome = dataframe_with_outcome.copy()


        if convert_to_years:
            # Create a copy of the outcome column and convert it to years
            dataframe_with_standardized_outcome = convertDaysToYears(dataframe_with_standardized_outcome, outcome_column_label)

            # Rename the converted column with the standardized name
            dataframe_with_standardized_outcome.rename(columns={f"{outcome_column_label}_years": standard_column_label}, inplace=True)
        else:

            # Make a copy of the outcome column with the standardized name
            dataframe_with_standardized_outcome[standard_column_label] = dataframe_with_standardized_outcome[outcome_column_label]
    
    return dataframe_with_standardized_outcome