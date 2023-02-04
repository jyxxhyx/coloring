from unittest import TestCase

import pandas as pd

from output_handler.plot import draw_iteration


class TestAnalyzer(TestCase):
    def test_draw_iteration(self):
        progress = {'Incumbent': [9, 8, 7, 6], 'BestBd': [0, 1, 3, 5], 'Time': [0, 1, 2, 3]}
        progress = pd.DataFrame(progress)
        draw_iteration(progress, file_name='test.jpg')
        draw_iteration(progress)
        return
