import numpy as np

from coalitions import State, Configuration, EgalitarianCoalition, SnobCoalition, MigrationInstabilityCalculator, CoalitionInstabilityCalculator
from utils import bell, get_all_possible_partitions, central_rule_median

def check_state(agents):
    state = State(agents, central_rule_median)
    state.coalition_creator = SnobCoalition
    calculator = CoalitionInstabilityCalculator(state)
    instability = calculator.calculate()
    if instability > 0:
        print('world: ' + str(agents))
        print('instability: ' + str(instability))

# check_state([0, 0, 0, 0.311, 0.311, 1])

# step = 0.1
# def fill_column(agents, index):
#     for i in range(0, int(1/step)):
#         agents[index] += step
#         print('world: ' + str(agents))
#         # check_state(agents)

# for n in range(3, 4):
#     agents = np.zeros(n)
#     for i in range(1, n):
#         for j in range(i, n):
#             agents[n-j] = 0
#             fill_column(agents, n-j)


step = 0.001
# for i2 in np.arange(0, 1.0, step):
#     for i3 in np.arange(i2, 1.0, step):
#         agents = [0, i2, i3]
#         unique_word_count = len(set(agents))
#         if unique_word_count <= 2:
#             break
#         check_state(agents)

for i2 in np.arange(0, 1.0, step):
    for i3 in np.arange(i2, 1.0, step):
        for i4 in np.arange(i3, 1.0, step):
            agents = [0, i2, i3, i4]
            unique_word_count = len(set(agents))
            if unique_word_count <= 2:
                break
            check_state(agents)

# for i2 in np.arange(0, 1.0, step):
#     for i3 in np.arange(i2, 1.0, step):
#         for i4 in np.arange(i3, 1.0, step):
#             for i5 in np.arange(i4, 1.0, step):
#                 agents = [0, i2, i3, i4, i5]
#                 unique_word_count = len(set(agents))
#                 if unique_word_count <= 2:
#                     break
#                 check_state(agents)

# for i2 in np.arange(0, 1.0, step):
#     for i3 in np.arange(i2, 1.0, step):
#         for i4 in np.arange(i3, 1.0, step):
#             for i5 in np.arange(i4, 1.0, step):
#                 for i6 in np.arange(i5, 1.0, step):
#                     agents = [i1, i2, i3, i4, i5, i6]
#                     unique_word_count = len(set(agents))
#                     if unique_word_count <= 2:
#                         break
#                     check_state(agents)

# step = 0.1

# for i2 in np.arange(0, 1.0, step):
#     for i3 in np.arange(i2, 1.0, step):
#         agents = [0, i2, i3]
#         print(agents)