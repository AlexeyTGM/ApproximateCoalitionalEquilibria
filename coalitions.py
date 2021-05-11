from abc import ABC, abstractmethod
import numpy as np
from utils import get_all_possible_partitions, all_subsets


class State:
    def __init__(self, agents, median_rule=lambda members: np.median(members), g=1, t=1):
        self.agents = np.array(agents)
        self.median_rule = median_rule
        self.g = g
        self.t = t
        self.coalition_creator = EgalitarianCoalition


class Coalition(ABC):
    def __init__(self, state, members):
        self.state = state
        self.members = np.array(list(members))
        self.g = self.state.g
        self.t = self.state.t
        # print(state.agents[np.array(members)])
        self.update_median()

    def update_median(self):
        self.m = self.state.median_rule(self.state.agents[self.members])

    def __repr__(self):
        return str(self.members)

    def add(self, member):
        self.members = np.append(self.members, [member])
        self.update_median()

    def remove(self, member):
        index = np.argwhere(self.members == member)
        self.members = np.delete(self.members, index)
        self.update_median()

    @abstractmethod
    def cost(self, member_index):
        pass


class EgalitarianCoalition(Coalition):
    def __init__(self, state, members):
        super().__init__(state, members)

    def cost(self, member_index):
        member_positions = self.state.agents[np.array(self.members)]
        medians = np.full(member_positions.shape, self.m)
        # print(member_positions)
        # print(medians)
        # print(np.abs(np.subtract(member_positions, medians)))
        total_t = np.sum(np.abs(np.subtract(member_positions, medians)))
        # print(total_t)
        return (self.g + self.t * total_t) / len(self.members)


class SnobCoalition(Coalition):
    def __init__(self, state, members):
        super().__init__(state, members)

    def cost(self, member_index):
        return self.g / len(self.members) + self.t * np.abs(self.m - self.state.agents[member_index])


class Configuration:
    def __init__(self, state, coalitions):
        self.state = state
        self.coalitions = [self.state.coalition_creator(self.state, coalition_members)
                           for coalition_members in coalitions]

    def __repr__(self):
        return str([coalition for coalition in self.coalitions])

    def get_coalition(self, member):
        for coalition in self.coalitions:
            if member in coalition.members:
                return coalition
        return None


class MigrationInstabilityCalculator:
    def __init__(self, state):
        self.state = state

    def get_initial_cost(self, configuration, member):
        coalition = configuration.get_coalition(member)
        cost = coalition.cost(member)
        return cost

    def calculate_config(self, configuration):
        delta = 0
        agents_len = len(self.state.agents)

        initial_costs = [self.get_initial_cost(configuration, member)
                         for member in range(0, agents_len)]

        for member in range(0, agents_len):
            current_coalition = configuration.get_coalition(member)
            current_cost = current_coalition.cost(member)
            # current_coalition.remove(member)
            costs = []
            for coalition in configuration.coalitions:
                if coalition != current_coalition:
                    coalition.add(member)
                    cost = coalition.cost(member)
                    costs.append(cost)
                    coalition.remove(member)
                else:
                    costs.append(float("inf"))
            min_cost_index = np.argmin(costs)
            delta = min(delta, initial_costs[member] - costs[min_cost_index])

        return delta

    def create_all_configurations(self):
        agents_len = len(self.state.agents)
        all_possible_coalitions = list(get_all_possible_partitions(
            list(range(0, agents_len)), agents_len))
        configurations = [Configuration(self.state, coalitions)
                          for coalitions in all_possible_coalitions]
        return configurations

    def calculate(self):
        configurations = self.create_all_configurations()
        deltas = [self.calculate_config(configuration)
                  for configuration in configurations]
        max_delta_index = np.argmax(deltas)
        return (max_delta_index, deltas[max_delta_index])


class CoalitionInstabilityCalculator:
    def __init__(self, state, length=0):
        self.state = state
        self.length = len(state.agents) if length == 0 else length
        superset_ = list(all_subsets(list(range(0, len(self.state.agents)))))
        self.superset = [EgalitarianCoalition(self.state, list(members)) for members in superset_]

    def check_is_stable(self, configuration):
        is_best = True
        for coalition in self.superset:
            check_if_better = []
            for member in coalition.members:
                if coalition.cost(member) < configuration.get_coalition(member).cost(member):
                    check_if_better.append(True)
                else:
                    check_if_better.append(False)
            if all(check_if_better) == True:
                is_best = False
                return is_best
        return is_best

    def calculate_abs_instability_for(self, configuration):
        instability = 0
        for coalition in self.superset:
            delta = float("inf")
            for member in coalition.members:
                diff = configuration.get_coalition(member).cost(member) - coalition.cost(member)
                if diff < delta:
                    delta = diff
            if instability < delta:
                instability = delta
        return instability

    def calculate_config_costs(self, configuration):
        delta = 0
        agents_len = len(self.state.agents)

        member_costs = np.array([None] * agents_len)
        for coalition in configuration.coalitions:
            for member in coalition.members:
                member_cost = coalition.cost(member)
                member_costs[member] = member_cost

        return member_costs

    def create_all_configurations(self):
        all_possible_coalitions = list(get_all_possible_partitions(
            list(range(0, len(self.state.agents))), self.length))
        configurations = [Configuration(self.state, coalitions)
                          for coalitions in all_possible_coalitions]
        return configurations

    def calculate(self):
        configurations = self.create_all_configurations()
        deltas = []

        for initial_configuration in configurations:
            deltas.append(self.calculate_abs_instability_for(initial_configuration))

        return np.amin(deltas)
