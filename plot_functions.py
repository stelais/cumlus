"""
This is not working yet
"""
# Astropy / Numpy
import numpy as np
from astropy import constants as const
from astropy import units as u

# Bokeh imports
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, DataTable, TableColumn
from bokeh.models.widgets import Div
from bokeh.plotting import figure, show, save
from bokeh.layouts import column, row

# My routine imports
from cumlus.sensitivity_equations import command_to_return_relative_signal_to_noise_ratio
from cumlus.simple_plot import plotter


def plot_relative_signal_to_noise_ratio_in_function_of(relative_snr, in_function_of, string_in_function_of,
                                                       fixed_param, color):

    output_file(f'/plots/relative_signal_to_noise_ratio_in_function_of_{string_in_function_of}.html')

    p1 = figure(title=f"Relative signal to noise ratio in function of {string_in_function_of}",
                plot_width=600, plot_height=350,
                x_range=(9039, 9042), y_range=(4,35))
    ## PLotting model
    p1 = plotter(in_function_of, relative_snr, [], p1, legend_label=f'{fixed_param}', y_label_name='Magnification',
                 color=color, plot_errorbar=False, t0_error_plot=False, t0=None, t0_error=None, type_plot='line')
    show(p1)


if __name__ == '__main__':
    # ==================================================================================================================
    #                              SETTING SOME PHOTONS AND PHOTOELECTRONS AS UNIT
    # ==================================================================================================================
    # "photons" unit definition
    photons = u.def_unit('photons')
    # "photoelectrons" unit definition
    photoelectrons = u.def_unit('photoelectrons')


    # ==================================================================================================================
    #                                            SET YOUR PARAMETERS HERE
    # ==================================================================================================================
    # Star properties
    wavelength_star_peak = np.float(550e-9) * u.meter
    luminosity_of_the_star = np.float(4e26) * u.watt

    # Telescope properties
    distance_from_observer = np.float(10e0) * u.lightyear

    ### distance_from_observer = np.arange(10e0,26e3, 10e1)* u.lightyear

    telescope_diameter = np.float(15e0) * u.cm
    quantum_efficiency_value = 0.95
    etenue_value = 0.95
    dark_current = 0.001 * photoelectrons/u.second  # (e-/s)
    read_out = 3.0 * photoelectrons/u.second  # This do not seem right.
                                            # Everything for read out seems not to be /time (divided)
    diffuse_background = 1.0 * photoelectrons/u.second

    # Gravitational Lenses parameters:
    magnification = 1.34

    relative_signal_to_noise_ratio = command_to_return_relative_signal_to_noise_ratio(wavelength_star_peak, luminosity_of_the_star,
                                                     distance_from_observer, telescope_diameter,
                                                     quantum_efficiency_value, etenue_value, dark_current,
                                                     read_out, diffuse_background,
                                                     magnification)


    print(relative_signal_to_noise_ratio)
