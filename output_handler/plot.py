from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd


def draw_iteration(progress: pd.DataFrame, file_name: Optional[str] = None):
    progress.plot(x='Time', y=['Incumbent', 'BestBd'], kind='line')
    if file_name:
        plt.savefig(file_name)
    else:
        plt.show()
    return
