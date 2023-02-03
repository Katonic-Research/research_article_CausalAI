We introduce the Salesforce CausalAI Library, an open-source library for causal analysis
using observational data. It supports causal discovery and causal inference for tabular and
time series data, of both discrete and continuous types. This library includes algorithms
that handle linear and non-linear causal relationships between variables, and uses multiprocessing for speed-up. We also include a data generator capable of generating synthetic
data with specified structural equation model for both the aforementioned data formats
and types, that helps users control the ground-truth causal process while investigating
various algorithms. Finally, we provide a user interface (UI) that allows users to perform
causal analysis on data without coding. The goal of this library is to provide a fast and
flexible solution for a variety of problems in the domain of causality. This technical report
describes the Salesforce CausalAI API along with its capabilities, the implementations of
the supported algorithms, and experiments demonstrating their performance and speed.
Our library is available at https://github.com/salesforce/causalai.