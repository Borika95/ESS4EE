# job_plotter.py

import matplotlib.pyplot as plt
import numpy as np


class JobPlotter:
    """
    A utility for visualizing motifs and their associated jobs in time-series data.

    Attributes:
        df (pd.DataFrame): The input data containing time-series values.
        motif_results (dict): Identified motifs and associated jobs.
    """
    def __init__(self, df, motif_results):
        self.df = df
        self.motif_results = motif_results
        self.jobs = {desc: idx for idx, desc in enumerate(
            set(job for results in self.motif_results.values() for _, _, _, job in results))}
        self.colors = ['#555555', '#bbbbbb', '#cccccc', '#dddddd']

    def plot(self):
        """
        Plots the time-series data with highlighted motifs and their jobs.
        """
        fig, axes = plt.subplots(nrows=len(self.motif_results), figsize=(14, 2 * len(self.motif_results)))

        if not isinstance(axes, np.ndarray):
            axes = [axes]

        for ax, (column, motifs) in zip(axes, self.motif_results.items()):
            ax.plot(self.df.index, self.df[column], color='black', label='Data')
            for start, length, color_idx, job in motifs:
                color = self.colors[color_idx % len(self.colors)]
                ax.axvspan(start, start + length, color=color, alpha=0.5, label=job)

            ax.set_title(f'Motifs in {column}')
            ax.legend()
            ax.set_xlabel('Time')
            ax.set_ylabel('Value')

        plt.tight_layout()
        plt.show()
