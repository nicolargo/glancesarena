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
assert cpu.stats['total'].value == 3
assert cpu.stats['total'].mean() == 2
assert cpu.stats['total'].max() == 3
assert cpu.stats['total'].min() == 1
cpu.reset()

# NETWORK
network = NetworkPlugin(retention=3)
network.stat_key = 'interface'
network.update('bytes_recv', 1, 'eth0')
network.update('bytes_recv', 2, 'eth0')
network.update('bytes_recv', 3, 'eth0')
print(f'{asdict(network):}')
assert network.stats['eth0']['bytes_recv'].value == 3
assert network.stats['eth0']['bytes_recv'].mean() == 2
assert network.stats['eth0']['bytes_recv'].max() == 3
assert network.stats['eth0']['bytes_recv'].min() == 1
network.update('bytes_recv', 4, 'eth0')
print(f'{asdict(network):}')
assert network.stats['eth0']['bytes_recv'].value == 4
assert network.stats['eth0']['bytes_recv'].max() == 4
assert network.stats['eth0']['bytes_recv'].min() == 2
