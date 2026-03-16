import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class RotorStatorView(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.fig = Figure(figsize=(4, 3))
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.setLayout(layout)

        # Defaultparameter
        self.rotor_diameter = 100
        self.eccentricity = 20
        self.pitch = 500
        self.stages = 1

        self.calculate_geometry()

    def set_parameters(self, rotor_diameter, eccentricity, rotor_pitch, stages):
        # Parameter updaten
        self.rotor_diameter = rotor_diameter
        self.eccentricity = eccentricity
        self.pitch = rotor_pitch
        self.stages = stages

        self.calculate_geometry()

    def stator_polar(self, R, e):
        # Stator-Kontur 2D
        n = 720
        phi = np.linspace(0, 2*np.pi, n, endpoint=False)
        c = np.cos(phi)
        s = np.sin(phi)

        limit = R / e
        mask_line = np.abs(np.tan(phi)) >= limit

        r_line = np.zeros_like(phi)
        r_line[mask_line] = R / np.abs(s[mask_line])

        disc = np.maximum(R**2 - (e**2)*(s**2), 0)
        root = np.sqrt(disc)

        r_right = e*c + root
        r_left  = -e*c + root
        r_circle = np.where(c >= 0, r_right, r_left)

        r = np.where(mask_line, r_line, r_circle)

        Xs = r * c
        Ys = r * s
        
        return Xs, Ys

    def calculate_geometry(self):
        # Geometrien berechnen
        R = self.rotor_diameter / 2
        e = self.eccentricity
        pitch = self.pitch
        L = (self.stages + .2) * pitch

        n_z = 150
        z = np.linspace(0.0, L, n_z)

        # Rotor    
        n_theta = 200
        theta = np.linspace(0.0, 2.0 * np.pi, n_theta)

        Zr, TH = np.meshgrid(z, theta, indexing='ij')

        phi_r = 2 * np.pi * Zr / pitch

        x_c = e * np.cos(phi_r)
        y_c = e * np.sin(phi_r)

        Xr = x_c + R * np.cos(TH)
        Yr = y_c + R * np.sin(TH)
        Zr = Zr

        # Stator
        x_s_2d, y_s_2d = self.stator_polar(R, e)

        x_s = x_s_2d.reshape(1, -1)
        y_s = y_s_2d.reshape(1, -1)

        phi_s = phi_r[:, 0].reshape(-1, 1)

        Xs = x_s * np.cos(phi_s) - y_s * np.sin(phi_s)
        Ys = x_s * np.sin(phi_s) + y_s * np.cos(phi_s)
        Zs = np.repeat(z.reshape(-1, 1), x_s.shape[1], axis=1)

        self.plot_geometry(Xr, Yr, Zr, Xs, Ys, Zs)

    def plot_geometry(self, Xr, Yr, Zr, Xs, Ys, Zs):

        self.fig.clear()
        ax = self.fig.add_subplot(111, projection='3d')
        
        ax.plot_surface(Zr, Xr, Yr, color='tab:orange', alpha = .9)
        ax.plot_surface(Zs, Xs, Ys, color='tab:blue', alpha = .5)

        ax.legend(['Rotor', 'Stator'], loc='center', bbox_to_anchor=(.1, .9))
        ax.set_aspect('equal')
        ax.view_init(elev=20, azim=225)

        self.canvas.draw()
