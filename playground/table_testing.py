from table import Table, TableFormatError
import yaml

# load in yaml file
file =  "E:\\Projects\\Python\\dnd-tools\\tables\\example.yaml"
loaded = []

with open(file, 'r') as fobj:
    tables = list(yaml.load_all(fobj, Loader=yaml.FullLoader))
    try:
        for t in tables:
            loaded.append(Table(file, t))
    except Exception as e:
        print(e) 

for each in loaded:
    print(each.getName())
    print(each.group)