# qaoa-maxcut-qiskit
Quantum Approximative Optimization Algorithm with Bayesian optimizer to MAXCUT problem

```python
from qiskit import QuantumCircuit, Aer, execute

def QAOA(graph, par):
    qc = QuantumCircuit(graph.number_of_nodes())
    qc.h(range(graph.number_of_nodes()))
    for i in range(int(len(par)/2)):
      for edge in graph.edges():
        qc.cp(-2*par[i]*g.get_edge_data(edge[0],edge[1])['weight'], edge[0], edge[1])
        qc.p(par[i], edge[0])
        qc.p(par[i], edge[1])
      qc.rx(2*par[int(len(par)/2)+i],range(graph.number_of_nodes()))
      result = execute(qc, Aer.get_backend('statevector_simulator')).result()
    return result.get_statevector(qc)
```

Graph
```python
import networkx as nx
g = nx.random_regular_graph(3,8)
for k,l in g.edges():
  g[k][l]['weight'] = 1.0
nx.draw_networkx(g)
```

Cost Hamiltonian from qiskit quantum gates
```python
def cost_ham(graph):
    qc = QuantumCircuit(graph.number_of_nodes())
    for edge in graph.edges():
      qc.cp(-2*3.1415,edge[0],edge[1])
      qc.p(3.1415, edge[0])
      qc.p(3.1415, edge[1])
    backend = Aer.get_backend('unitary_simulator')  
    job = backend.run(qc)
    result = job.result()
    return result.get_unitary(qc, decimals=4)
```
Expected value of Cost Function
```python
import numpy as np
def cost_expected(graph, ket):
  h = np.array(cost_ham(graph))
  return np.conj(ket).dot(h.dot(ket)).real

cost_expected(g, np.array(QAOA(g, [1,2,1.8,2.9])))
```
Optimizer
```python
from scipy.optimize import minimize

par_qaoa = lambda par: QAOA(g, par)
par_cost = lambda state: cost_expected(g, np.array(state))

def cost_fun(par):
  state = par_qaoa(par)
  return par_cost(state)

p = [1.3,2.8, 1.0,2.0, 2.3,1.7, 0.2,0.5]
res = minimize(cost_fun, p[:2], method='SLSQP', options={})
```

