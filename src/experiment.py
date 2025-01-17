import numpy as np
import objective
import utilisation
import optimisation
import argparse
import pathlib

if __name__ == "__main__":
    """
    RECOMMENDED PARAMETERS (GUESSES AT THE MOMENT, BASED ON USING 64 CORES)
        max_primary=10,
        max_secondary=10,
        population_size=240,
        keep_size=40,
        number_of_iterations=500,
        initial_number_of_mutatation_repetitions=6,
        cooling_rate=0.25,
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "total_primary",
        type=int,
        help="Total number of primary vehicles in the allocation.",
    )
    parser.add_argument(
        "total_secondary",
        type=int,
        help="Total number of secondary vehicles in the allocation.",
    )
    parser.add_argument(
        "max_primary",
        type=int,
        help="Maximum number of primary vehicles to place in the same location.",
    )
    parser.add_argument(
        "max_secondary",
        type=int,
        help="Maximum number of secondary vehicles to place in the same location.",
    )
    parser.add_argument(
        "population_size",
        type=int,
        help="Number of potential solutions in a population.",
    )
    parser.add_argument(
        "keep_size",
        type=int,
        help="Number of solutions to keep for the next generation.",
    )
    parser.add_argument(
        "number_of_iterations",
        type=int,
        help="Number of iterations to run the optimisation for.",
    )
    parser.add_argument(
        "initial_number_of_mutatation_repetitions",
        type=int,
        help="The number of mutations to carry out successivly at the beginning of the optimisation.",
    )
    parser.add_argument(
        "cooling_rate",
        type=float,
        help="The rate at which the number of successive mutations decreases.",
    )
    parser.add_argument(
        "demand_scenario",
        type=str,
        help="The demand scenario to use (13, 19, 34, or 45).",
    )
    parser.add_argument(
        "scenario_id",
        type=str,
        help="Identifier used to save the results file.",
    )
    parser.add_argument("num_workers", type=int, help="The number of cores to use.")
    parser.add_argument(
        "--progress_bar", help="Use a progress bar or not.", action="store_true"
    )
    args = parser.parse_args()

    ## Read in all data (time units in minutes)
    raw_travel_times = np.genfromtxt("./data/travel_times_matrix.csv", delimiter=",")
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
    vehicle_locations, pickup_locations = tuple(map(range, raw_travel_times.shape))
    weights_single_vehicle = np.array([0, 0, 1])
    weights_multiple_vehicles = np.array([1, 1, 0])
    primary_survivals, secondary_survivals = objective.get_survival_time_vectors(
        survival_functions, primary_vehicle_travel_times, secondary_vehicle_travel_times
    )
    service_rate_primary = 1 / (3.885893339206694 * 60)
    service_rate_secondary = 1 / (1.0382054942769607 * 60)
    demand_rates = (
        np.genfromtxt(f"./data/demand_{args.demand_scenario}.csv", delimiter=",") / 1440
    )
    results_dir = pathlib.Path("./results")
    results_dir.mkdir(exist_ok=True)

    hyperparams_row = np.array(
        [
            int(args.scenario_id),
            int(args.demand_scenario),
            args.total_primary,
            args.total_secondary,
            args.population_size,
            args.keep_size,
            args.number_of_iterations,
            args.initial_number_of_mutatation_repetitions,
            args.cooling_rate,
            args.max_primary,
            args.max_secondary,
        ]
    )
    hyperparams_row_names = [
        "scenario_id",
        "demand_scenario",
        "total_primary",
        "total_secondary",
        "population_size",
        "keep_size",
        "number_of_iterations",
        "initial_number_of_mutatation_repetitions",
        "cooling_rate",
        "max_primary",
        "max_secondary",
    ]

    # Carry out the optimisation
    (
        best_primary,
        best_secondary,
        objective_by_iteration,
    ) = optimisation.optimise(
        number_of_locations=67,
        number_of_primary_vehicles=args.total_primary,
        number_of_secondary_vehicles=args.total_secondary,
        max_primary=args.max_primary,
        max_secondary=args.max_secondary,
        population_size=args.population_size,
        keep_size=args.keep_size,
        number_of_iterations=args.number_of_iterations,
        mutation_function=optimisation.mutate_retain_vehicle_numbers,
        initial_number_of_mutatation_repetitions=args.initial_number_of_mutatation_repetitions,
        cooling_rate=args.cooling_rate,
        demand_rates=demand_rates,
        primary_survivals=primary_survivals,
        secondary_survivals=secondary_survivals,
        weights_single_vehicle=weights_single_vehicle,
        weights_multiple_vehicles=weights_multiple_vehicles,
        beta=beta,
        R=R,
        vehicle_station_utilisation_function=utilisation.solve_utilisations,
        seed=0,
        num_workers=args.num_workers,
        progress_bar=args.progress_bar,
        service_rate_primary=service_rate_primary,
        service_rate_secondary=service_rate_secondary,
    )

    best_primary_with_hyperparams = np.append(hyperparams_row, best_primary)
    best_secondary_with_hyperparams = np.append(hyperparams_row, best_secondary)

    allocation_titles = hyperparams_row_names + [
        f"a{str(i).zfill(2)}" for i in range(67)
    ]
    population_titles = (
        hyperparams_row_names
        + ["iteration"]
        + [str(i) for i in range(args.population_size)]
    )

    hyperparams_repeat = (
        np.repeat(hyperparams_row, args.number_of_iterations)
        .reshape(len(hyperparams_row), args.number_of_iterations)
        .T
    )
    hyperparams_repeat_with_index = np.vstack(
        [hyperparams_repeat.T, np.arange(args.number_of_iterations)]
    ).T
    objective_by_iteration_with_hyperparameters = np.concatenate(
        [hyperparams_repeat_with_index, objective_by_iteration], axis=1
    )

    np.savetxt(
        f"./results/allocation_primary_{args.scenario_id}.csv",
        [best_primary_with_hyperparams],
        delimiter=",",
        header=",".join(allocation_titles),
        comments="",
    )
    np.savetxt(
        f"./results/allocation_secondary_{args.scenario_id}.csv",
        [best_secondary_with_hyperparams],
        delimiter=",",
        header=",".join(allocation_titles),
        comments="",
    )

    np.savetxt(
        f"./results/population_objectives_{args.scenario_id}.csv",
        objective_by_iteration_with_hyperparameters,
        delimiter=",",
        header=",".join(population_titles),
        comments="",
    )
