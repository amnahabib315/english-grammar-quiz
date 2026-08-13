from analytics import accuracy_by_category, accuracy_by_difficulty
import matplotlib.pyplot as plt

def plot_category_accuracy(db):
    data = accuracy_by_category(db)
    labels = [row[0] for row in data] 
    #its a list with tuples each tuple has 4 elements we want first element of each tuple which is category name
    values = [row[3] for row in data]
    plt.figure(figsize=(8, 6))
    plt.bar(labels, values)
    plt.title("Accuracy by Category")
    plt.ylabel("Accuracy (%)", labelpad=10)
    plt.xlabel("Category" , labelpad=10)
    plt.ylim(0, 100) #it sets y-axis limits from 0 to 100 otherwise it automatically adjust y-axis limits based on data
    plt.xticks(rotation=30, ha='right')
    #it tilts lables to 30deg in right direction
    plt.tight_layout() 
    #it sets the layout of the plot to fit within the figure area and avoid overlapping elements
    plt.show()

def plot_difficulty_accuracy(db):
    data = accuracy_by_difficulty(db)
    labels = [row[0] for row in data]
    values = [row[3] for row in data]
    plt.figure(figsize=(8, 6))
    plt.bar(labels, values)
    plt.title("Accuracy by Difficulty")
    plt.ylabel("Accuracy (%)", labelpad=10)
    plt.xlabel("Difficulty", labelpad=10)
    plt.ylim(0, 100)
    plt.show()