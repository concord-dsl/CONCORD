import pandas as pd
import networkx as nx
import json, os
from tqdm import tqdm

def read_json(file_path):
    """
    Reads a JSON file and returns its contents as a Python dictionary.
    
    Args:
        file_path (str): The path to the JSON file.
        
    Returns:
        dict: The contents of the JSON file as a Python dictionary.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except:
        return None
    

def merge_graphs(graphs):
    """
    Merges a list of NetworkX graphs into a single graph with a central node
    linked to each input graph via a "MEMBER_OF" edge.

    Returns:
        merged_graph (nx.MultiDiGraph): Merged graph with central node and "MEMBER_OF" edges.
    """
    json_graphs = list(map(read_json, graphs))
    if None in json_graphs:
        return None
    nx_graphs = list(map(nx.readwrite.json_graph.node_link_graph, json_graphs))
    if (len(json_graphs) == 0) or (len(nx_graphs) == 0):
        return None
    
    class_graph_id = 1e7
    class_graph = nx.disjoint_union_all(nx_graphs)
    class_graph.add_node(class_graph_id, node_type="CLASS_DECLARATION", code="CLASS")
    
    
    method_nodes = []
    for node, data in class_graph.nodes(data=True):
        if ('node_type' in data) and (data['node_type'] == "METHOD_DECLARATION"):
            method_nodes.append(node)
    
    for i, method_node in enumerate(method_nodes):
        class_graph.add_edge(class_graph_id, method_node, key=f'memof{i}', label='MEMBER_OF')
    

    return class_graph


def save_multidigraph_to_json(graph, file_path):
    """
    Saves a NetworkX MultiDiGraph to a JSON file.

    Args:
        graph (nx.MultiDiGraph): NetworkX MultiDiGraph to be saved.
        file_path (str): File path including the file name and extension for the saved graph.
    """
    # Convert the graph to a dictionary representation
    graph_dict = nx.node_link_data(graph)

    # Save the dictionary to a JSON file
    with open(file_path, "w") as f:
        json.dump(graph_dict, f, indent=4)


def get_file_full_path(project, rep):
    return f"./methods/{rep}/{project}"

dst = "./classes"

class_mapping = read_json("./mapping/final_class_methods_mapping.json")

fe = pd.read_csv("./FE.csv")
mfa = pd.read_csv("./MFA.csv")

total_classes = set(list(fe['concord_class'].tolist() + mfa['concord_class'].tolist()))

mapper = {}

# First Step: Create class graphs
for _class in tqdm(total_classes):
    
    class_name = _class
    project = class_mapping[_class]['project']
    # Map files to their full path
    r1_methods = list(map(lambda x: os.path.join(get_file_full_path(project, 'R1'), x), class_mapping[class_name]['r1_methods']))
    r2_methods = list(map(lambda x: os.path.join(get_file_full_path(project, 'R2'), x), class_mapping[class_name]['r2_methods']))
    r3_methods = list(map(lambda x: os.path.join(get_file_full_path(project, 'R3'), x), class_mapping[class_name]['r3_methods']))

    # Create a class for each rep
    r1_class = merge_graphs(r1_methods)
    if r1_class == None:
        continue
    r2_class = merge_graphs(r2_methods)
    if r2_class == None:
        continue
    r3_class = merge_graphs(r3_methods)
    if r1_class == None:
        continue  

    # Create new folder if it does not not exists
    r1_subfolder = os.path.join(dst, "R1", project)
    r2_subfolder = os.path.join(dst, "R2", project)
    r3_subfolder = os.path.join(dst, "R3", project)
    
    if not os.path.exists(r1_subfolder):
        os.makedirs(r1_subfolder)
        
    if not os.path.exists(r2_subfolder):
        os.makedirs(r2_subfolder)
        
    if not os.path.exists(r3_subfolder):
        os.makedirs(r3_subfolder)
        
    # Save classes at each folder
    c1 = f"{project}_{class_name}_R1.json"
    c2 = f"{project}_{class_name}_R2.json"
    c3 = f"{project}_{class_name}_R3.json"
    
    r1_class_name = os.path.join(r1_subfolder, c1)
    r2_class_name = os.path.join(r2_subfolder, c2)
    r3_class_name = os.path.join(r3_subfolder, c3)
    
    mapper[_class] = [c1, c2, c3]
    
    save_multidigraph_to_json(r1_class, r1_class_name)
    save_multidigraph_to_json(r2_class, r2_class_name)
    save_multidigraph_to_json(r3_class, r3_class_name)
    