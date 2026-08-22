import tkinter as tk
from database import Database
import charts
from analytics import show_report
from main import VALID_CATEGORIES
from tkinter import messagebox


class QuizApp:
    def __init__(self, root):
        #root is the main window of the application, passed in from the main block at the bottom
        self.root = root
        self.root.title("English Grammar Quiz")
        self.root.geometry("500x600") #geometry is a method that sets the size of the window

        # shared colors and fonts, defined once here, reused everywhere below
        # so the whole app looks consistent instead of styled screen by screen
        self.bg_color = "#f0f0f0"
        self.title_color = "#2C3E50"
        self.btn_color = "#4A90E2"
        self.font_name = "Segoe UI"

        self.root.configure(bg=self.bg_color) #bg color

        # one shared button style dict, reused on every button in the app
        self.btn_style = {
            "width": 35,
            "font": (self.font_name, 14), 
            "bg": self.btn_color,
            "fg": "white", #fg is button text color
            "activebackground": "#3E7FCB",
            "relief": "flat", #flat means no border
            "cursor": "hand2", #cursor means the mouse pointer will change to a hand when hovering over the button
        }

        self.db = Database()
        self.show_main_menu()

    def clear_window(self):
        #wedgit is term for any element in a GUI like buttons,labels,text boxes
        for widget in self.root.winfo_children():
            widget.destroy()
            #winfo_children is method that returns list of all widgets in  window
            #and destroy() is a method that removes the widget from the window
            #here its iterating over all the widgets in  window and destroying them 
            #so we can draw a new screen in  same window instead opening  new one each time

    def show_main_menu(self):
        self.clear_window()
        container = tk.Frame(self.root, bg=self.bg_color)
        container.place(relx=0.5, rely=0.5, anchor="center")  
        #relx and rely are used to position the container in the center of the window
        #container is frame that holds all the buttons and labels in the main menu
        tk.Label(container, text="English Grammar Quiz", font=(self.font_name, 26, "bold"), 
                 fg=self.title_color, bg=self.bg_color).pack(pady=20)

        tk.Button(container, text="Take Quiz", command=self.show_quiz_setup, **self.btn_style).pack(pady=8)
        tk.Button(container, text="View Performance Report", command=self.show_report_screen, **self.btn_style).pack(pady=8)
        tk.Button(container, text="View Performance Charts", command=self.show_charts_menu, **self.btn_style).pack(pady=8)
        tk.Button(container, text="Exit", command=self.root.quit, **self.btn_style).pack(pady=8)

        # small footer so the app feels complete, not abruptly ending after the buttons
        tk.Label(container, text="Python • SQLite • Matplotlib", font=(self.font_name, 9),
                 fg="#7f8c8d", bg=self.bg_color).pack(pady=(25, 0))

    def show_charts_menu(self):
        self.clear_window()
        container = tk.Frame(self.root, bg=self.bg_color)
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="Performance Charts", font=(self.font_name, 26, "bold"),
                 fg=self.title_color, bg=self.bg_color).pack(pady=20)

        tk.Button(container, text="Accuracy by Category",
                  command=lambda: charts.plot_category_accuracy(self.db), **self.btn_style).pack(pady=7)
        #lambda is comand here to pass the db object to the function plot_category_accuracy when the button is clicked
        tk.Button(container, text="Accuracy by Difficulty",
                  command=lambda: charts.plot_difficulty_accuracy(self.db), **self.btn_style).pack(pady=7)
        tk.Button(container, text="Accuracy Over Time",
                  command=lambda: charts.plot_accuracy_over_time(self.db), **self.btn_style).pack(pady=7)
        tk.Button(container, text="Correct vs Incorrect",
                  command=lambda: charts.plot_correct_vs_incorrect(self.db), **self.btn_style).pack(pady=7)
        tk.Button(container, text="View Full Dashboard",
                  command=lambda: charts.show_dashboard(self.db), **self.btn_style).pack(pady=7)    
        #pack and paddy are used to add space between the buttons and the label in the GUI
        tk.Button(container, text="Back to Main Menu", command=self.show_main_menu, **self.btn_style).pack(pady=20)

    def show_report_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Performance Report", font=(self.font_name, 26, "bold"),
                 fg=self.title_color, bg=self.bg_color).pack(pady=15)

        outer = tk.Frame(self.root, bg=self.bg_color)
        outer.pack(pady=10) #outer frame is used to hold the text box and the scrollbar

        frame = tk.Frame(outer, bg=self.bg_color)
        frame.pack() #text box frame that holds text box and scrollbar

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y") #fill y means the scrollbar will fill the entire height of the frame

        text_box = tk.Text(frame, wrap="word", font=("Consolas", 13), width=70, height=26,
                            yscrollcommand=scrollbar.set, relief="solid", borderwidth=1)
        text_box.pack(side="left")
        scrollbar.config(command=text_box.yview)

        # keeping green/red performance indicators as-is — these help users
        # immediately spot strengths vs weak areas, so they stay unchanged
        text_box.tag_configure("heading", font=("Consolas", 14, "bold"), justify="center")
        text_box.tag_configure("good", foreground="#2E7D32", justify="center")
        text_box.tag_configure("warn", foreground="#C62828", justify="center")
        text_box.tag_configure("normal", justify="center")

        report_text = show_report(self.db)
        for line in report_text.split("\n"):
            if line.startswith("Category:") or line.startswith("Difficulty:") or line.startswith("Overall Quiz") or line.startswith("Weakest"):
                text_box.insert("end", line + "\n", "heading")
            elif "Accuracy:" in line:
                # pull the number out of a line like "  Accuracy: 58.82% needs practice"
                percent_str = line.split("Accuracy:")[1].split("%")[0].strip()
                accuracy_value = float(percent_str)
                tag = "good" if accuracy_value >= 60 else "warn"
                text_box.insert("end", line + "\n", tag)
            else:
                text_box.insert("end", line + "\n", "normal")

        text_box.config(state="disabled")
        tk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu, **self.btn_style).pack(pady=15)

    def show_quiz_setup(self):
        self.clear_window()
        container = tk.Frame(self.root, bg=self.bg_color)
        container.place(relx=0.5, rely=0.5, anchor="center")
        #container used to center the buttons and label in the middle of the window

        tk.Label(container, text="Choose Difficulty", font=(self.font_name, 26, "bold"),
                 fg=self.title_color, bg=self.bg_color).pack(pady=15)

        # loop creates one button per difficulty level instead of writing 3 separate lines
        for level in ["easy", "medium", "hard"]:
            # l=level freezes the CURRENT loop value into the lambda right now,
            # otherwise all 3 buttons would end up using whatever "level" is
            # LAST set to (a common lambda-in-a-loop mistake)
            tk.Button(container, text=level.capitalize(),
                      command=lambda l=level: self.select_difficulty(l), **self.btn_style).pack(pady=7)

        tk.Button(container, text="Back to Main Menu", command=self.show_main_menu, **self.btn_style).pack(pady=20)

    def select_difficulty(self, difficulty):
        # stores the user's choice so later steps (category selection, then
        # fetching questions) know which difficulty to use
        self.selected_difficulty = difficulty
        self.show_category_setup()
    
    def start_quiz(self):
        print("Selected difficulty:", self.selected_difficulty)
        print("Selected categories:", self.selected_categories)
    # NEEDS: actually fetch questions and show the first one

    def show_category_setup(self):
        self.clear_window()
        container = tk.Frame(self.root, bg=self.bg_color)
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="Choose Categories", font=(self.font_name, 26, "bold"),
                 fg=self.title_color, bg=self.bg_color).pack(pady=15)

        #tracks which categories are currently selected
        self.selected_categories = []
        #keeps a reference to each button so we can change its color when clicked
        self.category_buttons = {}

        for cat in VALID_CATEGORIES:
            btn = tk.Button(container, text=cat, command=lambda c=cat: self.toggle_category(c),
                            **{**self.btn_style, "bg": "white", "fg": "black"})
            btn.pack(pady=6) #pack is used to add space between buttons and the label
            self.category_buttons[cat] = btn

        # thin horizontal line to visually separate category choices from the action buttons
        separator = tk.Frame(container, height=3, bg="#000000", width=300)
        separator.pack(pady=15)

        tk.Button(container, text="Start Quiz", command=self.start_quiz, **self.btn_style).pack(pady=8)
        tk.Button(container, text="Back to Main Menu", command=self.show_main_menu, **self.btn_style).pack(pady=5)
    def toggle_category(self, category):
        btn = self.category_buttons[category]
        if category in self.selected_categories:
            self.selected_categories.remove(category)
            btn.config(bg="white", fg="black")#config method is used to change the button color
        else:
            self.selected_categories.append(category)
            btn.config(bg=self.btn_color, fg="white")
    
    def confirm_exit_quiz(self):
        confirmed = messagebox.askyesno("Exit Quiz", "Your progress will not be saved. Are you sure you want to exit?")
        if confirmed:
            self.show_main_menu()
    #if they click "No", nothing happens — they stay on the current quiz screen


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()