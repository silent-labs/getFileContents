import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import keyboard
import pystray
from PIL import Image
import threading
import setproctitle
import json
from datetime import datetime

class FileProcessorApp:
    def __init__(self):
        setproctitle.setproctitle('getFileContents')
        
        # Definir colores para los temas
        self.light_theme = {
            'bg': '#f0f0f0',
            'fg': '#333333',
            'button_bg': '#007bff',
            'button_fg': '#ffffff',
            'tree_bg': '#ffffff',
            'tree_fg': '#333333',
            'accent': '#007bff',
            'hover': '#0056b3',
            'selected': '#e8f0fe'
        }
        
        self.dark_theme = {
            'bg': '#2b2b2b',
            'fg': '#ffffff',
            'button_bg': '#007bff',
            'button_fg': '#ffffff',
            'tree_bg': '#333333',
            'tree_fg': '#ffffff',
            'accent': '#007bff',
            'hover': '#0056b3',
            'selected': '#1a3f5f'
        }
        
        # Cargar tema guardado o usar claro por defecto
        self.current_theme = self.load_theme_preference()
        
        self.window = tk.Tk()
        self.window.title("File Contents Processor")
        self.window.geometry("1200x800")
        
        # Configurar el estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Crear el contenedor principal con padding
        self.main_frame = ttk.Frame(self.window, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header frame
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título de la aplicación
        self.title_label = ttk.Label(
            self.header_frame,
            text="File Contents Processor",
            font=('Segoe UI', 24, 'bold')
        )
        self.title_label.pack(side=tk.LEFT)

        # Frame para botones de acción
        self.action_frame = ttk.Frame(self.main_frame)
        self.action_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Path frame con estilo moderno
        self.path_frame = ttk.Frame(self.action_frame)
        self.path_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.path_label = ttk.Label(
            self.path_frame,
            text="📁 Ningún directorio seleccionado",
            font=('Segoe UI', 10)
        )
        self.path_label.pack(side=tk.LEFT, pady=5)

        # Botones con estilo moderno
        self.buttons_frame = ttk.Frame(self.action_frame)
        self.buttons_frame.pack(fill=tk.X)

        self.select_button = ttk.Button(
            self.buttons_frame,
            text="📂 Seleccionar Carpeta",
            command=self.select_folder,
            style='Accent.TButton'
        )
        self.select_button.pack(side=tk.LEFT, padx=(0, 10))

        self.theme_button = ttk.Button(
            self.buttons_frame,
            text="🎨 Cambiar Tema",
            command=self.toggle_theme,
            style='Accent.TButton'
        )
        self.theme_button.pack(side=tk.LEFT)

        # Frame principal para el Treeview
        self.files_frame = ttk.Frame(self.main_frame)
        self.files_frame.pack(fill=tk.BOTH, expand=True)

        # Label para la lista
        self.files_label = ttk.Label(
            self.files_frame,
            text="Archivos Disponibles",
            font=('Segoe UI', 12, 'bold')
        )
        self.files_label.pack(anchor=tk.W, pady=(0, 10))

        # Crear el Treeview y scrollbars
        self.tree_container = ttk.Frame(self.files_frame)
        self.tree_container.pack(fill=tk.BOTH, expand=True)

        # Scrollbars
        self.vsb = ttk.Scrollbar(self.tree_container, orient="vertical")
        self.hsb = ttk.Scrollbar(self.tree_container, orient="horizontal")
        
        # Treeview
        self.tree = ttk.Treeview(
            self.tree_container,
            columns=("size", "modified", "type"),
            selectmode="extended",
            yscrollcommand=self.vsb.set,
            xscrollcommand=self.hsb.set
        )

        # Configurar scrollbars
        self.vsb.config(command=self.tree.yview)
        self.hsb.config(command=self.tree.xview)

        # Configurar columnas
        self.tree.heading("#0", text="Nombre", anchor=tk.W)
        self.tree.heading("size", text="Tamaño", anchor=tk.W)
        self.tree.heading("modified", text="Modificado", anchor=tk.W)
        self.tree.heading("type", text="Tipo", anchor=tk.W)

        self.tree.column("#0", width=400, minwidth=200)
        self.tree.column("size", width=100, minwidth=100)
        self.tree.column("modified", width=150, minwidth=150)
        self.tree.column("type", width=100, minwidth=100)

        # Empaquetar Treeview y scrollbars
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra de búsqueda
        self.search_frame = ttk.Frame(self.files_frame)
        self.search_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_files)
        
        self.search_entry = ttk.Entry(
            self.search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 10)
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Placeholder para la búsqueda
        self.search_entry.insert(0, "🔍 Buscar archivos...")
        self.search_entry.bind('<FocusIn>', self.on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self.on_search_focus_out)

        # Frame para botones de acción inferiores
        self.bottom_frame = ttk.Frame(self.main_frame)
        self.bottom_frame.pack(fill=tk.X, pady=(20, 0))

        # Contador de selección
        self.selection_label = ttk.Label(
            self.bottom_frame,
            text="0 archivos seleccionados",
            font=('Segoe UI', 10)
        )
        self.selection_label.pack(side=tk.LEFT)

        self.process_button = ttk.Button(
            self.bottom_frame,
            text="✨ Procesar Seleccionados",
            command=self.process_files,
            style='Accent.TButton'
        )
        self.process_button.pack(side=tk.RIGHT)

        # Status bar
        self.status_bar = ttk.Label(
            self.main_frame,
            text="Presiona Ctrl+Alt+P para mostrar/ocultar la ventana",
            font=('Segoe UI', 9),
            foreground='gray'
        )
        self.status_bar.pack(fill=tk.X, pady=(20, 0))

        self.folder_path = None
        self.file_paths = {}  # Diccionario para guardar las rutas completas

        # Configurar atajo global
        try:
            keyboard.unhook_all()
        except:
            pass
        keyboard.add_hotkey('ctrl+alt+p', self.toggle_window, suppress=True)
        
        # Configurar icono de bandeja
        self.icon = self.create_tray_icon()
        self.window.protocol('WM_DELETE_WINDOW', self.hide_window)
        
        self.is_visible = False
        
        # Vincular evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.update_selection_count)

    def update_selection_count(self, event=None):
        """Actualiza el contador de archivos seleccionados"""
        count = len(self.tree.selection())
        self.selection_label.config(
            text=f"{count} {'archivo seleccionado' if count == 1 else 'archivos seleccionados'}"
        )

    def on_search_focus_in(self, event):
        """Maneja el evento de focus en la barra de búsqueda"""
        if self.search_entry.get() == "🔍 Buscar archivos...":
            self.search_entry.delete(0, tk.END)

    def on_search_focus_out(self, event):
        """Maneja el evento de pérdida de focus en la barra de búsqueda"""
        if not self.search_entry.get():
            self.search_entry.insert(0, "🔍 Buscar archivos...")

    def filter_files(self, *args):
        """Filtra los archivos según el texto de búsqueda"""
        search_text = self.search_var.get().lower()
        if search_text == "🔍 buscar archivos...":
            return

        # Limpiar árbol
        self.tree.delete(*self.tree.get_children())

        # Si no hay texto de búsqueda, mostrar todos los archivos
        if not search_text:
            self.update_file_list()
            return

        # Filtrar y mostrar archivos que coincidan
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                if search_text in file.lower():
                    file_path = os.path.join(root, file)
                    self.add_file_to_tree(file_path)

    def get_file_size(self, size_in_bytes):
        """Convierte el tamaño en bytes a una forma legible"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_in_bytes < 1024:
                return f"{size_in_bytes:.1f} {unit}"
            size_in_bytes /= 1024
        return f"{size_in_bytes:.1f} TB"

    def get_file_type(self, file_path):
        """Obtiene el tipo de archivo basado en su extensión"""
        ext = os.path.splitext(file_path)[1].lower()
        return ext[1:].upper() if ext else "File"

    def add_file_to_tree(self, file_path):
        """Añade un archivo al Treeview con su información"""
        try:
            # Obtener información del archivo
            file_stats = os.stat(file_path)
            rel_path = os.path.relpath(file_path, self.folder_path)
            size = self.get_file_size(file_stats.st_size)
            modified = datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M')
            file_type = self.get_file_type(file_path)

            # Insertar en el Treeview
            self.tree.insert(
                "",
                tk.END,
                text=rel_path,
                values=(size, modified, file_type),
                tags=('file',)
            )
            
            # Guardar la ruta completa
            self.file_paths[rel_path] = file_path
        except Exception as e:
            print(f"Error procesando {file_path}: {e}")

    def update_file_list(self):
        """Actualiza la lista de archivos en el Treeview"""
        self.tree.delete(*self.tree.get_children())
        self.file_paths.clear()
        
        if not self.folder_path:
            return

        for root, _, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.add_file_to_tree(file_path)

    def process_files(self):
        """Procesa los archivos seleccionados"""
        if not self.folder_path:
            return

        selected_items = self.tree.selection()
        if not selected_items:
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")],
            title="Guardar resultado como"
        )
        
        if not output_path:
            return

        output = []
        for item in selected_items:
            rel_path = self.tree.item(item)['text']
            file_path = self.file_paths.get(rel_path)
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        output.append(f"\n------- {file_path} -------\n")
                        output.append(content)
                        output.append("\n")
                except Exception as e:
                    print(f"Error leyendo {file_path}: {e}")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(output)

    def create_tray_icon(self):
        # Crear un icono simple (puedes reemplazarlo con tu propio .ico)
        image = Image.new('RGB', (64, 64), color='blue')
        menu = pystray.Menu(
            pystray.MenuItem("Mostrar", self.show_window),
            pystray.MenuItem("Salir", self.quit_app)
        )
        icon = pystray.Icon("name", image, "File Contents Processor", menu)
        return icon

    def toggle_window(self):
        if self.is_visible:
            self.hide_window()
        else:
            self.show_window()
        self.is_visible = not self.is_visible

    def show_window(self):
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()
        self.is_visible = True

    def hide_window(self):
        self.window.withdraw()
        if not self.icon.visible:
            threading.Thread(target=self.icon.run).start()
        self.is_visible = False

    def quit_app(self):
        self.icon.stop()
        self.window.destroy()

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.path_label.config(text=f"📁 {self.folder_path}")
            self.update_file_list()

    def apply_theme(self):
        """Aplica el tema actual a todos los widgets"""
        theme = self.dark_theme if self.current_theme == 'dark' else self.light_theme
        
        # Configurar estilos
        self.configure_styles()
        
        # Configurar widgets tradicionales de tk que no usan ttk
        self.window.configure(bg=theme['bg'])

        # Actualizar los estilos ttk
        self.style.configure('TFrame', background=theme['bg'])
        self.style.configure('TLabel', 
            background=theme['bg'],
            foreground=theme['fg']
        )
        
        # Configurar estilo del Treeview
        self.style.configure("Treeview",
            background=theme['tree_bg'],
            foreground=theme['tree_fg'],
            fieldbackground=theme['tree_bg']
        )
        
        # Configurar selección del Treeview
        self.style.map('Treeview',
            background=[('selected', theme['selected'])],
            foreground=[('selected', theme['tree_fg'])]
        )

        # Configurar estilo de los botones
        self.style.configure('Accent.TButton',
            background=theme['accent'],
            foreground=theme['button_fg']
        )
        self.style.map('Accent.TButton',
            background=[('active', theme['hover']), ('pressed', theme['hover'])],
            foreground=[('active', theme['button_fg']), ('pressed', theme['button_fg'])]
        )

    def configure_styles(self):
        """Configura los estilos personalizados para los widgets"""
        theme = self.dark_theme if self.current_theme == 'dark' else self.light_theme
        
        # Estilo para botones principales
        self.style.configure(
            'Accent.TButton',
            padding=(20, 10),
            font=('Segoe UI', 10)
        )

        # Estilo para frames
        self.style.configure(
            'TFrame',
            background=theme['bg']
        )

        # Estilo para labels
        self.style.configure(
            'TLabel',
            font=('Segoe UI', 10)
        )

        # Estilo para el Treeview
        self.style.configure(
            'Treeview',
            font=('Segoe UI', 10),
            rowheight=25
        )
        
        # Estilo para el encabezado del Treeview
        self.style.configure(
            'Treeview.Heading',
            font=('Segoe UI', 10, 'bold')
        )

        # Estilo para scrollbar
        self.style.configure(
            'Vertical.TScrollbar',
            background=theme['bg'],
            troughcolor=theme['bg'],
            arrowsize=12
        )

    def toggle_theme(self):
        """Alterna entre tema claro y oscuro"""
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.save_theme_preference()
        self.apply_theme()

    def save_theme_preference(self):
        """Guarda la preferencia del tema en un archivo"""
        config = {'theme': self.current_theme}
        try:
            with open('theme_config.json', 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Error al guardar la preferencia del tema: {e}")

    def load_theme_preference(self):
        """Carga la preferencia del tema desde el archivo"""
        try:
            with open('theme_config.json', 'r') as f:
                config = json.load(f)
                return config.get('theme', 'light')
        except:
            return 'light'

    def run(self):
        self.apply_theme()  # Aplicar tema inicial
        # Iniciar minimizado
        self.hide_window()
        self.window.mainloop()

if __name__ == "__main__":
    app = FileProcessorApp()
    app.run()
