import numpy as np
from astropy import constants as const
from astropy import units as u


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
    snr = photoelectrons_per_second_signal / np.sqrt(photoelectrons_per_second_signal + dark_current_noise +
                                                     read_out_noise + diffuse_background)
    return snr


if __name__ == '__main__':

    # Star properties
    wavelength_star_peak = np.float(550e-9) * u.meter
    luminosity_of_the_star = np.float(4e26) * u.watt

    # Telescope properties
    distance_from_observer = np.float(10e0) * u.lightyear
    telescope_diameter = np.float(15e0) * u.cm
    quantum_efficiency_value = 0.95
    etenue_value = 0.95

    # Gravitational Lenses parameters:
    magnification = 1.34

    # "photons" unit definition
    photons = u.def_unit('photons')
    # "photoelectrons" unit definition
    photoelectrons = u.def_unit('photoelectrons')

    energy_of_a_photon = planck_einstein_relation(wavelength_star_peak)
    number_emitted_photons_per_second = photons_emitted_by_a_star_per_second(luminosity_of_the_star, energy_of_a_photon)

    photons_from_a_certain_distance = photons_arriving_to_a_certain_distance(number_emitted_photons_per_second, distance_from_observer)

    number_photons_getting_in = photons_after_telescope_aperture(photons_from_a_certain_distance, telescope_diameter)

    generated_photoelectrons = photoelectrons_no_amplification(number_photons_getting_in,
                                                               quantum_efficiency_value, etenue_value)

    photoelectrons_when_lensed = photoelectrons_with_amplification(generated_photoelectrons, magnification)
    #

    print(f"\nNumber of emitted photons by a star of \nluminosity {luminosity_of_the_star} and \nwavelength peak "
          f"{wavelength_star_peak} \nper second:")
    print_cyan(number_emitted_photons_per_second.to(photons/u.s))
    print(f"\nNumber of photons arriving to an observer {distance_from_observer} away per area and second: ")
    print_cyan(photons_from_a_certain_distance.to(photons/(u.cm ** 2 *u.s)))

    print(f"\nNumber of photons getting in the telescope of aperture {telescope_diameter} in diameter: ")
    print_cyan(number_photons_getting_in.to(photons/u.s))

    print(f"\nNumber of photonelectrons generated when the quantum efficiency is {quantum_efficiency_value}"
          f"and the etenue is {etenue_value}: ")
    print_cyan(generated_photoelectrons.to(photoelectrons/u.s))

    print(f"\nNumber of photonelectrons generated when there is an amplification of {magnification}")
    print_cyan(photoelectrons_when_lensed.to(photoelectrons/u.s))