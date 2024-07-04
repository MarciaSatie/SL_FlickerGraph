import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
import json

try:
    # Opening JSON file
    with open('Z_FlickerValues.json', 'r') as f:
        # Returns JSON object as a dictionary
        data = json.load(f)
    
except Exception as e:
    print("An error occurred: {}".format(e))

# Extract posX and posY values into separate lists
x = [float(item['posX']) for item in data]
y = [float(item['posY']) for item in data]
timeline = [int(item['id']) for item in data]

# Plotting the points
fig, ax = plt.subplots(figsize=(16, 7))
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
plt.plot(timeline, x, label='Value in X',marker='o')
plt.plot(timeline, y, label='Value in Y', marker='.', linestyle='--')

legend= plt.legend(loc='upper left')
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
      
    if current_size[0]>15:
        ax.set_xticks(np.arange(0, len(timeline), step=2))
        plt.draw()
    elif current_size[0] <= 15 and current_size[0] > 8:
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
            indexValue = annotation_index_x['ind'][0] if is_contained_x else annotation_index_y['ind'][0]
            # Get the location of the point
            data_point_location = scatter_x.get_offsets()[indexValue] if is_contained_x else scatter_y.get_offsets()[indexValue]
            # Update annotation with new position and text
            annotations[indexValue].xy = data_point_location
            text_label = 'x: {:.3f} | y: {:.3f}'.format(x[indexValue], y[indexValue]) 
            annotations[indexValue].set_text(text_label)
            annotations[indexValue].set_visible(True)
            visible_any_annotation = True
            legend.set_visible(False)
        if not visible_any_annotation:
            for annotation in annotations:
                annotation.set_visible(False)
            legend.set_visible(True)
        fig.canvas.draw_idle()

fig.canvas.mpl_connect('motion_notify_event', hover)

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
