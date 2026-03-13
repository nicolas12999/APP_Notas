"""
Aplicación gráfica CRUD con CustomTkinter.
Interfaz moderna con tema oscuro para gestión de items en MySQL.
"""
import customtkinter as ctk
from tkinter import messagebox
from database import Database


class App(ctk.CTk):
    """Ventana principal de la aplicación."""

    def __init__(self):
        super().__init__()

        # --- Configuración de ventana ---
        self.title("📦 Gestor de Items — Docker App")
        self.geometry("900x650")
        self.minsize(750, 550)

        # Tema oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- Conexión a BD ---
        self.db = Database()
        self.db_connected = self.db.connect()

        # --- Construir interfaz ---
        self._build_header()
        self._build_form()
        self._build_table()
        self._build_status_bar()

        # Cargar datos iniciales
        self.refresh_items()

        # Cerrar BD al salir
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # =========================================
    # UI Components
    # =========================================

    def _build_header(self):
        """Encabezado con título y estado de conexión."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header,
            text="📦 Gestor de Items",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).pack(side="left")

        status_color = "#2ecc71" if self.db_connected else "#e74c3c"
        status_text = "● Conectado" if self.db_connected else "● Desconectado"
        self.status_label = ctk.CTkLabel(
            header,
            text=status_text,
            font=ctk.CTkFont(size=14),
            text_color=status_color,
        )
        self.status_label.pack(side="right")

    def _build_form(self):
        """Formulario para añadir nuevo item."""
        form_frame = ctk.CTkFrame(self, corner_radius=12)
        form_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            form_frame,
            text="Añadir nuevo item",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=0, column=0, columnspan=3, padx=15, pady=(15, 10), sticky="w")

        # Nombre
        ctk.CTkLabel(form_frame, text="Nombre:", font=ctk.CTkFont(size=13)).grid(
            row=1, column=0, padx=(15, 5), pady=5, sticky="w"
        )
        self.entry_nombre = ctk.CTkEntry(
            form_frame, placeholder_text="Nombre del item", width=250
        )
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Descripción
        ctk.CTkLabel(form_frame, text="Descripción:", font=ctk.CTkFont(size=13)).grid(
            row=2, column=0, padx=(15, 5), pady=5, sticky="w"
        )
        self.entry_desc = ctk.CTkEntry(
            form_frame, placeholder_text="Descripción del item", width=250
        )
        self.entry_desc.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Botones
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=1, column=2, rowspan=2, padx=15, pady=5)

        ctk.CTkButton(
            btn_frame,
            text="➕ Añadir",
            command=self._add_item,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=120,
            height=36,
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(pady=(0, 5))

        ctk.CTkButton(
            btn_frame,
            text="🔄 Refrescar",
            command=self.refresh_items,
            fg_color="#3498db",
            hover_color="#2980b9",
            width=120,
            height=36,
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack()

        form_frame.columnconfigure(1, weight=1)

    def _build_table(self):
        """Tabla de items con scroll."""
        table_container = ctk.CTkFrame(self, corner_radius=12)
        table_container.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(
            table_container,
            text="Items en base de datos",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(padx=15, pady=(15, 5), anchor="w")

        # Scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(
            table_container, corner_radius=8
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        # Header
        header_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#2c3e50", corner_radius=6)
        header_frame.pack(fill="x", pady=(0, 5))

        headers = [("ID", 60), ("Nombre", 200), ("Descripción", 320), ("Fecha", 160), ("", 80)]
        for text, width in headers:
            ctk.CTkLabel(
                header_frame,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=width,
                anchor="w",
            ).pack(side="left", padx=5, pady=8)

        # Container para las filas de datos
        self.rows_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.rows_frame.pack(fill="both", expand=True)

    def _build_status_bar(self):
        """Barra de estado inferior."""
        self.status_bar = ctk.CTkLabel(
            self,
            text="Listo",
            font=ctk.CTkFont(size=11),
            text_color="#95a5a6",
            anchor="w",
        )
        self.status_bar.pack(fill="x", padx=20, pady=(0, 10))

    # =========================================
    # Lógica
    # =========================================

    def refresh_items(self):
        """Recargar lista de items desde la BD."""
        # Limpiar filas existentes
        for widget in self.rows_frame.winfo_children():
            widget.destroy()

        if not self.db_connected:
            ctk.CTkLabel(
                self.rows_frame,
                text="⚠ No hay conexión a la base de datos",
                text_color="#e74c3c",
                font=ctk.CTkFont(size=14),
            ).pack(pady=30)
            self.status_bar.configure(text="Error: sin conexión a MySQL")
            return

        items = self.db.get_items()

        if not items:
            ctk.CTkLabel(
                self.rows_frame,
                text="No hay items registrados",
                text_color="#7f8c8d",
                font=ctk.CTkFont(size=13),
            ).pack(pady=30)
            self.status_bar.configure(text="0 items")
            return

        for i, item in enumerate(items):
            bg = "#34495e" if i % 2 == 0 else "#2c3e50"
            row = ctk.CTkFrame(self.rows_frame, fg_color=bg, corner_radius=4)
            row.pack(fill="x", pady=1)

            fecha_str = item["created_at"].strftime("%Y-%m-%d %H:%M") if item.get("created_at") else ""

            values = [
                (str(item["id"]), 60),
                (item["nombre"], 200),
                (item.get("descripcion", "") or "", 320),
                (fecha_str, 160),
            ]
            for text, width in values:
                ctk.CTkLabel(
                    row, text=text, width=width, anchor="w", font=ctk.CTkFont(size=12)
                ).pack(side="left", padx=5, pady=6)

            ctk.CTkButton(
                row,
                text="🗑",
                width=50,
                height=28,
                fg_color="#e74c3c",
                hover_color="#c0392b",
                font=ctk.CTkFont(size=13),
                command=lambda id_=item["id"]: self._delete_item(id_),
            ).pack(side="left", padx=5, pady=4)

        self.status_bar.configure(text=f"{len(items)} item(s) cargados")

    def _add_item(self):
        """Añadir nuevo item validando entrada."""
        nombre = self.entry_nombre.get().strip()
        descripcion = self.entry_desc.get().strip()

        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return

        if len(nombre) > 100:
            messagebox.showwarning("Validación", "El nombre no puede superar 100 caracteres.")
            return

        if self.db.add_item(nombre, descripcion):
            self.entry_nombre.delete(0, "end")
            self.entry_desc.delete(0, "end")
            self.refresh_items()
            self.status_bar.configure(text=f"Item '{nombre}' añadido correctamente")
        else:
            messagebox.showerror("Error", "No se pudo añadir el item.")

    def _delete_item(self, item_id: int):
        """Eliminar item previa confirmación."""
        if messagebox.askyesno("Confirmar", f"¿Eliminar item #{item_id}?"):
            if self.db.delete_item(item_id):
                self.refresh_items()
                self.status_bar.configure(text=f"Item #{item_id} eliminado")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el item.")

    def _on_close(self):
        """Cerrar la aplicación limpiamente."""
        self.db.close()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
