"""Simple Tkinter UI skeleton for ticket management."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .. import config
from ..db import models

engine = create_engine(config.DB_URL)
models.Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class TicketApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tickets HelpDesk")
        self.geometry("800x600")
        self.session = Session()
        self.create_widgets()
        self.refresh_tree()

    def create_widgets(self):
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, pady=5)
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(search_frame, text="Aplicar", command=self.refresh_tree).pack(
            side=tk.LEFT, padx=5
        )

        self.tree = ttk.Treeview(
            self,
            columns=("number", "status", "urgency"),
            show="headings",
        )
        self.tree.heading("number", text="Ticket")
        self.tree.heading("status", text="Estado")
        self.tree.heading("urgency", text="Urgencia")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.open_details)

        self.tree.tag_configure("cerrado", background="#d0ffd0")
        self.tree.tag_configure("abierto", background="#ffd0d0")

        refresh_btn = ttk.Button(self, text="Refrescar", command=self.refresh)
        refresh_btn.pack(side=tk.BOTTOM, pady=10)

    def refresh_tree(self):
        query = self.session.query(models.Ticket)
        term = self.search_var.get().strip()
        if term:
            query = query.filter(models.Ticket.number.contains(term))

        self.tree.delete(*self.tree.get_children())
        for t in query.all():
            tag = t.status or "abierto"
            self.tree.insert("", tk.END, values=(t.number, t.status, t.urgency), tags=(tag,))

    def open_details(self, event):
        item = self.tree.focus()
        if not item:
            return
        ticket_number = self.tree.item(item, "values")[0]
        ticket = (
            self.session.query(models.Ticket).filter_by(number=ticket_number).first()
        )
        if not ticket:
            return

        win = tk.Toplevel(self)
        win.title(f"Ticket {ticket.number}")
        win.geometry("600x400")

        notes_label = ttk.Label(win, text="Observaciones Personales:")
        notes_label.pack(anchor=tk.W, padx=10, pady=(10, 0))
        notes = tk.Text(win, height=4)
        notes.pack(fill=tk.X, padx=10)
        if ticket.personal_notes:
            notes.insert(tk.END, ticket.personal_notes)

        attach_frame = ttk.Frame(win)
        attach_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        attach_list = tk.Listbox(attach_frame)
        attach_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        def open_file(event):
            idx = attach_list.curselection()
            if not idx:
                return
            path = attach_list.get(idx[0])
            webbrowser.open(Path(path).absolute().as_uri())

        attach_list.bind("<Double-1>", open_file)

        for att in ticket.attachments:
            attach_list.insert(tk.END, att.path)

        def add_file():
            path = filedialog.askopenfilename()
            if not path:
                return
            dest_dir = config.ATTACHMENTS_DIR / ticket.number
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / Path(path).name
            try:
                dest.write_bytes(Path(path).read_bytes())
            except Exception as exc:
                messagebox.showerror("Error", str(exc))
                return
            att = models.Attachment(ticket_id=ticket.id, path=str(dest), from_email=False)
            self.session.add(att)
            self.session.commit()
            attach_list.insert(tk.END, str(dest))

        add_btn = ttk.Button(attach_frame, text="Agregar adjunto", command=add_file)
        add_btn.pack(side=tk.RIGHT, padx=5)

        obs_frame = ttk.Frame(win)
        obs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        ttk.Label(obs_frame, text="Observaciones IA recientes:").pack(anchor=tk.W)
        obs_list = tk.Listbox(obs_frame, height=5)
        obs_list.pack(fill=tk.BOTH, expand=True)
        observations = (
            self.session.query(models.Observation)
            .filter_by(ticket_id=ticket.id)
            .order_by(models.Observation.date.desc())
            .limit(5)
            .all()
        )
        for o in observations:
            obs_list.insert(tk.END, f"{o.date:%Y-%m-%d}: {o.summary}")

        def save_and_close():
            ticket.personal_notes = notes.get("1.0", tk.END).strip()
            self.session.commit()
            win.destroy()

        save_btn = ttk.Button(win, text="Guardar", command=save_and_close)
        save_btn.pack(pady=5)

    def refresh(self):
        from ..processor import process_new_emails

        try:
            process_new_emails()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

        self.refresh_tree()


def main():
    app = TicketApp()
    app.mainloop()


if __name__ == "__main__":
    main()
