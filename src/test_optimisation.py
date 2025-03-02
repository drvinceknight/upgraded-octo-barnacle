import objective
import optimisation
import utilisation
import numpy as np
import random


def test_move_vehicle_of_same_type():
    primary_allocation = np.array([0, 1, 5, 1])
    secondary_allocation = np.array([3, 9, 0, 0])
    max_allocation = 5

    np.random.seed(1)
    (
        resulting_primary_allocation,
        resulting_secondary_allocation,
    ) = optimisation.move_vehicle_of_same_type(
        allocation_for_moving=primary_allocation,
        allocation_not_for_moving=secondary_allocation,
        max_allocation=max_allocation,
    )

    assert sum(primary_allocation) == sum(resulting_primary_allocation)
    assert sum(secondary_allocation) == sum(resulting_secondary_allocation)
    assert np.array_equal(secondary_allocation, resulting_secondary_allocation)
    assert np.array_equal(resulting_primary_allocation, np.array([0, 1, 4, 2]))
    assert resulting_primary_allocation.dtype.type is np.int64
    assert resulting_secondary_allocation.dtype.type is np.int64


def test_switch_primary_to_secondary():
    primary_allocation = np.array([0, 1, 5, 1])
    secondary_allocation = np.array([3, 9, 0, 0])
    max_allocation = 5

    np.random.seed(1)
    (
        resulting_primary_allocation,
        resulting_secondary_allocation,
    ) = optimisation.switch_primary_to_secondary(
        primary_allocation=primary_allocation,
        secondary_allocation=secondary_allocation,
        max_allocation=max_allocation,
    )

    assert sum(primary_allocation) - 1 == sum(resulting_primary_allocation)
    assert sum(secondary_allocation) + 3 == sum(resulting_secondary_allocation)
    assert np.array_equal(resulting_secondary_allocation, np.array([5, 9, 1, 0]))
    assert np.array_equal(resulting_primary_allocation, np.array([0, 1, 4, 1]))
    assert resulting_primary_allocation.dtype.type is np.int64
    assert resulting_secondary_allocation.dtype.type is np.int64


def test_switch_secondary_to_primary():
    primary_allocation = np.array([0, 1, 5, 1])
    secondary_allocation = np.array([3, 9, 0, 0])
    max_allocation = 5

    np.random.seed(1)
    (
        resulting_primary_allocation,
        resulting_secondary_allocation,
    ) = optimisation.switch_secondary_to_primary(
        primary_allocation=primary_allocation,
        secondary_allocation=secondary_allocation,
        max_allocation=max_allocation,
    )

    assert sum(primary_allocation) + 1 == sum(resulting_primary_allocation)
    assert sum(secondary_allocation) - 3 == sum(resulting_secondary_allocation)
    assert np.array_equal(resulting_secondary_allocation, np.array([2, 7, 0, 0]))
    assert np.array_equal(resulting_primary_allocation, np.array([0, 1, 5, 2]))
    assert resulting_primary_allocation.dtype.type is np.int64
    assert resulting_secondary_allocation.dtype.type is np.int64


def test_mutate_retain_vehicle_numbers_with_seed_0():
    primary_allocation = np.array([0, 1, 5, 1])
    secondary_allocation = np.array([3, 9, 0, 0])
    max_allocation = 5

    np.random.seed(0)
    (
        resulting_primary_allocation,
        resulting_secondary_allocation,
    ) = optimisation.mutate_retain_vehicle_numbers(
        primary_allocation=primary_allocation,
        secondary_allocation=secondary_allocation,
        max_primary=max_allocation,
        max_secondary=max_allocation,
    )

    assert sum(primary_allocation) + (sum(secondary_allocation) / 3) == sum(
        resulting_primary_allocation
    ) + (sum(resulting_secondary_allocation) / 3)
    assert np.array_equal(resulting_secondary_allocation, np.array([3, 9, 0, 0]))
    assert np.array_equal(resulting_primary_allocation, np.array([0, 1, 4, 2]))
    assert resulting_primary_allocation.dtype.type is np.int64
    assert resulting_secondary_allocation.dtype.type is np.int64


def test_mutate_retain_vehicle_numbers_with_seed_1():
    primary_allocation = np.array([0, 1, 5, 1])
    secondary_allocation = np.array([3, 9, 0, 0])
    max_allocation = 5

    np.random.seed(1)
    (
        resulting_primary_allocation,
        resulting_secondary_allocation,
    ) = optimisation.mutate_retain_vehicle_numbers(
        primary_allocation=primary_allocation,
        secondary_allocation=secondary_allocation,
        max_primary=max_allocation,
        max_secondary=max_allocation,
    )

    assert sum(primary_allocation) + (sum(secondary_allocation) / 3) == sum(
        resulting_primary_allocation
    ) + (sum(resulting_secondary_allocation) / 3)
    assert np.array_equal(resulting_secondary_allocation, np.array([3, 8, 0, 1]))
    assert np.array_equal(resulting_primary_allocation, np.array([0, 1, 5, 1]))
    assert resulting_primary_allocation.dtype.type is np.int64
    assert resulting_secondary_allocation.dtype.type is np.int64


def test_mutate_full_with_seed_0():
    primary_allocation = np.array([0, 1, 5, 1])
    secondary_allocation = np.array([3, 9, 0, 0])
    max_allocation = 5

    np.random.seed(0)
    (
        resulting_primary_allocation,
        resulting_secondary_allocation,
    ) = optimisation.mutate_full(
        primary_allocation=primary_allocation,
        secondary_allocation=secondary_allocation,
        max_primary=max_allocation,
        max_secondary=max_allocation,
    )

    assert sum(primary_allocation) + (sum(secondary_allocation) / 3) == sum(
        resulting_primary_allocation
    ) + (sum(resulting_secondary_allocation) / 3)
    assert np.array_equal(resulting_secondary_allocation, np.array([3, 9, 0, 0]))
    assert np.array_equal(resulting_primary_allocation, np.array([0, 1, 4, 2]))
    assert resulting_primary_allocation.dtype.type is np.int64
    assert resulting_secondary_allocation.dtype.type is np.int64


def test_mutate_full_with_seed_1():
    primary_allocation = np.array([0, 1, 5, 1])
    secondary_allocation = np.array([3, 9, 0, 0])
    max_allocation = 5

    np.random.seed(1)
    (
        resulting_primary_allocation,
        resulting_secondary_allocation,
    ) = optimisation.mutate_full(
        primary_allocation=primary_allocation,
        secondary_allocation=secondary_allocation,
        max_primary=max_allocation,
        max_secondary=max_allocation,
    )

    assert sum(primary_allocation) + (sum(secondary_allocation) / 3) == sum(
        resulting_primary_allocation
    ) + (sum(resulting_secondary_allocation) / 3)
    assert np.array_equal(resulting_secondary_allocation, np.array([3, 8, 0, 1]))
    assert np.array_equal(resulting_primary_allocation, np.array([0, 1, 5, 1]))
    assert resulting_primary_allocation.dtype.type is np.int64
    assert resulting_secondary_allocation.dtype.type is np.int64


def test_mutate_full_with_seed_3():
    primary_allocation = np.array([0, 1, 5, 1])
    secondary_allocation = np.array([3, 9, 0, 0])
    max_allocation = 5

    np.random.seed(3)
    (
        resulting_primary_allocation,
        resulting_secondary_allocation,
    ) = optimisation.mutate_full(
        primary_allocation=primary_allocation,
        secondary_allocation=secondary_allocation,
        max_primary=max_allocation,
        max_secondary=max_allocation,
    )

    assert sum(primary_allocation) + (sum(secondary_allocation) / 3) == sum(
        resulting_primary_allocation
    ) + (sum(resulting_secondary_allocation) / 3)
    assert np.array_equal(resulting_secondary_allocation, np.array([5, 9, 1, 0]))
    assert np.array_equal(resulting_primary_allocation, np.array([0, 0, 5, 1]))
    assert resulting_primary_allocation.dtype.type is np.int64
    assert resulting_secondary_allocation.dtype.type is np.int64


def test_mutate_full_with_seed_5():
    primary_allocation = np.array([0, 1, 5, 1])
    secondary_allocation = np.array([3, 9, 0, 0])
    max_allocation = 5

    np.random.seed(5)
    (
        resulting_primary_allocation,
        resulting_secondary_allocation,
    ) = optimisation.mutate_full(
        primary_allocation=primary_allocation,
        secondary_allocation=secondary_allocation,
        max_primary=max_allocation,
        max_secondary=max_allocation,
    )

    assert sum(primary_allocation) + (sum(secondary_allocation) / 3) == sum(
        resulting_primary_allocation
    ) + (sum(resulting_secondary_allocation) / 3)
    assert np.array_equal(resulting_secondary_allocation, np.array([2, 7, 0, 0]))
    assert np.array_equal(resulting_primary_allocation, np.array([1, 1, 5, 1]))
    assert resulting_primary_allocation.dtype.type is np.int64
    assert resulting_secondary_allocation.dtype.type is np.int64


def test_repeat_mutation():
    primary_allocation = np.array([0, 1, 5, 1])
    secondary_allocation = np.array([3, 9, 0, 0])
    max_allocation = 5

    # Make allocations manually
    np.random.seed(5)
    allocations = [[np.array(primary_allocation), np.array(secondary_allocation)]]
    for repeat in range(10):
        new_primary_allocation, new_secondary_allocation = optimisation.mutate_full(
            primary_allocation=allocations[-1][0],
            secondary_allocation=allocations[-1][1],
            max_primary=max_allocation,
            max_secondary=max_allocation,
        )
        allocations.append(
            [np.array(new_primary_allocation), np.array(new_secondary_allocation)]
        )

    # Make allocations with repeat function
    allocations_repeat = [
        [np.array(primary_allocation), np.array(secondary_allocation)]
    ]
    for repeat in range(10):
        np.random.seed(5)
        new_primary_allocation, new_secondary_allocation = optimisation.repeat_mutation(
            mutation_function=optimisation.mutate_full,
            times_to_repeat=repeat + 1,
            primary_allocation=primary_allocation,
            secondary_allocation=secondary_allocation,
            max_primary=max_allocation,
            max_secondary=max_allocation,
        )
        allocations_repeat.append(
            [np.array(new_primary_allocation), np.array(new_secondary_allocation)]
        )

    for repeat in range(10):
        assert np.allclose(allocations[repeat], allocations_repeat[repeat])


def test_create_initial_population():
    number_of_locations = 6
    population_size = 15
    number_of_primary_vehicles = 8
    number_of_secondary_vehicles = 12
    max_primary = 3
    max_secondary = 4

    np.random.seed(0)
    population = optimisation.create_initial_population(
        number_of_locations=number_of_locations,
        number_of_primary_vehicles=number_of_primary_vehicles,
        number_of_secondary_vehicles=number_of_secondary_vehicles,
        max_primary=max_primary,
        max_secondary=max_secondary,
        population_size=population_size,
    )

    assert population.shape == (population_size, 2, number_of_locations)
    for primary_allocation, secondary_allocation in population:
        assert primary_allocation.sum() == number_of_primary_vehicles
        assert secondary_allocation.sum() == number_of_secondary_vehicles
        assert primary_allocation.max() <= max_primary
        assert secondary_allocation.max() <= max_secondary
        assert primary_allocation.dtype.type is np.int64
        assert secondary_allocation.dtype.type is np.int64

    first_primary_allocation, first_secondary_allocation = population[0]

    assert np.array_equal(first_primary_allocation, np.array([2, 1, 2, 1, 1, 1]))
    assert np.array_equal(first_secondary_allocation, np.array([1, 0, 2, 2, 3, 4]))


def test_create_initial_population_with_randomising_vehicle_numbers():
    number_of_locations = 6
    population_size = 15
    number_of_primary_vehicles = 8
    number_of_secondary_vehicles = 12
    max_primary = 3
    max_secondary = 4

    np.random.seed(0)
    population = optimisation.create_initial_population(
        number_of_locations=number_of_locations,
        number_of_primary_vehicles=number_of_primary_vehicles,
        number_of_secondary_vehicles=number_of_secondary_vehicles,
        max_primary=max_primary,
        max_secondary=max_secondary,
        population_size=population_size,
        randomise_vehicle_numbers=True,
    )

    assert population.shape == (population_size, 2, number_of_locations)
    for primary_allocation, secondary_allocation in population:
        assert primary_allocation.sum() + (
            secondary_allocation.sum() / 3
        ) == number_of_primary_vehicles + (number_of_secondary_vehicles / 3)
        assert primary_allocation.max() <= max_primary
        assert secondary_allocation.max() <= max_secondary
        assert primary_allocation.dtype.type is np.int64
        assert secondary_allocation.dtype.type is np.int64

    first_primary_allocation, first_secondary_allocation = population[0]

    assert np.array_equal(first_primary_allocation, np.array([2, 1, 2, 1, 2, 1]))
    assert np.array_equal(first_secondary_allocation, np.array([1, 0, 2, 2, 1, 3]))


def test_rank_population():
    # Read in data
    raw_travel_times = np.genfromtxt(
        "./test_data/travel_times_matrix.csv", delimiter=","
    )
    beta = objective.get_beta(travel_times=raw_travel_times)
    primary_vehicle_travel_times = raw_travel_times / 0.75
    secondary_vehicle_travel_times = raw_travel_times / 1.215
    R = objective.get_R(
        primary_vehicle_travel_times=primary_vehicle_travel_times,
        secondary_vehicle_travel_times=secondary_vehicle_travel_times,
    )
    survival_functions = (
        lambda t: 1 / (1 + np.exp(0.26 + 0.139 * t)),
        lambda t: np.heaviside(15 - t, 1),
        lambda t: np.heaviside(60 - t, 1),
    )
    demand_rates = np.genfromtxt("./test_data/demand.csv", delimiter=",") / 1440
    vehicle_locations, pickup_locations = tuple(map(range, raw_travel_times.shape))

    weights_single_vehicle = np.array([0, 0, 1])
    weights_multiple_vehicles = np.array([1, 1, 0])

    primary_survivals, secondary_survivals = objective.get_survival_time_vectors(
        survival_functions, primary_vehicle_travel_times, secondary_vehicle_travel_times
    )

    # Utilisations and allocations for resource level 61
    given_utilisations_primary_61 = np.genfromtxt(
        "./test_data/primary_utilisations_61.csv", delimiter=","
    )
    given_utilisations_secondary_61 = np.genfromtxt(
        "./test_data/secondary_utilisations_61.csv", delimiter=","
    )
    allocation_61 = np.genfromtxt(
        "./test_data/allocation_61.csv", delimiter=","
    ).astype(np.int64)

    # Create population
    random.seed(0)
    population = np.array(
        [
            [
                random.sample(list(allocation_61[:67]), 67),
                random.sample(list(allocation_61[67:]), 67),
            ]
            for entry in range(10)
        ]
    )
    assert population.shape == (10, 2, 67)

    ranked_population, objective_values = optimisation.rank_population(
        population=population,
        demand_rates=demand_rates,
        primary_survivals=primary_survivals,
        secondary_survivals=secondary_survivals,
        weights_single_vehicle=weights_single_vehicle,
        weights_multiple_vehicles=weights_multiple_vehicles,
        beta=beta,
        R=R,
        vehicle_station_utilisation_function=utilisation.given_utilisations,
        num_workers=7,
        given_utilisations_primary=given_utilisations_primary_61,
        given_utilisations_secondary=given_utilisations_secondary_61,
    )

    assert ranked_population.shape == (10, 2, 67)
    assert np.all(objective_values[:-1] >= objective_values[1:])
    previous_objective_value = float("inf")
    for allocation in ranked_population:
        next_objective_value = objective.get_objective(
            demand_rates=demand_rates,
            primary_survivals=primary_survivals,
            secondary_survivals=secondary_survivals,
            weights_single_vehicle=weights_single_vehicle,
            weights_multiple_vehicles=weights_multiple_vehicles,
            beta=beta,
            R=R,
            vehicle_station_utilisation_function=utilisation.given_utilisations,
            allocation_primary=allocation[0],
            allocation_secondary=allocation[1],
            given_utilisations_primary=given_utilisations_primary_61,
            given_utilisations_secondary=given_utilisations_secondary_61,
        )
        assert previous_objective_value >= next_objective_value
        previous_objective_value = next_objective_value


def test_optimise(benchmark):
    # Read in data
    raw_travel_times = np.genfromtxt(
        "./test_data/travel_times_matrix.csv", delimiter=","
    )
    beta = objective.get_beta(travel_times=raw_travel_times)
    primary_vehicle_travel_times = raw_travel_times / 0.75
    secondary_vehicle_travel_times = raw_travel_times / 1.215
    R = objective.get_R(
        primary_vehicle_travel_times=primary_vehicle_travel_times,
        secondary_vehicle_travel_times=secondary_vehicle_travel_times,
    )
    survival_functions = (
        lambda t: 1 / (1 + np.exp(0.26 + 0.139 * t)),
        lambda t: np.heaviside(15 - t, 1),
        lambda t: np.heaviside(60 - t, 1),
    )
    demand_rates = np.genfromtxt("./test_data/demand.csv", delimiter=",") / 1440
    vehicle_locations, pickup_locations = tuple(map(range, raw_travel_times.shape))

    weights_single_vehicle = np.array([0, 0, 1])
    weights_multiple_vehicles = np.array([1, 1, 0])

    primary_survivals, secondary_survivals = objective.get_survival_time_vectors(
        survival_functions, primary_vehicle_travel_times, secondary_vehicle_travel_times
    )
    pop_size = 20
    num_iters = 30
    max_alloc = 4
    num_vehicles = 20

    best_primary, best_secondary, objective_by_iteration = benchmark(
        optimisation.optimise,
        number_of_locations=67,
        number_of_primary_vehicles=num_vehicles,
        number_of_secondary_vehicles=num_vehicles,
        max_primary=max_alloc,
        max_secondary=max_alloc,
        population_size=pop_size,
        keep_size=5,
        number_of_iterations=num_iters,
        mutation_function=optimisation.mutate_retain_vehicle_numbers,
        initial_number_of_mutatation_repetitions=1,
        cooling_rate=1,
        demand_rates=demand_rates,
        primary_survivals=primary_survivals,
        secondary_survivals=secondary_survivals,
        weights_single_vehicle=weights_single_vehicle,
        weights_multiple_vehicles=weights_multiple_vehicles,
        beta=beta,
        R=R,
        vehicle_station_utilisation_function=utilisation.constant_utilisation,
        seed=0,
        num_workers=7,
        progress_bar=False,
        utilisation_rate_primary=0.7,
        utilisation_rate_secondary=0.4,
    )
    best_over_time = objective_by_iteration.max(axis=1)

    assert len(best_primary) == 67
    assert len(best_secondary) == 67
    assert max(best_primary) <= max_alloc
    assert max(best_secondary) <= max_alloc
    assert sum(best_primary) == num_vehicles
    assert sum(best_secondary) == num_vehicles
    assert objective_by_iteration.shape == (num_iters, pop_size)
    assert np.all(best_over_time[:-1] <= best_over_time[1:])
