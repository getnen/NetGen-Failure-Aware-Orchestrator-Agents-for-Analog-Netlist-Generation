import math
import sys
sys.path.insert(0, "<REDACTED>")
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('circuit')

circuit.V('dd', 'VDD', circuit.gnd, 'DC 5')
circuit.V('in_param', 'Vin', circuit.gnd, 'DC 1.2 AC 1')
circuit.V('bias', 'Vbias', circuit.gnd, 'DC 2.5')
circuit.R('load', 'VDD', 'Vout', '10k')
circuit.MOSFET('p_1', 'Ncas', 'Vin', circuit.gnd, circuit.gnd, model='NMOS', w='50u', l='1u')
circuit.MOSFET('p_2', 'Vout', 'Vbias', 'Ncas', 'Ncas', model='NMOS', w='50u', l='1u')
circuit.model('NMOS', 'NMOS', **{"level": "1", "vto": "0.7", "kp": "100u", "lambda": "0.02"})
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

