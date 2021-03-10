from bayes_opt import BayesianOptimization

from qaoa.backend import counts
from qaoa.qaoa import QAOA
from qaoa.utils import *


class QAOA_solver():
    def __init__(self, graph, nodes):
        """
        QAOA_solver runs the Quantum Approximative Optimization Algorithm (QAOA) using bayesian optimization.
        :param graph: represents the problem
        :param nodes: list
        """
        self._graph = graph
        self._qa = QAOA(graph, nodes)

    def black_box_function(self, beta1, beta2, beta3, gamma1, gamma2, gamma3):
        """
        Cost function to optimization process
        :param beta:
        :param gamma:
        :return:
        max_cost:float the cost value obtained as a evaluation of cost function and best bitstring
        """

        gammas = np.array([gamma1, gamma2, gamma3])
        betas = np.array([beta1, beta2, beta3])

        self._qa.set_parameters(gammas, betas)
        self._qa.set_circuit_fixed()

        #sim_results, shots = self._qa.run_simulator()

        #sampled_cost, max_cost = post_processing(self._graph, counts(sim_results), shots)

        #return sampled_cost
        return beta1**2 - gamma1

    def run_bayesian_optimizer(self, p=1):
        """
        Bayesian optimizer for QAOA layers p = 1,2,3
        :param p: number of layers
        :return:
        """

        # Bounded region of parameter space
        pbounds = {'beta1': (-0.25, 0.25), 'beta2': (0, 0.0001), 'beta3': (0, 0.0001),
                   'gamma1': (1.0, 2.0), 'gamma2': (0, 0.0001), 'gamma3': (0, 0.0001)}
        if p == 2:
            pbounds = {'beta1': (-0.25, 0.25), 'beta2': (-3.14, 3.14), 'beta3': (0, 0.0001),
                       'gamma1': (1.0, 2.0), 'gamma2': (-3.14, 3.14), 'gamma3': (0, 0.0001)}
        if p == 3:
            pbounds = {'beta1': (-0.25, 0.25), 'beta2': (-3.14, 3.14), 'beta3': (-3.14, 3.14),
                       'gamma1': (1.0, 2.0), 'gamma2': (-3.14, 3.14), 'gamma3': (-3.14, 3.14)}

        self._optimizer = BayesianOptimization(
            f=self.black_box_function,
            pbounds=pbounds,
            random_state=1,
        )
        self._optimizer.maximize(init_points=5, n_iter=50)
