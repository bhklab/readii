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