import random
import numpy as np
from collections import Counter, defaultdict

"""
We design a mechanism to encourage students to participate on Slack
Students are incentivized to participate using (real) points

The mechanism posts an open-ended discussion question. Each student
must write a response in order to get points and can upvote 3 responses at most.

1. students get bonus points if their response has the highest number of upvotes
2. students get points if they upvote (one of the) most upvoted responses

Note that the number of upvotes each response receives is not shown to students

==========================================

We model the problem as follows:
1. Each response has a "response quality" value > 0
2. Each student decides to upvote a response as a function of its quality
    - randomly pick one
    - pick response proportional to quality
    - pick response proportional to superlinear function of quality
    - pick response heuristically (students are going to read all posts; time constraint)
    - a combination of all 4
3. Each student particpates (i.e write response) with a participation probability

Metrics to measure truthful behaviour
1. correlation between response quality and number of upvotes
2. number of upvotes distribution (most will recv. few or none..)
==========================================

Our experiments evaluate how overall contribution depends on
response quality and the criterion that students to upvote responses

> Show that the mechanism works as intended, either using a
  theoretical framework, or through simulations. In both cases, make any
  reasonable assumptions about individual behavior and decision making.

"""
def get_distribution(c):
    x, p = map(np.array, zip(*sorted(c.items())))
    p = p.astype(float)/np.sum(p)
    return x,p

def run(num_students, participat_prob, upvote_prob, get_quality, select_response, add_noise=False, noise_sd=0.1, unif_p=0.2):

    def add_noise(x):
        if random.random() < unif_p: return random.random()
        return x
        # x_ = x + np.random.normal(scale=noise_sd)
        # return min(1, max(0, x_))

    rid_upvote_map = {}
    rid_qual_map = {}

    # add responses
    for rid in xrange(num_students):
        if random.random() < participat_prob:
            rid_qual_map[rid] = get_quality()
            rid_upvote_map[rid] = 0

    rid_qual_noisy_map = {k:add_noise(v) for k,v in rid_qual_map.items()}
    xk, pk = get_distribution(rid_qual_noisy_map if add_noise else rid_qual_map)

    # upvotes
    for student in range(num_students):
        if random.random() < upvote_prob:
            for _ in xrange(3):
                selected = select_response(xk, pk)
                rid_upvote_map[selected] += 1

    xk2, pk2 = get_distribution(rid_upvote_map)

    qual_upvotes = [(rid_qual_map[k], rid_upvote_map[k]) for k in rid_qual_map]


    return {
        'quality': rid_qual_map,
        'upvotes': rid_upvote_map,
        'upvotes_dist': (xk2,pk2),
        'data': map(np.array, zip(*sorted(qual_upvotes)))
    }

# response quality distributions

def uniform_response_quality():
    return np.random.uniform()

def left_skewed_response_quality():
    return np.random.beta(5,3)

# upvote mechanisms

def uniform_upvote_response(xk, pk):
    return random.choice(xk)

def quality_upvote_response(xk, pk):
    return np.random.choice(xk, p=pk)

def heuristic_upvote_response(xk, pk, budget=0.05):
    n = int(round(budget*len(xk)))
    idx = np.random.choice(np.array(range(len(xk))), size=n)
    sub_xk, sub_pk = xk[idx], pk[idx]
    sub_pk = sub_pk.astype(float)/np.sum(sub_pk)
    return quality_upvote_response(sub_xk, sub_pk)

# misc

def get_zero_inflated_uniform_response_quality(p):
    def f():
        if random.random() < p: return 0
        return uniform_response_quality()
    return f

def get_zero_inflated_left_skewed_response_quality(p):
    def f():
        if random.random() < p: return 0
        return left_skewed_response_quality(mean, sd)
    return f

