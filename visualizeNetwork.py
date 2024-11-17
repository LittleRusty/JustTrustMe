import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import config

# Build web visualization.  Lines between players represent mutually trusting relationships.
# Shading of the nodes from red to green denotes success of finding players to matchmake with each pass. Red = low, Green = high
def visualizeNetworkGraph(mmplayersDict):
    G = nx.Graph()
    labelsDict = {}
    percentMatchFound = [0] * 50
    for playerID in mmplayersDict:
        G.add_node(playerID)
    for playerID, player in mmplayersDict.items(): # add all trusted connections
        labelsDict[playerID] = player.PlayerType[0]
        percentMatchFound[playerID] = int(player.MatchesFound/config.simSettings['mmIterations'] * 100)
        for tps in player.Trust:
            G.add_edge(player.id, tps)
    for playerID, player in mmplayersDict.items(): # remove connections that aren't mutually trusted
        for dps in player.Distrust:
            try:
                G.remove_edge(dps, player.id)
            except:
                pass
   
    norm = mpl.colors.Normalize(vmin=0, vmax=100)
    sm = plt.cm.ScalarMappable(cmap=plt.cm.RdYlGn, norm=norm)
    sm.set_array([])
    ax = plt.gca()
    ax.set_axis_off()
    nx.draw_networkx(G, labels=labelsDict, with_labels=True, node_color=percentMatchFound, cmap=plt.cm.RdYlGn)
    plt.colorbar(sm, ticks=np.linspace(0,100,3), ax=ax)
    plt.show()