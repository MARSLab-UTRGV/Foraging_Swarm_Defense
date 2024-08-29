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

    return labels.tolist()

print("Python DBSCAN module imported successfully")