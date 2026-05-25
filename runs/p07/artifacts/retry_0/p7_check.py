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


analysis = simulator.operating_point()
for node in analysis.nodes.values(): 
    print(f"{str(node)}\t{float(analysis[str(node)][0]):.6f}")
vin_name = ""
for element in circuit.elements:
    for pin in element.pins:
        if "vin" in str(pin.node).lower() and element.name.lower().startswith("v"):
            vin_name = element.name
            break

circuit.element(vin_name).dc_value = "5"

simulator2 = circuit.simulator()
analysis2 = simulator2.operating_point()


node = 'vout'

has_node = False
# find any node with "vout"
for element in circuit.elements:
    # get pins
    for pin in element.pins:
        if "vout" == str(pin.node).lower():
            has_node = True
            break
if has_node == False:
    for element in circuit.elements:
        for pin in element.pins:
            if "vout" in str(pin.node).lower():
                node = str(pin.node)
                break

vout2 = float(analysis2[node][0])

circuit.element(vin_name).dc_value = "0"

simulator3 = circuit.simulator()
analysis3 = simulator3.operating_point()

vout3 = float(analysis3[node][0])

import sys
if vout2 <= 2.5 and vout3 >= 2.5 and vout3 - vout2 >= 1.0:
    print("The circuit functions correctly.\n")
    sys.exit(0)

print("The circuit does not function correctly.\n"
    "It can not invert the input voltage.\n"
    f"When input is 5V, output is {vout2:.2f}V.\n"
    f"When input is 0V, output is {vout3:.2f}V.\n"
    "Please fix the wrong operating point.\n")

sys.exit(2)




