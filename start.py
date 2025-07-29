import tkinter as tk
from tkinter import messagebox
import configparser
import os
import obd
from obd import OBDStatus
from mainwindow import MainWindowPart

CONFIG_FILE = "config.ini"

class BMW_OBD_App:
    def __init__(self):
        self.config = self.load_config()
        self.debug = self.config.getboolean('DEBUG', 'debug_mode', fallback=False)
        self.can_port = self.config.get('OBD', 'can_port', fallback='COM3')
        self.connection = None
        self.vin = "" # wie auch, wenn das Programm erst hochgefahren ist?!
        
        if not self.debug:
            try:
                self.connection = obd.OBD(self.can_port)
                status = self.connection.status()

                if status != OBDStatus.OBD_CONNECTED:
                    print(f"Verbindung nicht vollständig. Status: {status}")
            except Exception as e:
                print(f"Konnte keine Verbindung herstellen: {e}")
                self.connection = None
        else:
            print("DEBUG MODE: Keine echte OBD-Verbindung! Wir simulieren eine Verbindung.")

        # self.launch_main_window()

    def load_config(self):
        config = configparser.ConfigParser()
        if not os.path.exists(CONFIG_FILE):
            messagebox.showerror("Fehlende Konfigurationsdatei", f"{os.path.abspath(CONFIG_FILE)} konnte nicht gefunden werden.")
            exit(1)
        config.read(CONFIG_FILE)
        if 'DEBUG' not in config:
            config['DEBUG'] = {'debug_mode': 'false'}
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)
        return config
    
    def launch_main_window(self):
        main_window = MainWindowPart(vin=self.vin, config=self.config, connection=self.connection)


    def detect_can(self, model_entry):
        try:
            connection = obd.OBD(self.can_port)
            if connection.is_connected():
                vin_resp = connection.query(obd.commands.VIN)
                if vin_resp and vin_resp.value:
                    messagebox.showinfo("CAN-Erkennung erfolgreich", f"Fahrzeug erkannt: {vin_resp.value}")
                    model_entry.delete(0, tk.END)
                    model_entry.insert(0, vin_resp.value)
                    self.connection = connection
                    self.vin = vin_resp.value
                    return connection
                else:
                    messagebox.showwarning("Erkannt", "Verbindung erfolgreich, aber VIN nicht lesbar.")
                    connection.close()
            else:
                messagebox.showerror("Fehler", f"Keine Verbindung über {self.can_port}.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Verbindungsfehler: {e}")
        return None

    def start_gui(self):
        root = tk.Tk()
        root.title("BMW OBD Start")
        root.geometry("500x800")
        root.resizable(False, False)
        root.attributes('-toolwindow', False)
        root.iconbitmap('favico.ico')

        if self.debug:
            tk.Label(root, text="DEBUG MODE", font=("Helvetica", 14, "bold"), fg="red").pack(pady=(10, 0))

        tk.Label(root, text="BMW FIN:", font=("Helvetica", 14)).pack(pady=10)
        model_entry = tk.Entry(root, font=("Helvetica", 12))
        model_entry.pack(pady=10)

        def on_continue():
            model = model_entry.get().strip()
            if not model:
                messagebox.showwarning("Modell erforderlich", "CAN-Erkennung verwenden")
                return
            root.destroy()
            # Übergib Verbindung und VIN an MainWindowPart
            MainWindowPart(vin=model, config=self.config, connection=self.connection)

        def debug_skip():
            root.destroy()
            # Im Debug Mode: Keine echte Verbindung, aber feste VIN
            MainWindowPart(
                vin="wbaux110x0a687741", 
                config=self.config, 
                connection=None
                )

        tk.Button(root, text="CAN automatisch erkennen", command=lambda: self.detect_can(model_entry), font=("Helvetica", 12)).pack(pady=5)
        tk.Button(root, text="Weiter", command=on_continue, font=("Helvetica", 12)).pack(pady=20)

        if self.debug:
            debug_button = tk.Button(root, text=">> SKIP", command=debug_skip,
                                    font=("Helvetica", 10), fg="white", bg="red")
            debug_button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor='se')

        root.mainloop()

    def run(self):
        self.start_gui()

if __name__ == "__main__":
    try:
        app = BMW_OBD_App()
        app.run()
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        exit(1)
