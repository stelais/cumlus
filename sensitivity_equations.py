import numpy as np
from astropy import constants as const
from astropy import units as u


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
    photons_getting_in * quantum_efficiency * etenue

if __name__ == '__main__':

    wavelength_star_peak = np.float(550e-9) * u.meter
    luminosity_of_the_star = np.float(4e26) * u.watt
    distance_from_observer = np.float(10e0) * u.lightyear
    telescope_diameter = np.float(15e0) * u.cm

    # "photons" unit definition
    photons = u.def_unit('photons')

    energy_of_a_photon = planck_einstein_relation(wavelength_star_peak)
    number_emitted_photons_per_second = photons_emitted_by_a_star_per_second(luminosity_of_the_star, energy_of_a_photon)
    print(number_emitted_photons_per_second.to(photons/u.s))
    photons_from_a_certain_distance = photons_arriving_to_a_certain_distance(number_emitted_photons_per_second, distance_from_observer)
    print(photons_from_a_certain_distance.to(photons/(u.cm ** 2 *u.s)))
    number_photons_getting_in = photons_after_telescope_aperture(photons_from_a_certain_distance, telescope_diameter)
    print(number_photons_getting_in.to(photons/u.s))

