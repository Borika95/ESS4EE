import pandas as pd



#NOTE: The parameters in the shell are placeholders and may be changed to suite individual needs.
#NOTE: The EnPIs calculated in the shell use offline data and only provide a template for the calculation of EnPIs in the Inference Engine.
def calculate_EnPIs(dataframe, example_algorithm_result):
    """
        Calculate various Energy Performance Indicators (EnPIs) from dataframes.

        Parameters:
            dataframe (pd.DataFrame): A DataFrame containing energy/time data.
            example_algorithm_result (int): The result of an example algorithm that will be used in the calculation of EnPIs.

        Returns:
            tuple: (EnPIs, normalized_EnPIs)
                EnPIs (dict): A dictionary with calculated EnPIs.
                normalized_EnPIs (dict): A dictionary with normalized EnPIs.
    """

    # Initialize EnPI dictionaries
    EnPIs = {}
    EnPIs_mean = {}
    EnPIs_min = {}
    EnPIs_max = {}
    EnPIs_sum = {}

    # Process the dataframe (our dataframe only contains data in the first column)
    column = dataframe.columns[0]

    # Calculate mean, min, and max
    mean = dataframe[column].mean()
    EnPIs_mean[f"Mean {column}"] = mean

    minimum = dataframe[column].min()
    EnPIs_min[f"Min {column}"] = minimum

    maximum = dataframe[column].max()
    EnPIs_max[f"Max {column}"] = maximum

    # Use example algorithm result to calculate sum
    EnPIs_sum[f"Sum {column}"] = example_algorithm_result

    # Combine all EnPIs
    EnPIs.update(EnPIs_mean)
    EnPIs.update(EnPIs_min)
    EnPIs.update(EnPIs_max)
    EnPIs.update(EnPIs_sum)

    # Normalize EnPIs so that they can be used in the Fuzzy Inference System
    normalized_EnPIs = {}

    for key, value in EnPIs.items():
        normalized_EnPIs[key] = value / maximum

    return EnPIs, normalized_EnPIs