# boot.py
# Runs once at startup, before main.py.

import gc
gc.collect()
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

print('boot: ready')
