from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.frame = QWidget()
        self.setCentralWidget(self.frame)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()