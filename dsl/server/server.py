import subprocess
import logging
import re
from pathlib import Path
from cpgqls_client import CPGQLSClient, import_code_query, workspace_query

JOERN_DIR = Path(__file__).parent.resolve().parent.joinpath('joern', 'joern-cli')

def start_joern_server(host='localhost', port=8080):
    """
    This method spanws a joern server. It makes sure that server is spawned by repeatedly sending a dummy query (in this case `version`)
    until a valid response is received.
    """
    logging.info(f'Starting joern server.')
    server_proc = subprocess.Popen([Path.joinpath(JOERN_DIR, 'joern'),"--server"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    server_endpoint = f'{host}:{str(port)}'
    logging.info(f'Waiting for joern server to spawn.')
    client = CPGQLSClient(server_endpoint)
    query = 'version'
    while True:
        try:
            result = client.execute(query)
            ver = result['stdout']
            prog = re.compile(r"\".*\"")
            ver = prog.search(ver).group(0)
            logging.info(f"Joern server with version {ver}")
            break
        except:    
            pass

    return server_proc, client