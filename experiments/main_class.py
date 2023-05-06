import argparse
import os
import sys

import numpy as np
from data_module.lightning_data_class import DataModule
from graph_models.gcn import GCN
from graph_models.ggnn import GGNN
from graph_models.gat import GAT
from graph_models.ggnn_gap import GGNNGAP

import torch
import pytorch_lightning as pl
from pytorch_lightning import loggers as pl_loggers

from utils.data import static_splitter
from graph_models.lightning_classifier import ConcordClassifier

from transformers import AutoTokenizer, AutoModel

os.environ["CUDA_LAUNCH_BLOCKING"] = "1"


import timeit

def torch_setup(seed=4096):
    seed = seed
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


if __name__ == '__main__':
    torch_setup(seed=4096)
    #torch.multiprocessing.set_start_method('spawn')
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=str, help='Root directory to JSON files',
                        required=True)
    parser.add_argument('--repr', type=str, required=True, help='Name of the representation.')
    parser.add_argument('--type', type=str, help='Datapoints type', choices=['method', 'class'], default='method')
    parser.add_argument('--embedding_model', type=str, required=True, help='Path of the pretrained huggingface embedding model.')
    parser.add_argument('--data_src', type=str, help='CSV file of the dataset.', required=True)
    parser.add_argument('--feature_size', type=int, help='Size of feature vector for each node', default=128)
    parser.add_argument('--graph_embed_size', type=int, help='Size of the Graph Embedding', default=200)
    parser.add_argument('--num_steps', type=int, help='Number of steps in GGNN', default=6)
    parser.add_argument('--batch_size', type=int, help='Batch Size for training', default=32)
    parser.add_argument('--epochs', type=int, help='Batch Size for training', default=40)
    parser.add_argument('--read_out', type=str, help='GNN readout function', choices=['sum', 'mean'], default='sum')
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    args.device = device

    train_split, test_split, val_split =  static_splitter(args.data_src)

    tokenizer = AutoTokenizer.from_pretrained(args.embedding_model)
    encoder = AutoModel.from_pretrained(args.embedding_model)

    args.embeddings = encoder.embeddings.word_embeddings.weight.data.cpu().detach().clone().numpy()
    args.tokenizer = tokenizer
    
    if args.type == "method":
        max_edge_types = 9
        args.edge_mapping = {
        "AST: ": 0,
        "NCS": 1,
        "COMPUTED_FROM": 2,
        "FOR_EXEC": 3,
        "FOR_NEXT": 4,
        "WHILE_NEXT": 5,
        "WHILE_EXEC": 6,
        "GUARDED_BY": 7,
        "GURADED_BY_NEGATION": 8,
    } 
    else:
        max_edge_types = 10
        args.edge_mapping = {
        "AST: ": 0,
        "NCS": 1,
        "COMPUTED_FROM": 2,
        "FOR_EXEC": 3,
        "FOR_NEXT": 4,
        "WHILE_NEXT": 5,
        "WHILE_EXEC": 6,
        "GUARDED_BY": 7,
        "GURADED_BY_NEGATION": 8,
        "MEMBER_OF": 9
    }

    data_module = DataModule(args.data_src, args)

    
    if args.model_type == 'GGNN':
        graph_model = GGNN(
                            input_dim=args.feature_size, 
                            output_dim=args.graph_embed_size,
                            num_steps=args.num_steps, 
                            max_edge_types=max_edge_types, 
                            read_out=args.read_out
                            )
    if args.model_type == 'GGNN-GAP':
        graph_model = GGNNGAP(
                            input_dim=args.feature_size, 
                            output_dim=args.graph_embed_size,
                            num_steps=args.num_steps, 
                            max_edge_types=max_edge_types, 
                            )
    
    elif args.model_type == 'GCN':
        graph_model = GCN(input_dim=args.feature_size, output_dim=args.graph_embed_size, num_layers=6, read_out=args.read_out)

    elif args.model_type == 'GAT':
        graph_model = GAT(
                            input_dim=args.feature_size, 
                            output_dim=args.graph_embed_size, 
                            attention_heads=8, 
                            feat_dp=.2, 
                            attention_dp=.2 , 
                            read_out=args.read_out
                            )
    else:
        raise ValueError('Invalid model name')
    
    smell_name = str(os.path.basename(args.data_src)).replace('.csv', '')
    experiment_name = f"{smell_name}_{args.repr}"
    
    tb_logger = pl_loggers.TensorBoardLogger(save_dir=f'/home/mootez/projects/def-tusharma/mootez/logs/{experiment_name}')
    
    loss_function = torch.nn.CrossEntropyLoss(reduction='sum')
    model = ConcordClassifier(graph_model, loss_function)
    trainer = pl.Trainer(
        accelerator='gpu',
        devices=[0],
        max_epochs=args.epochs,
        logger=tb_logger
    )
    start = timeit.default_timer()
    trainer.fit(model, datamodule=data_module)
    stop = timeit.default_timer()
    print(f'Training time: {stop - start}')
    trainer.test(model, datamodule=data_module)