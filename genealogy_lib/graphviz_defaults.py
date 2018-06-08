sing_colors = [
    "#FF0000",
    "#0000FF",
]
trait_shapes = [
    "circle",
    "triangle"
]
default_graphviz_parameters = {

    "graph-attributes" : [
        ("nodesep", "0.1"),
        ("ranksep", "1"),
        ("size", "5"),
        ("ratio", "fill")
    ],

    "node-attributes" : [
        ("style", "filled"),
        ("fontcolor", "white"),
        ("shape", "circle"),
        ("width", "1"),
        ("fontsize", "20.0")
    ],
    "dot-command": "dot",

    "edge-attributes" : [
        ("penwidth", "4")
    ],

    "cs-to-color" : (
        lambda cs: sing_colors[cs[0]]
    ),
    "cs-to-shape" : (
        lambda cs: trait_shapes[cs[1]] if len(cs) == 2 else trait_shapes[0]
    )
}
