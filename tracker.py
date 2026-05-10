import tkinter as tk
from tkinter import ttk
import json
import os

# ── Data ──────────────────────────────────────────────────────────────────────

PHASES = [
    {
        "title": "Phase 1 — Python Basics",
        "week": "Week 1–2",
        "emoji": "🐍",
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
        "week": "Week 3–4",
        "emoji": "📦",
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
        "week": "Week 5–6",
        "emoji": "⚡",
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
        "week": "Week 7+",
        "emoji": "🔐",
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
        "week": "Week 7+",
        "emoji": "💻",
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
        "week": "Week 7+",
        "emoji": "📊",
        "topics": [
            "numpy — arrays & math",
            "pandas — DataFrames",
            "matplotlib — charts & graphs",
            "scikit-learn — basic ML",
            "CSV analyser project",
            "Data visualisation project",
        ],
    },
]

SAVE_FILE = "tracker_progress.json"

# ── Theme ─────────────────────────────────────────────────────────────────────

C = {
    "bg":          "#12121e",
    "surface":     "#1c1c2e",
    "card":        "#22223a",
    "card_border": "#35355a",
    "accent":      "#7c6af7",
    "text":        "#e8e8ff",
    "muted":       "#7070a0",
    "subtext":     "#a0a0c8",

    "todo_bg":     "#2a2a40",
    "todo_fg":     "#8888b0",
    "prog_bg":     "#2e2410",
    "prog_fg":     "#f0a832",
    "done_bg":     "#0e2e22",
    "done_fg":     "#3dd68c",

    "bar_track":   "#2a2a40",
    "bar_todo":    "#44446a",
    "bar_prog":    "#f0a832",
    "bar_done":    "#3dd68c",
}

STATES      = ["todo", "progress", "done"]
STATE_LABEL = {
    "todo":     "  ○  To Do  ",
    "progress": "  ◑  In Progress  ",
    "done":     "  ●  Done  ",
}

# ── App ───────────────────────────────────────────────────────────────────────

class TrackerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Python Learning Tracker")
        self.root.geometry("860x920")
        self.root.configure(bg=C["bg"])
        self.root.resizable(True, True)

        self.state_vars  = {}
        self.btn_widgets = {}
        self.phase_meta  = []

        self.load_progress()
        self.build_ui()

    # ── Persistence ───────────────────────────────────────────────────────────

    def load_progress(self):
        self.saved = {}
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                self.saved = json.load(f)

    def save_progress(self):
        with open(SAVE_FILE, "w") as f:
            json.dump(self.state_vars, f, indent=2)

    # ── UI ────────────────────────────────────────────────────────────────────

    def build_ui(self):

        # ── Header
        header = tk.Frame(self.root, bg=C["bg"])
        header.pack(fill="x", padx=28, pady=(22, 4))

        tk.Label(
            header,
            text="🐍  Python Learning Tracker",
            font=("Helvetica", 28, "bold"),
            bg=C["bg"], fg=C["text"],
        ).pack(side="left")

        tk.Button(
            header,
            text="↺  Reset all",
            command=self.reset_all,
            bg=C["surface"], fg=C["muted"],
            relief="flat", font=("Helvetica", 14),
            cursor="hand2", padx=14, pady=6,
        ).pack(side="right")

        # ── Overall progress
        self.overall_label = tk.Label(
            self.root, text="",
            font=("Helvetica", 15),
            bg=C["bg"], fg=C["subtext"],
        )
        self.overall_label.pack(anchor="w", padx=28, pady=(10, 3))

        bar_wrap = tk.Frame(self.root, bg=C["bar_track"], height=14)
        bar_wrap.pack(fill="x", padx=28, pady=(0, 6))
        bar_wrap.pack_propagate(False)

        self.overall_fill = tk.Frame(bar_wrap, bg=C["accent"], height=14)
        self.overall_fill.place(x=0, y=0, relheight=1, width=0)

        # ── Legend
        legend = tk.Frame(self.root, bg=C["bg"])
        legend.pack(anchor="w", padx=28, pady=(4, 16))

        tk.Label(legend, text="Click any button to cycle:",
                 font=("Helvetica", 13), bg=C["bg"], fg=C["muted"]).pack(side="left", padx=(0, 10))

        for state in STATES:
            cfg = self.btn_colors(state)
            tk.Label(
                legend,
                text=STATE_LABEL[state],
                font=("Helvetica", 13, "bold"),
                bg=cfg["bg"], fg=cfg["fg"],
                padx=6, pady=4,
                relief="flat",
            ).pack(side="left", padx=4)

        # ── Scrollable area
        wrap = tk.Frame(self.root, bg=C["bg"])
        wrap.pack(fill="both", expand=True, padx=28, pady=(0, 10))

        canvas = tk.Canvas(wrap, bg=C["bg"], highlightthickness=0)
        sb = ttk.Scrollbar(wrap, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg=C["bg"])

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        frame_id = canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)

        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(frame_id, width=e.width)
        )

        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units")
        )

        # ── Build each phase card, stacked and centred
        for i, phase in enumerate(PHASES):
            self.build_phase_card(i, phase)

        self.update_overall()

    def build_phase_card(self, phase_idx, phase):

        card = tk.Frame(
            self.scroll_frame, bg=C["card"],
            highlightbackground=C["card_border"],
            highlightthickness=1,
            padx=18, pady=16,
        )
        card.pack(fill="x", pady=8)

        # Phase title row
        top = tk.Frame(card, bg=C["card"])
        top.pack(fill="x")

        tk.Label(
            top,
            text=f"{phase['emoji']}  {phase['title']}",
            font=("Helvetica", 18, "bold"),
            bg=C["card"], fg=C["text"],
        ).pack(side="left")

        tk.Label(
            top,
            text=phase["week"],
            font=("Helvetica", 14),
            bg=C["card"], fg=C["muted"],
        ).pack(side="right")

        # Phase progress label
        pct_label = tk.Label(
            card, text="",
            font=("Helvetica", 14),
            bg=C["card"], fg=C["subtext"],
        )
        pct_label.pack(anchor="w", pady=(5, 3))

        # Phase progress bar
        bar_wrap = tk.Frame(card, bg=C["bar_track"], height=8)
        bar_wrap.pack(fill="x", pady=(0, 14))
        bar_wrap.pack_propagate(False)

        bar_fill = tk.Frame(bar_wrap, bg=C["bar_todo"], height=8)
        bar_fill.place(x=0, y=0, relheight=1, width=0)

        # Divider
        tk.Frame(card, bg=C["card_border"], height=1).pack(fill="x", pady=(0, 10))

        # Topic rows — button on the RIGHT
        topic_keys = []
        for topic in phase["topics"]:
            key = f"p{phase_idx}_{topic}"
            topic_keys.append(key)
            self.state_vars[key] = self.saved.get(key, "todo")

            row = tk.Frame(card, bg=C["card"], pady=4)
            row.pack(fill="x")

            # Topic label (left, expands)
            tk.Label(
                row,
                text=topic,
                font=("Helvetica", 15),
                bg=C["card"], fg=C["text"],
                anchor="w",
            ).pack(side="left", fill="x", expand=True)

            # Cycle button (right)
            btn = tk.Button(
                row,
                text="",
                font=("Helvetica", 13, "bold"),
                relief="flat", cursor="hand2",
                padx=12, pady=5, bd=0,
                command=lambda k=key, tk_keys=topic_keys,
                               pl=pct_label, bf=bar_fill:
                    self.cycle_state(k, tk_keys, pl, bf),
            )
            btn.pack(side="right", padx=(14, 0))
            self.btn_widgets[key] = btn
            self.refresh_btn(key)

        self.phase_meta.append((topic_keys, pct_label, bar_fill))
        self.update_phase_bar(topic_keys, pct_label, bar_fill)

    # ── State logic ───────────────────────────────────────────────────────────

    def btn_colors(self, state):
        return {
            "todo":     {"bg": C["todo_bg"], "fg": C["todo_fg"]},
            "progress": {"bg": C["prog_bg"], "fg": C["prog_fg"]},
            "done":     {"bg": C["done_bg"], "fg": C["done_fg"]},
        }[state]

    def refresh_btn(self, key):
        state = self.state_vars[key]
        cfg   = self.btn_colors(state)
        self.btn_widgets[key].config(
            text=STATE_LABEL[state],
            bg=cfg["bg"], fg=cfg["fg"],
            activebackground=cfg["bg"],
            activeforeground=cfg["fg"],
        )

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

        extra = f"  ·  {prog} in progress" if prog else ""
        pct_label.config(text=f"{done}/{total} topics done{extra}  ·  {pct}%")

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

        extra = f"  ·  {prog} in progress" if prog else ""
        self.overall_label.config(
            text=f"Overall  ·  {done}/{total} topics done{extra}  ·  {pct}%"
        )
        self.overall_fill.update_idletasks()
        pw = self.overall_fill.master.winfo_width()
        self.overall_fill.place(x=0, y=0, relheight=1, width=max(1, int(pw * pct / 100)))

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
