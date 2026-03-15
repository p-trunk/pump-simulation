import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QFormLayout, QLineEdit, QPushButton, QTabWidget,
                             QGroupBox, QComboBox, QHBoxLayout, QSizePolicy)
from PyQt6.QtCore import Qt

from rotor_stator_view import RotorStatorView

class MainWindow(QMainWindow):

    def __init__(self):
    
        super().__init__()

        self.setWindowTitle('PCP Simulation')
        self.setMinimumSize(700, 400)

        # Tabs für Eingaben und Plots
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Eingabe-Tab
        self.input_tab = QWidget()
        self.input_tab.setStyleSheet('QLabel { min-width: 180px; max-width: 180px }'
                                     'QLineEdit { min-width: 100px; max-width: 100px }'
                                     'QComboBox { min-width: 100px; max-width: 100px }')
        self.tabs.addTab(self.input_tab, 'Eingaben')

        # Kennlinien-Tab
        self.plot_tab = QWidget()
        self.tabs.addTab(self.plot_tab, 'Kennlinien')

        self._build_input_tab()
        self._build_plot_tab()

    def _build_input_tab(self):
        # Eingabe-Tab
        input_layout = QVBoxLayout()
        main_layout = QHBoxLayout()

        # Geometrie-Eingaben
        pump_group = QGroupBox('Pumpenparameter')
        pump_form = QFormLayout()

        self.input_rotor_diameter = QLineEdit()
        self.input_eccentricity = QLineEdit()
        self.input_rotor_pitch = QLineEdit()
        self.input_stages = QComboBox()
        self.input_stages.addItems(['1', '2', '4', '8'])

        self.input_rotor_diameter.setText('100')
        self.input_eccentricity.setText('20')
        self.input_rotor_pitch.setText('500')
        self.input_stages.setCurrentText('1')

        pump_form.addRow('Rotordurchmesser in mm:', self.input_rotor_diameter)
        pump_form.addRow('Exzentrizität in mm:', self.input_eccentricity)
        pump_form.addRow('Rotorsteigung in mm:', self.input_rotor_pitch)
        pump_form.addRow('Anzahl der Stufen:', self.input_stages)

        pump_group.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        pump_group.setLayout(pump_form)
        input_layout.addWidget(pump_group)

        # Button für Rotor-Update
        self.button_rotor_update = QPushButton('Rotor und Stator updaten')
        self.button_rotor_update.clicked.connect(self.update_rotor_view)

        input_layout.addSpacing(8)
        input_layout.addWidget(self.button_rotor_update, alignment=Qt.AlignmentFlag.AlignCenter)

        # Fluid-Eingaben
        fluid_group = QGroupBox('Fluideigenschaften')
        fluid_form = QFormLayout()

        self.input_viscosity = QLineEdit()
        self.input_density = QLineEdit()

        self.input_viscosity.setText('1')
        self.input_density.setText('1000')

        fluid_form.addRow('Viskosität in mPa s:', self.input_viscosity)
        fluid_form.addRow('Dichte in kg/m³:', self.input_density)

        fluid_group.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        input_layout.addSpacing(8)
        fluid_group.setLayout(fluid_form)
        input_layout.addWidget(fluid_group)

        # Button zum Berechnen
        self.button_calculate = QPushButton('Simulation starten')
        self.button_calculate.clicked.connect(self.run_simulation)

        input_layout.addSpacing(8)
        input_layout.addWidget(self.button_calculate, alignment=Qt.AlignmentFlag.AlignCenter)
        input_layout.addStretch(1)

        # Rotor/ Stator-Zeichnung
        self.rotor_view = RotorStatorView()
        self.rotor_view.setMinimumSize(0, 0)
        self.rotor_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.rotor_view)

        self.input_tab.setLayout(main_layout)

    def _build_plot_tab(self):
        # Kennlinien-Tab
        layout = QVBoxLayout()

        layout.addWidget(QPushButton('Hier sind später tolle Kennlinien'))
        self.plot_tab.setLayout(layout)
    
    def update_rotor_view(self):
        # Update Rotor-Stator-Plot
        try:
            d = float(self.input_rotor_diameter.text())
            e = float(self.input_eccentricity.text())
            h = float(self.input_rotor_pitch.text())
            S = int(self.input_stages.currentText())
            self.rotor_view.set_parameters(d, e, h, S)
        except ValueError:
            pass

    def run_simulation(self):
        # Simulation starten
        print('Eingegebene Werte:')
        print('Rotordurchmesser:', self.input_rotor_diameter.text())
        print('Exzentrizität:', self.input_eccentricity.text())
        print('Steigung:', self.input_rotor_pitch.text())
        print('Stufen:', self.input_stages.text())
        print('Viskosität:', self.input_viscosity.text())
        print('Dichte:', self.input_density.text())

        # Wechsel zum Plot-Tab
        self.tabs.setCurrentWidget(self.plot_tab)

# Main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
