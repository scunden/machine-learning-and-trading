#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import random
from copy import deepcopy

class RTLearner():
    def __init__(self, leaf_size=1, verbose=False, tree=None):
        self.tree = deepcopy(tree)
        self.leaf_size = leaf_size
        self.verbose = verbose
        
    def author(self):  
        return 'scunden3'
        
    def get_feature(self, X, y):
        return random.randint(0,X.shape[1]-1)
    
    def get_starting_dim(self, left_tree):
        if left_tree.ndim == 1:
            return 2
        elif left_tree.ndim > 1:
            return left_tree.shape[0] + 1
    
    def build_tree(self, X, y):
        leaf = np.array([-1, np.mean(y), np.nan, np.nan])
        
        if X.shape[0] < self.leaf_size:
            return leaf
        
        elif np.all(y == y[0]):
            return leaf
        
        elif np.all(X == X[0,:]):
            return leaf
        
        else:
            feature = self.get_feature(X, y)
            split_val = np.median(X[:, feature])
            subset = X[:, feature] <= split_val
            
            if np.all(subset) or np.all(~subset):
                return leaf
            
            left_tree = self.build_tree(X[X[:, feature] <= split_val], y[X[:, feature] <= split_val])
            right_tree = self.build_tree(X[X[:, feature] > split_val], y[X[:, feature] > split_val])
            
            root = np.array([feature, split_val, 1, self.get_starting_dim(left_tree)])
                        
            return np.vstack((root, left_tree, right_tree))
    
    def add_evidence(self, X, y):
        new_tree = self.build_tree(X,y)
        
        if self.tree:
            self.tree = np.vstack(self.tree, new_tree) 
        else:
            self.tree = new_tree
    
    def search(self, observation, row=0):
        split_val = self.tree[row, 1]
        feature = int(self.tree[row, 0])
        
        if feature == -1:
            return split_val
        elif observation[feature] <= split_val:
            return self.search(observation, row + int(self.tree[row, 2]))
        else:
            return self.search(observation, row + int(self.tree[row, 3]))
        
    def query(self, observations):
        return np.apply_along_axis(self.search, 1, observations)    

