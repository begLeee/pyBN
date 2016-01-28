"""
*******************
Bayesian Estimation
Parameter Learning
*******************

"""
from __future__ import division
__author__ = """Nicholas Cullen <ncullen.th@dartmouth.edu>"""

import numpy as np


def bayes_estimator(bn, data, equiv_sample=None):
	"""
	Bayesian Estimation method of parameter learning.
	This method proceeds by either 1) assuming a uniform prior
	over the parameters based on the Dirichlet distribution
	with an equivalent sample size = *sample_size*, or
	2) assuming a prior as specified by the user with the 
	*prior_dict* argument. The prior distribution is then
	updated from observations in the data based on the
	Multinomial distribution - for which the Dirichlet
	is a "conjugate prior."

	Note that the Bayesian and MLE estimators essentially converge
	to the same set of values as the size of the dataset increases.

	Also note that, unlike the structure learning algorithms, the
	parameter learning functions REQUIRE a passed-in BayesNet object
	because there MUST be some pre-determined structure for which
	we can actually learn the parameters. You can't learn parameters
	without structure - so structure must always be there first!

	Arguments
	---------
	*data* : a nested numpy array
		Data from which to learn parameters

	*sample_size* : an integer
		The "equivalent sample size" (see function summary)

	*prior_dict* : a dictionary, where key = random variable
		and for each key the value is another dictionary where
		key = an instantiation for the random variable and the
		value is its FREQUENCY (an integer value, NOT its relative
		proportion/probability).
	
	Returns
	-------
	None

	Effects
	-------
	- modifies/sets bn.data to the learned parameters

	Notes
	-----

	"""
	if equiv_sample is None:
		equiv_sample = len(data)

	obs_dict = dict.fromkeys(bn.nodes())
	# set empty conditional probability table for each RV
	for rv in bn.nodes():
		# get number of values in the CPT = product of scope vars' cardinalities
		p_idx = int(np.prod([bn.card(p) for p in bn.parents(rv)])*bn.card(rv))
		bn.F[rv]['cpt'] = [equiv_sample/p_idx]*p_idx
	
	# loop through each row of data
	for row in data:

		# loop through each RV and increment its observed parent-self value
		for rv in bn.nodes():
			obs_dict[rv] = row[rv]

			value_indices = np.empty(bn.scope_size(rv))
			value_indices[0] = bn.value_idx(rv, obs_dict[rv])

			strides = np.empty(bn.scope_size(rv))
			strides[0] = 1

			for i,p in enumerate(bn.parents(rv)):
				value_indices[i+1] = bn.value_idx(p,obs_dict[p])
				strides[i+1] = bn.stride(rv, p)
			
			offset = int(np.sum(value_indices*strides))
			bn.F[rv]['cpt'][offset] += 1
	
	for rv in bn.nodes():
		for val_idx in xrange(len(bn.F[rv]['cpt'])):
			bn.F[rv]['cpt'][val_idx] /= len(data)*2












