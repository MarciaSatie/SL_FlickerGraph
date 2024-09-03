import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox, CheckButtons
import numpy as np
import json
import os
import sys


# **********************   Functions Begin ************************************************************
def load_json_data(filepath):
    """Load JSON data from a file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print("An error occurred: {}".format(e))
        sys.exit(1)

def initialize_plot(data):
    """Initialize the plot with data."""
    x = [float(item['posX']) for item in data]
    y = [float(item['posY']) for item in data]
    timeline = [int(item['id']) for item in data]
    n = [float(item.get('posN', 0)) for item in data]

    fig, ax = plt.subplots(figsize=(20, 15))

    scatter_x = plt.scatter(timeline, x, c="blue", s=40, label='Value in X')
    scatter_y = plt.scatter(timeline, y, c="green", s=40, label='Value in Y')
    scatter_n = plt.scatter(timeline, n, c="darkgoldenrod", s=40, label='Value in N')

    line_x, = plt.plot(timeline, x, label='Value in X', marker='o', color='blue')
    line_y, = plt.plot(timeline, y, label='Value in Y', marker='.', linestyle='--', color='green')
    line_n, = plt.plot(timeline, n, label='Value in N', marker='*', linestyle='--', color='darkgoldenrod')

    legend = plt.legend(loc='bottom left')

    plt.xlabel('Frames range')
    #plt.ylabel('Flicker value range')
    plt.grid(True)
    plt.title('Flicker graph!')
    fig.set_size_inches(16, 7)
    # Text Box - Set fixed y-axis limits
    ylimit = 1
    ax.set_ylim(-ylimit, ylimit)
    plt.xticks(range(timeline[-1] + 1))

    return fig, ax, scatter_x, scatter_y, scatter_n, line_x, line_y, line_n, legend, timeline

def on_resize(event, ax, timeline):
    """Handle figure resize event."""
    current_size = fig.get_size_inches()
    print("Current figure size: {} x {}".format(current_size[0], current_size[1]))

    if current_size[0] >= 15:
        ax.set_xticks(np.arange(0, len(timeline), step=1))
        plt.draw()
    elif current_size[0] < 15 and current_size[0] > 8:
        print("Warning: Window width is smaller than 15 inches.")
        ax.set_xticks(np.arange(0, len(timeline), step=2))
        plt.draw()
    elif current_size[0] <= 8:
        print("Warning: Window width is smaller than 8 inches.")
        ax.set_xticks(np.arange(0, len(timeline), step=10))
        plt.draw()

def hover(event, scatter_x, scatter_y, scatter_n, annotations, fig):
    """Update annotations on hover."""
    if event.inaxes == ax:
        visible_any_annotation = False
        is_contained_x, index_x = scatter_x.contains(event)
        is_contained_y, index_y = scatter_y.contains(event)
        is_contained_n, index_n = scatter_n.contains(event)

        if is_contained_x or is_contained_y or is_contained_n:
            index_value = index_x['ind'][0] if is_contained_x else index_y['ind'][0] if is_contained_y else index_n['ind'][0]
            data_point_location = scatter_x.get_offsets()[index_value] if is_contained_x else scatter_y.get_offsets()[index_value] if is_contained_y else scatter_n.get_offsets()[index_value]
            annotations[index_value].xy = data_point_location
            text_label = u'x: {:.3f} | y: {:.3f} | n: {:.3f}'.format(x[index_value], y[index_value], n[index_value])
            annotations[index_value].set_text(text_label)
            annotations[index_value].set_visible(True)
            visible_any_annotation = True

        if not visible_any_annotation:
            for annotation in annotations:
                annotation.set_visible(False)
        fig.canvas.draw_idle()

def update_y_limit(text, ax):
    """Update the y-axis (graph's height) limit based on input."""
    try:
        ylimit = float(text)
        ax.set_ylim(-ylimit, ylimit)
        plt.draw()
    except ValueError:
        print ("Invalid input for vertical limit. Please enter a valid number.")

def update_amplitude(text, scatter_x, scatter_y, scatter_n, line_x, line_y, line_n):
    """Update the amplitude of the data points based on input."""
    global new_x, new_y, new_n
    try:
        percentage = float(text)
        new_x = [val * (1 + percentage / 100.0) for val in new_x]
        new_y = [val * (1 + percentage / 100.0) for val in new_y]
        new_n = [val * (1 + percentage / 100.0) for val in new_n]

        scatter_x.set_offsets(np.c_[timeline, new_x])
        scatter_y.set_offsets(np.c_[timeline, new_y])
        scatter_n.set_offsets(np.c_[timeline, new_n])

        line_x.set_ydata(new_x)
        line_y.set_ydata(new_y)
        line_n.set_ydata(new_n)

        plt.draw()
    except ValueError:
        print ("Invalid input for amplitude percentage. Please enter a valid number.")

def reset_amplitude(event, scatter_x, scatter_y, scatter_n, line_x, line_y, line_n):
    """Reset the amplitude to original values."""
    global new_x, new_y, new_n
    new_x = list(x)
    new_y = list(y)
    new_n = list(n)

    scatter_x.set_offsets(np.c_[timeline, new_x])
    scatter_y.set_offsets(np.c_[timeline, new_y])
    scatter_n.set_offsets(np.c_[timeline, new_n])

    line_x.set_ydata(new_x)
    line_y.set_ydata(new_y)
    line_n.set_ydata(new_n)

    plt.draw()

def zoom(event, ax, zoom_in=True):
    """Zoom in or out of the plot."""
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()
    factor = 0.8 if zoom_in else 1.2
    ax.set_xlim([x * factor for x in xlims])
    ax.set_ylim([y * factor for y in ylims])
    plt.draw()

def toggle_visibility(label, scatter_x, scatter_y, scatter_n, line_x, line_y, line_n, legend):
    """Toggle the visibility of plot elements."""
    if label == 'Show X':
        scatter_x.set_visible(not scatter_x.get_visible())
        line_x.set_visible(not line_x.get_visible())
    elif label == 'Show Y':
        scatter_y.set_visible(not scatter_y.get_visible())
        line_y.set_visible(not line_y.get_visible())
    elif label == 'Show N':
        scatter_n.set_visible(not scatter_n.get_visible())
        line_n.set_visible(not line_n.get_visible())
    elif label == 'Show Legend':
        legend.set_visible(not legend.get_visible())
    plt.draw()

# **********************   Functions End ************************************************************
# **********************   Main Begin ***************************************************************
# Main script
if __name__ == "__main__":
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the path to the JSON file
    json_file_path = os.path.join(script_dir, 'Z_FlickerValues.json')
    print("JSON file path: {}".format(json_file_path))

    data = load_json_data(json_file_path)
    fig, ax, scatter_x, scatter_y, scatter_n, line_x, line_y, line_n, legend, timeline = initialize_plot(data)

    # Extract posX, posY, and posN values into separate lists
    global x, y, n, new_x, new_y, new_n
    x = [float(item['posX']) for item in data]
    y = [float(item['posY']) for item in data]
    n = [float(item.get('posN', 0)) for item in data]
    new_x = list(x)
    new_y = list(y)
    new_n = list(n)

    annotations = []
    for i in range(len(timeline)):
        annotation = ax.annotate(
            u'x: {:.3f}\ny: {:.3f}\nn: {:.3f}'.format(x[i], y[i], n[i]), 
            (timeline[i], y[i]), 
            textcoords="offset points", 
            xytext=(10,10), 
            ha='center',
            bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='yellow'),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5'),
        )
        annotations.append(annotation)
        annotation.set_visible(False)

    # Update canvas, based on mouse interection.
    fig.canvas.mpl_connect('resize_event', lambda event: on_resize(event, ax, timeline))
    fig.canvas.mpl_connect('motion_notify_event', lambda event: hover(event, scatter_x, scatter_y, scatter_n, annotations, fig))

    # check box to enable and disable line gtraph and legend.
    ax_check = plt.axes([0.01, 0.7, 0.08, 0.2])
    check_buttons = CheckButtons(ax_check, ['Show X', 'Show Y', 'Show N', 'Show Legend'], [True, True, True, True])
    check_buttons.on_clicked(lambda label: toggle_visibility(label, scatter_x, scatter_y, scatter_n, line_x, line_y, line_n, legend))

    pos = 0.22
    # update graph height 
    plt.subplots_adjust(bottom=0.35)
    ax_box = plt.axes([0.2, pos, 0.02, 0.05])
    textBox = TextBox(ax_box, "Set Flicker Value Range: ", initial="1")
    textBox.on_submit(lambda text: update_y_limit(text, ax))

    # Update aplitude values in %
    ax_box2 = plt.axes([0.2, pos-0.05, 0.02, 0.05])
    textBox2 = TextBox(ax_box2, "Set Amplitude %: ", initial="0")
    textBox2.on_submit(lambda text: update_amplitude(text, scatter_x, scatter_y, scatter_n, line_x, line_y, line_n))

    # Reset amplitude values to the original
    ax_reset = plt.axes([0.23, pos-0.05, 0.08, 0.05])
    reset_button = Button(ax_reset, 'Reset')
    reset_button.on_clicked(lambda event: reset_amplitude(event, scatter_x, scatter_y, scatter_n, line_x, line_y, line_n))

    ax_zoom_in = plt.axes([0.7, pos, 0.08, 0.05])
    zoom_in_button = Button(ax_zoom_in, 'Zoom In')
    zoom_in_button.on_clicked(lambda event: zoom(event, ax, zoom_in=True))

    ax_zoom_out = plt.axes([0.8, pos, 0.08, 0.05])
    zoom_out_button = Button(ax_zoom_out, 'Zoom Out')
    zoom_out_button.on_clicked(lambda event: zoom(event, ax, zoom_in=False))

 
    plt.show()
    
# **********************   Main End ***************************************************************