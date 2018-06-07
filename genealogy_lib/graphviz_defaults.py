sing_colors = [
    "#FF0000",
    "#0000FF",
]
double_colors = [
    [
        "#ff4040",
        "#4040ff",
    ],
    [
        "#bf0000",
        "#0000b2",
    ]
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

    "edge-attributes" : [
        ("penwidth", "4")
    ],

    "cs-to-color" : (
        lambda cs: sing_colors[cs[0]] if len(cs) == 1 else double_colors[cs[0]][cs[1]]
    )

}
