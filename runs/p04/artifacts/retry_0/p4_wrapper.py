import math
import sys
sys.path.insert(0, "<REDACTED>")
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('circuit')

circuit.V('dd', 'VDD', circuit.gnd, 'DC 5')
circuit.V('bias', 'Vbias', circuit.gnd, 'DC 1.8')
circuit.V('in_param', 'Vin', circuit.gnd, 'DC 0.8 AC 1')
circuit.R('load', 'VDD', 'Vout', '47k')
circuit.MOSFET('p_1', 'Vout', 'Vbias', 'Vin', 'Vin', model='NMOSCG', w='50u', l='1u')
circuit.model('NMOSCG', 'NMOS', **{"level": "1", "vto": "0.7", "kp": "100u", "lambda": "0.02"})
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

