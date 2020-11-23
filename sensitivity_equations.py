"""
This is a script to calculate the sensitivity of a telescope to detect microlensing exoplanet's signal
"""

import numpy as np
from astropy import constants as const
from astropy import units as u
from bokeh.io import output_file
from bokeh.plotting import figure, show

from cumlus.simple_plot import plotter


def print_cyan(to_be_printed):
    print("\033[96m {}\033[00m".format(to_be_printed))


def planck_einstein_relation(wavelength):
    """
    This function calculates the energy of a photon in a specific wavelength
    :param wavelength in meter
    :return: energy_photon in joule
    """
    planck_constant = const.h
    speed_of_light = const.c
    energy_photon = (planck_constant * speed_of_light) / wavelength
    return energy_photon


def photons_emitted_by_a_star_per_second(luminosity, energy_photon):
    """
    This function calculates how many photons are emitted from a star according to its luminosity
    :param luminosity:
    :param energy_photon:
    :return: number_photons
    """
    number_photons = luminosity / energy_photon
    return number_photons * photons


def photons_arriving_to_a_certain_distance(number_photons, distance):
    """
    how many photons will arrive to this region far from the star
    :param number_photons:
    :param distance:
    :return:
    """
    photons_arriving = number_photons / (4 * np.pi * distance ** 2)
    return photons_arriving


def photons_after_telescope_aperture(number_photons_per_area, aperture, type='round'):
    """

    :param number_photons_per_area:
    :param aperture:
    :param type:
    :return:
    """
    if type == 'round':
        number_photons = number_photons_per_area * (4 * np.pi * (aperture/2) ** 2)
    else:
        number_photons = number_photons_per_area * (aperture ** 2)
    return number_photons


def photoelectrons_no_amplification(photons_getting_in, quantum_efficiency, etenue):
    """
    This function consider the quantum efficiency and the etenue to see how many photoelectrons are generated when
    a specific number os photons come in the telescope.
    :param photons_getting_in:
    :param quantum_efficiency:
    :param etenue:
    :return: number_photoelectrons
    """
    number_photoelectrons = (photons_getting_in/photons) * quantum_efficiency * etenue
    return number_photoelectrons * photoelectrons


def photoelectrons_with_amplification(number_photoelectrons, amplification):
    """
    Gravitational microlensing works like a lens. The lens star curves the space-time, bending the light from the
    back source star. Therefore, more photons come in, then, more photoelectrons are generated.
    :param number_photoelectrons:
    :param amplification:
    :return: more_photoelecrons
    """
    more_photoelecrons = number_photoelectrons * amplification
    return more_photoelecrons


def signal_to_noise_ratio(photoelectrons_per_second_signal, dark_current_noise, read_out_noise, diffuse_background):
    """
    This function calculated the signal to noise, using as input the count of photoelectrons per second for all of these
    signal, dark_current_noise, read_out_noise, and diffuse_background.
    :param photoelectrons_per_second_signal:
    :param dark_current_noise:
    :param read_out_noise:
    :param diffuse_background:
    :return: signal to noise ratio
    """
    # This is the formula found in the paper. but it is weird
    # snr = photoelectrons_per_second_signal / np.sqrt(photoelectrons_per_second_signal + dark_current_noise +
    #                                                  read_out_noise + diffuse_background)
    # so I wll try with the square
    snr = photoelectrons_per_second_signal / np.sqrt(photoelectrons_per_second_signal**2 + dark_current_noise**2 +
                                                     read_out_noise**2 + diffuse_background**2)

    return snr


def relative_signal_to_noise_ratio_calculator(snr_base, snr_detection):
    """
    this function calculates the relative signal to noise ratio
    :param snr_base:
    :param snr_detection:
    :return:
    """
    relative_snr = (snr_detection - snr_base)/snr_base
    return relative_snr


def command_to_return_relative_signal_to_noise_ratio(wavelength_star_peak, luminosity_of_the_star,
                                                     distance_from_observer, telescope_diameter,
                                                     quantum_efficiency_value, etenue_value, dark_current,
                                                     read_out, diffuse_background,
                                                     magnification):
    """
    This function commands the other functions to give us the relative signal to noise ratio
    :param wavelength_star_peak:
    :param luminosity_of_the_star:
    :param distance_from_observer:
    :param telescope_diameter:
    :param quantum_efficiency_value:
    :param etenue_value:
    :param dark_current:
    :param read_out:
    :param diffuse_background:
    :param magnification:
    :return: relative signal to noise ratio
    """

    # ==================================================================================================================
    #                                            RUNNING MAIN CODE
    # ==================================================================================================================
    energy_of_a_photon = planck_einstein_relation(wavelength_star_peak)
    number_emitted_photons_per_second = photons_emitted_by_a_star_per_second(luminosity_of_the_star, energy_of_a_photon)

    photons_from_a_certain_distance = photons_arriving_to_a_certain_distance(number_emitted_photons_per_second,
                                                                             distance_from_observer)

    number_photons_getting_in = photons_after_telescope_aperture(photons_from_a_certain_distance, telescope_diameter)

    generated_photoelectrons = photoelectrons_no_amplification(number_photons_getting_in,
                                                               quantum_efficiency_value, etenue_value)

    photoelectrons_when_lensed = photoelectrons_with_amplification(generated_photoelectrons, magnification)

    signal_to_noise_ratio_no_microlensing = signal_to_noise_ratio(generated_photoelectrons,
                                                                  dark_current, read_out, diffuse_background)

    signal_to_noise_ratio_microlensing = signal_to_noise_ratio(photoelectrons_when_lensed,
                                                               dark_current, read_out, diffuse_background)

    relative_signal_to_noise_ratio = relative_signal_to_noise_ratio_calculator(signal_to_noise_ratio_no_microlensing,
                                                                    signal_to_noise_ratio_microlensing)
    # ==================================================================================================================
    #                          PRINTING INTERMEDIARY STEPS JUST TO FOLLOW WHAT IS GOING ON
    # ==================================================================================================================
    print(f"\nNumber of emitted photons by a star of \nluminosity {luminosity_of_the_star} and \nwavelength peak "
          f"{wavelength_star_peak} \nper second:")
    print_cyan(number_emitted_photons_per_second.to(photons / u.s))
    print(f"\nNumber of photons arriving to an observer {distance_from_observer} away per area and second: ")
    print_cyan(photons_from_a_certain_distance.to(photons / (u.cm ** 2 * u.s)))

    print(f"\nNumber of photons getting in the telescope of aperture {telescope_diameter} in diameter: ")
    print_cyan(number_photons_getting_in.to(photons / u.s))

    print(f"\nNumber of photoelectrons generated when the quantum efficiency is {quantum_efficiency_value}"
          f"and the etenue is {etenue_value}: ")
    print_cyan(generated_photoelectrons.to(photoelectrons / u.s))

    print(f"\nNumber of photoelectrons generated when there is an amplification of {magnification}")
    print_cyan(photoelectrons_when_lensed.to(photoelectrons / u.s))

    print(
        f"\nAssuming dar current of {dark_current}, read noise of {read_out} and background count of {diffuse_background}")
    # print(f"Signal to Noise ratio without microlensing")
    # print_cyan((signal_to_noise_ratio_no_microlensing.to((photoelectrons / u.s) ** (1 / 2))).value)
    # print(f"Signal to Noise ratio with microlensing of {magnification} magnification")
    # print_cyan((signal_to_noise_ratio_microlensing.to((photoelectrons / u.s) ** (1 / 2))).value)
    print(f"Signal to Noise ratio without microlensing")
    print_cyan(signal_to_noise_ratio_no_microlensing.value)
    print(f"Signal to Noise ratio with microlensing of {magnification} magnification")
    print_cyan(signal_to_noise_ratio_microlensing.value)
    print("Relative signal to noise (snr_microlensing - snr_base)/snr_base")
    print_cyan(relative_signal_to_noise_ratio)
    return signal_to_noise_ratio_no_microlensing, signal_to_noise_ratio_microlensing, relative_signal_to_noise_ratio


def plot_relative_signal_to_noise_ratio_in_function_of(in_function_of, relative_snr, string_in_function_of,
                                                       fixed_param, color, p1):

    ## PLotting model
    p1 = plotter(in_function_of, relative_snr, [], p1, legend_label=f'{fixed_param}',
                 x_label_name='Diameter aperture', y_label_name='Signal to Noise Ratio',
                 color=color, plot_errorbar=False, t0_error_plot=False, t0=None, t0_error=None, type_plot='line',
                 legend_location="top_left")
    return p1


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
    wavelength_star_peak = np.float(4e-7) * u.meter # for red stars, sun in green: np.float(550e-9) * u.meter
    luminosity_of_the_star = 0.02 *np.float(4e26) * u.watt  #25 luminosity of the sun for a red dwarf m2v

    # Telescope properties
    distance_from_observer = np.float(10e0) * u.lightyear
    telescope_diameter = np.float(15e0) * u.cm
    quantum_efficiency_value = 0.95
    etenue_value = 0.95
    dark_current = 0.001 * photoelectrons/u.second  # (e-/s)
    read_out = 3.0 * photoelectrons/u.second  # This do not seem right.
                                            # Everything for read out seems not to be /time (divided)
    diffuse_background = 1.0 * photoelectrons/u.second

    # Gravitational Lenses parameters:
    magnification = 1.34

    # signal_to_noise_ratio_no_microlensing, signal_to_noise_ratio_microlensing, relative_signal_to_noise_ratio = \
    #     command_to_return_relative_signal_to_noise_ratio(
    #                                                      wavelength_star_peak, luminosity_of_the_star,
    #                                                      distance_from_observer, telescope_diameter,
    #                                                      quantum_efficiency_value, etenue_value, dark_current,
    #                                                      read_out, diffuse_background,
    #                                                      magnification)

    telescope_diameter = np.arange(8e0, 30e0) * u.cm

    distance_from_observer_s = [np.float(1.5e3) * u.parsec, np.float(3e3) * u.parsec,  np.float(4e3) * u.parsec,
                                np.float(5e3) * u.parsec, np.float(6e3) * u.parsec, np.float(7e3) * u.parsec]
    colors = ['black', 'maroon', 'blueviolet', 'skyblue', 'green', 'orange']

    output_file(f'plots/relative_signal_to_noise_ratio_in_function_of_telescope_diameter.html')

    p1 = figure(title=f"Relative signal to noise ratio in function of telescope diameter",
                plot_width=900, plot_height=500)

    for distance_from_observer, color in zip(distance_from_observer_s, colors):
        signal_to_noise_ratio_no_microlensing, signal_to_noise_ratio_microlensing, relative_signal_to_noise_ratio = command_to_return_relative_signal_to_noise_ratio(wavelength_star_peak, luminosity_of_the_star,
                                                         distance_from_observer, telescope_diameter,
                                                         quantum_efficiency_value, etenue_value, dark_current,
                                                         read_out, diffuse_background,
                                                         magnification)

        p1 = plot_relative_signal_to_noise_ratio_in_function_of(telescope_diameter.value, signal_to_noise_ratio_no_microlensing,
                                                           'Telescope Diameter', f'Observer {distance_from_observer} away',
                                                           color, p1)
    show(p1)

