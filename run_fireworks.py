import argparse
from preprocess import preprocess
from EnsemblePursuit.EnsemblePursuit import EnsemblePursuit
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
import vispy
from fireworks_viz import MainWindow, Canvas

'''
python run_fireworks.py --stat C:/Users/koester_lab/Documents/Maria/CarsenData/stat.npy --spks C:/Users/koester_lab/Documents/Maria/CarsenData/spks.npy --n_ens 3 --lam 0.01
'''

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Read in data, fit ensemble pursuit, visualize clusters.')
    parser.add_argument('--stat', help='Path to stat.npy file')
    parser.add_argument('--spks', help='Path to spks.npy file')
    parser.add_argument('--n_ens', help='Number of ensembles to fit.')
    parser.add_argument('--lam', help='Ensemble pursuit regularization parameter')
    args = parser.parse_args()
    spks=np.load(args.spks)
    ep=EnsemblePursuit(n_components=int(args.n_ens),lam=float(args.lam),n_kmeans=int(args.n_ens))
    U=ep.fit(spks.T).weights
    spks_,pos=preprocess(args.stat,args.spks)
    #visualization
    ens_n=0
    canvas = Canvas(ens_n,spks_,pos,U)
    vispy.use('PyQt5')
    w = MainWindow(canvas)
    w.show()
    vispy.app.run()
