# this didn't work
# import cumlus.FigureData.FigureData as FigureData
# FigureData.go(figure_file='commercial_camera_QE.png', output_file='myfigure.data')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def cleaning_data(dataframe, qe_initial, qe_final, wavelength_initial, wavelength_final):
    """
    Clean "wrong" data, that might come from reading the borders of the graph
    :param dataframe: data points
    :param qe_initial: cut out any points with qe smaller than
    :param qe_final: cut out any points with qe larger than
    :param wavelength_initial: cut out any points with wavelength smaller than
    :param wavelength_final: cut out any points with wavelength larger than
    :return:
    """
    clean_qe_df = dataframe[dataframe['quantum_efficiency'] >= qe_initial]
    clean_qe_df = clean_qe_df[clean_qe_df['quantum_efficiency'] <= qe_final]
    clean_wave_df = clean_qe_df[
        (clean_qe_df['wavelength'] >= wavelength_initial) | (clean_qe_df['wavelength'].isnull())]
    clean_wave_df = clean_wave_df[clean_wave_df['wavelength'] <= wavelength_final]
    return clean_wave_df


def super_smooth(clean_dataframe, fill_initial, fill_final, wavelength_initial, wavelength_final):
    """
    Smooths the data so we have a nice function, without the weirdness that can appear while using a code to read the
    data points from the figure
    :param clean_dataframe: the dataframe
    :param fill_initial: fill the values for qe on the left equals this
    :param fill_final: fill the values for qe on the right equals this
    :param wavelength_initial: starts generating data points from wavelength staring here
    :param wavelength_final: finishes generating data points till wavelength here
    :return:
    """
    qe_in_func_wavelength1 = interp1d(clean_dataframe['wavelength'], clean_dataframe['quantum_efficiency'],
                                      bounds_error=False, fill_value=(fill_initial, fill_final))
    wavelength_smooth1 = np.linspace(wavelength_initial, wavelength_final, 100)
    qe_smooth1 = qe_in_func_wavelength1(wavelength_smooth1)

    qe_in_func_wavelength2 = interp1d(wavelength_smooth1, qe_smooth1,
                                      bounds_error=False, fill_value=(fill_initial, fill_final))
    wavelength_smooth2 = np.linspace(wavelength_initial, wavelength_final, 1000)
    qe_smooth2 = qe_in_func_wavelength2(wavelength_smooth2)
    return wavelength_smooth2, qe_smooth2


def get_quantum_efficiency_commercial_camera():
    """
    Return the wavelength, and the quantum effiency for the commercial camera
    Goldeye G-130 TEC1
    (file Goldeye_G-130_TEC1_PRELIM_DataSheet_V1.0.0_en-2 2.pdf)
    :return:
    smooth_wavelength - the array with the wavelength range defined in the function
    smooth_qe - the array QE in function of wavelength that we interpolated
    """
    quantum_efficiency_df = pd.read_csv('commercial_camera_QE.csv')

    # wavelength, quantum_efficiency
    clean_wave_df = cleaning_data(dataframe=quantum_efficiency_df,
                                  qe_initial=1, qe_final=79,
                                  wavelength_initial=401, wavelength_final=1790)
    smooth_wavelength, smooth_qe = super_smooth(clean_dataframe=clean_wave_df,
                                                fill_initial=60, fill_final=0,
                                                wavelength_initial=400, wavelength_final=1800)
    return smooth_wavelength, smooth_qe


def get_quantum_efficiency_h2rg():
    """
    Return the wavelength, and the quantum effiency for the H2RG camera
    (HxRG_family2011ASPC__437__383B.pdf)
    :return:
    wavelength_number - the array with the wavelength range defined in the function
    qe_number - the array QE in function of wavelength that we interpolated
    """
    quantum_efficiency_df_184 = pd.read_csv('H2RG_QE_red.csv')
    quantum_efficiency_df_211 = pd.read_csv('H2RG_QE_blue.csv')
    quantum_efficiency_df_212 = pd.read_csv('H2RG_QE_black.csv')
    # wavelength, quantum_efficiency
    clean_wave_df_184 = cleaning_data(dataframe=quantum_efficiency_df_184,
                                      qe_initial=0.0, qe_final=1.1,
                                      wavelength_initial=0.84, wavelength_final=2.61)
    clean_wave_df_211 = cleaning_data(dataframe=quantum_efficiency_df_211,
                                      qe_initial=0.0, qe_final=1.1,
                                      wavelength_initial=0.84, wavelength_final=2.67)
    clean_wave_df_212 = cleaning_data(dataframe=quantum_efficiency_df_212,
                                      qe_initial=0.0, qe_final=1.1,
                                      wavelength_initial=0.84, wavelength_final=2.72)
    wavelength_184, qe_184 = super_smooth(clean_dataframe=clean_wave_df_184,
                                          fill_initial=0.908, fill_final=0,
                                          wavelength_initial=0.846, wavelength_final=2.7)
    wavelength_211, qe_211 = super_smooth(clean_dataframe=clean_wave_df_211,
                                          fill_initial=0.901, fill_final=0,
                                          wavelength_initial=0.864, wavelength_final=2.7)
    wavelength_212, qe_212 = super_smooth(clean_dataframe=clean_wave_df_212,
                                          fill_initial=0.920, fill_final=0,
                                          wavelength_initial=0.880, wavelength_final=2.7)
    return wavelength_184, qe_184, wavelength_211, qe_211, wavelength_212, qe_212


def plots(wavelength_commercial_, qe_commercial_,
          wavelength_184_, qe_184_,
          wavelength_211_, qe_211_,
          wavelength_212_, qe_212_):
    plt.plot(wavelength_commercial_, qe_commercial_)
    plt.title('Commercial Camera Goldeye G-130 TEC1')
    plt.xlabel('wavelength (nm)')
    plt.ylabel('quantum efficiency (%)')
    plt.show()
    plt.close()
    plt.plot(wavelength_184_, qe_184_, color='red', label='Science 1 H2RG #184')
    plt.plot(wavelength_211_, qe_211_, color='navy', label='Science 2 H2RG #211')
    plt.plot(wavelength_212_, qe_212_, color='black', label='Science 3 H2RG #212')
    plt.title('HgCdTe H2RG')
    plt.xlabel('wavelength (micron)')
    plt.ylabel('quantum efficiency')
    plt.show()
    plt.close()


if __name__ == '__main__':
    wavelength_commercial, qe_commercial = get_quantum_efficiency_commercial_camera()
    wavelength_184, qe_184, wavelength_211, qe_211, wavelength_212, qe_212 = get_quantum_efficiency_h2rg()
    plots(wavelength_commercial, qe_commercial, wavelength_184, qe_184, wavelength_211, qe_211, wavelength_212, qe_212)
    qe_commercial = qe_commercial/100
    wavelength_184 = wavelength_184*1000
    wavelength_211 = wavelength_211 * 1000
    wavelength_212 = wavelength_212 * 1000

    dictionary = {'wavelength_commercial': wavelength_commercial,
                  'qe_commercial': qe_commercial,
                  'wavelength_184': wavelength_184,
                  'qe_184': qe_184,
                  'wavelength_211': wavelength_211,
                  'qe_211': qe_211,
                  'wavelength_212': wavelength_212,
                  'qe_212': qe_212}
    # xtinct_redden_df = pd.DataFrame(list(dictionary.items()), columns=['Parameters', 'Values'])
    # extinct_redden_df.to_csv('/Users/sishitan/Documents/Analysis_MOA-2020-BLG-135/for_paper/extinction_reddening.csv')
    qe_dataframe = pd.DataFrame(dictionary)
    qe_dataframe.to_csv('/Users/sishitan/Documents/Cumlus/cumlus/reading_plots/qe_values.csv')
    print("")

