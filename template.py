import os

list_of_files = [
    
    'settings.py',
    'setup.toml',
    'README.md',
    'requirements.txt',
    'main.py',
    'LICENSE',
    'Dockerfile',
    '.gitignore',
    'Makefile',
    'tests/test_main.py',
    'tests/__init__.py',
    'src/__init__.py',
    'MANIFEST.in',
    '.dockerignore',
    '.gitattributes',
    '.editorconfig',
    '.bumpversion.cfg',
    'docker-compose.yml',
    'app.py',
    'src/__init__.py',
    'src/constant/__init__.py',
    'src/utils.py/__init__.py',
    'src/utils.py/common.py',
    'database/config.yml',
    'src/exception/__init__.py',
    'src/logger/__init__.py',
    'src/pipeline/__init__.py',
    'src/pipeline/inference_pipeline.py',
    'src/components/__init__.py',
    'src/components/data_fetching.py',
    'src/components/data_transformation.py',
    'src/components/data_insertion_database.py',
    'src/entity/__init__.py',
    'src/entity/config.py',
    'artifact/DataFetchArtifacts'
]


def create_file():
    
    for file in list_of_files:
        directory = os.path.dirname(file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('')
            print(f'Created {file}')
        else:
            print(f'{file} File already created')
            
            
create_file()