import math
import sys
sys.path.insert(0, "<REDACTED>")
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('circuit')

circuit.V('dd', 'VDD', circuit.gnd, 'DC 5')
circuit.V('in_param', 'Vin', circuit.gnd, 'DC 1.5 AC 1')
circuit.R('p_1', 'VDD', 'n1', '47k')
circuit.R('p_2', 'VDD', 'n2', '47k')
circuit.R('p_3', 'VDD', 'Vout', '47k')
circuit.MOSFET('p_1_2', 'n1', 'Vin', circuit.gnd, circuit.gnd, model='NMOS', w='50u', l='1u')
circuit.MOSFET('p_2_2', 'n2', 'n1', circuit.gnd, circuit.gnd, model='NMOS', w='50u', l='1u')
circuit.MOSFET('p_3_2', 'Vout', 'n2', circuit.gnd, circuit.gnd, model='NMOS', w='50u', l='1u')
circuit.model('NMOS', 'NMOS', **{"level": "1", "vto": "1.2", "kp": "33u", "lambda": "0.02"})
# .op
# .ac dec 20 1 1e9
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

