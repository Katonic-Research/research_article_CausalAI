import streamlit as st
from pathlib import Path
from PIL import Image

st.set_page_config(
    page_title='Interactive research article using Streamlit',  
    layout = 'centered', 
    initial_sidebar_state = 'auto'
)
st.markdown('*Research article*')
st.title('Salesforce CausalAI Library: A Fast and Scalable Framework for Causal Analysis of Time Series and Tabular Data')
st.subheader("Authors")
st.warning('''
Devansh Arpit, Matthew Fernandez, Chenghao Liu1, Weiran Yao, Wenzhuo Yang,Paul Josel
, Shelby Heinecke, Eric Hu, Huan Wang, Steven Hoi, Caiming Xiong
, Kun Zhang, and Juan Carlos Niebles

AI Research, Salesforce

Carnegie Mellon University

Corresponding Authors: {darpit, jniebles}@salesforce.com
''')

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

st.header('Abstract')
abstract = read_markdown_file("pages/abstract.md")
st.info(abstract)

st.markdown('''**Keywords:** *Causality*, *Causal Discovery*, *Causal Inference*, *Scalable*,*Fast*,*Time Series
Data*,*Tabular Data*,*Light-weight*''')

st.header('Introduction')
intro_markdown = read_markdown_file("pages/introduction.md")
st.write(intro_markdown, unsafe_allow_html=True)

st.image('image/time-series-1.png')
st.caption('''Figure 1: Salesforce CausalAI Library Pipeline. We support causal discovery and causal
inference. The causal discovery module takes as input a data object (containing
observational data) and a prior knowledge object (containing any expert partial
prior knowledge, optional), and outputs a causal graph. The causal inference
module takes a causal graph as input (which could be directly provided by the
user or estimated using the causal discovery module) along with the user specified
interventions, and outputs the estimated effect on the specified target variable.''')

intro_markdown_2 = read_markdown_file("pages/intro_2.md")
st.write(intro_markdown_2, unsafe_allow_html=True)

st.header('Related Work')
st.write(
    '''
    Table 1 summarizes the main features supported by the Salesforce CausalAI library versus the existing libraries for causal analysis. The key differentiating features of our library are
parallelization and a user interface (UI), that are aimed at making causal analysis more scalable and user friendly. Our UI allows the users to run causal discovery and causal
inference algorithms on their local machines without the need to write code. In terms of parallelization, we use the Python Ray library (Moritz et al., 2018) (optional) such that
the implementation of the algorithm is tied to it, which makes the user’s interaction with the API simple, i.e., the user can simply specify as an argument whether or not to use
multi-processing. Tigramite also supports parallelization, but uses MPI4Py (Dalcin and Fang, 2021), which we found to be slower compared to Ray. Additionally, in Tigramite’s
implementation of the PC algorithm, the process of finding the causal neighbors of a variable is run in parallel for each variable. Note that each causal neighbor discovery may require
an exponential number (in terms of the number of variables) of conditional independence (CI) tests. Our implementation on the other hand runs the CI tests themselves within each
causal neighbor discovery process in parallel. This makes our implementation more efficient.CausalNex on the other hand uses Pytorch for parallelization.
    '''
)

st.image('image/table-2.png')
st.caption('''Table 1: A comparison of features supported by Salesforce CausalAI library vs existing libraries
for causal analysis. Note that all libraries support causal discovery. CI: Causal Inference,
DK: Domain Knowledge, UI: User Interface, CDT: Causal Discovery Toolbox.''')

st.header('Library Architecture and API Description')
st.write(
    '''
    The Salesforce CausalAI Library API is composed of four main components– data layer,prior knowledge, causal discovery, and causal inference, as described in subsections below.

The data layer includes data generator, data transform and data specification modules.The prior knowledge layer helps the user specify any partial knowledge about the causal relationship between variables. The causal discovery layer aims at retrieving the underlying
causal graph from observational data. Finally, the causal inference layer aims at estimating the average treatment effect (ATE) and conditional ATE (CATE) of interventions on a subset of variables on a specified target variable. Aside from these components, we also
support causal graph visualization and evaluation of the correctness of the estimated causal graph when the ground truth graph is available.
    '''
)

st.subheader('Data Layer')
st.write('**Data Generator**')
st.write('''
The function DataGenerator can be used to generate synthetic time series and tabular data according to a user specified additive noise structural equation model (SEM). As an
example, consider a tabular data system with random variables A, B and C, then an instance of an additive noise SEM is,
''')
st.latex(r'''A = N_{1}()''')
st.latex(r'''B = k_{1} \times F_{1}(A) + N_{2}()''')
st.latex(r'''C = k_{2} \times F_{2}(A) + k_{3} \times F_{3}(B)+ N_{3}()''')

st.write('''
where N(i) and F(i) are callable functions, k(i) are constants, all of which are user specified. 
This SEM is passed as the following dictionary sem ''')
st.latex(r'''{A : [], B : [(A, k_{1}, F_{1})], C :[(A, k_{2}, F_{2}),(B, k_{3}, F_{3})]}''') 
st.write('The noise functions ')
noise_fn = st.latex(r''' noise f_{n} = [N_{1}, N_{2}, N_{3}]''')

arch = read_markdown_file("pages/architecture.md")
st.write(arch, unsafe_allow_html=True)

st.write('**Data Transform**')
with st.expander("Expand"):
    st.write('''
    For time series data, two transform modules are supported– StandardizeTransform and DifferenceTransform. StandardizeTransform subtracts and divides each element with the 
    corresponding feature-wise mean and standard deviation respectively. DifferenceTransform performs temporal differencing, i.e., computes the difference between two time-steps 
    separated by a given interval. This interval can be specified by the user. Note that in case there are NaN values in the data array, the output of these transformation only contains 
    NaNs at the location of the original NaNs. These modules use NumPy array format as input and output. Finally, multiple arrays may be passed to these modules in the case of disjoint time 
    series data (E.g. one time series is a daily record from January to March 2001, and another from January to March 2002).
    
    For tabular data, only StandardizeTransform is currently supported, which works identically to the time series case.
    ''')

st.write('**Data Object**')
with st.expander("Expand"):
    st.write('''
    In order to feed observational data to the causal discovery algorithms in our API, the raw data– NumPy arrays and a list of variable names (optional), is used to instantiate a
CausalAI data object. Note that any data transformation must be applied to the NumPy array prior to instantiating a data object. For time series and tabular data, TimeSeriesData
and TabularData must be initialized with the aforementioned data respectively. For time series data, multiple arrays may be passed to the TimeSeriesData class in the case of
disjoint time series data (E.g. one time series is a daily record from January to March 2001, and another from January to March 2002). Users may also optionally specify if the data
contains or may contain NaNs, so they may be handled. These data objects contain some useful methods (E.g. for extracting the data corresponding to the parents of a variable for
a given observation or time step), but they are mainly designed to be used internally by the causal discovery algorithms, and users may treat the data object as a blackbox
    ''')

st.subheader('Prior Knowledge')

st.write(
    '''
    The module PriorKnowledge can be optionally used to specify any partial prior knowledge about the causal graph. This module is used in causal discovery algorithms supported by
our API. Specifically, there are four types of prior knowledge that users may specify in the form of arguments to the PriorKnowledge class– forbidden_links, existing_links,
root_variables, and leaf_variables. The argument forbidden_links should specify which variables cannot be the parents of a variable. The argument existing_links should
specify which variables are known to be the parents of a variable. The argument root_variables should specify which variables cannot have any causal parents. Finally, the argument
leaf_variables should specify which variables cannot have any causal children.

Note that these specifications are accepted in the same format for both tabular and time series data. Specifically, in the time series case, the user may specify that A → B is
forbidden, which implies that no time lagged or instantaneous state of variable A can cause B at any time step. Further, existing_links are not utilized for time series data since
time lag information cannot be specified in PriorKnowledge. The reasoning behind this design choice is that it is more likely that domain experts may know whether two time series
variables are causally related, but less likely that they know which specific time lag of one variable causes another.
'''
)
st.subheader('Causal discovery')
discovery = read_markdown_file("pages/discovery.md")
st.write(discovery, unsafe_allow_html=True)

st.subheader('**Causal inference**')
st.write('''
    We support the class CausalInference to perform causal inference for tabular and time series data, which can be used to compute average treatment effect (ATE) and conditional
ATE (CATE). This class can be initialized using a 2D NumPy data array data, a list of variable names var_names, a Python dictionary specifying the causal graph causal_graph
corresponding to the data, a prediction_model to be used for learning the mapping function between different variables, the argument discrete (bool) specifying whether the data is
continuous or discrete. Another argument use_multiprocessing (bool) may also be specified at initialization which can be used to speed up computation. Typically, multi-processing
has an advantage when prediction_model is a non-linear model.

To perform ATE upon initialization, the method ate should be called with the arguments target_var and treatments. Here target_var is the name of the variable on which
ATE needs to be estimated, and treatments is a list of Python dictionary, or a dictionary specifying the intervention variables and their corresponding treatment and control values. Specifically, this Python dictionary has three keys called var_name, treatment_value,
control_value.

To perform CATE upon initialization, the method cate should be called. This method takes two additional arguments in addition to those described for the ate method above.
They are conditions and condition_prediction_model.
''')

st.header('Causal Discovery Algorithms')
st.write('''
Causal discovery aims at finding the underlying directed causal graph from observational data, where the variables (or features) are treated as nodes in the graph, and the edges
are unknown. For two variables A and B in a graph, the edge A → B denotes A causes B. Observational data is simply a set of observations recorded in the past without actively
making any interventions. Typically, finding causal relationships between variables would require performing interventions. But under certain assumptions, it is possible to extract
the underlying causal relationships between variables from observational data as well. In this section, we describe some of such algorithms that are supported by our library, their
assumptions, and their implementation details.
''')

algorithm = read_markdown_file("pages/algorithms.md")
st.write(algorithm, unsafe_allow_html=True)

st.header('Causal Inference Algorithms')

st.write(
    '''
    Causal inference involves finding the numerical estimate of intervening one set of variables,on another variable. This type of inference is fundamentally different from what machine
learning models do when they predict one variable given another as input, which is based on correlation between the two variables found in the training data. In contrast, causal
inference tries to estimate how a change in one variable propagates to the target variable while traversing the causal graph from the intervened variable to the target variable along
the directed edges. This means that even if two or more variables are correlated, intervening one may not have any effect on another variable if there is no causal path between them.
Specifically, in this library, we support estimating average treatment effect (ATE) and conditional ATE (CATE). Suppose we are interested in estimating the ATE of some intervention of a set of variables denoted as X, on a variable Y . The treatment and control
values of X are denoted as xt and xc. Then ATE is defined as,
    '''
)

st.header('Experiments')

st.write(
    '''**Causal Discovery for Time Series**

Experimental Settings We conduct empirical studies on synthetic data to verify the efficiency of CausalAI library. Specifically, We compare PC algorithm in CausalAI library
with hat in causal-learn2 library and tigramite library. To achieve fair comparison, the p-value threshold and maximum condition set size are set to 0.05 and 4. We report results
on two settings, considering the effect of different number of variables and the effect of different number of samples, respectively. We evaluate the training time and F1 score of the
estimated graphs.

Results Figure 2 reports the time cost required by each model. We can find that CausalAI and tigramite are much faster than causal-learn. This is because both of these two libraries
consider the characteristics of time series and reduce the potential search space when uncovering the causal relationships. We also observe a speedup via using multi-processing in
CausalAI, especially when handling data with large sample size or large variable size. This verifies the efficacy of the proposed method in CausalAI to handle large scale data.
In Figure 3, we also show the F1 score between the estimated causal graphs and the ground truth causal graph. We find that CausalAI and tigramite performs much better
than causal-learn. This is because the PC algorithm in causal-learn is a more general implementation without considering the characteristic of time series. Therefore, it is necessary
to manually include suitable prior knowledge to further improve its performance.
    '''
)

st.header('Conclusions and Future Work')
st.info('''
    We introduce the Salesforce CausalAI Library, an open source library for causal analysis of time series and tabular data. The Salesforce CausalAI Library aims to provide a onestop solution to the various needs in causal analysis including handling different data types,
data generation, multi-processing for speed-up, utilizing domain knowledge and providing a user-friendly code-free interface.
We continue to develop this library and invite the research community to contribute by submitting pull requests to our GitHub repository. Some of our future plans are to include
support for heterogeneous data types (mixed continuous and discrete types), support for GPU based computing, more algorithms for causal discovery and inference, and support for
latent variables.
   ''')

st.header('Contributions')
st.warning('''
   **Devansh Arpit**: Implemented the code for Salesforce CausalAI Library v1.0, except some
parts of the VARLINGAM algorithm. Created the Sphinx documentation for the GitHub
repository. Wrote the blog. Wrote this tech report, except for the experiments section.

**Matthew Fernandez**: Implemented the UI to test and showcase the CausalAI Library.

**Chenghao Liu**: Implemented the VARLINGAM algorithm, wrote the experiments section and helped in the literature review.

**Weiran Yao**: Coded algorithm which will be added to the next version of the CausalAI
library.

**Wenzhuo Yang**: Coded algorithm which will be added to the next version of the CausalAI library.

**Paul Josel**: Helped in the UI design and organization process.

**Shelby Heinecke**: Contributed to the conception and initial direction of the library. Contributed to the literature review.

**Eric Hu**: Coordinated UI design and implementation.

**Huan Wang**: Contributed to the library design regarding tabular/time series data structures, choices of algorithms, and UI features.

**Stephen Hoi**: Contributed to the high-level discussions on the project. General feedback for the project and the report.

**Caiming Xiong**: Initiated project idea and contributed to the high-level direction of the library. General project feedback.

**Kun Zhang**: Contributed to causal discovery algorithm selection and design. General project feedback.

**Juan Carlos Niebles**: Contributed to the high-level project direction and scope, oversaw project execution and coordinated team effort.
   ''')

st.header('Reference Link')
st.write("Research article - https://arxiv.org/pdf/2301.10859v1.pdf")
st.write('Repository link - https://github.com/salesforce/causalai')

st.header('References')

with st.expander("Expand"):
    references = read_markdown_file("pages/references.md")
    st.write(references, unsafe_allow_html=True)


















