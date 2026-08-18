import analytics 
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import textwrap
#Patch is a shape object specifically rectangle/square 
# exists purely as a visual in matplotli used here for creating a small colored swatch to show in  legend


CATEGORY_ORDER = {"Tenses": 0, "Parts of Speech": 1, "Subject-Verb Agreement": 2, "Common Errors": 3}
#we have to define order bcz chart sets them in alphabetical order
DIFFICULTY_ORDER = {"easy": 0, "medium": 1, "hard": 2}


def get_color(v):
    # shared color rule so all charts + dashboard use the exact same thresholds, defined once
    if v >= 60:
        return '#4CAF50'   # green
    elif v >= 40:
        return '#FFA726'   # orange
    else:
        return '#E53935'   # red


def plot_category_accuracy(db, ax=None):
    data = analytics.accuracy_by_category(db)
    if not data:
        print("\nNo data yet — take a quiz first!")
        return
    data = sorted(data, key=lambda row: CATEGORY_ORDER[row[0]]) 
    labels = [row[0] for row in data] 
    #its a list with tuples each tuple has 4 elements we want first element of each tuple which is category name
    values = [row[3] for row in data]
    colors = [get_color(v) for v in values]   # now uses shared get_color instead of repeated if/elif

    # standalone = True means this was called on its own (normal chart view);
    # False means it was handed an ax by show_dashboard(), so it should just
    # draw into that ax and skip the window-only extras (legend/caption/save)
    standalone = ax is None
    if standalone:
        # fig = the whole window, ax = just the chart area — controlling them
        # separately is what lets the legend live in its OWN reserved space,
        # completely outside the chart, so it can never overlap tall bars
        fig, ax = plt.subplots(figsize=(9, 6.5))

    ax.bar(labels, values, color=colors)
    ax.set_title("Accuracy by Category", fontsize=16 if standalone else 12, fontweight='bold', pad=15 if standalone else 8)
    ax.set_ylim(0, 100)
    #it sets y-axis limits from 0 to 100 otherwise it automatically adjust y-axis limits based on data

    wrapped_labels = [textwrap.fill(l, 12) for l in labels]
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(wrapped_labels, rotation=0, fontsize=10 if standalone else 8)
    #it tilts bar lables to 30deg in right direction

    ax.grid(axis='y', alpha=0.3)
    #The whole figure(entire window) is measured on a scale from 0 to 1 called figure coordinates
    ax.tick_params(axis='y', labelsize=10 if standalone else 8)

    for i, v in enumerate(values):
        ax.text(i, v + 2, f"{v:.1f}%", ha='center', fontsize=10 if standalone else 8)
#it adds text labels above each bar displaying the accuracy where v+2 is the space diff bw bar and lable

    ax.set_facecolor('#f5f5f5')
    #get current axes means this grabs the chart area itself so we can set its background color to light gray

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    #removes top and right border lines

    avg = sum(values) / len(values)
    ax.axhline(y=avg, color='blue', linestyle=':', linewidth=1)   # note: no label= here anymore, legend is now built manually below

    # everything below this line is ONLY for standalone viewing —
    # dashboard mini-charts skip legend/labels/caption/save to stay clean
    if not standalone:
        return

    ax.set_ylabel("Accuracy (%)", labelpad=10, fontsize=12, fontweight='bold')
    ax.set_xlabel("Category", labelpad=10, fontsize=12, fontweight='bold')

    legend_elements = [
    Patch(facecolor='#4CAF50', label='Good (≥60%)'),
    Patch(facecolor='#FFA726', label='Needs Improvement (40–59%)'),
    #creates fake green square just for legend explaining what green bars mean
    Patch(facecolor='#E53935', label='Weak (<40%)'),
    plt.Line2D([0], [0], color='blue', linestyle=':', label=f'Overall Average: {avg:.1f}%')
]
    # fig.legend (not ax.legend/plt.legend) attaches the legend to the WHOLE
    # figure, in figure-coordinates (0 to 1 top-to-bottom), independent of
    # the chart's own coordinate space — this is what guarantees it can
    # never collide with bars, no matter how tall they get
    fig.legend(handles=legend_elements, loc='upper center', ncol=4, fontsize=8, frameon=False, bbox_to_anchor=(0.5, 0.98))
    #displays a small key on the chart explaining what the line represents
    #its an overall average

    best_idx = values.index(max(values))
    best_label = labels[best_idx]
    best_value = values[best_idx]
    worst_idx = values.index(min(values))
    worst_label = labels[worst_idx]
    worst_value = values[worst_idx]
    fig.text(0.5, 0.01, f"Best: {best_label} ({best_value:.1f}%)  |  Weakest: {worst_label} ({worst_value:.1f}%)",
    ha='center', fontsize=11, fontweight='bold', style='italic')
    #ha=horizontal allignment
    #places text at a specific position overall figure 0.5 means horiz center 0.01 means very close to the bottom edge

    # explicit, guaranteed control over vertical space: chart area only
    # occupies from 18% to 80% of the figure height — legend gets the top
    # 20%, caption gets the bottom 18%, no automatic guessing involved
    fig.subplots_adjust(top=0.80, bottom=0.18)

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


def plot_difficulty_accuracy(db, ax=None):
    data = analytics.accuracy_by_difficulty(db)
    if not data:
        print("\nNo data yet — take a quiz first!")
        return
    data = sorted(data, key=lambda row: DIFFICULTY_ORDER[row[0]])#sorted runs once per tuple
    #lambda compares data with difficulty order and sorts it in difficulty order way
    #data gaves  order the way its stred in attempt table
    #for each row, look up its difficulty name's position number and reorder rows by that number
    labels = [row[0] for row in data]
    values = [row[3] for row in data]
    colors = [get_color(v) for v in values]   # shared color rule

    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(9, 6.5))

    ax.bar(labels, values, color=colors)
    ax.set_title("Accuracy by Difficulty", fontsize=16 if standalone else 12, fontweight='bold', pad=15 if standalone else 8)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)

    for i, v in enumerate(values):
        ax.text(i, v + 2, f"{v:.1f}%", ha='center', fontsize=10 if standalone else 8)

    ax.set_facecolor('#f5f5f5')

    ax.spines['top'].set_visible(False) #border lines across chart
    ax.spines['right'].set_visible(False)

    wrapped_labels = [textwrap.fill(l, 12) for l in labels]
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(wrapped_labels, rotation=0, fontsize=10 if standalone else 8)
    #this sets bar lable size
    ax.tick_params(axis='y', labelsize=10 if standalone else 8)

    avg = sum(values) / len(values)
    ax.axhline(y=avg, color='blue', linestyle=':', linewidth=1)
    #axhline stands for axis horizontal line draws a horizontal line across the chart at the specified y-value (avg)

    if not standalone:
        return

    ax.set_ylabel("Accuracy (%)", labelpad=10, fontsize=12, fontweight='bold')
    ax.set_xlabel("Difficulty", labelpad=10, fontsize=12, fontweight='bold')

    legend_elements = [ #this is for representing in the legend box
    Patch(facecolor='#4CAF50', label='Good (≥60%)'),
    Patch(facecolor='#FFA726', label='Needs Improvement (40–59%)'),
    Patch(facecolor='#E53935', label='Weak (<40%)'),
    plt.Line2D([0], [0], color='blue', linestyle=':', label=f'Overall Average: {avg:.1f}%')
    #2D line is used to create a custom legend entry for the average line
]
    fig.legend(handles=legend_elements, loc='upper center', ncol=4, fontsize=8, frameon=False, bbox_to_anchor=(0.5, 0.98))

    best_idx = values.index(max(values))
    best_label = labels[best_idx]
    best_value = values[best_idx]
    worst_idx = values.index(min(values))
    worst_label = labels[worst_idx]
    worst_value = values[worst_idx]
    fig.text(0.5, 0.01, f"Best: {best_label} ({best_value:.1f}%)  |  Weakest: {worst_label} ({worst_value:.1f}%)",
    ha='center', fontsize=11, fontweight='bold', style='italic')

    fig.subplots_adjust(top=0.80, bottom=0.18)

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


def plot_accuracy_over_time(db, ax=None):
    standalone = ax is None
    data = analytics.accuracy_by_date(db, limit=8 if standalone else 4)
    data = list(reversed(data))
    if not data:
        print("\nNo data yet — take a quiz first!")
        return
    dates = [row[0] for row in data]
    accuracies = [row[1] for row in data]

    if standalone:
        fig, ax = plt.subplots(figsize=(9, 6.5))

    ax.plot(dates, accuracies, marker='o', color='#4CAF50')
    ax.set_title("Accuracy Over Time", fontsize=16 if standalone else 12, fontweight='bold', pad=15 if standalone else 8)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)
    for i, v in enumerate(accuracies):  
        ax.text(dates[i], v + 2, f"{v:.1f}%", ha='center', fontsize=10 if standalone else 8)

    ax.tick_params(axis='x', rotation=0, labelsize=10 if standalone else 8)
    ax.tick_params(axis='y', labelsize=10 if standalone else 8)
    avg = sum(accuracies) / len(accuracies)
    avg_line = ax.axhline(y=avg, color='blue', linestyle=':', linewidth=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False) 
    ax.set_facecolor('#f5f5f5')

    if not standalone:
        return

    ax.set_xlabel("Date", fontsize=12, fontweight='bold', labelpad=10)
    ax.set_ylabel("Accuracy (%)", fontsize=12, fontweight='bold', labelpad=10)

    fig.legend(handles=[avg_line], labels=[f'Overall Average: {avg:.1f}%'], loc='upper center', ncol=1, 
    fontsize=8, frameon=False, bbox_to_anchor=(0.5, 0.98))
    fig.subplots_adjust(top=0.80, bottom=0.18)
    plt.show()
    while True:
        save_choice = input("Save this chart as an image? (y/n): ").strip().lower()
        if save_choice == 'y':
            plt.savefig("accuracy_over_time.png", dpi=150, bbox_inches='tight')
            print("Chart saved as accuracy_over_time.png")
            break
        elif save_choice == 'n':
            print("Chart not saved.")
            break
        else:
            print("Invalid input. Please enter y or n.")


def plot_correct_vs_incorrect(db, ax=None):
    total, correct, accuracy = analytics.overall_stats(db)
    if total == 0:
        print("\nNo data yet — take a quiz first!")
        return

    incorrect = total - correct
    labels = ['Correct', 'Incorrect']
    values = [correct, incorrect]
    colors = ['#4CAF50', '#E53935']

    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(8, 8))

    ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90,
           textprops={'fontsize': 12 if standalone else 9})
    ax.set_title("Correct vs Incorrect Answers", fontsize=16 if standalone else 12, fontweight='bold',
                 pad=20 if standalone else 8)

    if not standalone:
        return

    plt.show()
    while True:
        save_choice = input("Save this chart as an image? (y/n): ").strip().lower()
        if save_choice == 'y':
            plt.savefig("correct_vs_incorrect.png", dpi=150, bbox_inches='tight')
            print("Chart saved as correct_vs_incorrect.png")
            break
        elif save_choice == 'n':
            print("Chart not saved.")
            break
        else:
            print("Invalid input. Please enter y or n.")


def show_dashboard(db):
    # reuses the same 4 chart functions above, just handing each one an ax
    # to draw into instead of letting them open their own window
    if not analytics.accuracy_by_category(db):
        print("\nNo data yet — take a quiz first!")
        return

    fig, axes = plt.subplots(2, 2, figsize=(15, 11))

    plot_category_accuracy(db, ax=axes[0, 0])
    plot_difficulty_accuracy(db, ax=axes[0, 1])
    plot_accuracy_over_time(db, ax=axes[1, 0])
    plot_correct_vs_incorrect(db, ax=axes[1, 1])

    fig.suptitle("Performance Dashboard", fontsize=18, fontweight='bold')
    fig.subplots_adjust(hspace=0.5, wspace=0.3, top=0.90)
    plt.show()
    while True:
            save_choice = input("Save this chart as an image? (y/n): ").strip().lower()
            if save_choice == 'y':
                plt.savefig("overall_dashboard.png", dpi=150, bbox_inches='tight')
                print("Chart saved as overall_dashboard.png")
                break
            elif save_choice == 'n':
                print("Chart not saved.")
                break
            else:
                print("Invalid input. Please enter y or n.")