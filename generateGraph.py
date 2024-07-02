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
fig, ax = plt.subplots()
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
    annotation_visibility = annotation.get_visible()
    if event.inaxes ==ax:
        is_contained, annotation_index = scatter_x.contains(event)
        print(is_contained,annotation_index)
        if is_contained:
            data_point_location = scatter_x.get_offsets()[annotation_index['ind'][0]]
            annotation.xy = data_point_location
            
            text_label = 'x: {:.3f} | y: {:.3f}'.format(x[i], y[i]) 
            annotation.set_text(text_label)
            annotation.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if annotation_visibility:
                annotation.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect('motion_notify_event', hover)

plt.legend()
# Naming the x axis
plt.xlabel('Frames range')
# Naming the y axis
plt.ylabel('Flicker value range')

# Adding grid
plt.grid(True)
# Giving a title to my graph
plt.title('Flicker graph!')

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
