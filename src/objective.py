"""
This modules contains code to calculate the objective function (expected
survival) for a given set of input parameters and a given allocation of
emergency vehicles.
"""
import numpy as np


def get_beta(travel_times):
    """
    Obtain beta (as described in the paper) as a function of a given travel time
    matrix.

    Parameters
    ----------
    travel_times : np.array
        The travel time matrix rows correspond to ambulance locations and the
        columns correspond to pickup locations.

    Returns
    -------
    np.array
    """
    ambulance_locations = range(travel_times.shape[0])
    pickup_locations = range(travel_times.shape[1])
    return np.array(
        [
            [
                [
                    0 if a2 == a1 else float(travel_times[a1][p] <= travel_times[a2][p])
                    for a2 in ambulance_locations
                ]
                for a1 in ambulance_locations
            ]
            for p in pickup_locations
        ]
    )


def get_R(primary_vehicle_travel_times, secondary_vehicle_travel_times):
    """
    Obtain R (as described in the paper) as a function of a given travel time
    matrices.

    Parameters
    ----------
    primary_vehicle_travel_times : np.array
        The travel time matrix for primary vehicles. Rows correspond to
        ambulance locations and the columns correspond to pickup locations.
    secondary_vehicle_travel_times : np.array
        The travel time matrix for secondary vehicles. Rows correspond to
        ambulance locations and the columns correspond to pickup locations.

    Returns
    -------
    np.array
    """
    ambulance_locations = range(primary_vehicle_travel_times.shape[0])
    pickup_locations = range(primary_vehicle_travel_times.shape[1])
    return np.array(
        [
            [
                [
                    float(
                        primary_vehicle_travel_times[a1][p]
                        <= secondary_vehicle_travel_times[a2][p]
                    )
                    for a2 in ambulance_locations
                ]
                for a1 in ambulance_locations
            ]
            for p in pickup_locations
        ]
    )


def get_survival_time_vectors(
    survival_functions, primary_vehicle_travel_times, secondary_vehicle_travel_times
):
    """
    Obtain the survival time vectors

    Parameters
    ----------
    survival_functions : iterable
        An iterable of the survival functions for each patient class
    primary_vehicle_travel_times : np.array
        The travel time matrix for primary vehicles. Rows correspond to
        ambulance locations and the columns correspond to pickup locations.
    secondary_vehicle_travel_times : np.array
        The travel time matrix for secondary vehicles. Rows correspond to
        ambulance locations and the columns correspond to pickup locations.

    Returns
    -------
    tuple
      Returns two arrays:
          + `primary_survivals[k][p][a]` indicating the probability of
             survival for patients of type k, at pickup location p, by
             a primary vehicle from location a;
          + `secondary_survivals[k][p][a]` indicating the probability of
             survival for patients of type k, at pickup location p, by
             a secondary vehicle from location a.
    """
    primary_survivals = np.dstack(
        [survival_functions[i](primary_vehicle_travel_times) for i in range(3)]
    ).T
    secondary_survivals = np.dstack(
        [survival_functions[i](secondary_vehicle_travel_times) for i in range(3)]
    ).T
    return primary_survivals, secondary_survivals


def get_is_not_busy_vector(
    vehicle_station_utilisation,
    allocation,
):
    """
    Returns the probability vector of given stations not being busy.

    Parameters
    ----------
    vehicle_station_utilisation : np.array
        The utilisation of vehicles at every station
    allocation : np.array
        The number of vehicles at every station

    Returns
    -------
    np.array
        Returns a vector:
          + `is_not_busy[a]` indicating the probability of a vehicle
             at location a not being busy.
    """
    is_not_busy = 1 - np.power(vehicle_station_utilisation, allocation)
    return is_not_busy


def get_all_same_closer_busy_vector(vehicle_station_utilisation, allocation, beta):
    """
    Returns the probability of all vehicles of the same type that are preferred
    being busy.

    Parameters
    ----------
    vehicle_station_utilisation : np.array
        The utilisation of vehicles at every station
    allocation : np.array
        The number of vehicles at every station
    beta : np.array
        A three dimensional array denoting which vehicles are preferred.

    Returns
    -------
    np.array
        Returns a vector:
          + `all_same_closer_busy[a][p]` indicating the probability
          of all vehicles of the same type and closer to p than
          a being busy.
    """
    all_same_closer_busy = np.prod(
        np.power(
            vehicle_station_utilisation,
            np.multiply(beta.transpose(0, 2, 1), allocation),
        ),
        axis=2,
    ).T
    return all_same_closer_busy


def get_all_primary_closer_busy_vector(vehicle_station_utilisation, allocation, R):
    """
    Returns the probability of all primary vehicles that are preferred
    being busy.

    Parameters
    ----------
    vehicle_station_utilisation : np.array
        The utilisation of vehicles at every station
    allocation : np.array
        The number of vehicles at every station
    R : np.array
        A three dimensional array denoting which primary vehicles are preferred.

    Returns
    -------
    np.array
        Returns a vector:
          + `all_primary_closer_busy_vector[a][p]` indicating
          the probability of all primary vehicles closer to p
          than a secondary vehicle at a being busy.
    """
    all_primary_closer_busy_vector = np.prod(
        np.power(
            vehicle_station_utilisation, np.multiply(R.transpose(0, 2, 1), allocation)
        ),
        axis=2,
    )
    return all_primary_closer_busy_vector


def get_all_secondary_closer_busy_vector(vehicle_station_utilisation, allocation, R):
    """
    Returns the probability of all secondary vehicles that are preferred
    being busy.

    Parameters
    ----------
    vehicle_station_utilisation : np.array
        The utilisation of vehicles at every station
    allocation : np.array
        The number of vehicles at every station
    R : np.array
        A three dimensional array denoting which primary vehicles are preferred.

    Returns
    -------
    np.array
        Returns a vector:
          + `all_secondary_closer_busy_vector[a][p]` indicating
          the probability of all secondary vehicles closer to p
          than a primary vehicle at a being busy.
    """
    all_secondary_closer_busy_vector = np.prod(
        np.power(
            vehicle_station_utilisation,
            np.multiply(1 - R, allocation),
        ),
        axis=2,
    )
    return all_secondary_closer_busy_vector


def get_psi(primary_survivals, primary_is_not_busy, all_closer_busy_primary):
    """
    Returns the value of psi

    Parameters
    ----------
    primary_survivals : np.array
        The survival probability due to primary vehicles.
    primary_is_not_busy : np.array
        The probability of a primary vehicle not being busy
    all_closer_busy_primary : np.array
        the probability of all vehicles of the same time that are preferred being busy

    Returns
    -------
    np.array
        Returns a vector:
          + `psi[k][p][a]` indicating the probability of survival
          of a patient at pickup location p of type k by a primary
          vehicle at location a.
    """
    psi = primary_survivals * primary_is_not_busy * all_closer_busy_primary.T
    return psi


def get_psi_tilde(
    primary_survivals,
    secondary_survivals,
    primary_is_not_busy,
    secondary_is_not_busy,
    all_closer_busy_primary,
    all_closer_busy_secondary,
    all_secondary_closer_than_primary_busy,
    all_primary_closer_than_secondary_busy,
):
    """
    Returns the value of psi tilde

    Parameters
    ----------
    primary_survivals : np.array
        The survival probability due to primary vehicles.
    secondary_survivals : np.array
        The survival probability due to secondary vehicles.
    primary_is_not_busy : np.array
        The probability of a primary vehicle not being busy
    secondary_is_not_busy : np.array
        The probability of a secondary vehicle not being busy
    all_closer_busy_primary : np.array
        the probability of all primary vehicles of the same type that are preferred being busy
    all_closer_busy_secondary : np.array
        the probability of all secondary vehicles of the same type that are preferred being busy
    all_secondary_closer_than_primary_busy : np.array
        the probability of all secondary vehicles that are preferred being busy
    all_primary_closer_than_secondary_busy : np.array
        the probability of all primary vehicles that are preferred being busy

    Returns
    -------
    np.array
        Returns a vector:
          + `psi_tilde[k][p][a]` indicating the probability of survival
          of a patient at pickup location p of type k by a secondary
          vehicle at location a.
    """
    pass

    secondary_reached = (
        secondary_survivals
        * secondary_is_not_busy
        * all_closer_busy_secondary.T
        * all_primary_closer_than_secondary_busy
    )

    primary_reached = (
        primary_survivals
        * primary_is_not_busy
        * all_closer_busy_primary.T
        * all_secondary_closer_than_primary_busy
    )

    psi_tilde = secondary_reached + primary_reached
    return psi_tilde


def get_objective(
    demand_rates,
    primary_survivals,
    secondary_survivals,
    weights_single_vehicle,
    weights_multiple_vehicles,
    beta,
    R,
    vehicle_station_utilisation_function,
    allocation_primary,
    allocation_secondary,
    cache=None,
    **kwargs,
):
    """
    Returns the value of psi tilde

    Parameters
    ----------
    demand_rates : np.array
        The demand rates of given patient classes from given pickup locations.
    primary_survivals : np.array
        The survival probability due to primary vehicles.
    secondary_survivals : np.array
        The survival probability due to secondary vehicles.
    weights_single_vehicle : np.array
        The weighting given to each class of patients
    weights_multiple_vehicles : np.array
        The weighting given to each class of patients
    beta : np.array
        A three dimensional array denoting which vehicles are preferred.
    R : np.array
        A three dimensional array denoting which primary vehicles are preferred.
    allocation_primary : np.array
        An integer array of number of primary vehicles at every station
    allocation_secondary : np.array
        An integer array of number of secondary vehicles at every station
    vehicle_station_utilisation_function : callable
          returns two arrays of floats -- must be defined with `(**kwargs)`.
    cache : dict
        a dictionary mapping tuples of str representations of allocations
        to objective function values.
    **kwargs : keyword arguments
        remaining keyword arguments to be passed to the vehicle station
        utilisation function.



    Returns
    -------
    float
        Returns the value of the objective function.
    """

    if (cache is not None) and (
        (keyname := (str(allocation_primary), str(allocation_secondary))) in cache
    ):
        return cache[keyname]
    (
        primary_vehicle_station_utilisation,
        secondary_vehicle_station_utilisation,
    ) = vehicle_station_utilisation_function(
        demand_rates=demand_rates,
        primary_survivals=primary_survivals,
        secondary_survivals=secondary_survivals,
        weights_single_vehicle=weights_single_vehicle,
        weights_multiple_vehicles=weights_multiple_vehicles,
        beta=beta,
        R=R,
        allocation_primary=allocation_primary,
        allocation_secondary=allocation_secondary,
        **kwargs,
    )

    primary_is_not_busy = get_is_not_busy_vector(
        primary_vehicle_station_utilisation, allocation_primary
    )
    secondary_is_not_busy = get_is_not_busy_vector(
        secondary_vehicle_station_utilisation, allocation_secondary
    )

    all_closer_busy_primary = get_all_same_closer_busy_vector(
        primary_vehicle_station_utilisation, allocation_primary, beta
    )

    all_closer_busy_secondary = get_all_same_closer_busy_vector(
        secondary_vehicle_station_utilisation, allocation_secondary, beta
    )

    all_primary_closer_than_secondary_busy = get_all_primary_closer_busy_vector(
        primary_vehicle_station_utilisation, allocation_primary, R
    )
    all_secondary_closer_than_primary_busy = get_all_secondary_closer_busy_vector(
        secondary_vehicle_station_utilisation, allocation_secondary, R
    )

    psi = get_psi(primary_survivals, primary_is_not_busy, all_closer_busy_primary)
    psi_tilde = get_psi_tilde(
        primary_survivals,
        secondary_survivals,
        primary_is_not_busy,
        secondary_is_not_busy,
        all_closer_busy_primary,
        all_closer_busy_secondary,
        all_secondary_closer_than_primary_busy,
        all_primary_closer_than_secondary_busy,
    )

    g = (
        ((psi.T * weights_single_vehicle) * demand_rates.T).sum(axis=2)
        + ((psi_tilde.T * weights_multiple_vehicles) * demand_rates.T).sum(axis=2)
    ).sum()

    if cache is not None:
        cache[keyname] = g

    return g


def get_survival_A1_only(
    demand_rates,
    primary_survivals,
    secondary_survivals,
    weights_single_vehicle,
    weights_multiple_vehicles,
    beta,
    R,
    vehicle_station_utilisation_function,
    allocation_primary,
    allocation_secondary,
    **kwargs,
):
    """
    Returns the expected number of A1 patients surviving

    Parameters
    ----------
    demand_rates : np.array
        The demand rates of given patient classes from given pickup locations.
    primary_survivals : np.array
        The survival probability due to primary vehicles.
    secondary_survivals : np.array
        The survival probability due to secondary vehicles.
    weights_single_vehicle : np.array
        The weighting given to each class of patients
    weights_multiple_vehicles : np.array
        The weighting given to each class of patients
    beta : np.array
        A three dimensional array denoting which vehicles are preferred.
    R : np.array
        A three dimensional array denoting which primary vehicles are preferred.
    allocation_primary : np.array
        An integer array of number of primary vehicles at every station
    allocation_secondary : np.array
        An integer array of number of secondary vehicles at every station
    vehicle_station_utilisation_function : callable
          returns two arrays of floats -- must be defined with `(**kwargs)`.
    **kwargs : keyword arguments
        remaining keyword arguments to be passed to the vehicle station
        utilisation function.



    Returns
    -------
    float
        Returns the value of the expected number of A1 patients surviving
    """
    (
        primary_vehicle_station_utilisation,
        secondary_vehicle_station_utilisation,
    ) = vehicle_station_utilisation_function(
        demand_rates=demand_rates,
        primary_survivals=primary_survivals,
        secondary_survivals=secondary_survivals,
        weights_single_vehicle=weights_single_vehicle,
        weights_multiple_vehicles=weights_multiple_vehicles,
        beta=beta,
        R=R,
        allocation_primary=allocation_primary,
        allocation_secondary=allocation_secondary,
        **kwargs,
    )

    primary_is_not_busy = get_is_not_busy_vector(
        primary_vehicle_station_utilisation, allocation_primary
    )
    secondary_is_not_busy = get_is_not_busy_vector(
        secondary_vehicle_station_utilisation, allocation_secondary
    )

    all_closer_busy_primary = get_all_same_closer_busy_vector(
        primary_vehicle_station_utilisation, allocation_primary, beta
    )

    all_closer_busy_secondary = get_all_same_closer_busy_vector(
        secondary_vehicle_station_utilisation, allocation_secondary, beta
    )

    all_primary_closer_than_secondary_busy = get_all_primary_closer_busy_vector(
        primary_vehicle_station_utilisation, allocation_primary, R
    )
    all_secondary_closer_than_primary_busy = get_all_secondary_closer_busy_vector(
        secondary_vehicle_station_utilisation, allocation_secondary, R
    )

    psi_tilde = get_psi_tilde(
        primary_survivals,
        secondary_survivals,
        primary_is_not_busy,
        secondary_is_not_busy,
        all_closer_busy_primary,
        all_closer_busy_secondary,
        all_secondary_closer_than_primary_busy,
        all_primary_closer_than_secondary_busy,
    )

    return (psi_tilde[0].T * demand_rates[0].T).sum()
