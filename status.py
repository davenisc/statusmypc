import psutil
import tkinter as tk
from tkinter import Canvas
import threading
import time

class SystemMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")

        # Configurar la transparencia de la ventana
        self.root.attributes('-alpha', 0.9)  # Ajusta la opacidad de la ventana (0.0 a 1.0)
        self.root.attributes('-transparentcolor', 'white')  # El color blanco será transparente

        # Crear un canvas para dibujar los círculos con fondo transparente
        self.canvas = Canvas(root, width=400, height=300, bg='white', highlightthickness=0)
        self.canvas.pack()

        # Variables para los IDs de los círculos
        self.ram_circle = None
        self.disk_circle = None
        self.cpu_circle = None

        # Iniciar el monitoreo en un hilo separado
        self.update_thread = threading.Thread(target=self.update)
        self.update_thread.daemon = True
        self.update_thread.start()

    def draw_circle(self, x, y, r, outline, fill, percentage, label, label_color):
        # Dibujar el círculo con el porcentaje de uso en el centro
        self.canvas.create_oval(x - r, y - r, x + r, y + r, outline=outline, fill=fill, width=2)
        # Añadir el título del círculo
        self.canvas.create_text(x, y - r - 20, text=label, fill=label_color, font=("Arial", 12, 'bold'))
        # Dibujar el texto con borde para mejor legibilidad
        self.canvas.create_text(x-1, y-1, text=f"{percentage}%", fill=label_color, font=("Arial", 16, 'bold'))
        self.canvas.create_text(x+1, y-1, text=f"{percentage}%", fill=label_color, font=("Arial", 16, 'bold'))
        self.canvas.create_text(x-1, y+1, text=f"{percentage}%", fill=label_color, font=("Arial", 16, 'bold'))
        self.canvas.create_text(x+1, y+1, text=f"{percentage}%", fill=label_color, font=("Arial", 16, 'bold'))
        self.canvas.create_text(x, y, text=f"{percentage}%", fill="white", font=("Arial", 16, 'bold'))

    def update(self):
        while True:
            # Obtener los valores actuales de RAM, disco y CPU
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            cpu_usage = psutil.cpu_percent(interval=1)

            # Limpiar el canvas
            self.canvas.delete("all")

            # Dibujar los círculos con los nuevos valores y sus títulos
            self.draw_circle(100, 150, 40, "gray", "gray", ram_usage, "RAM", "blue")
            self.draw_circle(200, 150, 40, "gray", "gray", disk_usage, "Disk", "green")
            self.draw_circle(300, 150, 40, "gray", "gray", cpu_usage, "CPU", "red")

            # Esperar un segundo antes de actualizar nuevamente
            time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitor(root)
    root.mainloop()
