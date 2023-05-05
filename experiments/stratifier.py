import argparse
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

def stratified_sampling(X, y, train_size=0.8, val_size=0.1, test_size=0.1, random_state=42):
    """
    Perform stratified sampling to split a dataset into train, validation, and test sets with the specified ratios.
    Inputs:
        - X: a pandas DataFrame or NumPy array containing the features
        - y: a pandas Series or NumPy array containing the class labels
        - train_size: the proportion of the dataset to include in the training set (default: 0.8)
        - val_size: the proportion of the dataset to include in the validation set (default: 0.1)
        - test_size: the proportion of the dataset to include in the test set (default: 0.1)
        - random_state: the random seed to use for the sampling (default: 42)
    Outputs:
        - X_train: a pandas DataFrame or NumPy array containing the features of the training set
        - X_val: a pandas DataFrame or NumPy array containing the features of the validation set
        - X_test: a pandas DataFrame or NumPy array containing the features of the test set
        - y_train: a pandas Series or NumPy array containing the class labels of the training set
        - y_val: a pandas Series or NumPy array containing the class labels of the validation set
        - y_test: a pandas Series or NumPy array containing the class labels of the test set
    """
    # Split the dataset into a combined training and validation set and a test set
    X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=test_size, stratify=y, random_state=random_state)
    
    # Split the training and validation set into separate sets
    val_ratio = val_size / (train_size + val_size)
    X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=val_ratio, stratify=y_train_val, random_state=random_state)
    
    print(f"Train set class distribution: {np.bincount(y_train)}")
    print(f"Validation set class distribution: {np.bincount(y_val)}")
    print(f"Test set class distribution: {np.bincount(y_test)}") 

    return X_train, X_val, X_test, y_train, y_val, y_test


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--data_src', type=str, required=True, help='CSV file.')
    parser.add_argument('--X', type=str, help='Feature column.',
                        required=True)
    parser.add_argument('--y', type=str, required=True, help='Label column.')
    parser.add_argument('--output', type=str, required=True, help='Output file path.')
    args = parser.parse_args()

    df = pd.read_csv(args.data_src)
    X_col, y_col = args.X, args.y
    
    X_col=X_col.split(',')

    X, y = df[X_col], df[y_col]

    X_train, X_val, X_test, y_train, y_val, y_test = stratified_sampling(X, y)

    train = pd.concat([X_train, y_train], axis=1)
    val = pd.concat([X_val, y_val], axis=1)
    test = pd.concat([X_test, y_test], axis=1)

    train['split'] = ['train'] * len(train['label'])
    val['split'] = ['val'] * len(val['label'])
    test['split'] = ['test'] * len(test['label'])

    stratified_dataset = pd.concat([train, val, test], axis=0, ignore_index=True)

    stratified_dataset.to_csv(args.output, index=None)
