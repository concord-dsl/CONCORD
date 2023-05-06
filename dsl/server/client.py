from cpgqls_client import CPGQLSClient, import_code_query, workspace_query
from server.server import start_joern_server
import time
from server.queries import get_protected_statements

print(f"Starting joern server")

server_proc = start_joern_server()
server_endpoint = "localhost:8080"
client = CPGQLSClient(server_endpoint)
query = import_code_query("/home/mootez/research/concord/dsl/examples/repos/SampleCodeCSmells",)
q2 = get_protected_statements()

while True:
    try:
        result = client.execute(query)
        print(query)
        print(result['stdout'])
        result = client.execute(q2)
        print(result['stdout'])
        break
    except:    
        pass

print(f"{'=' * 25}")
server_proc.kill()
print("Shutting down server")
print(f"Server shutdown.")