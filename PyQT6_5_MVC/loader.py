import time
from PyQt6.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot


class LoaderSignals(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()


class Loader(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = LoaderSignals()

    @pyqtSlot()
    def run(self):
        total_n = 100
        for n in range(total_n):

            if n in (25, 50, 75):
                time.sleep(1)

            progress_pc = int(100 * float(n + 1) / total_n)  # Progress 0-100% as int
            self.signals.progress.emit(progress_pc)

            time.sleep(0.02)

        self.signals.finished.emit()