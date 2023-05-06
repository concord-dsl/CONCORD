## Running the GNN models

This folder contains the implementation of the GNN models used to classify code smells.

### Requirements
Make sure to have python 3.9 installed along with the package manager `pip`. To install the dependencies run the following command: 

`pip install -r requirements.txt`

### Training the Models

As discussed in the paper, the problem is formulated a one-vs-all classification. Hence, for each code smell, a model will be trained. Since we have three representations then a total of `num_smells * num_representations = 12` models will be trained.  

To train models on the `ComplexMethod` or `ComplexConditional` smells, run the following command:

```
python3 main.py \
--root=<RAW_DATA_PATH>
--model_type=GGNN-GAP \
--repr=<REPRESENTATION> \
--type=method \
--embedding_model=microsoft/codebert-base \
--data_src=<CSV_FILE> \
--feature_size=768 \
--graph_embed_size=128 \
--num_steps=4 \
--batch_size=128 \
--epochs=40 \

```
Where:
- `root`: the root directory where the raw data will exists. For instance, `~/data/methods` if you have unzipped the `methods.tar.gz` in the `data` directory.
- `repr`: is the name of the representation: `R1`, `R2`, and `R3`. This is case sensitive, meaning providing `r1` will not work.
- `data_src`: the name of the CSV file of the dataset (e.g. `CM.csv`). By default, these CSV files are provided in the `data` folder.

To generate the initial feature representation of the nodes of each graph we used a pretrained CodeBERT. If you enviornment does not have access to internet, make sure to update the `embedding_model` variable to pinpoint to the path of CodeBERT on your local machine.  

To train models on the `FeatureEnvy` or `MultifacetedAbstraction` smells, run `main_class.py` instead. The paramters are the same, except:

- `root`: should pinpoint to `~/data/classes`.
- `type`: should be set to "class"