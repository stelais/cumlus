# this didn't work
# import cumlus.FigureData.FigureData as FigureData
# FigureData.go(figure_file='commercial_camera_QE.png', output_file='myfigure.data')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def get_quantum_efficiency_commercial_camera():
    """
    Return the wavelength, and the quantum effiency for the commercial camera
    Goldeye G-130 TEC1
    :return:
    """
    quantum_efficiency_df = pd.read_csv('commercial_camera_QE.csv')

    # wavelength, quantum_efficiency
    clean_qe_df = quantum_efficiency_df[quantum_efficiency_df['quantum_efficiency'] >= 1]
    clean_qe_df = clean_qe_df[clean_qe_df['quantum_efficiency'] <= 79]
    clean_wave_df = clean_qe_df[(clean_qe_df['wavelength'] >= 401) | (clean_qe_df['wavelength'].isnull())]
    clean_wave_df = clean_wave_df[clean_wave_df['wavelength'] <= 1790]

    qe_in_func_wavelength1 = interp1d(clean_wave_df['wavelength'], clean_wave_df['quantum_efficiency'],
                                      bounds_error=False, fill_value=(60, 0))

    wavelength_smooth1 = np.linspace(400, 1800, 100)
    qe_smooth1 = qe_in_func_wavelength1(wavelength_smooth1)

    qe_in_func_wavelength2 = interp1d(wavelength_smooth1, qe_smooth1,
                                      bounds_error=False, fill_value=(60, 0))
    wavelength_smooth2 = np.linspace(400, 1800, 1000)
    qe_smooth2 = qe_in_func_wavelength2(wavelength_smooth2)
    return wavelength_smooth2, qe_smooth2


if __name__ == '__main__':
    wavelength, quantum_efficiency = get_quantum_efficiency_commercial_camera()
    plt.plot(wavelength, quantum_efficiency)
    plt.show()
