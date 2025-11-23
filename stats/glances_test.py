from dataclasses import asdict

from glances_plugin import Plugin
from glances_stat import Stat

# CPU
cpu_total = Stat('%', retention=3)
cpu_total.update(1)
cpu_total.update(2)
cpu_total.update(3)
print(f'{asdict(cpu_total):}')
assert cpu_total.value == 3
assert cpu_total.history == [1, 2, 3]
assert cpu_total.mean() == 2
assert cpu_total.max() == 3
assert cpu_total.min() == 1
cpu_total.update(4)
assert cpu_total.value == 4
assert cpu_total.history == [2, 3, 4]
cpu_total.reset()
assert cpu_total.mean() is None
assert cpu_total.max() is None
assert cpu_total.min() is None

cpu = Plugin('cpu')
cpu.update('total', 1)
cpu.update('total', 2)
cpu.update('total', 3)
print(f'{asdict(cpu):}')
cpu.reset()
print(f'{asdict(cpu):}')

# NETWORK
# Todo...
