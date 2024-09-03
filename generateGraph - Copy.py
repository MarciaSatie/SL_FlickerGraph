import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox, CheckButtons
import numpy as np
import json
import os
import sys

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

# Extract posX, posY, and posN values into separate lists
x = [float(item['posX']) for item in data]
y = [float(item['posY']) for item in data]
timeline = [int(item['id']) for item in data]
n = [float(item.get('posN', 0)) for item in data]

# Plotting the points
fig, ax = plt.subplots(figsize=(16, 10))
scatter_x = plt.scatter(
    x=timeline,
    y=x,
    c="blue",
    s=40,
    label='Value in X'
)
scatter_y = plt.scatter(
    x=timeline,
    y=y,
    c="green",
    s=40,
    label='Value in Y'
)
scatter_n = plt.scatter(
    x=timeline,
    y=n,
    c="darkgoldenrod",  # Dark yellow
    s=40,
    label='Value in N'
)
line_x, = plt.plot(timeline, x, label='Value in X', marker='o', color='blue')
line_y, = plt.plot(timeline, y, label='Value in Y', marker='.', linestyle='--', color='green')
line_n, = plt.plot(timeline, n, label='Value in N', marker='*', linestyle='--', color='darkgoldenrod')  # Dark yellow

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
plt.xticks(range(timeline[-1] + 1))  # Ensure ticks cover the entire x-axis range

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
        'x: {:.3f}\ny: {:.3f}\nn: {:.3f}'.format(x[i], y[i], n[i]), 
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
        is_contained_n, annotation_index_n = scatter_n.contains(event)
        
        if is_contained_x or is_contained_y or is_contained_n:
            # Extract index of the point under cursor
            if is_contained_x:
                index_value = annotation_index_x['ind'][0]
            elif is_contained_y:
                index_value = annotation_index_y['ind'][0]
            else:  # is_contained_n
                index_value = annotation_index_n['ind'][0]
            
            # Get the location of the point
            data_point_location = scatter_x.get_offsets()[index_value] if is_contained_x else scatter_y.get_offsets()[index_value] if is_contained_y else scatter_n.get_offsets()[index_value]
            
            # Update annotation with new position and text
            annotations[index_value].xy = data_point_location
            text_label = 'x: {:.3f} | y: {:.3f} | n: {:.3f}'.format(x[index_value], y[index_value], n[index_value])
            annotations[index_value].set_text(text_label)
            annotations[index_value].set_visible(True)
            visible_any_annotation = True
        if not visible_any_annotation:
            for annotation in annotations:
                annotation.set_visible(False)
        fig.canvas.draw_idle()

fig.canvas.mpl_connect('motion_notify_event', hover)

# Text Box - Set fixed y-axis limits
ylimit = 1
ax.set_ylim(-ylimit, ylimit)  # Adjust these values as per your data range

def updateYLimit(text):
    try:
        ylimit = float(text)
        ax.set_ylim(-ylimit, ylimit)
        plt.draw()
    except ValueError:
        print("Invalid input for vertical limit. Please enter a valid number.")

plt.subplots_adjust(bottom=0.35)  # Adjust bottom to make space for the check buttons
ax_box = plt.axes([0.2, 0.3, 0.15, 0.05])
textBox = TextBox(ax_box, "Set Flicker Value Range: ", initial="1")

textBox.on_submit(updateYLimit)

# Text Box - Set Amplitude 
ax_box2 = plt.axes([0.2, 0.25, 0.15, 0.05])
textBox2 = TextBox(ax_box2, "Set values Amplitude %: ")

new_x = list(x)  # Initialize new_x
new_y = list(y)  # Initialize new_y
new_n = list(n)  # Initialize new_n

def updateAmplitude(text):
    global new_x, new_y, new_n  # Make new_x, new_y, and new_n accessible in the function
    try:
        percentage = float(text)
        # Update x, y, and n values based on the percentage from the current values
        new_x = [val * (1 + percentage / 100.0) for val in new_x]
        new_y = [val * (1 + percentage / 100.0) for val in new_y]
        new_n = [val * (1 + percentage / 100.0) for val in new_n]
        
        # Update the scatter plots
        scatter_x.set_offsets(np.c_[timeline, new_x])
        scatter_y.set_offsets(np.c_[timeline, new_y])
        scatter_n.set_offsets(np.c_[timeline, new_n])
        
        # Update the lines
        line_x.set_ydata(new_x)
        line_y.set_ydata(new_y)
        line_n.set_ydata(new_n)
        
        plt.draw()
    except ValueError:
        print("Invalid input for amplitude percentage. Please enter a valid number.")

textBox2.on_submit(updateAmplitude)

# Reset Button
ax_reset = plt.axes([0.23, 0.01, 0.08, 0.05])
button_reset = Button(ax_reset, 'Reset Amplitude')

def resetAmplitude(event):
    global new_x, new_y, new_n  # Make new_x, new_y, and new_n accessible in the function
    # Reset x, y, and n values to their original state
    new_x = list(x)
    new_y = list(y)
    new_n = list(n)
    
    # Update the scatter plots
    scatter_x.set_offsets(np.c_[timeline, new_x])
    scatter_y.set_offsets(np.c_[timeline, new_y])
    scatter_n.set_offsets(np.c_[timeline, new_n])
    
    # Update the lines
    line_x.set_ydata(new_x)
    line_y.set_ydata(new_y)
    line_n.set_ydata(new_n)
    
    plt.draw()

button_reset.on_clicked(resetAmplitude)

# Zoom In and Out buttons
ax_zoom_in = plt.axes([0.8, 0.01, 0.1, 0.05])
button_zoom_in = Button(ax_zoom_in, 'Zoom In')

ax_zoom_out = plt.axes([0.9, 0.01, 0.1, 0.05])
button_zoom_out = Button(ax_zoom_out, 'Zoom Out')

def zoom_in(event):
    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()
    ax.set_xlim([0.8*x for x in cur_xlim])
    ax.set_ylim([0.8*y for y in cur_ylim])
    plt.draw()

def zoom_out(event):
    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()
    ax.set_xlim([x/0.8 for x in cur_xlim])
    ax.set_ylim([y/0.8 for y in cur_ylim])
    plt.draw()

button_zoom_in.on_clicked(zoom_in)
button_zoom_out.on_clicked(zoom_out)

# Check Buttons
ax_check = plt.axes([0.01, 0.3, 0.1, 0.3], facecolor='lightgoldenrodyellow')
check = CheckButtons(ax_check, ['Show X', 'Show Y', 'Show N', 'Show Legend'], [True, True, True, True])

def check_func(label):
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

check.on_clicked(check_func)

plt.show()
