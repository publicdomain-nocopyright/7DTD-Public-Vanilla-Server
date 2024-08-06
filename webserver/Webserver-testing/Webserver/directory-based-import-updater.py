import os
import ast
import re
import json
import difflib

def get_py_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.py')]

def get_module_names(directory):
    return {os.path.splitext(f)[0]: f for f in get_py_files(directory)}

def take_snapshot(directory):
    snapshot = get_module_names(directory)
    snapshot_file = os.path.join(directory, '.module_snapshot.json')
    with open(snapshot_file, 'w') as f:
        json.dump(snapshot, f)
    return snapshot

def load_snapshot(directory):
    snapshot_file = os.path.join(directory, '.module_snapshot.json')
    if os.path.exists(snapshot_file):
        with open(snapshot_file, 'r') as f:
            return json.load(f)
    return None

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

def get_correct_filename(name, module_names):
    parts = name.split('.')
    corrected_parts = []
    for part in parts:
        corrected = module_names.get(part, part)
        corrected_parts.append(corrected)
    return '.'.join(corrected_parts)

def process_file(file_path, old_module_names, new_module_names):
    with open(file_path, 'r') as file:
        content = file.read()
        tree = ast.parse(content)

    lines = content.splitlines()
    changes = []
    imports = find_import_statements(tree)

    for import_info in imports:
        if import_info[2] == 'import':
            lineno, col_offset, _, module, as_name = import_info
            old_module = get_correct_filename(module, old_module_names)
            new_module = get_correct_filename(module, new_module_names)
            if new_module != old_module and new_module in new_module_names:
                old_line = lines[lineno - 1]
                new_line = old_line.replace(old_module, new_module)
                if new_line != old_line:
                    changes.append((lineno - 1, old_line, new_line))
                    lines[lineno - 1] = new_line
        elif import_info[2] == 'from':
            lineno, col_offset, _, from_module, import_name, as_name = import_info
            old_from = get_correct_filename(from_module, old_module_names)
            new_from = get_correct_filename(from_module, new_module_names)
            if new_from != old_from and new_from in new_module_names:
                old_line = lines[lineno - 1]
                new_line = old_line.replace(f"from {old_from}", f"from {new_from}")
                if new_line != old_line:
                    changes.append((lineno - 1, old_line, new_line))
                    lines[lineno - 1] = new_line

    return lines, changes

def update_imports(directory, old_module_names, new_module_names):
    py_files = get_py_files(directory)
    all_changes = {}

    for file in py_files:
        file_path = os.path.join(directory, file)
        new_content, changes = process_file(file_path, old_module_names, new_module_names)
        if changes:
            all_changes[file] = (new_content, changes)

    return all_changes

def show_changes(all_changes):
    if not all_changes:
        print("No changes needed.")
        return False

    print("The following changes will be made:")
    for file, (new_content, changes) in all_changes.items():
        print(f"\nFile: {file}")
        for line_num, old, new in changes:
            print(f"  Line {line_num + 1}:")
            print("    " + "\n    ".join(difflib.ndiff([old], [new])))

    return True

def apply_changes(directory, all_changes):
    for file, (new_content, _) in all_changes.items():
        with open(os.path.join(directory, file), 'w') as f:
            f.write('\n'.join(new_content))
    print("Changes applied successfully.")

def main():
    directory = '.'  # Current directory
    old_module_names = load_snapshot(directory)
    new_module_names = get_module_names(directory)

    if old_module_names is None or old_module_names != new_module_names:
        if old_module_names is None:
            print("No previous snapshot found. Taking initial snapshot...")
        else:
            print("Changes detected in directory structure.")
        
        all_changes = update_imports(directory, old_module_names or {}, new_module_names)
        
        if show_changes(all_changes):
            confirm = input("\nDo you want to apply these changes? (y/n): ").lower()
            if confirm == 'y':
                apply_changes(directory, all_changes)
            else:
                print("No changes were made.")
        
        take_snapshot(directory)
    else:
        print("No changes detected in directory structure.")

if __name__ == "__main__":
    main()