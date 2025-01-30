def exampleAlgorithm(dataframe):
    """
        An example algorithm that takes a dataframe and computes .

        Parameters:
            dataframe (pd.DataFrame): A non-empty dataframe containing machine data.

        Returns:
            val (int): The sum of all values.
    """
    return dataframe[dataframe.columns[0]].sum()
