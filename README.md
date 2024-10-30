# RDF Filesystem Project

The **RDF Filesystem Project** in Python transforms a traditional file system structure into an RDF graph, representing folders and files as semantic entities. This project leverages the RDFLib library and uses a GUI-based folder selection (via tkinter) to allow users to pick the directory to represent semantically.

## Features

- **Semantic File Representation**: Generates an RDF graph where folders and files are represented as classes and instances with hierarchical relationships.
- **SPARQL-ready Data**: Outputs an RDF/XML file that can be queried with SPARQL for insights into file structure.
- **Ontology Support**: Custom properties, such as `containsFile` and `isContainedIn`, create a semantically rich model.
- **User-Friendly Folder Selection**: The tkinter GUI allows for easy folder selection.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/sophisid/FileSystemRDF.git
    cd FileSystemRDF
    ```

2. Install the required Python packages:
    ```bash
    pip install rdflib
    ```

## Usage

1. **Run the script**:
   ```bash
   python rdf_filesystem.py
   ```

2. **Select a folder**:
   - If no folder path is provided via command line arguments, a GUI dialog will open, allowing the user to select the folder.

3. **Output**:
   - The script will generate an RDF/XML file named `folder_structure.rdf` in the project directory, representing the selected folder and its contents.

## Code Structure

- **Folder and File Nodes**: Each folder is represented as an `RDFS.Class`, and each file as an individual with the `fs:File` type.
- **Properties**: The script defines:
  - `fs:containsFile`: indicating a folder contains a file
  - `fs:isContainedIn`: indicating a file is contained within a folder
- **Namespace**: Uses a base namespace `http://example.org/filesystem#`.

## Example

```python
python rdf_filesystem.py /path/to/your/folder
```

Alternatively, select the folder from a dialog when running:
```bash
python rdf_filesystem.py
```

## Sample RDF Output

```xml
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
         xmlns:fs="http://example.org/filesystem#">

  <!-- Root folder -->
  <fs:root rdf:about="http://example.org/filesystem#root">
    <rdfs:label>Root</rdfs:label>
  </fs:root>
  
  <!-- File instance -->
  <fs:File rdf:about="http://example.org/filesystem#sample_file">
    <rdfs:label>sample_file.txt</rdfs:label>
    <fs:isContainedIn rdf:resource="http://example.org/filesystem#root"/>
  </fs:File>

</rdf:RDF>
```
