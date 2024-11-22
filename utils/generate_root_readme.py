import os

# Caminho da pasta atual
current_directory = os.getcwd()

# Lista de subpastas excluindo 'venv'
subfolders = [folder for folder in os.listdir(current_directory) if os.path.isdir(folder) and folder not in ['.git','venv','utils','files']]

# Cria uma string para o conteúdo do README
readme_content = ""
for folder in subfolders:
    # Caminho do README.md da subpasta
    readme_path = os.path.join(current_directory, folder, "README.md")
    
    # Verificar se o README.md existe e extrair o título e objetivo
    formatted_name = folder.replace("_", " ").title()
    objective_text = ""
    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            lines = f.readlines()
            if lines:
                # Extrair o título
                first_line = lines[0].strip()
                if first_line.startswith("# "):
                    formatted_name = first_line[2:].strip()
                
                # Extrair a seção "## Objective"
                for i, line in enumerate(lines):
                    if line.strip().lower() == "## objective":
                        if i + 1 < len(lines):
                            objective_text = lines[i + 1].strip()
                        break
    
    # Gerar a URL
    url = f"https://github.com/Patotricks15/Generative-AI-projects/tree/main/{folder}"
    # Adicionar ao conteúdo do README
    readme_content += f"[{formatted_name}]({url})\n\n"
    if objective_text:
        readme_content += f"Objective: {objective_text}\n"
    readme_content += "\n\n"

# Criar o arquivo README.md com o conteúdo gerado
with open("README.md", "w") as readme_file:
    readme_file.write(readme_content)

print("README.md criado com sucesso!")
