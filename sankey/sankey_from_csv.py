import plotly.graph_objects as go
import webcolors
import csv
import ast

import csv
import ast

def csv_to_dict(filename):
    """Load a CSV file into a dictionary where each column is a key and each row is a list of values for that key.
       Rows that contain string representations of lists are evaluated and converted into lists."""

    try:
        with open(filename, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            
            # Check if the CSV file has headers
            if reader.fieldnames is None:
                raise ValueError("CSV file does not have headers.")
            
            # Initialize lists for each header
            dict_of_columns = {fieldname: [] for fieldname in reader.fieldnames}
            
            for row in reader:
                for key in reader.fieldnames:
                    value = row[key]
                    try:
                        # Try to parse a list from the string, otherwise keep the original value
                        dict_of_columns[key].append(ast.literal_eval(value))
                    except (ValueError, SyntaxError):
                        # If the value can't be parsed as a list, add the string as-is
                        dict_of_columns[key].append(value)

        return dict_of_columns

    except FileNotFoundError as e:
        raise FileNotFoundError(f"File '{filename}' not found.") from e
    except Exception as e:
        raise Exception(f"An error occurred: {e}") from e

# Define a function to calculate the average color between two nodes for use in styling links in the Sankey diagram.
def average_color(color1, color2):
    """Return the average of two colors given as CSS color names."""
    # Convert color names to RGB tuples using webcolors.name_to_rgb()
    rgb1 = webcolors.name_to_rgb(color1)
    rgb2 = webcolors.name_to_rgb(color2)
    # Calculate the average of each pair of RGB values to get the combined color
    avg_rgb = tuple(int((c1 + c2) / 2) for c1, c2 in zip(rgb1, rgb2))
    # Convert averaged RGB tuple back to a hex color string
    return '#{:02x}{:02x}{:02x}'.format(*avg_rgb)

# Load the nodes and links from the CSV files
nodes = csv_to_dict('nodes.csv')
# Keep only label,color,customdata from the dict
nodes = {k: nodes[k] for k in ('label','color','customdata')}
links = csv_to_dict('links.csv')
# Keep only source,target,value from the dict
links = {k: links[k] for k in ('source','target','value')}

## Create a list of colors for the links by averaging the colors of the source and target nodes for each link.
links['color'] = [
    average_color(nodes['color'][src], nodes['color'][tgt])
    for src, tgt in zip(links['source'], links['target'])
]


# The following block of code (currently not used) would create a list of link labels in the format 'node1 -> node2'.
# This can be useful for annotating the links in the Sankey diagram with their source and target node names.
# links['label'] = [
#     f"{nodes['label'][src]} → {nodes['label'][tgt]}"
#     for src, tgt in zip(links['source'], links['target'])
# ]

# Specify other node and link options
node_options = {
    'pad': 15,  # Space between nodes
    'thickness': 40,  # Thickness of nodes
    'line': {
        'color': "black",  # Color of the boundary line of nodes
        'width': 0.5  # Width of the boundary line of nodes
    },
    # Hovertemplate for displaying additional information when hovering over nodes
    'hovertemplate': '%{label} : %{customdata[1]}<br>Definition: %{customdata[0]}<extra></extra>'
}

link_options = {
    'hovertemplate': '%{source.label} → %{target.label}<extra></extra>'
}

# Create the Sankey diagram figure using Plotly's go.Figure and adding a Sankey chart type.
fig = go.Figure(
    data=[
        go.Sankey(
            node={**nodes,**node_options},  # Nodes configuration dict
            link={**links,**link_options},  # Links configuration dict
            valueformat=".0f",  # Format link values as integers without decimal places
            valuesuffix="",  # No suffix added to the link values
            arrangement="snap",  # Places the nodes such that they snap into place
        )
    ]
)

# Update the layout of the figure to include a title and adjust the figure dimensions.
fig.update_layout(
    title={
        'text': "Change Example",      # Title text
        'x': 0.5,                      # X-position for centered alignment of the title
        'y': 0.97,                     # Y-position for the title to be placed at the top of the figure
        'xanchor': 'center',           # Ensures the title is centered on the x-position
        'yanchor': 'top',              # Anchors the title to the top position
        'font': {'size': 24},          # Sets the font size for the title
    },
    width=1500,                        # Width of the figure in pixels
    height=1000,                       # Height of the figure in pixels
    font=dict(size=16, color='black'), # Default font properties for other text elements
    # Additional layout properties can be set here if needed
)

# Show the final Sankey diagram in a browser or inline in a notebook environment.
fig.show()






