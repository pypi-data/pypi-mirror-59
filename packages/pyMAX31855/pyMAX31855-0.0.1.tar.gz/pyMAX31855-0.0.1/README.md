# pyMAX31855

This module is a Python3 based interface to a max31855 with k-type thermocouple.

It was tested on a raspberry pi 0 with [adafruit breakout board](https://www.adafruit.com/product/269).

The python module from adafruit was apparently broken.

Uses NIST correction for k-type thermocouple.

# A simple usage example
Connect the max31855 to [spi0.0](https://pinout.xyz/pinout/spi#)
and run this example code.
```
from pprint import pprint as pp
import time
from max31855 import max31855
obj_ = max31855(bus=0,device=0)
try:
    while True:
        pp(obj_.read_value())
        time.sleep(5)
except KeyboardInterrupt:
    pass
```

This will print a value dictionary (manually commented)

```
{'fault': None,#<-- the fault status
 'hexdata': '01781820',#<-- the sensors datagram
 't_rj': 24.125,#<-- cold junction temperature
 't_tc': 23.5,#<-- thermocouple temperature
 't_tc_lin': 23.471984356580563,#<-- linearized thermocouple temperature
 'u_rj': 0.9648033405278587,#<-- junction voltage
 'u_tc': -0.0257975}#<-- thermocouple voltage
```

