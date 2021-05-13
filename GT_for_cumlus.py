import numpy as np
from scipy.integrate import quad

# Constants
planck_constant = 6.62607004e-34   # m^2 kg/s
speed_of_light = 299792458  # m/s
boltzmann_constant = 1.38064852e-23  # m^2 kg s-2 K-1


# Functions
# From Gabor Thesis and Accuracy Performance of Star Trackers (Liebe 2002)

def radiative_spectral_emittance(wavelength_, temperature_):
    """
    The radiation from a black body at a given
    wavelength and temperature (Liebe 2002 eqn2 - Gabor eqn2.5)
    :param wavelength_: in m
    :param temperature_: in kelvin
    :return:
    """

    I_star = (2 * np.pi * planck_constant * speed_of_light ** 2) / \
             (wavelength_ ** 5 * (np.exp(planck_constant * speed_of_light / (wavelength_ * boltzmann_constant * temperature_)) - 1))
    return I_star


def radiant_flux_perratioflux_integral(lambda_interval_bottom_, lambda_interval_top_, temperature_):
    """
    The integral part of the equation 2.7 from Gabor thesis -  without "flux_ratio"
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
    Full equation 2.7 from Gabor thesis
    :param flux_sun_:
    :param lambda_interval_bottom_:
    :param lambda_interval_top_:
    :param temperature_:
    :return:
    """
    flux_star_fluxratio = radiant_flux_perratioflux_integral(lambda_interval_bottom_, lambda_interval_top_, temperature_)
    radiant_flux = np.sqrt(flux_sun_ * flux_star_fluxratio[0])
    radiant_flux_error = ((1/2)*np.sqrt(flux_sun_ * flux_star_fluxratio[0])/(flux_star_fluxratio[0]))*flux_star_fluxratio[1]
    return radiant_flux, radiant_flux_error


def planck_einstein_relation(wavelength_):
    """
    This function calculates the energy of a photon in a specific wavelength
    (Liebe 2002 eqn3 - Gabor eqn2.8)
    :param wavelength_ in meter
    :return: energy_photon in joule
    """
    energy_photon = (planck_constant * speed_of_light) / wavelength_
    return energy_photon


def photon_spectral_emittance(radiant_flux_, wavelength_):
    """
    Function for the luminosity of a star. [photons/(s*mm^2)]
    Gabor eqn 2.9
    :param radiant_flux_:
    :param wavelength_:
    :return:
    """

    L_star = radiant_flux_/planck_einstein_relation(wavelength_)
    return L_star


def sensor_photon_irradiance(wavelength_, radiant_flux_, quantum_efficiency_):
    """
    # TODO adapt here and below
    Gabor eqn 2.10 -- need to adapt, since it considers it a fix QE
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
    Gabor Eqn 2.11
    # TODO adapt here and above
    :param lambda_interval_bottom_:
    :param lambda_interval_top_:
    :param radiant_flux_:
    :param quantum_efficiency_:
    :return:
    """
    E_range = quad(sensor_photon_irradiance, lambda_interval_bottom_, lambda_interval_top_,
                            args=(radiant_flux_, quantum_efficiency_))
    return E_range


def photoelectrons_per_exposure_cauculator(E_range_pe_smm2_, magnitude_star_, exposuretime_sec_, diameter_telescope_mm2_):
    """
    Liebe 2002 eqn4
    :param E_range_pe_smm2_:
    :param magnitude_star_:
    :param exposuretime_sec_:
    :param diameter_telescope_mm2_:
    :return:
    """
    photoelectrons_per_exposure = E_range_pe_smm2_ * (1.0/(2.5**(magnitude_star_ - 0)) * exposuretime_sec_ * np.pi * (diameter_telescope_mm2_/2)**2)
    return photoelectrons_per_exposure


# From Sensitivity of an Active Space Telescope to Faint Sources
# and Extrasolar Planets (Angel and Woolf 1998)
def signal_to_noise_ratio(photoelectrons_per_second_signal, dark_current_noise, read_out_noise, diffuse_background):
    """
    This function calculated the signal to noise, using as input the count of photoelectrons per second for all of these
    signal, dark_current_noise, read_out_noise, and diffuse_background. From Angel and Woolf 1998
    :param photoelectrons_per_second_signal:
    :param dark_current_noise:
    :param read_out_noise:
    :param diffuse_background:
    :return: signal to noise ratio
    """
    # This is the formula found in the paper
    snr = photoelectrons_per_second_signal / np.sqrt(photoelectrons_per_second_signal + dark_current_noise +
                                                     read_out_noise + diffuse_background)

    return snr


if __name__ == '__main__':

    # Assumptions

    # Wavelength for passband:
    # Assumption: H-band
    # nm #check
    lambda_interval_bottom = 1300
    lambda_interval_top = 1900

    # temperature star
    # Assumption: a M5 star (http://astro.vaporia.com/start/mclass.html)
    temperature = 2800  # K

    # sun's flux
    flux_sun = 1361  # W/m^2

    # aperture telescope
    # Assumption: cumlus 18.5cm aperture
    diameter = 185 ##mm
    aperture_area = np.pi * (diameter/2)**2

    # magnitude star
    # Assumption: generic magnitude
    magnitude_star = 18.0

    # exposure time
    # # Assumption: I should compare with cumlus proposal values, which is 60s, but for now I will take 1.0s . just to have the values as photoelectrons/second
    exposure = 1.0

    radiant_flux, radiant_flux_error = radiant_flux_calculator(flux_sun_=flux_sun,
                                                                lambda_interval_bottom_=lambda_interval_bottom,
                                                                lambda_interval_top_= lambda_interval_top,
                                                                temperature_=temperature)

    print('F_star [W/m^2]: ', radiant_flux)
    E_range = total_number_of_incident_photon_per_second_per_area(lambda_interval_bottom_=lambda_interval_bottom*1e-9,
                                                                  lambda_interval_top_=lambda_interval_top*1e-9,
                                                                  radiant_flux_=radiant_flux,
                                                                  quantum_efficiency_=0.45)

    print('E_range [photoelectrons / s m^2]: ', E_range[0])


    photoelectrons = photoelectrons_per_exposure_cauculator(E_range[0], magnitude_star, exposure, diameter)
    print(f'We see {photoelectrons} [photoelectrons/second] in the H filter, from a Star mag {magnitude_star} and temperature: {temperature} \n using a {diameter/2} mm radius telescope')


    # Dark current
    # Assumptions: from cumlus proposal
    dark_current = 0.05 # (electrons/second)

    # Read out noise
    # Assumptions: from cumlus proposal
    read_noise_every_60_seconds = 18 # (electrons/60seconds)
    read_out = 0.3 # (electrons/second)

    # Diffuse Background
    # Assumptions: from cumlus proposal
    # PSF for 18cm optics, 1.4" in Hband
    total_sky_flux = 715 # (photons/60seconds)
    total_sky_flux_etenue_qe = 547 # (photons/60seconds)
    background = 9.11 # photons/second

    snr = signal_to_noise_ratio(photoelectrons_per_second_signal=photoelectrons, dark_current_noise=dark_current, read_out_noise=read_out, diffuse_background=background)
    print(f'S/N is {snr}. ')

    print(f'Assumptions:\nHband {lambda_interval_bottom}-{lambda_interval_top} nm')
    print(f'Temperature: {temperature} K')
    print(f'Suns flux: {flux_sun} W/m^2')
    print(f'Aperture diameter: {diameter} mm')
    print(f'Magnitude star: {magnitude_star}')
    print('----------------------------------')
    print(f'We see {photoelectrons} [photoelectrons/second] in the H filter, from a Star mag {magnitude_star} and temperature: {temperature}',
          f'\nusing a {diameter/2} mm radius telescope')

    print(f'\nDark current: {dark_current} electrons/second')
    print(f'Read out noise: {read_out} electrons/second')
    print(f'Diffuse Background: {background} photons/second')
    print('----------------------------------')
    print(f'We have a S/N equals to {snr}. ')


# ## TODO:
# - QE that varies with the wavelength (instead of a fix value) so we can use the camera values
# - QE for  H4RG:
# Mosby Jr, Gregory, et al. "Properties and characteristics of the WFIRST H4RG-10 detectors."
# - QE for Commercial camera:
# Goldeye G-130 TEC1
