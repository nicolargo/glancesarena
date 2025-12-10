import time
from dataclasses import asdict

from glances_plugin import CpuPlugin, NetworkPlugin

# from glances_stat import Stat
# cpu_total = Stat('%', retention=3)
# cpu_total.update(1)
# cpu_total.update(2)
# cpu_total.update(3)
# assert cpu_total.value == 3
# assert cpu_total.history == [1, 2, 3]
# assert cpu_total.mean() == 2
# assert cpu_total.max() == 3
# assert cpu_total.min() == 1
# cpu_total.update(4)
# assert cpu_total.value == 4
# assert cpu_total.history == [2, 3, 4]
# cpu_total.reset()
# assert cpu_total.mean() is None
# assert cpu_total.max() is None
# assert cpu_total.min() is None

# CPU
cpu = CpuPlugin()
cpu.update('total', 1)
cpu.update('total', 2)
cpu.update('total', 3)
print(f'{asdict(cpu):}')
# print(cpu.get_definition())
# print(cpu.get_definition('total'))
# print(cpu.get_stats())
# print(cpu.get_stats('total'))
print(cpu.get_history())
print(cpu.get_history('total'))
assert cpu.stats['total'].value == 3
assert cpu.stats['total'].mean() == 2
assert cpu.stats['total'].max() == 3
assert cpu.stats['total'].min() == 1
cpu.reset()

# NETWORK
network = NetworkPlugin()
network.stat_key = 'interface'
network.update('bytes_recv', 0, 'eth0')
time.sleep(1)
network.update('bytes_recv', 20, 'eth0')
time.sleep(1)
network.update('bytes_recv', 30, 'eth0')
# print(f'{asdict(network):}')
assert network.stats['eth0']['bytes_recv'].value == 30
assert network.stats['eth0']['bytes_recv'].max() == 30
assert network.stats['eth0']['bytes_recv'].min() == 0
time.sleep(1)
network.update('bytes_recv', 35, 'eth0')
print(f'{asdict(network):}')
assert network.stats['eth0']['bytes_recv'].value == 35
assert network.stats['eth0']['bytes_recv'].max() == 35
assert network.stats['eth0']['bytes_recv'].min() == 20
# assert network.stats['eth0']['bytes_recv_rate']['history'] == 5.0
