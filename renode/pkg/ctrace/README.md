Ctrace 
controller:
choose: 100MHz with 16 bits counter

time stamp is 64 bits and calculates by increase 1 in first 32 bits after timer counter reach limitation.
in this case -> max time stamp = (48bits) (16 bits) * 10 ns 

buffer:


Python:
timestamp = start_time + time stamp from controller