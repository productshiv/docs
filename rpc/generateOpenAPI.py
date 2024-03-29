import os
import yaml

def escape_path(path):
    # Escapes forward slashes by replacing them with ~1
    return path.replace("/", "~1")

def get_chain_paths(chain_folder):
    paths = {}
    for file_name in os.listdir(chain_folder):
        if file_name.endswith('.yml'):
            file_path = os.path.join(chain_folder, file_name)
            try:
                with open(file_path, 'r') as file:
                    chain_spec = yaml.safe_load(file)
                    if 'paths' in chain_spec:
                        for path, path_item in sorted(chain_spec['paths'].items()):
                            # Construct the reference path with escaped slashes
                            ref_path = os.path.join(chain_folder, file_name) + "#/paths/" + escape_path(path)
                            paths[path] = {'$ref': ref_path}
                    else:
                        print(f"No 'paths' found in {file_name}")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    return paths

main_spec = {
    'openapi': '3.1.0',
    'info': {
        'title': 'RPC',
        'version': '1.0.0'
    },
    'paths': {}
}

operations_dir = 'rpc/operations'

if os.path.exists(operations_dir):
    chains = sorted(os.listdir(operations_dir))
    for chain in chains:
        chain_folder = os.path.join(operations_dir, chain)
        if os.path.isdir(chain_folder):
            chain_paths = get_chain_paths(chain_folder)
            
            # Add a comment without single quotes
            main_spec['paths'][f'# {chain}'] = 'Start of chain'
            
            main_spec['paths'].update(chain_paths)
        else:
            print(f"Chain directory not found: {chain_folder}")
else:
    print(f"Operations directory not found: {operations_dir}")

with open('rpc/main.yml', 'w') as file:
    yaml.dump(main_spec, file, default_flow_style=False, sort_keys=False)
