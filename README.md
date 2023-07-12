# CATVehicle-REU-Dynamic-Encryption
Generate dynamic codes using camera data from vehicles

This repository contains various scripts used to
experiment with obtaining random data from two vehicles
using cameras looking at each other. The general goal
is to observe when vehicles in adjacent lanes of traffic
pass by the two vehicles of interest, and record the 
time of each event. The two vehicles can then use this along
with fuzzy vault cryptography technique to ensure they can
communicate privately, as they leverage data available only
to the two vehicles that seek to communicate, and not to 
adversaries that intend to eavesdrop on their communications.
