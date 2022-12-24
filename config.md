IMPORTANTS NOTES!!!!!!!!!!:

1. To simplified an integration process treat attribute in R in [F(n) = g(n) + r(n)], as an
   1D vector array consist osm features, example
[Building Area x WOI Building Area,
Road area x WOI Road Area,
Transmissio Area x WOI Transmission aera,
...
]
	Side note WOI is Weight of Importance, determining a cell who has threat proportional to its number 
as the most highest weight. i.e if the transmission tower cause a large harm to civiliant, if crash by
UAV, then it get the highest priority	
	If WOI is not inserted than it treats as the weight of one.

2. Do i need to implement Optimizer to find global minima?

Task to do for programming Stuff:
Modified the class with augment of Djikstra, Astar, and shortest part
Modified features of interest to include multiple tag value automatically.


file structure
using micko algo
using CAMIC algo
UPL
    PY main.py
    PY a_star.py
    FOLDER preprocessor
        MAP ATTR DOWNLOADER
            IF ATTR NOT AVAILABLE OFFLINE
                DONWLOAD FROM NOMINATIM 
            ELSE
                LOAD FROM DISK

        MAP ATTR PROCESSOR
            ATTR COMBINER AND DISSOLVER

    FOLDER postprocessor
        PATH SEARCHER
            GRAPH BUILDER
            --HEURISTIC MODELS--
            SEARCH ALGORITHM
            SPLINE ALGORITHM
        
        OPTIMIZER
            OPENMDAO
                GRAD BASED OPTIMIZER

    FOLDER AIRCRAFT MODELS
        AERODYNAMIC CALCULATION
        BALLISTIC CALCULATION
            STOCHASTIC BASE
            MDAO BASED
            

    FOLDER/CLASS/FUNCTION utils
        file_control.py


Basic Building blog for attribute

User request to process
