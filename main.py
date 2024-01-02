import subprocess
import importlib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk

from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import data_getters


data_getters.initialize_model()

def install_libraries():
    packages = ['numpy', 'matplotlib', 'seaborn', 'tkinter', 'pandas', 'sklearn', 'os']
    for lib in packages:
        try:
            importlib.import_module(lib)
        except ImportError:
            subprocess.run(['pip', 'install', lib])

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = (screen_width - 10)
        window_height = (screen_height - 80)
        self.geometry(f"{window_width}x{window_height}+0+0")
        self.title("Examining Video Game Sales")
        self.configure(bg="#2E3B4E")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (HomePage, IntroPage, ImportanceBreakdown, GenreBreakdown, ThemeBreakdown, KpiMetrics):
            page_name = F.__name__
            frame = F(parent=container, controller=self, close_app_callback=self.close_application)
            self.frames[page_name] = frame
            frame.pack(fill="both", expand=True)

        self.show_frame("HomePage")

    def close_application(self):
        self.destroy()

    def show_frame(self, page_name):
        for frame_name, frame in self.frames.items():
            if frame_name == page_name:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()


class HomePage(tk.Frame):
    def __init__(self, parent, controller, close_app_callback):
        tk.Frame.__init__(self, parent, bg="#2E3B4E")
        self.columnconfigure(0, weight=1)
        self.close_app_callback = close_app_callback

        title_frame = tk.Frame(self, bg="#2E3B4E")
        title_frame.grid(row=1, column=0, columnspan=3, pady=20)
        title = tk.Label(title_frame, text="Welcome to the Video Game Sales Analyzer", font=("Helvetica", 28),
                         bg="#2E3B4E", fg="#D1D9E6")
        title.pack(pady=30)
        subtitle = tk.Label(title_frame, text="a C964 project by Danae Miller", font=("Helvetica", 14), bg="#2E3B4E",
                            fg="#D1D9E6")
        subtitle.pack(pady=5)

        button_frame = tk.Frame(self, bg="#2E3B4E")
        button_frame.grid(row=2, column=0, pady=20)
        intro_button = tk.Button(button_frame, text="What does this model do?", font=("Verdana", 16), width=25, height=2,
                                 bg="#D1D9E6", fg="#2E3B4E", command=lambda: controller.show_frame("IntroPage"))
        intro_button.pack(padx=20, pady=10)
        importance_button = tk.Button(button_frame, text="How important is this data?", font=("Verdana", 16), width=25,
                                      height=2, bg="#D1D9E6", fg="#2E3B4E", command=lambda: controller.show_frame("ImportanceBreakdown"))
        importance_button.pack(padx=20, pady=10)
        genre_button = tk.Button(button_frame, text="Explore by genre", font=("Verdana", 16), width=25, height=2,
                                 bg="#D1D9E6", fg="#2E3B4E", command=lambda: controller.show_frame("GenreBreakdown"))
        genre_button.pack(padx=20, pady=10)
        theme_button = tk.Button(button_frame, text="Explore by theme", font=("Verdana", 16), width=25, height=2,
                                 bg="#D1D9E6", fg="#2E3B4E", command=lambda: controller.show_frame("ThemeBreakdown"))
        theme_button.pack(padx=20, pady=10)
        metrics_button = tk.Button(button_frame, text="KPIs", font=("Verdana", 16), width=25, height=2, bg="#D1D9E6",
                                   fg="#2E3B4E", command=lambda: controller.show_frame("KpiMetrics"))
        metrics_button.pack(padx=20, pady=10)

        filler_label = tk.Label(button_frame, bg="#2E3B4E")
        filler_label.pack(fill="both", expand=True)

        close_button = tk.Button(button_frame, text="Exit", font=("Verdana", 16), width=25, height=2, bg="#D1D9E6",
                                   fg="#2E3B4E", command=self.close_app_callback)
        close_button.pack(padx=20, pady=20)


class IntroPage(tk.Frame):
    def __init__(self, parent, controller, close_app_callback):
        tk.Frame.__init__(self, parent, bg="#2E3B4E")
        self.columnconfigure(0, weight=1)

        title = tk.Label(self, text="What does this model do?", font=("Helvetica", 28), bg="#2E3B4E",
                         fg="#D1D9E6")
        title.pack(pady=40)

        subtitle = tk.Label(self, text=("This project utilizes a Random Forests Regression algorithm\n"
                                        "to predict sales of video games based on many attributes."),
                            font=("Helvetica", 16), bg="#2E3B4E", fg="#D1D9E6", justify="center")
        subtitle.pack(pady=20)

        text = tk.Label(self, text=("    The model looks at the genre and the thematic content of the games, as well as its\n"
                        "price on release, and then examines a series of 27 features to make correlations about\n"
                        "which combinations of features do best in any given type of game.\n\n"
                        "    There were originally 33 features, but some proved to be wholly unimportant to game success,\n"
                        "namely the features regarding visual style. It was an interesting discovery to say the least.\n\n"
                        "    The dependent variable, our success metric, is number of copies sold per year."),
                        font=("Helvetica", 14), bg="#2E3B4E", fg="#D1D9E6", justify="center")
        text.pack(pady=20)

        back_button = tk.Button(self, text="Return", font=("Verdana", 16), width=25, height=2, bg="#D1D9E6",
                                fg="#2E3B4E", command=lambda: controller.show_frame("HomePage"))
        back_button.pack(pady=80)


class ImportanceBreakdown(tk.Frame):
    def __init__(self, parent, controller, close_app_callback):
        tk.Frame.__init__(self, parent, bg="#2E3B4E")
        self.columnconfigure(0, weight=1)

        label = tk.Label(self, text="How important is this data?", font=("Helvetica", 28), bg="#2E3B4E",
                         fg="#D1D9E6")
        label.pack(pady=40)

        feature_import_data = data_getters.get_feature_import()
        for title, import_percent in feature_import_data:
            feature_label = tk.Label(self, text=f"{title} accounted for {import_percent:.2f}% of the variability in sales figures.",
                                     font=("Helvetica", 14), bg="#2E3B4E", fg="#D1D9E6")
            feature_label.pack(pady=20)

        feature_frame = tk.Frame(self, bg="#2E3B4E")
        feature_frame.pack(side="top", fill="y", expand=True, pady=10, anchor="n")

        best_frame = tk.Frame(feature_frame, bg="#2E3B4E")
        best_frame.pack(side="left", padx=50, pady=10, anchor="n")

        best_features = data_getters.get_best_features()
        best_title = tk.Label(best_frame, text="The most important features for sales were: ", font=("Helvetica", 16),
                              bg="#2E3B4E", fg="#D1D9E6")
        best_title.pack(pady=10)
        for feature in best_features:
            best_label = tk.Label(best_frame, text=feature, font=("Helvetica", 12), bg="#2E3B4E", fg="#D1D9E6")
            best_label.pack(pady=2)

        worst_frame = tk.Frame(feature_frame, bg="#2E3B4E")
        worst_frame.pack(side="right", padx=50, pady=10, anchor="n")

        worst_features = data_getters.get_worst_features()
        worst_title = tk.Label(worst_frame, text="The least important features for sales were: ", font=("Helvetica", 16),
                              bg="#2E3B4E", fg="#D1D9E6")
        worst_title.pack(pady=10)
        for feature in worst_features:
            worst_label = tk.Label(worst_frame, text=feature, font=("Helvetica", 12), bg="#2E3B4E", fg="#D1D9E6")
            worst_label.pack(pady=2)

        back_button = tk.Button(self, text="Return", font=("Verdana", 16), width=25, height=2, bg="#D1D9E6",
                                fg="#2E3B4E", command=lambda: controller.show_frame("HomePage"))
        back_button.pack(pady=10)

class GenreBreakdown(tk.Frame):
    def __init__(self, parent, controller, close_app_callback):
        tk.Frame.__init__(self, parent, bg="#2E3B4E")
        self.columnconfigure(0, weight=1)

        label = tk.Label(self, text="Explore by Genre", font=("Helvetica", 28), bg="#2E3B4E",
                         fg="#D1D9E6")
        label.grid(row=0, column=0, columnspan=3, pady=20)

        dropdown_frame = tk.Frame(self, bg="#2E3B4E")
        dropdown_frame.grid(row=1, column=0, padx=50, pady=20)

        dd_label = tk.Label(dropdown_frame, text="Select a Genre", font=("Helvetica", 12), bg="#2E3B4E", fg="#D1D9E6")
        dd_label.pack(side="top", pady=10)
        genres = ["Action-Adventure", "Role-Playing", "Strategy", "Simulation", "Sports and Racing", "Visual Novels"]
        self.selected_genre = tk.StringVar()
        genre_dropdown = ttk.Combobox(dropdown_frame, textvariable=self.selected_genre, values=genres, state="readonly")
        genre_dropdown.pack(side="left", pady=10)
        action_button = tk.Button(dropdown_frame, text="Show Data", command=self.graph_by_genre)
        action_button.pack(side="left", pady=10)

        self.graph_frame = tk.Frame(self, bg="#2E3B4E")
        self.graph_frame.grid(row=2, column=0, columnspan=3, padx=50, pady=20)
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.fig.tight_layout(pad=6.0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        back_button = tk.Button(self, text="Return", font=("Verdana", 16), width=25, height=2, bg="#D1D9E6",
                                fg="#2E3B4E", command=lambda: controller.show_frame("HomePage"))
        back_button.grid(row=3, column=0, columnspan=3, padx=50, pady=20, sticky="s")

    def graph_by_genre(self):
        genre = self.selected_genre.get()
        grouped_df = data_getters.model_by_genre(genre)

        self.ax.clear()

        bar_width = 0.35
        theme_indices = range(10)
        index = np.array(theme_indices) - bar_width / 2
        bar1 = self.ax.bar(index, grouped_df['Actual_Sales'], bar_width, label='Actual')
        bar2 = self.ax.bar(index + bar_width, grouped_df['Predicted_Sales'], bar_width, label='Predicted')
        themes = []
        for i in theme_indices:
            themes.append(data_getters.all_mapping(i))

        self.ax.set_xlabel('Themes')
        self.ax.set_ylabel('Sales')
        self.ax.set_title('Actual vs Predicted Sales by Theme')
        self.ax.set_xticks(index + bar_width / 2)
        self.ax.set_xticklabels(themes, rotation=45, ha="right")
        self.ax.legend()

        self.canvas.draw()


class ThemeBreakdown(tk.Frame):
    def __init__(self, parent, controller, close_app_callback):
        tk.Frame.__init__(self, parent, bg="#2E3B4E")
        self.columnconfigure(0, weight=1)

        label = tk.Label(self, text="Explore by Theme", font=("Helvetica", 28), bg="#2E3B4E",
                         fg="#D1D9E6")
        label.grid(row=0, column=0, columnspan=3, pady=20)

        theme_dd_frame = tk.Frame(self, bg="#2E3B4E")
        theme_dd_frame.grid(row=1, column=0, padx=50, pady=20)

        dd_label = tk.Label(theme_dd_frame, text="Select a Theme", font=("Helvetica", 12), bg="#2E3B4E", fg="#D1D9E6")
        dd_label.pack(side="top", pady=10)
        themes = ["Anime", "Fantasy", "History", "Horror", "Modern", "Mystery", "Post-apocalyptic",
                  "Science-fiction", "Superhero", "War"]
        self.selected_theme = tk.StringVar()
        theme_dropdown = ttk.Combobox(theme_dd_frame, textvariable=self.selected_theme, values=themes, state="readonly")
        theme_dropdown.pack(side="left", pady=10)
        action_button = tk.Button(theme_dd_frame, text="Show Data", command=self.graph_by_theme)
        action_button.pack(side="left", pady=10)

        self.graph_frame = tk.Frame(self, bg="#2E3B4E")
        self.graph_frame.grid(row=2, column=0, columnspan=3, padx=50, pady=20)
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.fig.tight_layout(pad=6.0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        back_button = tk.Button(self, text="Return", font=("Verdana", 16), width=25, height=2, bg="#D1D9E6",
                                fg="#2E3B4E", command=lambda: controller.show_frame("HomePage"))
        back_button.grid(row=3, column=0, columnspan=3, padx=50, pady=20, sticky="s")

    def graph_by_theme(self):
        theme = self.selected_theme.get()
        grouped_df = data_getters.model_by_theme(theme)

        self.ax.clear()
        if grouped_df.empty:
            grouped_df['Actual_Sales'] = 0

        bar_width = 0.35
        genre_indices = range(11, 17)
        index = np.array(genre_indices) - bar_width / 2
        bar1 = self.ax.bar(index, grouped_df['Actual_Sales'], bar_width, label='Actual')
        bar2 = self.ax.bar(index + bar_width, grouped_df['Predicted_Sales'], bar_width, label='Predicted')
        genres = []
        for i in genre_indices:
            genres.append(data_getters.all_mapping(i))

        self.ax.set_xlabel('Genres')
        self.ax.set_ylabel('Sales')
        self.ax.set_title('Actual vs Predicted Sales by Genre')
        self.ax.set_xticks(index + bar_width / 2)
        self.ax.set_xticklabels(genres, rotation=45, ha="right")
        self.ax.legend()

        self.canvas.draw()


class KpiMetrics(tk.Frame):
    def __init__(self, parent, controller, close_app_callback):
        tk.Frame.__init__(self, parent, bg="#2E3B4E")
        self.columnconfigure(0, weight=1)

        page_canvas = tk.Canvas(self, bg="#2E3B4E", borderwidth=0)
        page_canvas.pack(side="left", fill="both", expand=True)
        page_frame = tk.Frame(page_canvas, bg="#2E3B4E")

        screen_width = self.winfo_screenwidth()
        window_width = (screen_width - 10)
        center_x = (window_width / 6)

        page_canvas.create_window((center_x, 0), window=page_frame, anchor="nw")

        scrollbar = ttk.Scrollbar(page_canvas, orient="vertical", command=page_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        page_canvas.config(yscrollcommand=scrollbar.set)

        label = tk.Label(page_frame, text="KPIs", font=("Helvetica", 28), bg="#2E3B4E",
                         fg="#D1D9E6")
        label.grid(row=0, column=0, columnspan=3, pady=50)

        mse = data_getters.get_mse()
        r2 = data_getters.get_r2()
        ev = data_getters.get_explained_var()
        residuals = data_getters.get_residuals()
        y_pred = data_getters.get_y_pred()
        var = data_getters.get_variance()
        ratio = (mse / var) * 100

        kpi_frame = tk.Frame(page_frame, bg="#2E3B4E")
        kpi_frame.grid(row=1, column=0, columnspan=3, pady=20)

        ev_frame = tk.Frame(kpi_frame, bg="#2E3B4E")
        ev_frame.pack(side="left", anchor="n", expand=True, fill="both", pady=10, padx=10)
        ev_title = tk.Label(ev_frame, text="Explained Variance", font=("Helvetica", 16), bg="#2E3B4E", fg="#D1D9E6")
        ev_title.pack(pady=10)
        ev_label = tk.Label(ev_frame, text=f"The Explained Variance value for this model is \n{ev:.4f}.",
                            font=("Helvetica", 12), bg="#2E3B4E", fg="#D1D9E6")
        ev_label.pack(pady=5)
        ev_descrip = tk.Label(ev_frame, text=f"An Explained Variance of {ev:.4f} tells us that the model is\n"
                                             "only slightly able to explain the variance in the dependent\n"
                                             "variable. It is too complex of a relationship to capture.",
                              font=("Helvetica", 12), bg="#2E3B4E", fg="#D1D9E6")
        ev_descrip.pack(pady=5)

        mse_frame = tk.Frame(kpi_frame, bg="#2E3B4E")
        mse_frame.pack(side="left", anchor="n", expand=True, fill="both", pady=10, padx=10)
        mse_title = tk.Label(mse_frame, text="Mean Squared Error", font=("Helvetica", 16), bg="#2E3B4E", fg="#D1D9E6")
        mse_title.pack(pady=10)
        mse_label = tk.Label(mse_frame, text=f"The MSE value for this model is \n{mse:.4f}.", font=("Helvetica", 12),
                              bg="#2E3B4E", fg="#D1D9E6")
        mse_label.pack(pady=5)
        mse_descrip = tk.Label(mse_frame, text=f"An Mean Squared Error of {mse:.4f} on a scaled range of {var:.2f} \n"
                                             f"tells us that the model's error margin is within {ratio:.2f}%\n"
                                             "of the true values, which -- considering video game sales can vary\n"
                                             "by tens of millions of copies per year -- is a decent estimate.",
                              font=("Helvetica", 12), bg="#2E3B4E", fg="#D1D9E6")
        mse_descrip.pack(pady=5)

        r2_frame = tk.Frame(kpi_frame, bg="#2E3B4E")
        r2_frame.pack(side="left", anchor="n", expand=True, fill="both", pady=10, padx=10)
        r2_title = tk.Label(r2_frame, text="R-Squared", font=("Helvetica", 16), bg="#2E3B4E", fg="#D1D9E6")
        r2_title.pack(pady=10)
        r2_label = tk.Label(r2_frame, text=f"The R2 value for this model is \n{r2:.4f}.", font=("Helvetica", 12),
                             bg="#2E3B4E", fg="#D1D9E6")
        r2_label.pack(pady=5)
        r2_descrip = tk.Label(r2_frame, text=f"An R-Squared value of {r2:.4f} in a model\n"
                              "of this complexity can be considered good, but not great.\n"
                              "R-Squared is more apt to use on linear regression models.",
                              font=("Helvetica", 12), bg="#2E3B4E", fg="#D1D9E6")
        r2_descrip.pack(pady=5)

        res_frame = tk.Frame(page_frame, bg="#2E3B4E")
        res_frame.grid(row=2, column=0, columnspan=3, pady=20)
        res_title = tk.Label(res_frame, text="Residual Analysis", font=("Helvetica", 16), bg="#2E3B4E", fg="#D1D9E6")
        res_title.pack(pady=10)
        res_descrip = tk.Label(res_frame, text="The scatterplot below plots the residuals, or the differences between\n"
                                               "the true values and the predicted values. A pattern in the residuals\n"
                                               "would show us that there were trends the model was missing; however, I \n"
                                               "feel satisfied that the residuals are dispersed enough in this graph\n"
                                               "to say with confidence we have not missed valuable information.",
                               font=("Helvetica", 12), bg="#2E3B4E", fg="#D1D9E6")
        res_descrip.pack(pady=5)

        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        sns.scatterplot(x=y_pred, y=residuals, ax=ax)
        ax.axhline(0, color='red', linestyle='--', linewidth=2)
        ax.set_title("Residual Plot")
        ax.set_xlabel("Predicted Values")
        ax.set_ylabel("Residuals")
        canvas = FigureCanvasTkAgg(fig, master=res_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        back_frame = tk.Frame(page_frame, bg="#2E3B4E")
        back_frame.grid(row=3, column=0, columnspan=3, pady=20)
        back_button = tk.Button(back_frame, text="Return", font=("Verdana", 16), width=25, height=2, bg="#D1D9E6",
                                fg="#2E3B4E", command=lambda: controller.show_frame("HomePage"))
        back_button.pack(side="top", fill="both", expand=True, pady=10)

        page_frame.update_idletasks()

        def on_frame_configure(event):
            page_canvas.configure(scrollregion=page_canvas.bbox("all"))

        def on_mousewheel(event):
            page_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        page_frame.bind("<Configure>", on_frame_configure)
        page_canvas.bind("<MouseWheel>", on_mousewheel)


if __name__ == "__main__":
    install_libraries()
    app = MainWindow()
    app.mainloop()
