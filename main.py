import os
import sys
import pathlib
from rdflib import Graph, Namespace, RDF, RDFS, Literal
from rdflib.namespace import NamespaceManager

# Use tkinter for GUI folder selection
if sys.version_info[0] < 3:
    import Tkinter as tk
    import tkFileDialog as filedialog
    from urllib import quote
else:
    import tkinter as tk
    from tkinter import filedialog
    from urllib.parse import quote

def get_folder_path():
    """Prompt the user to select a folder via GUI."""
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return folder_selected

def sanitize_ncname(name):
    """Sanitize a string to be a valid NCName for RDF/XML serialization."""
    import re
    # Replace '/' with '__' to indicate hierarchy
    name = name.replace('/', '__')
    # Replace leading '.' with 'dot_'
    name = re.sub(r'^\.+', 'dot_', name)
    # Replace any remaining invalid characters with '_'
    name = re.sub(r'[^A-Za-z0-9_\-\.]', '_', name)
    # If the first character is not a letter or underscore, prepend 'n'
    if not re.match(r'^[A-Za-z_]', name):
        name = 'n' + name
    return name

def traverse_directory(base_path, graph, parent_class_uri=None):
    base_path = pathlib.Path(base_path)
    base_name = base_path.name

    # Create a URI for the current folder using relative path
    relative_path = base_path.relative_to(root_path)
    if str(relative_path) == '.':
        uri_path = 'root'
    else:
        uri_path = str(relative_path).replace(os.sep, '/')
    local_name = sanitize_ncname(uri_path)
    base_uri = fs[local_name]

    if base_name == '':
        graph.add((base_uri, RDFS.label, Literal('Root')))
    else:
        graph.add((base_uri, RDFS.label, Literal(base_name)))

    graph.add((base_uri, RDF.type, RDFS.Class))

    # Include subclass relationship
    if parent_class_uri:
        graph.add((base_uri, RDFS.subClassOf, parent_class_uri))

    try:
        entries = list(base_path.iterdir())
    except (PermissionError, OSError):
        return

    for entry in entries:
        entry_name = entry.name

        if entry.is_dir():
            traverse_directory(entry, graph, base_uri)
        else:
            # Treat files as an individual, adding type and label and relationship to parent folder
            file_uri = fs[sanitize_ncname(entry_name)]
            graph.add((file_uri, RDF.type, fs.File))
            graph.add((file_uri, RDFS.label, Literal(entry_name)))
            graph.add((base_uri, fs.containsFile, file_uri))
            graph.add((file_uri, fs.isContainedIn, base_uri))

if __name__ == "__main__":
    fs_namespace = "http://example.org/filesystem#"
    fs = Namespace(fs_namespace)

    g = Graph()

    namespace_manager = NamespaceManager(g)
    namespace_manager.bind('fs', fs)
    namespace_manager.bind('rdf', RDF)
    namespace_manager.bind('rdfs', RDFS)
    g.namespace_manager = namespace_manager

    g.add((fs.containsFile, RDF.type, RDF.Property))
    g.add((fs.containsFile, RDFS.label, Literal("containsFile")))
    g.add((fs.isContainedIn, RDF.type, RDF.Property))
    g.add((fs.isContainedIn, RDFS.label, Literal("isContainedIn")))

    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = get_folder_path()

    if not folder_path:
        print("No folder selected.")
        sys.exit(1)

    # Set the root path for relative URI calculation
    root_path = pathlib.Path(folder_path)

    traverse_directory(root_path, g)

    # Serialize the graph to RDF/XML
    output_file = "folder_structure.rdf"
    g.serialize(destination=output_file, format='pretty-xml')

    print("RDF data has been written to {}".format(output_file))
