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
    :param luminosity:
    :param energy_photon:
    :return: number_photons
    """
    number_photons = luminosity / energy_photon
    return number_photons


if __name__ == '__main__':
    wavelength_star_peak = np.float(550e-9) * u.m
    luminosity_of_the_star = np.float(4e26) * u.watt

    energy_of_a_photon = planck_einstein_relation(wavelength_star_peak)
    number_emitted_photons_per_second = photons_emitted_by_a_star_per_second(luminosity_of_the_star, energy_of_a_photon)
    print(number_emitted_photons_per_second)

