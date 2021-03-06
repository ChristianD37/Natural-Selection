import os, json

def load_controls():
    controls = None
    with open(os.path.join('util','controls.json'), 'r+') as file:
        controls = json.load(file)
    return controls

def write_controls(new_controls):
    with open(os.path.join('util','controls.json'), 'w') as file:
        json.dump(new_controls, file)

def write_save(dir,data):
    with open(os.path.join(dir,'save.json'), 'w') as file:
        json.dump(data, file)