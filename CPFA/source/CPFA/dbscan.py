# dbscan_script.py
import sys
import json
from sklearn.cluster import DBSCAN
import numpy as np

def run_dbscan(epsilon, min_samples, data):
    # Convert data to a NumPy array for scikit-learn
    X = np.array(data)
    
    # Run DBSCAN
    db = DBSCAN(eps=epsilon, min_samples=min_samples).fit(X)
    
    # Extract the cluster labels
    labels = db.labels_
    
    # # Group the points by cluster
    # clusters = {}
    # # Group the noise points separately
    # noise = []
    # for point, label in zip(data, labels):
    #     if label == -1: # Noise points are labeled -1
    #         noise.append(point)
    #         continue
    #     clusters.setdefault(label, []).append(point)
    
    # # Convert the clusters dictionary to a list of lists (ignoring noise points)
    # clustered_points = list(clusters.values())

    return labels.tolist()














# if __name__ == '__main__':
#     # Read command line arguments
#     epsilon = float(sys.argv[1])
#     num_points = int(sys.argv[2])
#     dataset = json.loads(sys.argv[3])
    
#     # Run DBSCAN
#     clusters = run_dbscan(epsilon, num_points, dataset)
    
#     # Convert clusters to JSON and print to stdout
#     print(json.dumps(clusters))
