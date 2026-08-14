from analytics import accuracy_by_category, accuracy_by_difficulty
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
#Patch is a shape object specifically rectangle/square 
# exists purely as a visual in matplotli used here for creating a small colored swatch to show in  legend

CATEGORY_ORDER = {"Tenses": 0, "Parts of Speech": 1, "Subject-Verb Agreement": 2, "Common Errors": 3}
#we have to define order bcz chart sets them in alphabetical order
def plot_category_accuracy(db):
    data = accuracy_by_category(db)
    data = sorted(data, key=lambda row: CATEGORY_ORDER[row[0]]) 
    labels = [row[0] for row in data] 
    #its a list with tuples each tuple has 4 elements we want first element of each tuple which is category name
    values = [row[3] for row in data]
    colors = []
    for v in values:
        if v >= 60:
            colors.append('#4CAF50')   # green
        elif v >= 40:
            colors.append('#FFA726')   # orange
        else:
            colors.append('#E53935')   # red    
    plt.figure(figsize=(9, 6.5))
    plt.bar(labels, values, color=colors)
    plt.title("Accuracy by Category", fontsize=14, fontweight='bold', pad=20)
    plt.ylabel("Accuracy (%)", labelpad=10, fontsize=12, fontweight='bold')
    plt.xlabel("Category" , labelpad=10, fontsize=12, fontweight='bold')
    plt.ylim(0, 100)
    #it sets y-axis limits from 0 to 100 otherwise it automatically adjust y-axis limits based on data
    
    plt.xticks(rotation=30, ha='right')
    #it tilts bar lables to 30deg in right direction
    
    plt.grid(axis='y', alpha=0.3)
    #The whole figure(entire window) is measured on a scale from 0 to 1 called figure coordinates
    plt.yticks(fontsize=10)
    plt.tight_layout(rect=[0, 0.05, 1, 0.78]) #controls how much space is reserved around the chart 
    #it sets the layout of the plot to fit within the figure area and avoid overlapping elements
    
    for i, v in enumerate(values):
        plt.text(i, v + 2, f"{v:.1f}%", ha='center')
#it adds text labels above each bar displaying the accuracy where v+2 is the space diff bw bar and lable

    plt.gca().set_facecolor('#f5f5f5')
    #get current axes means this grabs the chart area itself so we can set its background color to light gray
    
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    #removes top and right border lines
    
    avg = sum(values) / len(values)
    plt.axhline(y=avg, color='blue', linestyle=':', linewidth=1)   # note: no label= here anymore, legend is now built manually below

    legend_elements = [
    Patch(facecolor='#4CAF50', label='Good (≥60%)'),
    Patch(facecolor='#FFA726', label='Needs Improvement (40–59%)'),
    #creates fake green square just for legend explaining what green bars mean
    Patch(facecolor='#E53935', label='Weak (<40%)'),
    plt.Line2D([0], [0], color='blue', linestyle=':', label=f'Overall Average: {avg:.1f}%')
]
    plt.legend(handles=legend_elements, loc='lower left', bbox_to_anchor=(0, 1.12), ncol=1, fontsize=9, frameon=False)
    #bbox_to_anchor=(1.02, 1) means the legend box is placed outside the chart area to the right, with its top aligned with the top of the chart
    #displays a small key on the chart explaining what the line represents
    #its an overall average
     
    best_idx = values.index(max(values))
    best_label = labels[best_idx]
    best_value = values[best_idx]
    worst_idx = values.index(min(values))
    worst_label = labels[worst_idx]
    worst_value = values[worst_idx]
    plt.figtext(0.5, 0.02, f"Best: {best_label} ({best_value:.1f}%)  |  Weakest: {worst_label} ({worst_value:.1f}%)",
    ha='center', fontsize=11, fontweight='bold', style='italic')
    #ha=horizontal allignment
    #places text at a specific position overall figure 0.5 means horiz center 0.02 means very close to the bottom edge
    plt.title(f"Accuracy by Category", fontsize=13, fontweight='bold')
    #title at the top of chart
    plt.show()
    while True:
        save_choice = input("Save this chart as an image? (y/n): ").strip().lower()
        if save_choice == 'y':
            plt.savefig("category_accuracy.png", dpi=150, bbox_inches='tight')
            print("Chart saved as category_accuracy.png")
            break
        elif save_choice == 'n':
            print("Chart not saved.")
            break
        else:
            print("Invalid input. Please enter y or n.")
    
    
    
DIFFICULTY_ORDER = {"easy": 0, "medium": 1, "hard": 2}    
def plot_difficulty_accuracy(db):
    data = accuracy_by_difficulty(db)
    data = sorted(data, key=lambda row: DIFFICULTY_ORDER[row[0]])#sorted runs once per tuple
    #lambda compares data with difficulty order and sorts it in difficulty order way
    #data gaves  order the way its stred in attempt table
    #for each row, look up its difficulty name's position number and reorder rows by that number
    labels = [row[0] for row in data]
    values = [row[3] for row in data]
    colors = [] #this list is for colors in the bar
    for v in values:
        if v >= 60:
            colors.append('#4CAF50')   # green
        elif v >= 40:
            colors.append('#FFA726')   # orange
        else:
            colors.append('#E53935')   # red
    
    plt.figure(figsize=(9, 6.5))
    plt.bar(labels, values, color=colors)
    plt.title("Accuracy by Difficulty", fontsize=14, fontweight='bold', pad=20)
    plt.ylabel("Accuracy (%)", labelpad=10, fontsize=12, fontweight='bold')
    plt.xlabel("Difficulty", labelpad=10, fontsize=12, fontweight='bold')
    plt.ylim(0, 100)
    plt.grid(axis='y', alpha=0.3)
    
    for i, v in enumerate(values):
        plt.text(i, v + 2, f"{v:.1f}%", ha='center')
        
    plt.gca().set_facecolor('#f5f5f5')
    
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    plt.xticks(fontsize=10)    
    #this sets bar lable size
    plt.yticks(fontsize=10)
    plt.tight_layout(rect=[0, 0.05, 1, 0.78])
     
    avg = sum(values) / len(values)
    plt.axhline(y=avg, color='blue', linestyle=':', linewidth=1) 
    #axhline stands for axis horizontal line draws a horizontal line across the chart at the specified y-value (avg)

    legend_elements = [ #this is for representing in the legend box
    Patch(facecolor='#4CAF50', label='Good (≥60%)'),
    Patch(facecolor='#FFA726', label='Needs Improvement (40–59%)'),
    Patch(facecolor='#E53935', label='Weak (<40%)'),
    plt.Line2D([0], [0], color='blue', linestyle=':', label=f'Overall Average: {avg:.1f}%')
    #2D line is used to create a custom legend entry for the average line
]
    plt.legend(handles=legend_elements, loc='lower left', bbox_to_anchor=(0, 1.12), ncol=1, fontsize=9, frameon=False)
    
    best_idx = values.index(max(values))
    best_label = labels[best_idx]
    best_value = values[best_idx]
    worst_idx = values.index(min(values))
    worst_label = labels[worst_idx]
    worst_value = values[worst_idx]
    plt.figtext(0.5, 0.02, f"Best: {best_label} ({best_value:.1f}%)  |  Weakest: {worst_label} ({worst_value:.1f}%)",
    ha='center', fontsize=11, fontweight='bold', style='italic')
    plt.title("Accuracy by Difficulty", fontsize=14, fontweight='bold')
    
    plt.show()
    while True:
        save_choice = input("Save this chart as an image? (y/n): ").strip().lower()
        if save_choice == 'y':
            plt.savefig("difficulty_accuracy.png", dpi=150, bbox_inches='tight')
            print("Chart saved as difficulty_accuracy.png")
            break
        elif save_choice == 'n':
            print("Chart not saved.")
            break
        else:
            print("Invalid input. Please enter y or n.")