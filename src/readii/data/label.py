import re
from pandas import DataFrame

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

    print(f"Converting time column {time_column_label} from days to years, using divide_by={divide_by}.")

    years_column_label = time_column_label + "_years"
    # Make a copy of the time column with the values converted from days to years and add suffic _years to the column name
    dataframe_with_outcome[years_column_label] = dataframe_with_outcome[time_column_label] / divide_by

    return dataframe_with_outcome