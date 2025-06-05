"""Simple Tkinter UI skeleton for ticket management."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
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

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("number", "status", "urgency"), show="headings")
        self.tree.heading("number", text="Ticket")
        self.tree.heading("status", text="Estado")
        self.tree.heading("urgency", text="Urgencia")
        self.tree.pack(fill=tk.BOTH, expand=True)

        refresh_btn = ttk.Button(self, text="Refrescar", command=self.refresh)
        refresh_btn.pack(side=tk.BOTTOM, pady=10)

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        tickets = self.session.query(models.Ticket).all()
        for t in tickets:
            self.tree.insert("", tk.END, values=(t.number, t.status, t.urgency))


def main():
    app = TicketApp()
    app.mainloop()


if __name__ == "__main__":
    main()
