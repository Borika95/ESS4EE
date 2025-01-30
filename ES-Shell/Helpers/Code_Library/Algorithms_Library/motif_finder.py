import numpy as np
import pandas as pd
import stumpy

class MotifFinder:
    """
    A tool to identify motifs (repeated patterns) in time-series data.

    Attributes:
        df (pd.DataFrame): The input data containing time-series values.
        patterns (dict): A dictionary to store patterns for each column.
        color_map (dict): Maps job descriptions to color indices for plotting.
    """
    def __init__(self, df):
        self.df = df
        self.patterns = {}
        self.color_map = {}

    def add_pattern(self, column, start, end, threshold, job):
        """
        Adds a pattern for motif search in a specified column.

        Args:
            column (str): Column name in the DataFrame.
            start (int): Start index of the pattern.
            end (int): End index of the pattern.
            threshold (float): Threshold for mean and standard deviation comparison.
            job (str): Description of the job associated with the pattern.
        """
        if column not in self.patterns:
            self.patterns[column] = []
        if job not in self.color_map:
            self.color_map[job] = len(self.color_map)
        self.patterns[column].append((start, end, threshold, job))

    def find_motifs(self):
        """
        Identifies motifs in the data based on defined patterns.

        Returns:
            dict: A dictionary with column names as keys and motif details as values.
        """
        motif_results = {}
        for column, patterns in self.patterns.items():
            df_column = self.df[column].dropna().astype(float)
            motif_results[column] = []

            for start, end, threshold, job in patterns:
                pattern = df_column[start:end]
                pattern_time = end - start
                pattern_mean = pattern.mean()
                pattern_std = pattern.std()

                profile = stumpy.match(pattern.values, df_column.values)
                indices = profile[:, 1]

                for i in indices:
                    motif_end = i + pattern_time
                    if motif_end > len(df_column):
                        continue
                    motif = df_column[i:motif_end]
                    motif_mean = motif.mean()
                    motif_std = motif.std()
                    mean_diff = abs(motif_mean - pattern_mean) / pattern_mean
                    std_diff = abs(motif_std - pattern_std) / pattern_std

                    if mean_diff <= threshold and std_diff <= threshold:
                        motif_results[column].append((i, pattern_time, self.color_map[job], job))
        return self.resolve_overlaps(motif_results)

    def resolve_overlaps(self, motif_results):
        """
        Resolves overlapping motifs to retain only the most significant ones.

        Args:
            motif_results (dict): Dictionary of identified motifs.

        Returns:
            dict: Non-overlapping motif results.
        """
        final_results = {}
        for column, results in motif_results.items():
            sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
            used_indices = set()
            final_results[column] = []
            for start, length, color, job in sorted_results:
                if any(i in used_indices for i in range(start, start + length)):
                    continue
                final_results[column].append((start, length, color, job))
                used_indices.update(range(start, start + length))
        return final_results

    def create_jobs_dataframe(self):
        """
        Creates a DataFrame for each column showing identified motifs and associated jobs.

        Returns:
            dict: A dictionary of DataFrames for each column.
        """
        job_dfs = {}
        motif_results = self.find_motifs()
        for column, motifs in motif_results.items():
            col_data = self.df[column].copy()
            jobs = pd.Series([None] * len(col_data), index=col_data.index)

            for start, length, _, job in motifs:
                jobs.iloc[start:start + length] = job

            job_dfs[column] = pd.DataFrame({column: col_data, 'Job': jobs})
        return job_dfs


