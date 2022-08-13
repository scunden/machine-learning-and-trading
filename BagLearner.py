#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import random
from copy import deepcopy
from scipy import stats

class BagLearner():
    def __init__(self, learner, kwargs, bags, boost, verbose):
        self.bags = bags
        self.learners = [learner(**kwargs) for x in range(self.bags)]
        
    def author(self):  
        return 'scunden3'
    
    def add_evidence(self, X, y):
        samples = np.array([random.choices([x for x in range(X.shape[0])], k=X.shape[0]) for bag in range(self.bags)])
        X_s  = [X[sample] for sample in samples]
        y_s = [y[sample] for sample in samples]
        for i, learner in enumerate(self.learners):
            learner.add_evidence(X_s[i], y_s[i])
    
    def query(self, observations):
        return stats.mode(np.array([learner.query(observations) for learner in self.learners]))[0][0] 

