import math
import sys
sys.path.insert(0, "<REDACTED>")
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('circuit')

circuit.V('dd', 'VDD', circuit.gnd, 'DC 5')
circuit.V('bias', 'Vbias', circuit.gnd, 'DC 1.0')
circuit.R('load', 'VDD', 'Vout', '10k')
circuit.MOSFET('p_1', 'Vout', 'Vbias', circuit.gnd, circuit.gnd, model='NMOS', w='50u', l='1u')
circuit.model('NMOS', 'NMOS', **{"vto": "0.6", "kp": "100u", "lambda": "0.02"})
# .op
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


load_resistances = [100, 300, 500, 750, 1000]
currents = []

import PySpice.Spice.BasicElement
target_output_node = 'Vout'.lower()
for element in circuit.elements:
    if isinstance(element, PySpice.Spice.BasicElement.Resistor):
        pins = [str(node).lower() for node in element.nodes]
        if target_output_node in pins:
            resistor_name = element.name
            node1, node2 = element.nodes
            break
else:
    for element in circuit.elements:
        if isinstance(element, PySpice.Spice.BasicElement.Resistor):
            resistor_name = element.name
            node1, node2 = element.nodes
            break


resistor = circuit[resistor_name]
for r_load in load_resistances:
    resistor.resistance = r_load
    analysis = simulator.operating_point()
    if str(node2) == "0":
        current = float(analysis[str(node1)][0]) / r_load
    elif str(node1) == "0":
        current = - float(analysis[str(node2)][0]) / r_load
    else:
        current = - (float(analysis[str(node1)][0]) - float(analysis[str(node2)][0])) / r_load
    currents.append(abs(current))

for r_load, current in zip(load_resistances, currents):
    print(f"Load: {r_load}, Current: {current}")

tolerance = 1e-6

current_variations = []
for i in range(4):
    current_variations.append(abs(currents[i+1] - currents[i]))

import sys
if min(current_variations) < tolerance and min(currents) > 1e-5:
    pass
    # print("The circuit functions correctly as a constant current source within the given tolerance.")
    # sys.exit(0)
else:
    print("The circuit does not function correctly as a current source.")
    sys.exit(2)

iin_name = None
for element in circuit.elements:
    if "ref" in element.name.lower(): # and element.name.lower().startswith("v"):
        iin_name = element.name

# print("iin_name", iin_name)
iin_name = None
if iin_name is None:
    print("The circuit functions correctly as a current source within the given tolerance.")
    sys.exit(0)


circuit.element(iin_name).dc_value = "0.00155"

# print(str(circuit))
simulator = circuit.simulator()
resistor.resistance = 500
analysis = simulator.operating_point()
if str(node2) == "0":
    current = float(analysis[str(node1)][0]) / r_load
elif str(node1) == "0":
    current = - float(analysis[str(node2)][0]) / r_load
else:
    current = - (float(analysis[str(node1)][0]) - float(analysis[str(node2)][0])) / r_load

# print("current", current)
# print("currents", currents)
# print("abs(current - currents[2])", abs(current - currents[2]))
if abs(current - currents[2]) < 1e-6:
    print("The circuit does not as a current source because it cannot replicate the Iref current.")
    sys.exit(2)
else:
    print("The circuit functions correctly as a current source within the given tolerance.")
    sys.exit(0)

