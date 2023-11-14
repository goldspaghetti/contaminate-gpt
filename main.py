from gui import MainWindow
from PyQt6.QtWidgets import QApplication
from tts import Sound

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    tts = Sound ()
    # tts.try_speak("What do you think about Xjasdlkfjg")
    # time.sleep(10)
    # status = sd.wait()
    # sd.stop()
    resp = tts.gpt("i threw a moldy cheese to you, dealing 20%")
    tts.try_speak(resp)

    app.exec()