from glob import glob
import logging
import os
from csv import reader
from shutil import rmtree
from cpgqls_client import import_code_query

from tasks.Task import Task
from utils.constants import BASE_GRAPHS
from utils.graph import load_json, save_json, transform_nodes
from utils.joern import generate_cpg, get_project_methods, generate_methods_graphs

class Representation:
    
    
    def __init__(self, *args, **kwargs):
        graph_types = set(list(map(lambda x: x.lower(), kwargs.get('base_graph_types'))))
        _result = graph_types - BASE_GRAPHS
        if _result:
            raise ValueError("Invalid base graph")
        kwargs['base_graphs'] = graph_types
        for attr, val in kwargs.items():
            setattr(self, attr, val)
        
    
    def create(self, joern_client):
        self.joern_client = joern_client
        logging.info(f"[{self.__class__.__name__.upper()}] {'=' * 5} {self.name} {'=' * 5}")
        # Load the repositories
        with open(self.repo_dirs, newline='') as f:
            repos = list(reader(f))
        
        for d in repos:
            # This folder will contain the resulting representations
            self.current_project_path = d[0]
            self.current_project_name = os.path.basename(self.current_project_path)
            logging.info(f"[{self.__class__.__name__.upper()}] Processing Project: {self.current_project_name}")
            # self.output_dir: specified by the user
            self.output_dir_path = os.path.join(self.output_dir, self.current_project_name ,self.name)
            try:
                os.makedirs(self.output_dir_path)
            except FileExistsError:
                logging.warn(f'[{self.__class__.__name__.upper()}] dir: {self.output_dir_path} already exsists, all changes will be overriden')
            
            # Load project into joern
            logging.info(f"[{self.__class__.__name__.upper()}] Loading {self.current_project_name} into joern.")
            try:
                query_result = self.joern_client.execute(import_code_query(self.current_project_path))
                if len(query_result['stdout']) == 0:
                    logging.error(f"[{self.__class__.__name__.upper()}] Could not load {self.current_project_name} into joern, skipping...")
                    print(f"{'=' * 50}")
                    print(query_result['stderr'])
                    print(f"{'=' * 50}")
                    continue
            except:
                logging.error(f"[{self.__class__.__name__.upper()}] Could not load {self.current_project_name} into joern due to memory errors, skipping...")
                continue
            logging.info(f"[{self.__class__.__name__.upper()}] {self.current_project_path} loaded successfully!")
            # Evaluate the tasks
            self.__execute_tasks()
            

        logging.info(f'[{self.__class__.__name__.upper()}] {self.name} Removing workspace folder')
        workspace_folder = os.path.join(os.getcwd(), 'workspace')
        rmtree(workspace_folder)
    
    def __generate_graphs(self, proj_dir, deleted):
        # Need to make connection with Joern
        logging.info(f'[{self.__class__.__name__.upper()}] {self.name} Generating {self.base_graphs}')
        return generate_methods_graphs(self.joern_client, proj_dir, self.base_graphs, self.output_dir_path, deleted)
    
    
    def __execute_tasks(self):
        for task in self.tasks:
            # First, execute file level operations
            deleted = task.evaluate_files(self.joern_client, self.output_dir_path)
            # Second, generate base graphs.
            #    If there are files deleted we need to generate the CPG, we pass `deleted` to __generate_graphs.
            base_graphs = self.__generate_graphs(self.current_project_path, deleted)
            # Finally, execute graph level operations
            for m, g in base_graphs.items():
                g_path = g
                g = load_json(g)
                g = transform_nodes(g)
                g = task.evaluate(g)
                save_json(g, g_path)
            #graph = task.evaluate(graph)

    
    def __save(self, rep):
        logging.info(f'[{self.__class__.__name__.upper()}] Saving {self.name}')
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "{\n\tname="+self.name+\
                "\n\trepo_dir=["+','.join(self.repo_dirs)+"]"+\
                "\n\tbase_graph_types=["+','.join(self.base_graph_types)+"]"+\
                "\n\ttasks=["+','.join([str(t) for t in self.tasks])+"]"+\
                    "\n}"