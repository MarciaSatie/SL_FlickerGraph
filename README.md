Flicker Graph Plotter

This script generates an interactive graph from JSON data containing posX, posY, and id values.
It is useful for visualizing data over a timeline, comparing two value ranges (X and Y), and exploring points interactively.

📌 Features

Loads data from a JSON file (Z_FlickerValues.json).

Plots X and Y values over the timeline (id).

Displays both scatter points and line plots for clarity.

Interactive hover tooltips showing posX and posY for each frame.

Zoom In / Zoom Out buttons to adjust the timeline range.

Grid, legends, and labeled axes for better readability.

📂 Input Data Format

The script expects a JSON file named Z_FlickerValues.json, containing an array of objects with at least the following keys:

[
  {
    "id": "0",
    "posX": "1.234",
    "posY": "2.345"
  },
  {
    "id": "1",
    "posX": "1.567",
    "posY": "2.678"
  }
]


id → frame or timeline index (integer).

posX → numeric value for X-axis data.

posY → numeric value for Y-axis data.

▶️ How to Run

Make sure you have Python 3 installed.

Install required dependencies:

pip install matplotlib numpy


Place your JSON file (Z_FlickerValues.json) in the same directory as the script.

Run the script:

python flicker_graph.py

📊 Example Output

The script produces a graph with:

Blue scatter points for X and Y data.

Solid line for X values.

Dashed line for Y values.

Tooltips with (x, y) values when hovering over points.

Buttons for zooming in/out on the timeline.

🛠️ Customization

Change the JSON filename in the script if your data file is named differently.

Modify colors, markers, or line styles in the plotting section to suit your needs.

Adjust zoom button behavior inside zoom_in and zoom_out functions.

📜 License

You can adapt and use this script freely for personal or project work.
