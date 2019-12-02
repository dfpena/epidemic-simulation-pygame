![STREMECOVER](http://go.pluricorp.com/websitemedia/gitlab/templatetop.svg)

# Pygame Epidemic Simulator <br>

Simulation of infection progression given a reasonably natural network of connected individuals.  [StremeCoder]([http://do.pluricorp.com/page/stremecoder](http://do.pluricorp.com/page/stremecoder) (Which is currently on sale for Developers for $10.00 using code: 4ix90v2) is used to maintain this code and generate different infection parameters, but is not required and the python source can be modified directly in the simloop function to simulate different disesases.

This simulation uses a social network generated in networkx

nx.newman_watts_strogatz_graph(nodes, k, prob) 

where

nodes = 1200

k = 20

prob = 0.1

To reduce runtime and reproduce the same population for each disease node a pickle was generated of that random starter population and run through a pygame simulation node.

The simulation takes in 

R0, infection probability, mortality rate, infection length, or infection probability if R0 is set to 0. Otherwise, infection probability is estimated from R0 algebraically. Each cycle of the simulation for each infected node connection infection and mortality are simulated by random number selection against provided probabilities.  The simulation is set to end at 365 days. To use this simulation in a montecarlo remove the pygame dependencies to eliminate the visualizations and perform your desired statistical calculation on the resulting network then repeat the process n times. 



## Demo

![Demo](https://raw.githubusercontent.com/dfpena/epidemic-simulation-pygame/master/demo.gif)

## Install

## Requirements

This simulation requires python3, pygame, networkx, and numpy 

### Pygame<br>

Runs the visualization of the node state changes

```
pip install pygame
or 
pip3 install pygame
```

### numpy<br>

To map the node network into the screen resolution space.   Refer to [SCIPY](https://www.scipy.org/install.html) 

```
conda install numpy
```



### NetworkX<br>

Generates the social network of nodes to run in the simulation

```
pip install networkx
or 
pip3 install networkx
```

## Usage

In a terminal run 

```
python episim.py
```

## License

[MIT](https://opensource.org/licenses/MIT)








