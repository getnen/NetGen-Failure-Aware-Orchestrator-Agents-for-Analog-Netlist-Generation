import math
import sys
sys.path.insert(0, "<REDACTED>")
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('circuit')

circuit.V('dd', 'VDD', circuit.gnd, 'DC 5')
circuit.V('in_param', 'Vin', circuit.gnd, 'DC 0')
circuit.MOSFET('p1', 'Vout', 'Vin', 'VDD', 'VDD', model='PMOS', l='1u', w='10u')
circuit.MOSFET('n1', 'Vout', 'Vin', circuit.gnd, circuit.gnd, model='NMOS', l='1u', w='10u')
circuit.model('NMOS', 'NMOS', **{"level": "1", "vto": "0.7", "kp": "120u", "lambda": "0.02"})
circuit.model('PMOS', 'PMOS', **{"level": "1", "vto": "-0.7", "kp": "50u", "lambda": "0.02"})
# .dc Vin 0 5 0.1
# .end

simulator = circuit.simulator()

try:
    analysis = simulator.operating_point()
    fopen = open("<REDACTED>", "w")
    for node in analysis.nodes.values():
        fopen.write(f"{str(node)}\t{float(analysis[str(node)][0]):.6f}\n")
    fopen.close()
except Exception as e:
    print("Analysis failed due to an error:")
    print(str(e))

