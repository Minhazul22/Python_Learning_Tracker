import tkinter as tk
from tkinter import ttk
import json
import os

# ── Data ──────────────────────────────────────────────────────────────────────

PHASES = [
    {
        "title": "Phase 1 — Python Basics",
        "week":  "Week 1-2",
        "topics": [
            "Variables & Data Types",
            "Input & Output",
            "Strings & f-strings",
            "Conditionals (if/elif/else)",
            "Loops (for/while)",
            "Lists & Dictionaries",
            "Functions",
        ],
    },
    {
        "title": "Phase 2 — OOP",
        "week":  "Week 3-4",
        "topics": [
            "Class & Constructor",
            "Methods & self",
            "Encapsulation",
            "Inheritance & super()",
            "Polymorphism",
            "Special methods (__str__, __len__)",
        ],
    },
    {
        "title": "Phase 3 — Power Features",
        "week":  "Week 5-6",
        "topics": [
            "List Comprehensions",
            "Lambda Functions",
            "Map, Filter, Reduce",
            "Exception Handling (try/except)",
            "File I/O (read/write files)",
            "Modules & Imports",
            "Virtual Environments & pip",
        ],
    },
    {
        "title": "Phase 4 — CyberSecurity Track",
        "week":  "Week 7+",
        "topics": [
            "Network scanning with socket",
            "Hashing with hashlib",
            "Packet analysis with scapy",
            "Web requests with requests",
            "Port scanner project",
            "Password strength checker project",
        ],
    },
    {
        "title": "Phase 4 — IT & Automation Track",
        "week":  "Week 7+",
        "topics": [
            "OS automation with os & shutil",
            "Shell commands with subprocess",
            "SSH automation with paramiko",
            "Task scheduling with schedule",
            "Log file analyser project",
            "File organiser project",
        ],
    },
    {
        "title": "Phase 4 — Data Track",
        "week":  "Week 7+",
        "topics": [
            "numpy - arrays & math",
            "pandas - DataFrames",
            "matplotlib - charts & graphs",
            "scikit-learn - basic ML",
            "CSV analyser project",
            "Data visualisation project",
        ],
    },
]

SAVE_FILE = "tracker_progress.json"

# ── Theme ─────────────────────────────────────────────────────────────────────

C = {
    "bg":        "#12121e",
    "surface":   "#1c1c2e",
    "accent":    "#7c6af7",
    "text":      "#e8e8ff",
    "muted":     "#7070a0",
    "subtext":   "#a0a0c8",
    "bar_track": "#2a2a40",
    "bar_todo":  "#44446a",
    "bar_prog":  "#f0a832",
    "bar_done":  "#3dd68c",
}

PHASE_COLORS = [
    {"card": "#1a2840", "border": "#2a4270", "title": "#6aaaff"},
    {"card": "#1a3424", "border": "#2a5c3a", "title": "#3dd68c"},
    {"card": "#28183e", "border": "#462a70", "title": "#c08aff"},
    {"card": "#381818", "border": "#6a2828", "title": "#ff7070"},
    {"card": "#183434", "border": "#285858", "title": "#3dd6d6"},
    {"card": "#342e14", "border": "#5a4e20", "title": "#f0d050"},
]

STATES = ["todo", "progress", "done"]

STATE_CONFIG = {
    "todo":     {"label": "  o  To Do      ", "bg": "#2a2a40", "fg": "#9090b8"},
    "progress": {"label": "  ~  In Progress", "bg": "#3a2e10", "fg": "#f0a832"},
    "done":     {"label": "  v  Done       ", "bg": "#0e2e22", "fg": "#3dd68c"},
}

CHECKBOX_CHAR = {
    "todo":     ("[ ]", "#7070a0"),
    "progress": ("[~]", "#f0a832"),
    "done":     ("[v]", "#3dd68c"),
}

FONT = "Helvetica"   # matches the chat font

# ── App ───────────────────────────────────────────────────────────────────────

class TrackerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Python Learning Tracker")
        self.root.geometry("900x880")
        self.root.configure(bg=C["bg"])
        self.root.resizable(True, True)

        self.state_vars   = {}
        self.btn_widgets  = {}
        self.check_labels = {}
        self.phase_meta   = []

        self.load_progress()
        self.build_ui()

    # ── Persistence ───────────────────────────────────────────────────────────

    def load_progress(self):
        self.saved = {}
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    raw = json.load(f)
                for k, v in raw.items():
                    if isinstance(v, bool):
                        self.saved[k] = "done" if v else "todo"
                    elif v in STATES:
                        self.saved[k] = v
                    else:
                        self.saved[k] = "todo"
            except Exception:
                self.saved = {}

    def save_progress(self):
        with open(SAVE_FILE, "w") as f:
            json.dump(self.state_vars, f, indent=2)

    # ── UI ────────────────────────────────────────────────────────────────────

    def build_ui(self):

        # Header
        header = tk.Frame(self.root, bg=C["bg"])
        header.pack(fill="x", padx=32, pady=(22, 4))

        tk.Label(
            header,
            text="Python Learning Tracker",
            font=(FONT, 22, "bold"),
            bg=C["bg"], fg=C["accent"],
        ).pack(side="left")

        tk.Button(
            header,
            text="Reset All",
            command=self.reset_all,
            bg=C["surface"], fg=C["muted"],
            relief="flat", font=(FONT, 11),
            cursor="hand2", padx=12, pady=5,
        ).pack(side="right")

        # Overall progress label
        self.overall_label = tk.Label(
            self.root, text="",
            font=(FONT, 12),
            bg=C["bg"], fg=C["subtext"],
        )
        self.overall_label.pack(anchor="center", pady=(10, 2))

        # Overall progress bar — 70% width, centered
        bar_outer = tk.Frame(self.root, bg=C["bg"])
        bar_outer.pack(fill="x", pady=(0, 4))

        bar_wrap = tk.Frame(bar_outer, bg=C["bar_track"], height=12)
        bar_wrap.pack(anchor="center", pady=0, ipadx=0)
        bar_wrap.pack_propagate(False)

        self.overall_fill = tk.Frame(bar_wrap, bg=C["accent"], height=12)
        self.overall_fill.place(x=0, y=0, relheight=1, width=0)

        # Store bar_wrap reference to measure width later
        self._overall_bar_wrap = bar_wrap

        # Legend
        legend = tk.Frame(self.root, bg=C["bg"])
        legend.pack(anchor="center", pady=(6, 14))

        tk.Label(
            legend, text="Click to cycle:  ",
            font=(FONT, 11), bg=C["bg"], fg=C["muted"],
        ).pack(side="left")

        for state, cfg in STATE_CONFIG.items():
            tk.Label(
                legend,
                text=cfg["label"],
                font=(FONT, 11, "bold"),
                bg=cfg["bg"], fg=cfg["fg"],
                padx=6, pady=3, relief="flat",
            ).pack(side="left", padx=3)

        # Scrollable area
        outer = tk.Frame(self.root, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=0, pady=(0, 8))

        self.canvas = tk.Canvas(outer, bg=C["bg"], highlightthickness=0)
        sb = ttk.Scrollbar(outer, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=C["bg"])

        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.win_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=sb.set)

        # Make inner frame fill canvas width
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.win_id, width=e.width)
        )

        self.canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.root.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(-1 * (e.delta // 120), "units")
        )

        # Phase cards
        for i, phase in enumerate(PHASES):
            self.build_phase_card(i, phase)

        # Update overall bar after layout settles
        self.root.after(100, self.update_overall)

    def build_phase_card(self, phase_idx, phase):
        pc = PHASE_COLORS[phase_idx % len(PHASE_COLORS)]

        # Outer centering frame — fills canvas width
        centering = tk.Frame(self.inner, bg=C["bg"])
        centering.pack(fill="x", pady=6)

        # Card is 70% of window width, centered using padx
        # We use a fixed padx trick: pack with expand but controlled padding
        card = tk.Frame(
            centering,
            bg=pc["card"],
            highlightbackground=pc["border"],
            highlightthickness=1,
            padx=16, pady=14,
        )
        # anchor center + fill="none" + relwidth via place won't work in pack,
        # so we bind centering frame width to set padx dynamically
        card.pack(anchor="center", fill="none", expand=False)

        # Dynamically resize card to 70% of centering frame width
        def resize_card(event, c=card, cf=centering):
            new_w = int(cf.winfo_width() * 0.70)
            c.config(width=new_w)
        centering.bind("<Configure>", resize_card)

        # Title row
        top = tk.Frame(card, bg=pc["card"])
        top.pack(fill="x")

        tk.Label(
            top,
            text=phase["title"],
            font=(FONT, 15, "bold"),
            bg=pc["card"], fg=pc["title"],
        ).pack(side="left")

        tk.Label(
            top,
            text=phase["week"],
            font=(FONT, 11),
            bg=pc["card"], fg=C["muted"],
        ).pack(side="right")

        # Phase progress label
        pct_label = tk.Label(
            card, text="",
            font=(FONT, 11),
            bg=pc["card"], fg=C["subtext"],
        )
        pct_label.pack(anchor="w", pady=(4, 2))

        # Phase progress bar
        bw = tk.Frame(card, bg=C["bar_track"], height=7)
        bw.pack(fill="x", pady=(0, 10))
        bw.pack_propagate(False)
        bar_fill = tk.Frame(bw, bg=C["bar_todo"], height=7)
        bar_fill.place(x=0, y=0, relheight=1, width=0)

        # Divider
        tk.Frame(card, bg=pc["border"], height=1).pack(fill="x", pady=(0, 8))

        # Topic rows
        topic_keys = []
        for topic in phase["topics"]:
            key = f"p{phase_idx}_{topic}"
            topic_keys.append(key)

            saved_val = self.saved.get(key, "todo")
            self.state_vars[key] = saved_val if saved_val in STATES else "todo"

            row = tk.Frame(card, bg=pc["card"], pady=3)
            row.pack(fill="x")

            # Checkbox
            cb_char, cb_fg = CHECKBOX_CHAR[self.state_vars[key]]
            cb_lbl = tk.Label(
                row,
                text=cb_char,
                font=(FONT, 12, "bold"),
                bg=pc["card"], fg=cb_fg,
                width=4, anchor="center",
            )
            cb_lbl.pack(side="left", padx=(0, 6))
            self.check_labels[key] = cb_lbl

            # Topic name
            tk.Label(
                row,
                text=topic,
                font=(FONT, 12),
                bg=pc["card"], fg=C["text"],
                anchor="w",
            ).pack(side="left", fill="x", expand=True)

            # Status button
            state = self.state_vars[key]
            scfg  = STATE_CONFIG[state]
            btn = tk.Button(
                row,
                text=scfg["label"],
                font=(FONT, 10, "bold"),
                bg=scfg["bg"], fg=scfg["fg"],
                activebackground=scfg["bg"],
                activeforeground=scfg["fg"],
                relief="flat", cursor="hand2",
                padx=8, pady=3, bd=0,
                command=lambda k=key, tk_=topic_keys,
                               pl=pct_label, bf=bar_fill:
                    self.cycle_state(k, tk_, pl, bf),
            )
            btn.pack(side="right", padx=(8, 0))
            self.btn_widgets[key] = btn

        self.phase_meta.append((topic_keys, pct_label, bar_fill))
        self.root.after(150, lambda tk_=topic_keys, pl=pct_label, bf=bar_fill:
                        self.update_phase_bar(tk_, pl, bf))

    # ── Logic ─────────────────────────────────────────────────────────────────

    def refresh_btn(self, key):
        state = self.state_vars[key]
        scfg  = STATE_CONFIG[state]
        self.btn_widgets[key].config(
            text=scfg["label"],
            bg=scfg["bg"], fg=scfg["fg"],
            activebackground=scfg["bg"],
            activeforeground=scfg["fg"],
        )
        cb_char, cb_fg = CHECKBOX_CHAR[state]
        self.check_labels[key].config(text=cb_char, fg=cb_fg)

    def cycle_state(self, key, topic_keys, pct_label, bar_fill):
        cur = self.state_vars[key]
        self.state_vars[key] = STATES[(STATES.index(cur) + 1) % len(STATES)]
        self.refresh_btn(key)
        self.update_phase_bar(topic_keys, pct_label, bar_fill)
        self.update_overall()
        self.save_progress()

    def update_phase_bar(self, topic_keys, pct_label, bar_fill):
        total = len(topic_keys)
        done  = sum(1 for k in topic_keys if self.state_vars[k] == "done")
        prog  = sum(1 for k in topic_keys if self.state_vars[k] == "progress")
        pct   = int((done / total) * 100) if total else 0

        extra = f"  |  {prog} in progress" if prog else ""
        pct_label.config(text=f"{done}/{total} done{extra}  |  {pct}%")

        bar_fill.update_idletasks()
        pw = bar_fill.master.winfo_width()
        bar_fill.place(x=0, y=0, relheight=1, width=max(1, int(pw * pct / 100)))
        color = C["bar_done"] if pct == 100 else C["bar_prog"] if (done or prog) else C["bar_todo"]
        bar_fill.config(bg=color)

    def update_overall(self):
        total = len(self.state_vars)
        done  = sum(1 for s in self.state_vars.values() if s == "done")
        prog  = sum(1 for s in self.state_vars.values() if s == "progress")
        pct   = int((done / total) * 100) if total else 0

        extra = f"  |  {prog} in progress" if prog else ""
        self.overall_label.config(
            text=f"Overall  |  {done}/{total} done{extra}  |  {pct}%"
        )

        # Set overall bar to 70% of window width
        self._overall_bar_wrap.update_idletasks()
        win_w  = self.root.winfo_width()
        bar_w  = int(win_w * 0.70)
        fill_w = int(bar_w * pct / 100)
        self._overall_bar_wrap.config(width=bar_w)
        self.overall_fill.place(x=0, y=0, relheight=1, width=max(1, fill_w))

    def reset_all(self):
        for key in self.state_vars:
            self.state_vars[key] = "todo"
            self.refresh_btn(key)
        for topic_keys, pct_label, bar_fill in self.phase_meta:
            self.update_phase_bar(topic_keys, pct_label, bar_fill)
        self.update_overall()
        self.save_progress()

# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app  = TrackerApp(root)
    root.mainloop()