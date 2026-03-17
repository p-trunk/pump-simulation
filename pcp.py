import numpy as np
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class CharacteristicsView(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.fig1 = Figure(figsize=(4, 4))
        self.canvas1 = FigureCanvas(self.fig1)
        self.fig2 = Figure(figsize=(4, 4))
        self.canvas2 = FigureCanvas(self.fig2)

        layout = QHBoxLayout()
        layout.addWidget(self.canvas1)
        layout.addWidget(self.canvas2)
        self.setLayout(layout)

        # Defaultparameter
        self.rotor_diameter = 100
        self.eccentricity = 20
        self.pitch = 500
        self.stages = 1

        self.viscosity = 1
        self.density = 1000

        self.calculate_characteristics()
    
    def set_parameters(self, rotor_diameter, eccentricity, rotor_pitch, stages, viscosity, density):
        # Parameter updaten
        self.rotor_diameter = rotor_diameter
        self.eccentricity = eccentricity
        self.pitch = rotor_pitch
        self.stages = stages
        self.viscosity = viscosity
        self.density = density

        self.calculate_characteristics()
    
    def calculate_characteristics(self):
        # meshgrid
        dp = np.linspace(0, self.stages * 6, 50)                                                # in bar
        n = np.linspace(0, 250, 50)                                                             # in 1/min

        DP, N = np.meshgrid(dp, n)

        # Theoretische Kennlinien berechnen
        self.V_chamber = 8 * self.eccentricity * self.rotor_diameter * self.pitch * 1e-9        # in m^3

        Vp_theoretical = N*60 * self.V_chamber                                                  # in m^3/h
        M_theoretical = self.V_chamber*DP*1e5 / (2 * np.pi)                                     # in Nm

        # Leckage berechnen
        c_ll = 1.4e-5
        c_lt = 1.4e-1

        Vp_ll = c_ll * self.V_chamber/(2*np.pi*self.viscosity*1e-3)*DP*1e5
        Vp_lt = c_lt * self.V_chamber**(2/3)*np.sqrt(2*DP*1e5/self.density)

        Vp_l = (Vp_ll + Vp_lt) / self.stages

        Vp_actual = Vp_theoretical - Vp_l
        Vp_actual[Vp_actual < 0] = 0

        # Verlustmoment berechnen
        c_vp = 1.4e-1
        c_vd = 1.2e2
        c_vv = 7.4e2
        M_vc = 5

        M_vp = c_vp * DP*1e5*self.V_chamber/(2*np.pi)
        M_vd = c_vd * self.density*(N/60)**2/(4*np.pi)*self.V_chamber**(5/3)
        M_vv = c_vv * self.viscosity*1e-3*self.V_chamber*N/60

        M_v = M_vp + (M_vd + M_vv + M_vc) * self.stages

        M_actual = M_theoretical + M_v

        self.plot_characteristics(DP, N, Vp_theoretical, Vp_actual, M_theoretical, M_actual)

    def plot_characteristics(self, DP, N, Vp_theoretical, Vp_actual, M_theoretical, M_actual):

        self.fig1.clear()
        ax = self.fig1.add_subplot(111, projection='3d')

        ax.set_title('Volumenstrom')
        
        ax.set_xlabel(r'$\Delta$p in bar')
        ax.set_ylabel(r'n in min$^{-1}$')
        ax.set_zlabel(r'$\mathrm{\dot{V}}$ in m$^3$ h$^{-1}$')

        ax.plot_surface(DP, N, Vp_theoretical, color='tab:blue', alpha=.25)
        ax.plot_surface(DP, N, Vp_actual, color='tab:orange', alpha=.75)
        
        ax.legend(['theoretisch', 'effektiv'], loc='center', bbox_to_anchor=(.9, .9))
        ax.view_init(elev=20, azim=-135)

        self.fig2.clear()
        ax = self.fig2.add_subplot(111, projection='3d')

        ax.set_title('Drehmoment')
        
        ax.set_xlabel(r'$\Delta$p in bar')
        ax.set_ylabel(r'n in min$^{-1}$')
        ax.set_zlabel(r'M in N m')

        ax.plot_surface(DP, N, M_theoretical, color='tab:blue', alpha=.25)
        ax.plot_surface(DP, N, M_actual, color='tab:orange', alpha=.75)
        
        ax.legend(['theoretisch', 'effektiv'], loc='center', bbox_to_anchor=(.1, .9))
        ax.view_init(elev=20, azim=-135)

        self.canvas1.draw()
        self.canvas2.draw()
