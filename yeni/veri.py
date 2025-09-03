from PyQt5 import QtCore
import numpy as np

class Veri(QtCore.QThread):
    data_ready = QtCore.pyqtSignal(str, dict, list)  
    # ("nav"/"raw", data_dict, led_bits)

    def __init__(self, nav_file, raw_file, parent=None):
        super().__init__(parent)
        self.nav_file = nav_file
        self.raw_file = raw_file
        self.running = False

    def run(self):
        self.running = True
        try:
            with open(self.nav_file, "rb") as f_nav, open(self.raw_file, "rb") as f_raw:
                while self.running:
                    # NAV 21 byte
                    nav_bytes = f_nav.read(21)
                    if len(nav_bytes) < 21:
                        break
                    # RAW 30 byte
                    raw_bytes = f_raw.read(30)
                    if len(raw_bytes) < 30:
                        break

                    # --- NAV için son 10 bit ---
                    nav_last = int.from_bytes(nav_bytes[-2:], "big")
                    nav_bits = [(nav_last >> i) & 1 for i in range(10)]

                    # --- RAW için son 10 bit ---
                    raw_last = int.from_bytes(raw_bytes[-2:], "big")
                    raw_bits = [(raw_last >> i) & 1 for i in range(10)]

                    # Fake veri (örnek olarak random)
                    nav_data = {
                        "linear_acc": [np.random.randn(100), np.random.randn(100), np.random.randn(100)],
                        "angular_vel": [np.random.randn(100), np.random.randn(100), np.random.randn(100)],
                        "temperature": [np.random.randn(100), np.random.randn(100), np.random.randn(100)],
                    }
                    raw_data = {
                        "linear_acc": [np.random.randn(100), np.random.randn(100), np.random.randn(100)],
                        "angular_vel": [np.random.randn(100), np.random.randn(100), np.random.randn(100)],
                        "temperature": [np.random.randn(100), np.random.randn(100), np.random.randn(100)],
                    }

                    self.data_ready.emit("nav", nav_data, nav_bits)
                    self.data_ready.emit("raw", raw_data, raw_bits)

                    self.msleep(200)
        except Exception as e:
            print("Hata:", e)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
