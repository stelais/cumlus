import numpy as np
from scipy.integrate import quad

# Constants
planck_constant = 6.62607004e-34  # m^2 kg/s
speed_of_light = 299792458  # m/s
boltzmann_constant = 1.38064852e-23 #m^2 kg s-2 K-1
# planck_constant = 6.626e-34  # m^2 kg/s
# speed_of_light = 299700000  # m/s
# boltzmann_constant = 1.38e-23 #m^2 kg s-2 K-1


def radiative_spectral_emittance(wavelength_, temperature_):
    """
    The radiation from a black body at a given
    wavelength and temperature is given by
    :param wavelength_: in m
    :param temperature_: in kelvin
    :return:
    """

    I_star = (2 * np.pi * planck_constant * speed_of_light ** 2) / \
             (wavelength_ ** 5 * (np.exp(
                 planck_constant * speed_of_light / (wavelength_ * boltzmann_constant * temperature_)) - 1))
    return I_star


def radiant_flux_perratioflux_integral(lambda_interval_bottom_, lambda_interval_top_, temperature_):
    """
    Equation 2.7 from Gabor thesis
    :param lambda_interval_bottom_: integral limit
    :param lambda_interval_top_: integral limit
    :param temperature_:
    :return:
    """
    F_star_fluxratio = quad(radiative_spectral_emittance, lambda_interval_bottom_, lambda_interval_top_,
                            args=temperature_)
    return F_star_fluxratio


def radiant_flux_calculator(flux_sun_, lambda_interval_bottom_, lambda_interval_top_, temperature_):
    """
    Total power in Watts/m^2
    :param flux_sun_:
    :param lambda_interval_bottom_:
    :param lambda_interval_top_:
    :param temperature_:
    :return:
    """
    flux_star_fluxratio = radiant_flux_perratioflux_integral(lambda_interval_bottom_, lambda_interval_top_,
                                                             temperature_)
    radiant_flux = np.sqrt(flux_sun_ * flux_star_fluxratio[0])
    radiant_flux_error = ((1 / 2) * np.sqrt(flux_sun_ * flux_star_fluxratio[0]) / (flux_star_fluxratio[0])) * \
                         flux_star_fluxratio[1]
    return radiant_flux, radiant_flux_error


def planck_einstein_relation(wavelength_):
    """
    This function calculates the energy of a photon in a specific wavelength
    :param wavelength_ in meter
    :return: energy_photon in joule
    """
    energy_photon = (planck_constant * speed_of_light) / wavelength_
    return energy_photon


def photon_spectral_emittance(radiant_flux_, wavelength_):
    """
    Function for the luminosity of a star. [photons/(s*mm^2)]
    :param radiant_flux_:
    :param wavelength_:
    :return:
    """

    L_star = radiant_flux_ / planck_einstein_relation(wavelength_)
    return L_star


def sensor_photon_irradiance(wavelength_, radiant_flux_, quantum_efficiency_):
    """
    the image sensor photon irradiance E_sensor [photons/(s*mm^2)]
    The amount of incident photon flux detected from the image sensor
    :param wavelength_:
    :param radiant_flux_:
    :param quantum_efficiency_:
    :return:
    """
    L_star = photon_spectral_emittance(radiant_flux_, wavelength_)
    E_sensor = L_star * quantum_efficiency_
    return E_sensor


def total_number_of_incident_photon_per_second_per_area(lambda_interval_bottom_, lambda_interval_top_,
                                                        radiant_flux_, quantum_efficiency_):
    """
    The total number of incident photons/[s*mm^2] that the image sensor is able to detect from the emittance of a star
    :param lambda_interval_bottom_:
    :param lambda_interval_top_:
    :param radiant_flux_:
    :param quantum_efficiency_:
    :return:
    """
    E_range = quad(sensor_photon_irradiance, lambda_interval_bottom_, lambda_interval_top_,
                   args=(radiant_flux_, quantum_efficiency_))
    return E_range


def flux_of_photons_intensity(E_range_, aperture_area_):
    """
    Flux of photon intensity in [photons/s] reaching the image sensor
    :param E_range_:
    :param aperture_area_:
    :return:
    """
    phi_sensor = E_range_ * aperture_area_
    return phi_sensor


def flux_intensity_scaled(phi_sensor_, magnitude_):
    phi_st = phi_sensor_ * 10 ** (0.4 * magnitude_)
    return phi_st


if __name__ == '__main__':

    # Wavelength for passband:
    lambda_interval_bottom = 400
    lambda_interval_top = 800

    # temperature star
    temperature = 5778  # K
    magnitude_star = 15

    # sun's flux
    flux_sun = 1361  # W/m^2

    # aperture telescope
    diameter = 0.15
    aperture_area = np.pi * (diameter/2)**2

    radiant_flux, radiant_flux_error = radiant_flux_calculator(flux_sun_=flux_sun,
                                                               lambda_interval_bottom_=lambda_interval_bottom,
                                                               lambda_interval_top_= lambda_interval_top,
                                                               temperature_=temperature)

    print('F_star [W/m^2]: ', radiant_flux)
    E_range = total_number_of_incident_photon_per_second_per_area(lambda_interval_bottom_=400e-9,
                                                                  lambda_interval_top_=800e-9,
                                                                  radiant_flux_=radiant_flux,
                                                                  quantum_efficiency_=0.95)
    print('Recheck E range units')
    print('E_range [photons / s m^2]: ', E_range[0])

    phi_sensor = flux_of_photons_intensity(E_range_=E_range[0], aperture_area_=aperture_area)
    print('phi_sensor [photons / s]: ', phi_sensor)
    print("")

    phi_for_specific_star = flux_intensity_scaled(phi_sensor_=phi_sensor, magnitude_=magnitude_star)
    print('phi_specific_star [photons / s]: ', phi_for_specific_star)
    print("")
    # TODO check units.
