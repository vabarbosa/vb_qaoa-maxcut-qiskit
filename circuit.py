from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit


"""
Qiskit quantum gates, quantum circuits defined to QAOA class
"""


def set_wires_circuit(nodes_num):
    """
    Setting quantum and classical registers
    :param nodes_num: number of nodes in the graph
    :return:
    qcircuit: QuantumCircuit
    """
    qr = QuantumRegister(nodes_num)
    cr = ClassicalRegister(nodes_num)
    qcircuit = QuantumCircuit(qr, cr)
    return qcircuit


def superposition_all(nodes_num, qcircuit):
    """
    Appling Hadamard gates to all qubits
    :param nodes_num: number of nodes in the graph
    :param qcircuit: QuantumCircuit
    """
    qcircuit.h(range(nodes_num))
    qcircuit.barrier()


def cost_unitary_maxcut(gamma, graph, qcircuit):
    """
    Appling the Ising type gates with angle gamma along the edges
    :param gamma:
    :param graph:
    :param qcircuit: QuantumCircuit
    :return:
    """
    for edge in graph.edges():
        k = edge[0]
        l = edge[1]
        qcircuit.cp(-2 * gamma, k, l)
        qcircuit.p(gamma, k)
        qcircuit.p(gamma, l)
    qcircuit.barrier()


def driver_unitary(nodes_num, beta, qcircuit):
    """
    The single qubit X rotations with angle beta to all qubits
    :param nodes_num:
    :param beta:
    :param qcircuit: QuantumCircuit
    """
    qcircuit.rx(2 * beta, range(nodes_num))
    qcircuit.barrier()


def to_classical(nodes_num, qcircuit):
    """
    The result in the computational basis
    :param nodes_num:
    :param qcircuit: QuantumCircuit
    :return:
    """
    qcircuit.measure(range(nodes_num), range(nodes_num))


def draw_circuit(qc):
    """
    Draw the circuit implementation
    :param qc: QuantumCircuit
    :return:
    """
    qc.draw(output='mpl')

