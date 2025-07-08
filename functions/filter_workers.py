# functions/filter_worker.py

from PyQt5.QtCore import QThread, pyqtSignal
import pandas as pd

class FilterWorker(QThread):
    result_ready = pyqtSignal(pd.DataFrame)

    def __init__(self, df, query=""):
        super().__init__()
        self.df = df
        self.query = query.lower().strip()

    def run(self):
        if self.query:
            result_df = self.df[self.df.apply(
                lambda row: row.astype(str).str.lower().str.contains(self.query).any(),
                axis=1
            )]
        else:
            result_df = self.df
        self.result_ready.emit(result_df)
