import time
from dataclasses import asdict

from glances_plugin import CpuPlugin, NetworkPlugin

# CPU
cpu = CpuPlugin()
cpu.update_field('total', 1)
cpu.update_field('total', 2)
cpu.update_field('total', 3)
cpu.update_field('system', 4)
cpu.update_field('system', 5)
cpu.update_field('system', 6)
print(asdict(cpu))
# print(cpu.name)
# print(cpu.description)
# print(cpu.get_definition())
# print(cpu.get_definition('total'))
# print(cpu.get_stats())
# print(cpu.get_stats('total'))
# print(cpu.get_history())
# print(cpu.get_history('total'))
assert cpu.stats['total'].value == 3
assert cpu.stats['total'].mean() == 2
assert cpu.stats['total'].max() == 3
assert cpu.stats['total'].min() == 1
cpu.reset()

# NETWORK
network = NetworkPlugin()
network.stat_key = 'interface'
network.update_field('bytes_recv', 0, 'eth0')
time.sleep(1)
network.update_field('bytes_recv', 20, 'eth0')
time.sleep(1)
network.update_field('bytes_recv', 30, 'eth0')
# print(asdict(network))
assert network.stats['eth0']['bytes_recv'].value == 30
assert network.stats['eth0']['bytes_recv'].max() == 30
assert network.stats['eth0']['bytes_recv'].min() == 0
time.sleep(1)
network.update_field('bytes_recv', 35, 'eth0')
print(f'{asdict(network):}')
assert network.stats['eth0']['bytes_recv'].value == 35
assert network.stats['eth0']['bytes_recv'].max() == 35
assert network.stats['eth0']['bytes_recv'].min() == 20
assert network.stats['eth0']['bytes_recv_rate'].history[-1][1] == 5.0
