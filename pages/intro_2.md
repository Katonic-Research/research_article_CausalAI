The above examples illustrate the fundamental limitations of using correlation based models for the problem of predicting the causal impact of one variable on another. This problem has important applications in several domains such as sales, medicine, diagnosis, etc.

For instance, a business might be interested in finding out whether more customers would be likely to purchase their products if they offered a discount, versus if they showed ads on the television. As another example, finding out if certain chemicals cause harmful effects on health can benefit the broader society. This type of knowledge facilitates interventions,which are actionable items that can be used to change future outcomes, as opposed to correlation based machine learning models, which are typically used for automation. Causal analysis tools help us discover which variables in a system can be intervened to achieve the desired outcome for a particular variable of interest.

Given the importance of this problem, several libraries exist on causal discovery and causal inference (Kalainathan and Goudet, 2019; Sharma and Kiciman, 2020; Beaumont et al., 2021). However, certain limitations still exist in existing libraries, such as computationally heavy implementation, and the lack of support for different data types and code-free user interface, which are required for a unified end-to-end system that supports a fast and easy to use system for the various types of problems in the domain of causal analysis.

We introduce the Salesforce CausalAI Library, a Python library for causal analysis that supports causal discovery and causal inference using observation data. The Salesforce CausalAI library pipeline is shown in figure 1. Some of the key features of our library
are:

- **Data**: Causal analysis on tabular and time series data, of both discrete and continuous types.

- **Missing Values**: Support for handling missing/NaN values in data.

- **Data Generator**: A synthetic data generator that uses a specified structural equation model (SEM) for generating tabular and time series data. This can be used for evaluating and comparing different causal discovery algorithms since the ground truth values are known.

- **Distributed Computing**: Use of multi-processing using the Ray (Moritz et al., 2018) library, that can be optionally turned on by the user when dealing with large datasets or number of variables for faster compute.

- **Targeted Causal Discovery**: In certain cases, we support targeted causal discovery, in which the user is only interested in discovering the causal parents of a specific variable of interest instead of the entire causal graph.
    This option reduces computational overhead.

- **Visualization**: Visualize tabular and time series causal graphs.

- **Domain Knowledge**: Incorporate any user provided partial prior knowledge about the causal graph in the causal discovery process.

- **Code-free UI**: Provide a code-free user interface in which users may directly upload their data and perform their desired choice of causal analysis algorithm at the click of a button.
