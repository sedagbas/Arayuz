import sys
from PyQt5 import QtWidgets
from arayuz import MainWindow
from veri import Veri


class Driver:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = MainWindow()

        self.veri_thread = None

        # Butonlar
        self.window.btn_start.clicked.connect(self.start_thread)
        self.window.btn_stop.clicked.connect(self.stop_thread)

        # Dosya seçim butonları
        self.window.file_select_nav.clicked.connect(self.select_nav_file)
        self.window.file_select_raw.clicked.connect(self.select_raw_file)

    def select_nav_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.window, "NAV Dosyası Seç", "", "Bin Files (*.bin)"
        )
        if path:
            self.window.file_path_nav.setText(path)

    def select_raw_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.window, "RAW Dosyası Seç", "", "Bin Files (*.bin)"
        )
        if path:
            self.window.file_path_raw.setText(path)

    def start_thread(self):
        nav_file = self.window.file_path_nav.text()
        raw_file = self.window.file_path_raw.text()
        if not nav_file or not raw_file:
            print("Dosya seçilmedi")
            return
        self.veri_thread = Veri(nav_file, raw_file)
        self.veri_thread.data_ready.connect(self.update_ui)
        self.veri_thread.start()

    def stop_thread(self):
        if self.veri_thread:
            self.veri_thread.stop()
            self.veri_thread = None

    def update_ui(self, side, data, led_bits):
        self.window.update_graphs(side, data)
        self.window.update_leds(side, led_bits)

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    d = Driver()
    d.run()
