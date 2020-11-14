# Fireworks

This is a visualization plugin for visualizing clusters of neurons learned using the EnsemblePursuit algorithm (https://github.com/MouseLand/EnsemblePursuit) from activity traces that have been extracted from calcium imaging recordings using spks.npy and stat.npy from the suite2p library https://github.com/MouseLand/suite2p

Usage:

This software requires pip installed EnsemblePursuit, numpy, sklearn, vispy, pyqtgraph. Clone this repository. In the command line cd to the cloned repository folder and run:

python run_fireworks.py --stat <path to stat file> --spks <path to spks file> --n_ens <number of clusters> --lam <regularization parameter, try 0.01>
  
An example file from mouse V1 viewing sparse noise stimuli can be found here: 

https://figshare.com/articles/dataset/Recording_of_19_000_neurons_across_mouse_visual_cortex_during_sparse_noise_stimuli/9505250

This project got into top 20 in the AlgoExpert software engineering competition and a video about using the program and the algorithm can be found here: 


[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/j_tgqfGCw_U/0.jpg)](https://www.youtube.com/watch?v=j_tgqfGCw_U)

