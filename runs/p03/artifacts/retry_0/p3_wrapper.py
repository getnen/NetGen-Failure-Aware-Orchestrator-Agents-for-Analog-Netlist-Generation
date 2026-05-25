import math
import sys
sys.path.insert(0, "<REDACTED>")
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('circuit')

circuit.V('dd', 'VDD', circuit.gnd, 'DC 5')
circuit.V('in_param', 'Vin', circuit.gnd, 'DC 2.5 AC 1')
circuit.MOSFET('p_1', 'VDD', 'Vin', 'Vout', 'Vout', model='NMOS1', w='50u', l='1u')
circuit.R('load', 'Vout', circuit.gnd, '10k')
circuit.model('NMOS1', 'NMOS', **{"level": "1", "vto": "0.7", "kp": "100u"})
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

