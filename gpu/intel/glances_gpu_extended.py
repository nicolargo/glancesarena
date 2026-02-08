import os
import re
import glob
import time
from collections import defaultdict
intel_fdinfo_available = True

class Plugin:

    def _get_intel_fdinfo_utilization(self):
        """Get Intel GPU utilization from /proc/*/fdinfo/*.
        
        Returns dict of {device_id: utilization_percent}
        """
        current_time = time.time()
        
        # Find all processes with GPU access
        pci_to_cycles = defaultdict(lambda: defaultdict(int))
        
        for proc_dir in glob.glob('/proc/[0-9]*'):
            try:
                pid = int(os.path.basename(proc_dir))
                fdinfo_dir = os.path.join(proc_dir, 'fdinfo')
                
                if not os.path.exists(fdinfo_dir):
                    continue
                
                for fdinfo_file in os.listdir(fdinfo_dir):
                    fdinfo_path = os.path.join(fdinfo_dir, fdinfo_file)
                    
                    try:
                        with open(fdinfo_path, 'r') as f:
                            content = f.read()
                        
                        # Check for Intel GPU
                        pci_match = re.search(r'drm-pdev:\s*([0-9a-f:\.]+)', content)
                        if not pci_match or 'drm-cycles-' not in content:
                            continue
                        
                        pci_addr = pci_match.group(1).lower()
                        
                        # Only process Intel GPUs we know about
                        if pci_addr not in self.intel_pci_to_id:
                            continue
                        
                        # Parse engine cycles
                        cycles_pattern = re.compile(r'drm-cycles-(\w+):\s+(\d+)')
                        total_cycles_pattern = re.compile(r'drm-total-cycles-(\w+):\s+(\d+)')
                        
                        for match in cycles_pattern.finditer(content):
                            engine = match.group(1)
                            value = int(match.group(2))
                            pci_to_cycles[pci_addr][engine + '_cycles'] += value
                        
                        for match in total_cycles_pattern.finditer(content):
                            engine = match.group(1)
                            value = int(match.group(2))
                            key = engine + '_total'
                            pci_to_cycles[pci_addr][key] = max(pci_to_cycles[pci_addr][key], value)
                    
                    except (OSError, PermissionError):
                        continue
            except (ValueError, OSError, PermissionError):
                continue
        
        # Calculate utilization
        utilization = {}
        
        for pci_addr, cycles in pci_to_cycles.items():
            device_id = self.intel_pci_to_id.get(pci_addr)
            if device_id is None:
                continue
            
            # Check if we have a previous measurement
            if pci_addr not in self.intel_fdinfo_last:
                # First measurement - store baseline
                self.intel_fdinfo_last[pci_addr] = {'cycles': dict(cycles), 'time': current_time}
                utilization[device_id] = 0.0
                continue
            
            last = self.intel_fdinfo_last[pci_addr]
            time_delta = current_time - last['time']
            
            if time_delta < 0.1:
                utilization[device_id] = 0.0
                continue
            
            # Calculate max utilization across all engines
            max_util = 0.0
            engines = set(k.replace('_cycles', '').replace('_total', '') for k in cycles.keys())
            
            for engine in engines:
                curr_cycles = cycles.get(engine + '_cycles', 0)
                curr_total = cycles.get(engine + '_total', 0)
                prev_cycles = last['cycles'].get(engine + '_cycles', 0)
                prev_total = last['cycles'].get(engine + '_total', 0)
                
                delta_cycles = curr_cycles - prev_cycles
                delta_total = curr_total - prev_total
                
                if delta_total > 0:
                    engine_util = (delta_cycles / delta_total) * 100.0
                    max_util = max(max_util, engine_util)
            
            utilization[device_id] = min(100.0, max(0.0, max_util))
            
            # Update last measurement
            self.intel_fdinfo_last[pci_addr] = {'cycles': dict(cycles), 'time': current_time}
        
        return utilization


p = Plugin()
print(p._get_intel_fdinfo_utilization())

