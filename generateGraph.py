import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import numpy as np
import json
import os

try:
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the path to the JSON file
    json_file_path = os.path.join(script_dir, 'Z_FlickerValues.json')

    # Print the absolute path to verify it
    print("JSON file path: {}".format(json_file_path))

    # Opening JSON file
    with open(json_file_path, 'r') as f:
        # Returns JSON object as a dictionary
        data = json.load(f)
    
except Exception as e:
    print("An error occurred: {}".format(e))
    sys.exit(1)  # Exit the script if an error occurs

# Extract posX and posY values into separate lists
x = [float(item['posX']) for item in data]
y = [float(item['posY']) for item in data]
timeline = [int(item['id']) for item in data]

# Plotting the points
fig, ax = plt.subplots(figsize=(16, 10))
scatter_x = plt.scatter(
    x=timeline,
    y=x,
    c="blue",
    s=40,
)
scatter_y = plt.scatter(
    x=timeline,
    y=y,
    c="blue",
    s=40,
)
plt.plot(timeline, x, label='Value in X', marker='o')
plt.plot(timeline, y, label='Value in Y', marker='.', linestyle='--')

legend = plt.legend(loc='upper left')
# Naming the x axis
plt.xlabel('Frames range')
# Naming the y axis
plt.ylabel('Flicker value range')

# Adding grid
plt.grid(True)
# Giving a title to my graph
plt.title('Flicker graph!')

# Resize the current figure window
fig.set_size_inches(16, 7)

# Set more ticks on x and y axes
plt.xticks(range(timeline[-1]))

# Function to print current figure size and check if width is less than 7 inches
def on_resize(event):
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

# Connect the resize event
fig.canvas.mpl_connect('resize_event', on_resize)

annotations = []
for i in range(len(timeline)):
    annotation = ax.annotate(
        'x: {:.3f}\ny: {:.3f}'.format(x[i], y[i]), 
        (timeline[i], y[i]), 
        textcoords="offset points", 
        xytext=(10,10), 
        ha='center',
        bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='yellow'),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5'),
    )
    annotations.append(annotation)
    annotation.set_visible(False)

def hover(event): 
    visible_any_annotation = False
    if event.inaxes == ax:
        is_contained_x, annotation_index_x = scatter_x.contains(event)
        is_contained_y, annotation_index_y = scatter_y.contains(event)
        
        if is_contained_x or is_contained_y:
            # Extract index of the point under cursor
            index_value = annotation_index_x['ind'][0] if is_contained_x else annotation_index_y['ind'][0]
            # Get the location of the point
            data_point_location = scatter_x.get_offsets()[index_value] if is_contained_x else scatter_y.get_offsets()[index_value]
            # Update annotation with new position and text
            annotations[index_value].xy = data_point_location
            text_label = 'x: {:.3f} | y: {:.3f}'.format(x[index_value], y[index_value]) 
            annotations[index_value].set_text(text_label)
            annotations[index_value].set_visible(True)
            visible_any_annotation = True
            legend.set_visible(False)
        if not visible_any_annotation:
            for annotation in annotations:
                annotation.set_visible(False)
            legend.set_visible(True)
        fig.canvas.draw_idle()

fig.canvas.mpl_connect('motion_notify_event', hover)

# Text Box - Set fixed y-axis limits
ylimit = 1
ax.set_ylim(0, ylimit)  # Adjust these values as per your data range

def updateYLimit(text):
    try:
        ylimit = float(text)
        ax.set_ylim(0, ylimit)
        plt.draw()
    except ValueError:
        print("Invalid input for vertical limit. Please enter a valid number.")

plt.subplots_adjust(bottom=0.2)
ax_box = plt.axes([0.2, 0.075, 0.02, 0.04])
textBox = TextBox(ax_box, "Set Flicker Value Range: ", initial="1")

textBox.on_submit(updateYLimit)

# Text Box - Set Amplitude 
ax_box2 = plt.axes([0.2, 0.025, 0.02, 0.04])
textBox2 = TextBox(ax_box2, "Set values Aplitude %: ")

#textBox2.on_submit()

# Zoom In and Out buttons
ax_zoom_in = plt.axes([0.8, 0.01, 0.15, 0.05])
ax_zoom_out = plt.axes([0.65, 0.01, 0.15, 0.05])
button_zoom_in = Button(ax_zoom_in, 'Zoom In')
button_zoom_out = Button(ax_zoom_out, 'Zoom Out')

def zoom_in(event):
    xlims = ax.get_xlim()
    new_xlims = [xlims[0] * 1.1, xlims[1] * 0.9]
    ax.set_xlim(new_xlims)
    plt.draw()

def zoom_out(event):
    xlims = ax.get_xlim()
    new_xlims = [xlims[0] * 0.9, xlims[1] * 1.1]
    ax.set_xlim(new_xlims)
    plt.draw()

button_zoom_in.on_clicked(zoom_in)
button_zoom_out.on_clicked(zoom_out)

# Function to show the plot
plt.show()
