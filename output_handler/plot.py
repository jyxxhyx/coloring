from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd


def draw_iteration(progress: pd.DataFrame, file_name: Optional[str] = None):
    ax = progress.plot(x='Time',
                       y=['Incumbent', 'BestBd'],
                       kind='line',
                       colormap='winter',
                       style='o--',
                       grid=True)
    ax.set_xlabel('Time')
    ax.set_ylabel('Objective')
    if file_name:
        plt.savefig(file_name)
    else:
        plt.show()
    return
