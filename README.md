# ESEM25: Towards a Domain-Specific Language for Configurable Graph Code Representations of Multilingual Corpora
![Overview of the study](figs/overview.png)

## Abstract

<ins>Background</ins>: Graph-based representations have gained attention for their ability to model structural and semantic information capturing relevant characteristics and features of source code for training deep learning models. However, existing tools face limitations: they lack flexibility in constructing cross-language graphs, produce non-interoperable outputs, and generate excessively large graphs, hindering their adoption and raising scalability and efficiency issues in graph-based neural network training.  
  
<ins>Aims</ins>: We introduce CONCORD, a domain-specific language (DSL), to address these challenges. We aim to 1) enable customizable graph-based code representations across programming languages, 2) reduce graph size complexity through simplification heuristics, and 3) improve scalability and reproducibility in software engineering tasks like code smell detection and vulnerability detection.  

<ins>Method</ins>: CONCORD provides a configurable DSL to automate graph construction and implements heuristics to reduce graph size while preserving critical information. We evaluate its effectiveness on two tasks: code smell detection and vulnerability detection. For each, we compare performance and graph size against baseline representations without simplification heuristics.  

<ins>Results</ins>: In code smell detection, CONCORD preserved 95.1% of baseline performance, and exceeded it by 5% in one setting, while reducing, on average, the number of nodes and edges by 13.11% and 13.67%, respectively. For vulnerability detection, it improved performance by 3.65% over the baseline while reducing the number of nodes and edges by 3.63% and 3.62%, respectively. This demonstrates that CONCORD’s heuristics maintain or enhance performance while improving scalability.  
  
<ins>Conclusions</ins>: CONCORD represents a step towards advancing graph-based code analysis by offering a flexible, language-agnostic approach to generate streamlined code representations. Its simplification heuristics balance performance and scalability, enabling efficient training of neural models without sacrificing accuracy. The tool reduces development overhead, promotes reproducibility through standardized representations, and broadens accessibility to graph-based methods for software engineering tasks.  

## Folder Structure
This replication package contains three major parts: the source code of the DSL, the implementation of the GNN model used in the experiment, and the data that was generated using CONCORD used to train the GNN model. 
- `data`: contains the generated data by CONCORD and used in the experiments.
- `dsl`: contains the source of CONCORD. Please check the README.md file at that folder for more information on how to use the language.
- `experiments`: contains the implementation of the GNN models.