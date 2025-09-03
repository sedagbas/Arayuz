import sys
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Form")
        self.setGeometry(200, 200, 1400, 800)

        main_layout = QtWidgets.QVBoxLayout(self)

        # === Üst Kısım ===
        top_layout = QtWidgets.QHBoxLayout()

        # NAV dosya seçim
        self.combo_nav = QtWidgets.QComboBox()
        self.combo_nav.addItems(["COM7", "COM8"])
        self.baudrate_header_nav = QtWidgets.QLineEdit()
        self.file_path_nav = QtWidgets.QLineEdit()
        self.file_select_nav = QtWidgets.QPushButton("Seç")
        top_layout.addWidget(self.combo_nav)
        top_layout.addWidget(self.baudrate_header_nav)
        top_layout.addWidget(self.file_path_nav)
        top_layout.addWidget(self.file_select_nav)

        # RAW dosya seçim
        self.combo_raw = QtWidgets.QComboBox()
        self.combo_raw.addItems(["COM7", "COM8"])
        self.baudrate_header_raw = QtWidgets.QLineEdit()
        self.file_path_raw = QtWidgets.QLineEdit()
        self.file_select_raw = QtWidgets.QPushButton("Seç")
        top_layout.addWidget(self.combo_raw)
        top_layout.addWidget(self.baudrate_header_raw)
        top_layout.addWidget(self.file_path_raw)
        top_layout.addWidget(self.file_select_raw)

        # Butonlar
        self.btn_start = QtWidgets.QPushButton("START")
        self.btn_stop = QtWidgets.QPushButton("STOP")
        top_layout.addWidget(self.btn_start)
        top_layout.addWidget(self.btn_stop)

        main_layout.addLayout(top_layout)

        # === Orta Kısım (Sol=Nav, Sağ=Raw) ===
        middle_layout = QtWidgets.QHBoxLayout()

        # ---------------- Sol taraf (NAV) ----------------
        left_layout = QtWidgets.QHBoxLayout()

        # LED sütunu
        led_column = QtWidgets.QVBoxLayout()
        self.leds_left = []
        for i in range(10):
            h = QtWidgets.QHBoxLayout()
            led = QtWidgets.QLabel()
            led.setFixedSize(30, 30)
            led.setStyleSheet("border-radius: 15px; background-color: red;")
            label = QtWidgets.QLabel(f"KOSUL_{i + 1}")
            h.addWidget(led)
            h.addWidget(label)
            h.addStretch()
            led_column.addLayout(h)
            self.leds_left.append(led)

        # Grafik sütunu
        graph_column = QtWidgets.QVBoxLayout()
        self.graphs_left = []
        for title in ["Linear Acc", "Angular Vel", "Temperature"]:
            fig = Figure(figsize=(5, 3))
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.set_title(title)
            canvas.ax = ax
            graph_column.addWidget(canvas, stretch=1)
            self.graphs_left.append(canvas)

        left_layout.addLayout(led_column, stretch=1)
        left_layout.addLayout(graph_column, stretch=3)

        # ---------------- Sağ taraf (RAW) ----------------
        right_layout = QtWidgets.QHBoxLayout()

        led_column_r = QtWidgets.QVBoxLayout()
        self.leds_right = []
        for i in range(10):
            h = QtWidgets.QHBoxLayout()
            led = QtWidgets.QLabel()
            led.setFixedSize(30, 30)
            led.setStyleSheet("border-radius: 15px; background-color: red;")
            label = QtWidgets.QLabel(f"KOSUL_{i + 1}")
            h.addWidget(led)
            h.addWidget(label)
            h.addStretch()
            led_column_r.addLayout(h)
            self.leds_right.append(led)

        graph_column_r = QtWidgets.QVBoxLayout()
        self.graphs_right = []
        for title in ["Linear Acc", "Angular Vel", "Temperature"]:
            fig = Figure(figsize=(5, 3))
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.set_title(title)
            canvas.ax = ax
            graph_column_r.addWidget(canvas, stretch=1)
            self.graphs_right.append(canvas)

        right_layout.addLayout(led_column_r, stretch=1)
        right_layout.addLayout(graph_column_r, stretch=3)

        middle_layout.addLayout(left_layout)
        middle_layout.addLayout(right_layout)
        main_layout.addLayout(middle_layout)

    # === Yardımcı Fonksiyonlar ===
    def set_led_color(self, led, state: bool):
        color = "green" if state else "red"
        led.setStyleSheet(f"border-radius: {led.width()//2}px; background-color: {color};")

    def update_graphs(self, side, data):
        graphs = self.graphs_left if side == "nav" else self.graphs_right
        for i, key in enumerate(["linear_acc", "angular_vel", "temperature"]):
            ax = graphs[i].ax
            ax.clear()
            ax.set_title(key)
            for axis_data in data[key]:
                ax.plot(axis_data)
            graphs[i].draw()

    def update_leds(self, side, bit_values):
        leds = self.leds_left if side == "nav" else self.leds_right
        for i, led in enumerate(leds):
            state = bool(bit_values[i])
            self.set_led_color(led, state)

