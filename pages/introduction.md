Causal inference aims at determining how a change in one part of a system affects another,
in isolation, i.e., no other parts of the system are allowed to change independently. Such
an inference is fundamentally different from predictions made by machine learning models,
which are based on correlation between variables. The reason behind this difference is
that correlation does not necessarily imply causation. As a simple example, consider two
discrete random variables, X and Y . X can independently take two states– −1 and +1
with probability 0.5 each. Y on the other hand takes the state 0 when X is −1, and states
−1 and +1 with probability 0.5 each, when X is +1. By design, X causes Y . However,
the correlation between the two variables is 0. Another example on the other end of the
spectrum is a scenario in which a third variable Z is a common cause of X and Y , and
there is no causal link between the latter two. In this case, it is likely that X and Y are
correlated. However, by design, any isolated change in X cannot cause changes in Y , since
Z is fixed.