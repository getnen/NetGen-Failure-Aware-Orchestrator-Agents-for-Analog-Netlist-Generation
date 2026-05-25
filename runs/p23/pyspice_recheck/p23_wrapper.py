import math
import sys
sys.path.insert(0, "<REDACTED>")
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('circuit')

circuit.V('dd', 'VDD', circuit.gnd, 'DC 5')
circuit.V('ref', 'Vref', circuit.gnd, 'DC 2.5')
circuit.C('ref_2', 'Vref', circuit.gnd, '10u')
circuit.C('wien1', 'Vout', 'Nwien', '10n')
circuit.R('wien1_2', 'Nwien', 'Vinp', '10k')
circuit.R('wien2', 'Vinp', 'Vref', '10k')
circuit.C('wien2_2', 'Vinp', 'Vref', '10n')
circuit.R('f', 'Vout', 'Vinn', '33k')
circuit.R('g', 'Vinn', 'Vref', '10k')
circuit.MOSFET('e_1', 'Ndp', 'Vinn', 'Ntail', 'Ntail', model='NMOS', w='500u', l='1u')
circuit.MOSFET('e_2', 'Ndn', 'Vinp', 'Ntail', 'Ntail', model='NMOS', w='500u', l='1u')
circuit.R('ld1', 'VDD', 'Ndp', '18k')
circuit.R('ld2', 'VDD', 'Ndn', '18k')
circuit.I('tail', 'Ntail', circuit.gnd, 'DC 260u')
circuit.MOSFET('e_3', 'Ndrv', 'Ndn', 'VDD', 'VDD', model='PMOS', w='900u', l='1u')
circuit.MOSFET('e_4', 'Ndrv', 'Ndn', circuit.gnd, circuit.gnd, model='NMOS', w='320u', l='1u')
circuit.MOSFET('e_5', 'Vout', 'Ndrv', 'VDD', 'VDD', model='PMOS', w='1600u', l='1u')
circuit.MOSFET('e_6', 'Vout', 'Ndrv', circuit.gnd, circuit.gnd, model='NMOS', w='520u', l='1u')
circuit.R('b1', 'Vout', 'Vinp', '3.3Meg')
circuit.R('b2', 'Vinp', 'Vref', '3.3Meg')
circuit.R('so', 'Vout', 'Vout_s', '47')
circuit.C('load', 'Vout_s', circuit.gnd, '20p')
circuit.C('bw', 'Ndn', 'Vout', '2p')
circuit.model('NMOS', 'NMOS', **{"level": "1", "vto": "0.75", "kp": "220u", "lambda": "0.025", "cgso": "1p", "cgdo": "1p"})
circuit.model('PMOS', 'PMOS', **{"level": "1", "vto": "-0.75", "kp": "110u", "lambda": "0.025", "cgso": "1p", "cgdo": "1p"})
# .ic V(Vinp)=2.55 V(Vinn)=2.45 V(Vout)=2.6 V(Vout_s)=2.6 V(Ndp)=3.0 V(Ndn)=3.0 V(Ntail)=0.85 V(Ndrv)=2.4
# .tran 1u 5m uic
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

