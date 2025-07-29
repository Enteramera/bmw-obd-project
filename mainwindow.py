
import rel as rel
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use('TkAgg')  # Verwende das TkAgg-Backend für Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import time
import obd
import random  # Für Debug-Simulation
from obd import OBDStatus

class MainWindowPart:
    def __init__(self, vin, config, connection=None):
        self.vin = vin
        self.config = config
        self.connection = connection
        self.active_button_index = 0
        self.debug = config.getboolean('DEBUG', 'debug_mode', fallback=False)
        self.can_port = config.get('OBD', 'can_port', fallback='COM3')

        if self.debug and self.connection is None:
            print(f"DEBUG MODE: keine echte OBD-Verbindung! Wir simulieren {str(self.vin).upper()}!")
        else:
            if not self.connection:
                try:
                    self.connection = obd.OBD(self.can_port)
                except Exception as e:
                    messagebox.showerror("Verbindungsfehler", f"OBD-Verbindung konnte nicht aufgebaut werden:\n{e}")
                    self.connection = None

        self.root = tk.Tk()
        self.root.title(f"Welcome, {str(self.vin).upper()}!")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        self.root.attributes('-toolwindow', False)
        self.root.iconbitmap('favico.ico')

        self.setup_menu()
        self.setup_ui()

        self.content_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.content_frame.pack(fill="both", expand=True)

        self.create_bottom_header_gradient()
        self.create_skewed_navigation_bar()

        self.show_fahrzeug()

        self.root.mainloop()

    def setup_menu(self):
        menubar = tk.Menu(self.root)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Über...", command=self.show_about)
        filemenu.add_separator()
        filemenu.add_command(label="Schließen", command=self.root.quit)
        menubar.add_cascade(label="Datei", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Hilfe", command=self.show_help)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)

    def show_about(self):
        messagebox.showinfo("Über BMW OBD Tool",
                            f"BMW OBD Tool\nVersion: {rel.version}\nAutor: {rel.author}\nBuild: {rel.build_date}")

    def show_help(self):
        messagebox.showinfo("Hilfe",
                            "Dieses Tool dient zur OBD-Diagnose von BMW Fahrzeugen.\n\nxxx")

    def setup_ui(self):
        pass  # Aktuell keine weiteren UI-Elemente notwendig

    def create_skewed_navigation_bar(self):
        nav_height = 50
        self.nav_frame = tk.Frame(self.root, height=nav_height)
        self.nav_frame.pack(side="bottom", fill="x")

        self.canvas = tk.Canvas(self.nav_frame, height=nav_height, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.buttons = [
            "Fahrzeug",
            "Diagnose",
            "Live-Daten",
            "Fehlercodes",
            "Service",
            "Einstellungen"
        ]

        self.btn_width = 180
        self.btn_height = 40
        self.skew = 20
        self.spacing = 0
        self.start_x = 20

        self.btn_polygons = []
        self.btn_texts = []

        for i, text in enumerate(self.buttons):
            active = (i == self.active_button_index)
            x1 = self.start_x + i * (self.btn_width + self.spacing)
            x2 = x1 + self.btn_width
            y1 = 5
            y2 = y1 + self.btn_height

            points = [x1 + self.skew, y1,
                      x2 + self.skew, y1,
                      x2 - self.skew, y2,
                      x1 - self.skew, y2]

            fill_color = "#0582ca" if active else "#003554"

            polygon = self.canvas.create_polygon(points, fill=fill_color, outline="white", width=2, tags=(f"btn{i}",))
            self.btn_polygons.append(polygon)

            font_weight = "bold" if active else "normal"
            text_id = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                              text=text.upper(),
                                              fill="white",
                                              font=("Arial", 11, font_weight),
                                              tags=(f"btn{i}",))
            self.btn_texts.append(text_id)

        for i in range(len(self.buttons)):
            self.canvas.tag_bind(f"btn{i}", "<Enter>", lambda e, idx=i: self.on_hover(idx))
            self.canvas.tag_bind(f"btn{i}", "<Leave>", lambda e, idx=i: self.on_leave(idx))
            self.canvas.tag_bind(f"btn{i}", "<Button-1>", lambda e, idx=i: self.on_click(idx))

    def on_hover(self, idx):
        if idx != self.active_button_index:
            self.canvas.itemconfig(self.btn_polygons[idx], fill="#0582ca")

    def on_leave(self, idx):
        if idx != self.active_button_index:
            self.canvas.itemconfig(self.btn_polygons[idx], fill="#003554")

    def on_click(self, idx):
        self.active_button_index = idx

        for i in range(len(self.buttons)):
            active = (i == idx)
            fill_color = "#0582ca" if active else "#003554"
            font_weight = "bold" if active else "normal"
            self.canvas.itemconfig(self.btn_polygons[i], fill=fill_color)
            self.canvas.itemconfig(self.btn_texts[i], font=("Arial", 11, font_weight))

        page = self.buttons[idx]
        if page == "Fahrzeug":
            self.show_fahrzeug()
        elif page == "Diagnose":
            self.show_diagnose()
        elif page == "Live-Daten":
            self.show_live_data()
        elif page == "Fehlercodes":
            self.show_fehlercodes()
        elif page == "Service":
            self.show_service()
        elif page == "Einstellungen":
            self.show_settings()

    def create_bottom_header_gradient(self):
        self.header_height = 15
        self.header_width = 1200
        self.header_canvas = tk.Canvas(self.root, width=self.header_width, height=self.header_height, highlightthickness=0)
        self.header_canvas.pack(side='bottom')
        self.draw_gradient(self.header_canvas, self.header_width, self.header_height, [
            (0.0, (129, 196, 255)),
            (0.5, (22, 88, 142)),
            (1.0, (231, 34, 46))
        ])

    def draw_gradient(self, canvas, width, height, colors):
        for i in range(width):
            rel_pos = i / (width - 1)
            for j in range(len(colors) - 1):
                if colors[j][0] <= rel_pos <= colors[j+1][0]:
                    left_pos, left_color = colors[j]
                    right_pos, right_color = colors[j+1]
                    local_rel = (rel_pos - left_pos) / (right_pos - left_pos)
                    r = int(left_color[0] + (right_color[0] - left_color[0]) * local_rel)
                    g = int(left_color[1] + (right_color[1] - left_color[1]) * local_rel)
                    b = int(left_color[2] + (right_color[2] - left_color[2]) * local_rel)
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    canvas.create_line(i, 0, i, height, fill=hex_color)
                    break

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_fahrzeug(self):
        self.clear_content()
        tk.Label(self.content_frame, text="🚗 Fahrzeug", fg="white", bg="#1e1e1e", font=("Helvetica", 16)).pack(pady=20)

    def show_diagnose(self):
        self.clear_content()
        tk.Label(self.content_frame, text="🔧 Diagnose", fg="white", bg="#1e1e1e", font=("Helvetica", 16)).pack(pady=20)

    def show_live_data(self):
        self.clear_content()
        tk.Label(self.content_frame, text="📊 Live-Daten", fg="white", bg="#1e1e1e", font=("Helvetica", 16, "bold")).pack(pady=20)

    def show_fehlercodes(self):
        self.clear_content()
        tk.Label(self.content_frame, text="🚨 Fehlercodes", fg="white", bg="#1e1e1e", font=("Helvetica", 16)).pack(pady=20)

    def show_service(self):
        self.clear_content()
        tk.Label(self.content_frame, text="🛠️ Service", fg="white", bg="#1e1e1e", font=("Helvetica", 16)).pack(pady=20)

    def show_settings(self):
        self.clear_content()
        tk.Label(self.content_frame, text="⚙️ Einstellungen", fg="white", bg="#1e1e1e", font=("Helvetica", 16)).pack(pady=20)
        debug_mode = self.config.getboolean('DEBUG', 'debug_mode', fallback=False)
        tk.Label(self.content_frame, text=f"Debug-Modus: {'Aktiviert' if debug_mode else 'Deaktiviert'}",
                 fg="white", bg="#1e1e1e", font=("Helvetica", 12)).pack(pady=10)