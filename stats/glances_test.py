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
cpu.reset()

# NETWORK
network = NetworkPlugin()
network.stat_key = 'interface'
network.update_field('bytes_recv', 0, 'eth0')
time.sleep(0.5)
network.update_field('bytes_recv', 20, 'eth0')
time.sleep(0.5)
network.update_field('bytes_recv', 30, 'eth0')
time.sleep(0.5)
network.update_field('bytes_recv', 35, 'eth0')
time.sleep(0.5)
network.update_field('bytes_recv', 60, 'eth0')
time.sleep(0.5)
network.update_field('bytes_recv', 70, 'eth0')
print(f'{asdict(network):}')
assert network.stats['eth0']['bytes_recv'].value == 70
print(network.stats['eth0']['bytes_recv'].min(period_seconds=1))
print(network.stats['eth0']['bytes_recv'].max(period_seconds=1))
print(network.stats['eth0']['bytes_recv'].mean(period_seconds=1))
print(network.stats['eth0']['bytes_recv'].mean())
