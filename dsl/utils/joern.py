import subprocess
from pathlib import Path
import json, os, logging
from server.queries import concord_query_builder
from cpgqls_client import import_code_query

import stats

JOERN_DIR = Path(__file__).parent.resolve().parent.joinpath('joern', 'joern-cli')
JOERN_SCRIPTS = Path(__file__).parent.resolve().parent.joinpath('joern', 'scripts')
CPG_OUT = Path(__file__).parent.resolve().parent.joinpath('out')

def generate_cpg(proj_dir: str = "", out_dir: str = ""):
    
    if not out_dir:
        raise ValueError('Missing output directory')
    # Generate CPG using joern-parse
    proj_name = Path(proj_dir).name
    cpg = f'{out_dir}/{proj_name}.bin'
    print("CPG DIR", cpg)
    out = subprocess.run([f'{JOERN_DIR}/joern-parse', '-o', cpg, proj_dir], 
                                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True, check=True)
    err = out.stderr
    return_code = out.returncode
    if err or return_code != 0:
        print(err)
        return None
    
    return cpg

def get_project_methods(cpg_dir: str = "", out_dir: str = ""):
    
    if not out_dir:
        raise ValueError('Missing output directory')
    # Return the list of methods
    proj_name = Path(cpg_dir).name.split('.')[0]
    # 2) Execute joern with get-methods.sc to return the list of methods
    proj_methods_file = f'{out_dir}/{proj_name}_methods.json'
    out: subprocess.CompletedProcess = subprocess.run([f'{JOERN_DIR}/joern','--script', 
                          f'{JOERN_SCRIPTS}/get-methods.sc', 
                          '--params', f'cpgFile={cpg_dir},outFile={proj_methods_file}'], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True, check=True)
    err = out.stderr
    return_code = out.returncode
    if err or return_code != 0:
        print(err)
        return None
    # 3) Parse the methods' file and return it
    with open(proj_methods_file, 'r') as methods_file:
        methods_arr = json.load(methods_file)
    
    methods = {m['id']: {'name': m['name'], 'fullName': m['fullName']}  for m in methods_arr}
    return methods, proj_methods_file

def generate_methods_graphs(joern_client ,project_dir: str = "", base_graphs: 'list[str]' = [], out_dir: str = "", deleted = False):
    
    if not out_dir:
        raise ValueError('Missing output directory')
    
    if not project_dir:
        raise ValueError('Missing project dictionary')
    
    project_name = Path(project_dir).name
    encoded_bgraphs = '_'.join(base_graphs)
    query_file = os.path.join(JOERN_SCRIPTS, "methods-to-graphs-json.sc")
    
    # If files were edited we have to re-import the project
    if deleted:
        logging.info(f'Files were edited in {project_name} reloading it into joern again')
        reaload_project_query = import_code_query(project_dir)
        try:
            result = joern_client.execute(reaload_project_query)
            if len(result['stdout']) == 0:
                    logging.error(f"Could not load {project_name} into joern, exiting...")
                    print(f"{'=' * 50}")
                    print(result['stdout'])
                    print(result['stderr'])
                    print(f"{'=' * 50}")
                    return None
                    
        except:
            logging.error(f"Could not load {project_name} into joern, exiting...")
    else:
        # We import the CPG file instead
        logging.info(f'No files were edited in {project_name} reloading its CPG into joern again')
        cpg_path = os.path.join(os.getcwd(), 'workspace', project_name, 'cpg.bin')
        load_cpg_query = f"loadCpg(\"{cpg_path}\")"
        result = joern_client.execute(load_cpg_query)


    query = concord_query_builder(query_file, outDir=out_dir, baseGraphs=encoded_bgraphs)
    result = joern_client.execute(query)
    if len(result['stdout']) == 0:
        logging.error(f"[JOERN] Could not extract {project_name} base methods...")
        print(f"{'=' * 50}")
        print(result['stderr'])
        print(result['stdout'])
        print(f"{'=' * 50}")


    # Load the methods file
    with open(Path(out_dir).joinpath(f'{project_name}_methods.json')) as f:
        methods = json.load(f)

    #Return mapping method_id -> method_base_graph_dir
    methods_base_graphs = {m['id']: f'{out_dir}/{m["name"]}_{m["id"]}_base.json' for m in methods}
    return methods_base_graphs

def combine_graphs():
    pass