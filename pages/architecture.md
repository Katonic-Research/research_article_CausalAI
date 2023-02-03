is passed as a list.

The procedure for generating data from this SEM is to traverse a topologically sorted order of variables in the corresponding causal graph and sample data– first sample the values of A, since it has no parents, then B and then C. The number of data samples is specified by T (int). The user may provide a random seed value seed (int), for reproducibility.DataGenerator accepts intervention if the goal is to generate data from a specified SEM while intervening on certain variables. This is passed as a dictionary, where keys are the
variable names to be intervened, and values are 1D NumPy arrays of length equal to T. The way this is achieved is identical to the previous case, except that DataGenerator intervenes on the intervention variables whenever they are encountered during the graph traversal.

Finally, the user may specify whether the generated data should be discrete or continuous via discrete (bool). In the discrete case, the DataGenerator function first generates continuous data, and then discretizes them by binning (the number of states can be specified
via nstates).

There are cases where it is desirable to generate data using a given SEM, both with and without interventions. To achieve this, the DataGenerator function is called twice, once without the intervention argument, and another with the intervention argument. This gives the user access to observational data from that SEM, but also provides the ground truthvalue of variables after a subset of variables are intervened. This is useful, for instance,when we want to evaluate the accuracy of causal inference algorithms. In such cases, it is important to specify the same random seed to the DataGenerator function in both the calls.




