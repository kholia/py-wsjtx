A python module to interpret and create WSJT-X UDP packets

Developed and tested with Python >= 3.6

Sample programs for:
  * Setting the WSJT-X Grid Square from an external GPS
  * Coloring callsigns in WSJT-X based on N1MM Logger+ dupe and multiplier status
  * JTAlert-X, N1MM Logger+, WSJT-X packet exchange
  
  
Example screen display for colorized callsigns, showing a new country multiplier in red:

<img src="https://github.com/bmo/py-wsjtx/raw/master/images/colorized_wsjtx.PNG" height="400">

Example screen display for N1MM Logger+, WSJT-X, JTAlert-X in simultaneous use with wsjtx-packet-exchanger.py

<img src="https://github.com/bmo/py-wsjtx/raw/master/images/packet_exchange.PNG" height="400">

Usage:

```
C:\Users\user\Desktop>python3 wsjtx_plugin.py
> Itone data (79 tones, FT8): 3 1 4 0 6 5 2 0 0 0 0 0 0 0 0 1 1 4 1 7 5 4 4 4 7 1 1 2 0 5 2 3 3 1 7 3 3 1 4 0 6 5 2 0 1 7 6 6 4 7 5 0 6 6 6 0 2 2 4 5 5 3 6 1 5 6 4 0 6 3 6 6 3 1 4 0 6 5 2
CQ VU3CER MK69
> Time: 4:25:45
> Itone data (105 tones, FT4): 3 1 4 0 6 5 2 0 0 0 0 0 0 0 0 1 1 4 1 7 5 4 4 4 7 1 1 2 0 5 2 3 3 1 7 3 3 1 4 0 6 5 2 0 1 7 6 6 4 7 5 0 6 6 6 0 2 2 4 5 5 3 6 1 5 6 4 0 6 3 6 6 3 1 4 0 6 5 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
CQ VU3CER MK69
> Time: 4:25:54
> Itone data (105 tones, FT4): 3 1 4 0 6 5 2 0 0 0 0 0 0 0 0 1 1 4 1 7 5 4 4 4 7 1 1 2 0 5 2 3 3 1 7 3 3 1 4 0 6 5 2 0 1 7 6 6 4 7 5 0 6 6 6 0 2 2 4 5 5 3 6 1 5 6 4 0 6 3 6 6 3 1 4 0 6 5 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
CQ VU3CER MK69
> Time: 4:25:54
> Itone data (105 tones, FT4): 0 1 3 2 1 0 3 3 1 1 2 3 3 0 3 1 3 1 0 2 3 3 2 2 3 2 2 0 3 3 1 1 2 1 0 2 3 0 0 2 3 1 2 1 0 3 0 1 2 3 3 0 0 2 2 2 3 2 0 1 0 2 0 0 0 1 2 3 1 0 0 1 3 1 1 2 3 0 1 1 3 3 1 1 1 2 2 0 1 3 3 3 3 3 1 0 0 2 3 3 2 0 1 0 0
CQ VU3CER MK68
> Time: 4:25:54
> Itone data (79 tones, FT8): 3 1 4 0 6 5 2 0 0 0 0 0 0 0 0 1 1 4 1 7 5 4 4 4 7 1 1 2 0 5 2 0 2 7 5 0 3 1 4 0 6 5 2 6 4 7 2 6 5 1 7 5 5 7 0 2 0 7 7 5 3 2 2 3 4 1 5 1 0 2 0 0 3 1 4 0 6 5 2
CQ VU3CER MK68
> Time: 4:28:15
> Itone data (79 tones, FT8): 3 1 4 0 6 5 2 0 0 0 0 0 0 0 0 1 1 4 1 7 5 4 4 4 7 1 1 2 0 5 2 0 2 7 5 0 3 1 4 0 6 5 2 6 4 7 2 6 5 1 7 5 5 7 0 2 0 7 7 5 3 2 2 3 4 1 5 1 0 2 0 0 3 1 4 0 6 5 2
CQ VU3CER MK68
> Time: 4:28:45
> Itone data (79 tones, FT8): 3 1 4 0 6 5 2 0 0 0 0 0 0 0 0 1 1 4 1 7 5 4 4 4 7 1 1 2 0 5 2 0 2 7 5 0 3 1 4 0 6 5 2 6 4 7 2 6 5 1 7 5 5 7 0 2 0 7 7 5 3 2 2 3 4 1 5 1 0 2 0 0 3 1 4 0 6 5 2
CQ VU3CER MK68
```
