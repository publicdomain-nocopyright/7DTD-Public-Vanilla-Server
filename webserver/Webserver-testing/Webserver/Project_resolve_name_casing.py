#git rm -r --cached .
#git add --all .
# https://stackoverflow.com/questions/17683458/how-do-i-commit-case-sensitive-only-filename-changes-in-git/55541435#55541435

import os
import re
import ast

def get_py_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.py')]
git rm -r --cached .
git add --all .
def get_module_names(directory):
    return {os.path.splitext(f)[0] for f in get_py_files(directory)}

def find_import_statements(tree):
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((node.lineno, node.col_offset, 'import', alias.name, alias.asname))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imports.append((node.lineno, node.col_offset, 'from', module, alias.name, alias.asname))
    return imports

def get_correct_casing(name, module_names):
    parts = name.split('.')
    corrected_parts = []
    for part in parts:
        lower_part = part.lower()
        corrected = next((m for m in module_names if m.lower() == lower_part), part)
        corrected_parts.append(corrected)
    return '.'.join(corrected_parts)

def process_file(file_path, module_names):
    with open(file_path, 'r') as file:
        content = file.read()
        tree = ast.parse(content)

    lines = content.splitlines()
    changes = []
    imports = find_import_statements(tree)

    # Process import statements
    for import_info in imports:
        if import_info[2] == 'import':
            lineno, col_offset, _, module, as_name = import_info
            correct_module = get_correct_casing(module, module_names)
            if correct_module != module:
                old_line = lines[lineno - 1]
                indent = old_line[:col_offset]
                old_import = old_line[col_offset:]
                new_import = old_import.replace(module, correct_module)
                new_line = f"{indent}{new_import}"
                changes.append((lineno - 1, old_line, new_line))
                lines[lineno - 1] = new_line
        else:  # from import
            lineno, col_offset, _, from_module, import_name, as_name = import_info
            correct_from = get_correct_casing(from_module, module_names)
            correct_import = get_correct_casing(import_name, module_names)
            if correct_from != from_module or correct_import != import_name:
                old_line = lines[lineno - 1]
                indent = old_line[:col_offset]
                old_import = old_line[col_offset:]
                new_import = old_import.replace(from_module, correct_from).replace(import_name, correct_import)
                new_line = f"{indent}{new_import}"
                changes.append((lineno - 1, old_line, new_line))
                lines[lineno - 1] = new_line

    # Process references in the code
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            for import_info in imports:
                if import_info[2] == 'import':
                    _, _, _, module, as_name = import_info
                    if node.id == (as_name or module.split('.')[-1]):
                        correct_module = get_correct_casing(module, module_names)
                        if correct_module != module:
                            old_line = lines[node.lineno - 1]
                            new_line = old_line[:node.col_offset] + correct_module.split('.')[-1] + old_line[node.col_offset + len(node.id):]
                            changes.append((node.lineno - 1, old_line, new_line))
                            lines[node.lineno - 1] = new_line
                elif import_info[2] == 'from':
                    _, _, _, from_module, import_name, as_name = import_info
                    if node.id == (as_name or import_name):
                        correct_import = get_correct_casing(import_name, module_names)
                        if correct_import != import_name:
                            old_line = lines[node.lineno - 1]
                            new_line = old_line[:node.col_offset] + correct_import + old_line[node.col_offset + len(node.id):]
                            changes.append((node.lineno - 1, old_line, new_line))
                            lines[node.lineno - 1] = new_line

    return lines, changes

def main():
    directory = '.'  # Current directory
    module_names = get_module_names(directory)
    py_files = get_py_files(directory)

    all_changes = {}

    for file in py_files:
        file_path = os.path.join(directory, file)
        new_content, changes = process_file(file_path, module_names)
        if changes:
            all_changes[file] = (new_content, changes)

    if not all_changes:
        print("No changes needed.")
        return

    print("The following changes will be made:")
    for file, (_, changes) in all_changes.items():
        print(f"\nFile: {file}")
        for line_num, old, new in changes:
            print(f"  Line {line_num + 1}:")
            print(f"    Old: {old}")
            print(f"    New: {new}")

    confirm = input("\nDo you want to apply these changes? (y/n): ").lower()
    if confirm == 'y':
        for file, (new_content, _) in all_changes.items():
            with open(os.path.join(directory, file), 'w') as f:
                f.write('\n'.join(new_content))
        print("Changes applied successfully.")
    else:
        print("No changes were made.")

if __name__ == "__main__":
    main()