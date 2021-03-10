import matplotlib.pyplot as plt
from qaoa.backend import simulator, counts, real_quantum_device, plot_results
from qaoa.circuit import superposition_all, driver_unitary, to_classical, set_wires_circuit, draw_circuit, \
    cost_unitary_maxcut
from qaoa.utils import *


class QAOA:
    def __init__(self, graph, nodes):
        """
        QAOA instance is a Quantum Approximative Optimization Algorithm in the MAXCUT graph problem.
        It defines and draws the quantum circuit. It runs in different backends.
        :param
        """
        self._graph = graph
        self._nodes = nodes
        #self.set_parameters(np.array([1.9]), np.array([0.2]))
        #self.set_circuit_fixed()
        self._results = None
        self._shots = None

    def set_parameters(self, gamma, beta):
        """
        Setting para
        :param gamma:
        :param beta:
        """
        self._gamma = gamma
        self._beta = beta

    def set_circuit_fixed(self):
        """

        :return:
        qc: QuantumCircuit
        """

        nodes_num = len(self._nodes)
        self._qc = set_wires_circuit(nodes_num)
        superposition_all(nodes_num, self._qc)

        p = self._gamma.size
        for i in range(p):
            # one layer: p = 1
            cost_unitary_maxcut(self._gamma[i], self._graph, self._qc)
            driver_unitary(nodes_num, self._beta[i], self._qc)

        to_classical(nodes_num, self._qc)


    def draw(self):
        """
        Draw the quantum gates in a quantum circuit
        """
        plt.show(draw_circuit(self._qc))


    def run_simulator(self):
        """

        :return:
        """
        self._results, self._shots = simulator(self._qc)

    def run_real_quantum_device(self):
        """

        :return:
        """
        self._results, self._shots = real_quantum_device(self._qc)

    def plot_run(self):
        """

        :return:
        """
        plt.show(plot_results(self._results))



    def show_results(self):
        """

        :return:
        """
        self._counts = counts(self._results)
        c_sampled, max_c = post_processing(self._graph, self._counts, self._shots)
        self._qaoa_results = [c_sampled, max_c]
