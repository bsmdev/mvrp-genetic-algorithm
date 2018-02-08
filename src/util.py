from typing import Tuple
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from itertools import cycle


def read_problem_file(filename: str) -> Tuple:
    file = open(filename, "r")
    line1 = list(map(lambda e: int(e), file.readline().split()))
    max_vehicles = line1[0]
    number_of_customers = line1[1]
    number_of_depots = line1[2]
    tmp_depots = []
    depots = defaultdict(list)
    customers = defaultdict(list)
    for i in range(number_of_depots):
        line = list(map(lambda e: int(e), file.readline().split()))
        tmp_depots.append(line)
    for i in range(number_of_customers):
        line = list(map(lambda e: int(e), file.readline().split()[0:5]))
        customer_id = line[0]
        coordinate = np.array([line[1], line[2]])
        service_duration = line[3]
        demand = line[4]
        customers[customer_id].extend([coordinate, service_duration, demand])
    for i in range(number_of_depots):
        line = list(map(lambda e: int(e), file.readline().split()[0:3]))
        depot_id = line[0]
        coordinate = np.array([line[1], line[2]])
        max_duration = tmp_depots[i][0]
        max_load = tmp_depots[i][1]
        depots[depot_id].extend([coordinate, max_duration, max_load])
    return customers, depots, max_vehicles


def plot(data):
    customers = data.customers
    depots = data.depots
    routes = data.routes
    cycol = cycle('grcm')

    plt.title("Fitness = " + str(round(data.calculate_fitness(), 7)))

    for customer_id in customers:
        x = customers[customer_id][0][0]
        y = customers[customer_id][0][1]
        plt.scatter(x, y, color='blue')

    for depot_id in depots:
        x_depot = x_start = depots[depot_id][0][0]
        y_depot = y_start = depots[depot_id][0][1]
        plt.scatter(x_depot, y_depot, color='red', marker="s")

        for route in routes[depot_id]:
            color = next(cycol)
            for customer_id in route:
                x_stop = customers[customer_id][0][0]
                y_stop = customers[customer_id][0][1]
                plt.plot([x_start, x_stop], [y_start, y_stop], color=color)
                x_start = x_stop
                y_start = y_stop

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5,
               handles=[mpatches.Patch(color='blue', label=str(len(customers)) + ' Customers'),
                        mpatches.Patch(color='red', label=str(len(depots)) + ' Depots'),
                        # mpatches.Patch(color='yellow', label="Fitness = " + str(round(data.calculate_fitness(), 7)))
                        ])
    plt.show()
