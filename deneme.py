import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QFrame, QSplitter
)
from PyQt5.QtCore import Qt
import pyqtgraph as pg


def create_side(title):
    """Bir tarafı (grafik + LED) oluşturan fonksiyon"""

    main_layout = QVBoxLayout()

    # Üst kısım: ComboBox + 2 Label
    top_layout = QHBoxLayout()
    combo = QComboBox()
    combo.addItems(["Seçenek 1", "Seçenek 2", "Seçenek 3"])
    lbl1 = QLabel("Label 1")
    lbl2 = QLabel("Label 2")
    top_layout.addWidget(combo)
    top_layout.addWidget(lbl1)
    top_layout.addWidget(lbl2)

    main_layout.addLayout(top_layout)

    # Grafikler
    for name in ["İvme", "Dönü", "Sıcaklık"]:
        plot = pg.PlotWidget()
        plot.setTitle(name)
        main_layout.addWidget(plot)

    # LED benzeri göstergeler (10 tane)
    led_layout = QHBoxLayout()
    for i in range(10):
        led = QFrame()
        led.setFixedSize(20, 20)
        led.setStyleSheet("background-color: gray; border-radius: 10px; border: 1px solid black;")
        led_layout.addWidget(led)
    main_layout.addLayout(led_layout)

    container = QWidget()
    container.setLayout(main_layout)
    return container


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Ekran 2'ye Bölme")

        splitter = QSplitter(Qt.Horizontal)

        left_side = create_side("Sol")
        right_side = create_side("Sağ")

        splitter.addWidget(left_side)
        splitter.addWidget(right_side)
        splitter.setSizes([500, 500])

        layout = QHBoxLayout()
        layout.addWidget(splitter)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
