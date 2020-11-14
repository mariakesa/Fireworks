# Fireworks

This is a visualization plugin for visualizing clusters of neurons learned using the EnsemblePursuit algorithm (https://github.com/MouseLand/EnsemblePursuit) from activity traces that have been extracted from calcium imaging recordings using spks.npy and stat.npy from the suite2p library https://github.com/MouseLand/suite2p

Usage:

This software requires pip installed EnsemblePursuit, numpy, sklearn, vispy, pyqtgraph. Clone this repository. In the command line cd to the cloned repository folder :

python run_fireworks.py --stat <path to stat file> --spks <path to spks file> --n_ens <number of clusters> --lam <regularization parameter, try 0.01>
'

