from analytics import accuracy_by_category, accuracy_by_difficulty
import matplotlib.pyplot as plt

def plot_category_accuracy(db):
    data = accuracy_by_category(db)
    labels = [row[0] for row in data] 
    #its a list with tuples each tuple has 4 elements we want first element of each tuple which is category name
    values = [row[3] for row in data]
    colors = ['#4CAF50' if v >= 60 else '#E53935' for v in values]
    
    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=colors)
    plt.title("Accuracy by Category", fontsize=14, fontweight='bold')
    plt.ylabel("Accuracy (%)", labelpad=10, fontsize=12, fontweight='bold')
    plt.xlabel("Category" , labelpad=10, fontsize=12, fontweight='bold')
    plt.ylim(0, 100)
    #it sets y-axis limits from 0 to 100 otherwise it automatically adjust y-axis limits based on data
    plt.xticks(rotation=30, ha='right')
    #it tilts bar lables to 30deg in right direction
    plt.yticks(fontsize=10)
    plt.tight_layout() 
    #it sets the layout of the plot to fit within the figure area and avoid overlapping elements
    for i, v in enumerate(values):
        plt.text(i, v + 2, f"{v:.1f}%", ha='center')
#it adds text labels above each bar displaying the accuracy where v+2 is the space diff bw bar and lable
    plt.gca().set_facecolor('#f5f5f5')
    #get current axes means this grabs the chart area itself so we can set its background color to light gray
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    #removes top and right border lines
    plt.show()
    
    
    
def plot_difficulty_accuracy(db):
    data = accuracy_by_difficulty(db)
    labels = [row[0] for row in data]
    values = [row[3] for row in data]
    colors = ['#4CAF50' if v >= 60 else '#E53935' for v in values]
    
    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=colors)
    plt.title("Accuracy by Difficulty", fontsize=14, fontweight='bold')
    plt.ylabel("Accuracy (%)", labelpad=10, fontsize=12, fontweight='bold')
    plt.xlabel("Difficulty", labelpad=10, fontsize=12, fontweight='bold')
    plt.ylim(0, 100)
    for i, v in enumerate(values):
        plt.text(i, v + 2, f"{v:.1f}%", ha='center')
    plt.gca().set_facecolor('#f5f5f5')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xticks(fontsize=10)    
    #this sets bar lable size
    plt.yticks(fontsize=10) 
    plt.show()