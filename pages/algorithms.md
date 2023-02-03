**PC Algorithm**

The Peter-Clark (PC) algorithm (Spirtes et al., 2000) is one of the most general purpose algorithms for causal discovery that can be used for both tabular and time series data,of both continuous and discrete types. Briefly, the PC algorithm works in two steps, it first identifies the undirected causal graph, and then (partially) directs the edges. In thefirst step, we check for the existence of a causal connection between every pair of variables by checking if there exists a condition set (a subset of variables excluding the two said
variables), conditioned on which, the two variables are independent. In the second step, the edges are directed by identifying colliders. Note that the edge orientation strategy of the PC algorithm may result in partially directed graphs. In the case of time series data, the
additional information about the time steps associated with each variable can also be used to direct the edges.
The PC algorithm makes four core assumptions: (1) Causal Markov condition, which implies that two variables that are d-separated in a causal graph are probabilistically independent, (2) faithfulness: no conditional independence can hold unless the Causal Markov condition is met, (3) no hidden confounders, and (4) no cycles in the causal graph. For time series data, it makes the additional assumption of stationarity: the properties of a random variable are agnostic to the time step.


Our implementation of the PC algorithm for time series supports lagged causal relationship discovery. Consider a dataset with N variables. To decide whether there is a causal edge between two variables, typically, this algorithm involves searching for condition sets
(this set always excludes the said two variables), for which the two variables are conditionally independent. If a set is found at any point, the search is terminated for the said two variables, and it is concluded that there is no causal edge between the them, otherwise there is one. As can be seen, in the worst case, this search may require an exponential number of steps to determine the existence of a causal edge between each pair of variables. In our implementation, we support the following ways to speed up this algorithm:

- The user may specify max_condition_set_size to be a small integer (default is 4) to terminate the search once the condition set size max_condition_set_size is reached. The intuition behind this is idea is that one may expect the causal graph to be sparsely connected, in which case, max_condition_set_size can be the maximum number of edges attached to a node.

- Multi-processing: For any given condition set size, all the conditional independence tests are independent of one another. We allow the user to exploit this fact and run these tests in parallel. This is optional, and is beneficial when the number of variables or samples are large. Since instantiating and terminating a Ray object (we use the Ray library for multi Salesforce CausalAI Library processing) adds a small overhead (typically a few seconds), using multi-processing may be slower for small datasets.

- In the case of time series specifically, we also support a mode in which conditional independence tests are performed using all the N − 2 variables. This can be done by setting max_condition_set_size = None. This way, the number of CI tests reduces from exponential to one, per pair of variables, thus saving compute time significantly in the worst case.Note that this technically makes sense in our implementation of PC because it supports only time-lagged causal discovery (assuming no contemporaneous relationships). 

Therefore,no colliders are possible for the two variables under test, since one of the variable is always the current time step, and all other variables are past time steps. However, note that using this full CI test may reduce the power of the independence test and result in less accurate causal discovery, as described in (Runge et al., 2019). To avoid this, one solution is to set
max_condition_set_size to be a small integer (similar to the description above). The difference in the time series case is that once the condition sets of size max_condition_set_size is reached, our implementation automatically performs the full CI test using all the variables that do not get eliminated as candidate parents during the greedy search process.

Thus our implementation serves as a middle ground between the traditional PC algorithm implementation and the implementation with full CI test.

**Granger Causality**

Granger causality (Granger, 1969) can be used for causal discovery in time series data without contemporaneous causal connections. The intuition behind Granger causality is that for two time series random variables X and Y , if including the past values of X to
predict Y improves the prediction performance, over using only the past values of Y , then X causes Y . In practice, to find the causal parents of a variable, this algorithm involves performing linear regression to predict that variable using the remaining variables, and using the regression coefficients to determine the causality.

Granger causality assumes: 

- linear relationship between variables, 
- covariance stationary: a temporal sequence of random variables all have the same mean and the covariance between the random variables at any two time steps depends only on their relative positions,and
- no hidden confounders.

This algorithm supports lagged causal relationship discovery. Since this algorithm involves running regression problems independently for each variable for the full causal graph,our implementation optionally allows the user to perform these optimization tasks using multi-processing for large datasets to speed up causal discovery.

**VARLINGAM**

VARLINGAM (Hyvärinen et al., 2010) can be used for causal discovery in time series data with contemporaneous causal connections. This algorithm can be broadly divided into two steps. First, we estimate the time lagged causal effects using vector autoregression. Second,
we estimate the instantaneous causal effects by applying the LiNGAM (Shimizu et al., 2006) algorithm on the residuals of the previous step, where LiNGAM exploits the non-Gaussianity of the residuals to estimate the instantaneous variables’ causal order.

This algorithm makes the following assumptions: 
- linear relationship between variables, 
- non-Gaussianity of the error (regression residuals), 
- no cycles among contemporaneous causal relations, and 
- no hidden confounders. We do not support multi-processing for this algorithm.
