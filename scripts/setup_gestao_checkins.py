import os
import shutil

workspace = r"c:\Users\jo_da\OneDrive\Área de Trabalho\V4\builders-hub-main"
bases_dir = os.path.join(workspace, "bases")
template_dir = os.path.join(bases_dir, "_template")
project_dir = os.path.join(bases_dir, "gestao-checkins")

if not os.path.exists(project_dir):
    if os.path.exists(template_dir):
        shutil.copytree(template_dir, project_dir)
    else:
        os.makedirs(os.path.join(project_dir, "dados"))
        os.makedirs(os.path.join(project_dir, "docs"))
        os.makedirs(os.path.join(project_dir, "referencias"))

env_example = os.path.join(project_dir, ".env.example")
env_file = os.path.join(project_dir, ".env")
if os.path.exists(env_example):
    shutil.copy(env_example, env_file)
elif not os.path.exists(env_file):
    open(env_file, 'w').close()

old_dir = r"C:\Users\jo_da\OneDrive\Área de Trabalho\Gestão\Check-ins"
new_data_dir = os.path.join(project_dir, "dados")

if not os.path.exists(new_data_dir):
    os.makedirs(new_data_dir)

if os.path.exists(old_dir):
    for f in os.listdir(old_dir):
        # We migrate JSON state and CSV files mostly.
        # It's better to bring all data files.
        if f.endswith('.json') or f.endswith('.csv'):
            shutil.copy(os.path.join(old_dir, f), os.path.join(new_data_dir, f))

print("Dados copiados para", new_data_dir)
