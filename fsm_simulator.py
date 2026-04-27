import tkinter as tk
from tkinter import ttk, messagebox
import math

# ──────────────────────────────────────────────
# FSM Logic
# ──────────────────────────────────────────────

TRANSITIONS = {
    'S': {'0': 'A', '1': 'B'},
    'A': {'0': 'C', '1': 'B'},
    'B': {'0': 'A', '1': 'B'},
    'C': {'0': 'C', '1': 'C'},
}
START_STATE  = 'S'
ACCEPT_STATE = 'B'
TRAP_STATE   = 'C'


def run_fsm(string: str):
    """
    Jalankan FSM pada string input.
    Kembalikan (accepted: bool, trace: list[dict])
    trace: [{'state': str, 'char': str|None}, ...]
    """
    state = START_STATE
    trace = [{'state': state, 'char': None}]

    for ch in string:
        state = TRANSITIONS[state][ch]
        trace.append({'state': state, 'char': ch})

    accepted = (state == ACCEPT_STATE)
    return accepted, trace


def validate_input(s: str):
    """Kembalikan pesan error atau None jika valid."""
    for ch in s:
        if ch not in ('0', '1'):
            return f"Karakter '{ch}' tidak valid. Hanya '0' dan '1' yang diperbolehkan."
    return None


# ──────────────────────────────────────────────
# Color / Style Constants
# ──────────────────────────────────────────────

BG        = "#F8F7F4"
BG2       = "#EEECEA"
FG        = "#1C1C1A"
FG2       = "#5F5E5A"
BORDER    = "#CCCBC4"

C_BLUE    = "#185FA5"
C_BLUE_LT = "#E6F1FB"
C_PURP    = "#534AB7"
C_PURP_LT = "#EEEDFE"
C_GRAY    = "#888780"
C_GRAY_LT = "#F1EFE8"
C_CORAL   = "#993C1D"
C_CORAL_LT= "#FAECE7"
C_GREEN   = "#27500A"
C_GREEN_LT= "#EAF3DE"
C_RED     = "#A32D2D"
C_RED_LT  = "#FCEBEB"

NODE_STYLES = {
    'S': {'fill': C_GRAY_LT,  'outline': C_GRAY,  'text': C_GRAY},
    'A': {'fill': C_BLUE_LT,  'outline': C_BLUE,  'text': C_BLUE},
    'B': {'fill': C_PURP_LT,  'outline': C_PURP,  'text': C_PURP},
    'C': {'fill': C_CORAL_LT, 'outline': C_CORAL, 'text': C_CORAL},
}
NODE_ACTIVE  = {'fill': C_BLUE,    'outline': '#0C447C', 'text': '#E6F1FB'}
NODE_ACCEPT  = {'fill': C_GREEN,   'outline': '#173404', 'text': '#EAF3DE'}
NODE_REJECT  = {'fill': C_RED,     'outline': '#501313', 'text': '#FCEBEB'}

FONT_NORMAL  = ("Segoe UI", 10)
FONT_BOLD    = ("Segoe UI", 10, "bold")
FONT_MONO    = ("Courier New", 11)
FONT_TITLE   = ("Segoe UI", 14, "bold")
FONT_SUB     = ("Segoe UI", 9)
FONT_NODE    = ("Segoe UI", 13, "bold")


# ──────────────────────────────────────────────
# Main Application
# ──────────────────────────────────────────────

class FSMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FSM Simulator — Bahasa L")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(900, 640)

        self._build_ui()
        self._draw_fsm()
        self.after(50, lambda: self.geometry("1020x700"))

    # ── UI Layout ─────────────────────────────

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=BG, pady=14, padx=20)
        hdr.pack(fill=tk.X)

        tk.Label(hdr, text="FSM Simulator", font=FONT_TITLE, bg=BG, fg=FG).pack(anchor="w")
        tk.Label(hdr,
            text="L = { x ∈ (0+1)* | karakter terakhir x adalah 1 dan x tidak memiliki substring 00 }",
            font=FONT_SUB, bg=BG, fg=FG2).pack(anchor="w", pady=(2, 0))

        sep = tk.Frame(self, bg=BORDER, height=1)
        sep.pack(fill=tk.X, padx=20)

        # Body
        body = tk.Frame(self, bg=BG, padx=20, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # Left column
        left = tk.Frame(body, bg=BG)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._build_input_area(left)
        self._build_result_area(left)
        self._build_trace_area(left)
        self._build_history_area(left)

        # Right column — FSM diagram
        right = tk.Frame(body, bg=BG, width=380)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        right.pack_propagate(False)

        self._build_diagram(right)

    def _build_input_area(self, parent):
        frm = tk.Frame(parent, bg=BG)
        frm.pack(fill=tk.X, pady=(0, 10))

        tk.Label(frm, text="Input String Biner", font=FONT_BOLD, bg=BG, fg=FG).pack(anchor="w")
        tk.Label(frm, text="Masukkan string yang terdiri dari 0 dan 1 (kosong = ε)",
                 font=FONT_SUB, bg=BG, fg=FG2).pack(anchor="w", pady=(1, 6))

        row = tk.Frame(frm, bg=BG)
        row.pack(fill=tk.X)

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(row, textvariable=self.entry_var, font=FONT_MONO,
                              bg="white", fg=FG, insertbackground=FG,
                              relief="flat", bd=1, highlightthickness=1,
                              highlightbackground=BORDER, highlightcolor=C_BLUE)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 8))
        self.entry.bind("<Return>", lambda e: self._on_run())
        self.entry.bind("<KeyRelease>", self._on_key)
        self.entry.focus()

        self.btn_run = tk.Button(row, text="▶  Jalankan", font=FONT_BOLD,
                                 bg=C_BLUE, fg="white", activebackground="#0C447C",
                                 activeforeground="white", relief="flat",
                                 padx=12, pady=6, cursor="hand2",
                                 command=self._on_run)
        self.btn_run.pack(side=tk.LEFT, padx=(0, 6))

        btn_clr = tk.Button(row, text="Reset", font=FONT_NORMAL,
                            bg=BG2, fg=FG, activebackground=BORDER,
                            relief="flat", padx=10, pady=6, cursor="hand2",
                            command=self._on_reset)
        btn_clr.pack(side=tk.LEFT)

        # Error label
        self.lbl_err = tk.Label(frm, text="", font=FONT_SUB, bg=BG, fg=C_RED)
        self.lbl_err.pack(anchor="w", pady=(2, 0))

        # Quick examples
        tk.Label(frm, text="Contoh test case:", font=FONT_SUB, bg=BG, fg=FG2).pack(anchor="w", pady=(8, 4))
        ex_row1 = tk.Frame(frm, bg=BG)
        ex_row1.pack(anchor="w")
        ex_row2 = tk.Frame(frm, bg=BG)
        ex_row2.pack(anchor="w", pady=(4, 0))

        examples_accept = [("1", True), ("01", True), ("101", True), ("1011", True), ("10101", True)]
        examples_reject = [("0", False), ("00", False), ("100", False), ("010", False), ("1001", False), ("ε", False)]

        tk.Label(ex_row1, text="✓ Diterima:", font=FONT_SUB, bg=BG, fg=C_GREEN).pack(side=tk.LEFT, padx=(0, 4))
        for val, _ in examples_accept:
            v = "" if val == "ε" else val
            btn = tk.Button(ex_row1, text=val, font=("Courier New", 9),
                            bg=C_GREEN_LT, fg=C_GREEN, relief="flat",
                            padx=6, pady=2, cursor="hand2",
                            command=lambda x=v: self._set_and_run(x))
            btn.pack(side=tk.LEFT, padx=2)

        tk.Label(ex_row2, text="✗ Ditolak:", font=FONT_SUB, bg=BG, fg=C_RED).pack(side=tk.LEFT, padx=(0, 4))
        for val, _ in examples_reject:
            v = "" if val == "ε" else val
            btn = tk.Button(ex_row2, text=val, font=("Courier New", 9),
                            bg=C_RED_LT, fg=C_RED, relief="flat",
                            padx=6, pady=2, cursor="hand2",
                            command=lambda x=v: self._set_and_run(x))
            btn.pack(side=tk.LEFT, padx=2)

    def _build_result_area(self, parent):
        self.result_frame = tk.Frame(parent, bg=BG)
        self.result_frame.pack(fill=tk.X, pady=(8, 0))

        self.result_label = tk.Label(self.result_frame, text="", font=FONT_BOLD,
                                     bg=BG2, fg=FG, anchor="w",
                                     padx=12, pady=10, relief="flat",
                                     wraplength=380, justify="left")
        self.result_label.pack(fill=tk.X)
        self.result_label.pack_forget()

    def _build_trace_area(self, parent):
        self.trace_outer = tk.Frame(parent, bg=BG)
        self.trace_outer.pack(fill=tk.X, pady=(10, 0))

        tk.Label(self.trace_outer, text="Jejak Transisi", font=FONT_BOLD,
                 bg=BG, fg=FG).pack(anchor="w")

        self.trace_canvas = tk.Canvas(self.trace_outer, bg=BG, height=36,
                                      highlightthickness=0)
        self.trace_canvas.pack(fill=tk.X, pady=(4, 0))
        self.trace_outer.pack_forget()

    def _build_history_area(self, parent):
        hist_frm = tk.Frame(parent, bg=BG)
        hist_frm.pack(fill=tk.BOTH, expand=True, pady=(14, 0))

        hdr_row = tk.Frame(hist_frm, bg=BG)
        hdr_row.pack(fill=tk.X)
        tk.Label(hdr_row, text="Riwayat", font=FONT_BOLD, bg=BG, fg=FG).pack(side=tk.LEFT)
        tk.Button(hdr_row, text="Hapus Riwayat", font=FONT_SUB,
                  bg=BG2, fg=FG2, relief="flat", padx=6, pady=1,
                  cursor="hand2", command=self._clear_history).pack(side=tk.RIGHT)

        cols = ("string", "hasil", "state_akhir")
        self.tree = ttk.Treeview(hist_frm, columns=cols, show="headings", height=6)
        self.tree.heading("string",     text="String")
        self.tree.heading("hasil",      text="Hasil")
        self.tree.heading("state_akhir",text="State Akhir")
        self.tree.column("string",      width=130, anchor="center")
        self.tree.column("hasil",       width=110, anchor="center")
        self.tree.column("state_akhir", width=90,  anchor="center")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", fieldbackground="white",
                        rowheight=24, font=FONT_MONO)
        style.configure("Treeview.Heading", font=FONT_BOLD,
                        background=BG2, foreground=FG, relief="flat")
        style.map("Treeview", background=[("selected", C_BLUE_LT)],
                  foreground=[("selected", C_BLUE)])
        self.tree.tag_configure("accept", foreground=C_GREEN)
        self.tree.tag_configure("reject", foreground=C_RED)

        sb = ttk.Scrollbar(hist_frm, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(6, 0))
        sb.pack(side=tk.RIGHT, fill=tk.Y, pady=(6, 0))
        self.tree.bind("<Double-1>", self._on_tree_select)

    def _build_diagram(self, parent):
        tk.Label(parent, text="Diagram FSM", font=FONT_BOLD,
                 bg=BG, fg=FG).pack(anchor="w", pady=(0, 6))

        self.canvas = tk.Canvas(parent, bg=BG, highlightthickness=0,
                                width=360, height=340)
        self.canvas.pack()

        # Legend
        leg = tk.Frame(parent, bg=BG)
        leg.pack(fill=tk.X, pady=(10, 0))
        tk.Label(leg, text="Keterangan:", font=FONT_SUB, bg=BG, fg=FG2).pack(anchor="w")

        items = [
            (C_GRAY_LT, C_GRAY, "S = State awal"),
            (C_BLUE_LT, C_BLUE, "A = Setelah baca 0"),
            (C_PURP_LT, C_PURP, "B = Accept state"),
            (C_CORAL_LT, C_CORAL, "C = Trap state"),
        ]
        for fill, fg, label in items:
            row = tk.Frame(leg, bg=BG)
            row.pack(anchor="w", pady=1)
            box = tk.Canvas(row, width=14, height=14, bg=BG, highlightthickness=0)
            box.pack(side=tk.LEFT, padx=(0, 5))
            box.create_oval(2, 2, 13, 13, fill=fill, outline=fg, width=1.5)
            tk.Label(row, text=label, font=FONT_SUB, bg=BG, fg=FG2).pack(side=tk.LEFT)

    # ── FSM Diagram Drawing ───────────────────

    NODE_POS = {
        'S': (60,  185),
        'A': (180, 105),
        'B': (180, 270),
        'C': (300, 105),
    }
    R = 26

    def _draw_fsm(self, highlight_state=None, mode='default'):
        c = self.canvas
        c.delete("all")
        R = self.R

        def arrow(x1, y1, x2, y2, label, color=C_GRAY, offset=(0,0), curve=0):
            if curve != 0:
                mx = (x1+x2)/2 + offset[0]
                my = (y1+y2)/2 + offset[1]
                c.create_line(x1, y1, mx, my, x2, y2, smooth=True,
                              arrow=tk.LAST, arrowshape=(8, 10, 4),
                              fill=color, width=1.5)
                c.create_text(mx + offset[0]*0.3, my + offset[1]*0.3,
                              text=label, font=FONT_SUB, fill=FG2)
            else:
                dx, dy = x2-x1, y2-y1
                length = math.hypot(dx, dy)
                if length == 0: return
                ux, uy = dx/length, dy/length
                sx, sy = x1 + ux*R, y1 + uy*R
                ex, ey = x2 - ux*(R+2), y2 - uy*(R+2)
                c.create_line(sx, sy, ex, ey, arrow=tk.LAST,
                              arrowshape=(8, 10, 4), fill=color, width=1.5)
                mx = (sx+ex)/2 + offset[0]
                my = (sy+ey)/2 + offset[1]
                c.create_text(mx, my, text=label, font=FONT_SUB, fill=FG2)

        def self_loop(cx, cy, label, dy=-40, color=C_GRAY):
            c.create_arc(cx-20, cy+dy, cx+20, cy+dy+40,
                         start=30, extent=300, style=tk.ARC,
                         outline=color, width=1.5)
            arr_x, arr_y = cx+18, cy+dy+28
            c.create_polygon(arr_x, arr_y, arr_x-6, arr_y-4, arr_x-4, arr_y+6,
                             fill=color, outline=color)
            c.create_text(cx + 32, cy+dy+18, text=label, font=FONT_SUB, fill=FG2)

        # ── Arrows ──
        S, A, B, CC = self.NODE_POS['S'], self.NODE_POS['A'], self.NODE_POS['B'], self.NODE_POS['C']

        # Start arrow
        c.create_line(S[0]-40, S[1], S[0]-R, S[1],
                      arrow=tk.LAST, arrowshape=(8, 10, 4), fill=C_GRAY, width=1.5)

        # S→A (0)
        arrow(S[0], S[1], A[0], A[1], "0", offset=(-12, -8))
        # S→B (1)
        arrow(S[0], S[1], B[0], B[1], "1", offset=(-12, 8))
        # A→B (1)
        arrow(A[0], A[1], B[0], B[1], "1", offset=(14, 0))
        # B→A (0) — offset left to separate from A→B
        arrow(B[0], B[1], A[0], A[1], "0", offset=(-14, 0))
        # A→C (0)
        arrow(A[0], A[1], CC[0], CC[1], "0", offset=(0, -12))
        # C self-loop (0,1) — loop ke atas, ukuran kecil
        c.create_arc(CC[0]-16, CC[1]-48, CC[0]+16, CC[1]-16,
                     start=200, extent=300, style=tk.ARC,
                     outline=C_GRAY, width=1.5)
        c.create_polygon(CC[0]-15, CC[1]-20, CC[0]-10, CC[1]-26,
                         CC[0]-6, CC[1]-16, fill=C_GRAY, outline=C_GRAY)
        c.create_text(CC[0]+18, CC[1]-46, text="0,1", font=FONT_SUB, fill=FG2)
        # B self-loop (1)
        self_loop(B[0], B[1], "1", dy=20)

        # ── Nodes ──
        for state, (nx, ny) in self.NODE_POS.items():
            style = dict(NODE_STYLES[state])
            if highlight_state == state:
                if mode == 'active':   style = dict(NODE_ACTIVE)
                elif mode == 'accept': style = dict(NODE_ACCEPT)
                elif mode == 'reject': style = dict(NODE_REJECT)

            c.create_oval(nx-R, ny-R, nx+R, ny+R,
                          fill=style['fill'], outline=style['outline'], width=2)
            # Double circle for accept state
            if state == ACCEPT_STATE:
                c.create_oval(nx-R+5, ny-R+5, nx+R-5, ny+R-5,
                              fill="", outline=style['outline'], width=1)
            c.create_text(nx, ny, text=state, font=FONT_NODE, fill=style['text'])

    # ── Event Handlers ────────────────────────

    def _on_key(self, event):
        self.lbl_err.config(text="")

    def _on_run(self):
        raw = self.entry_var.get().strip()
        err = validate_input(raw)
        if err:
            self.lbl_err.config(text=err)
            return
        self.lbl_err.config(text="")
        self._simulate(raw)

    def _on_reset(self):
        self.entry_var.set("")
        self.lbl_err.config(text="")
        self.result_label.pack_forget()
        self.trace_outer.pack_forget()
        self._draw_fsm()
        self.entry.focus()

    def _set_and_run(self, value):
        self.entry_var.set(value)
        self._simulate(value)

    def _on_tree_select(self, event):
        sel = self.tree.selection()
        if sel:
            item = self.tree.item(sel[0])
            val = item['values'][0]
            self._set_and_run("" if val == "ε (kosong)" else str(val))

    def _clear_history(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    # ── Simulation ────────────────────────────

    def _simulate(self, string):
        accepted, trace = run_fsm(string)
        final_state = trace[-1]['state']

        # Result box
        disp = f'"{string}"' if string else "ε (string kosong)"
        if accepted:
            msg  = f"{disp}  →  DITERIMA ✓"
            detail = "String berakhir di state B (accept state) — anggota bahasa L."
            self.result_label.config(text=f"{msg}\n{detail}",
                                     bg=C_GREEN_LT, fg=C_GREEN)
        else:
            msg = f"{disp}  →  DITOLAK ✗"
            if final_state == TRAP_STATE:
                detail = f"String mengandung substring \"00\" — berakhir di state C (trap)."
            elif string == "":
                detail = "String kosong tidak memenuhi syarat karakter terakhir = 1."
            else:
                detail = f"String tidak berakhir dengan karakter 1 — berakhir di state {final_state}."
            self.result_label.config(text=f"{msg}\n{detail}",
                                     bg=C_RED_LT, fg=C_RED)

        self.result_label.pack(fill=tk.X)

        # Trace
        self._draw_trace(trace, accepted)

        # Diagram highlight
        mode = 'accept' if accepted else 'reject'
        self._draw_fsm(highlight_state=final_state, mode=mode)

        # History
        disp_str = string if string else "ε (kosong)"
        tag = "accept" if accepted else "reject"
        hasil = "DITERIMA ✓" if accepted else "DITOLAK ✗"
        self.tree.insert("", 0, values=(disp_str, hasil, final_state), tags=(tag,))

    def _draw_trace(self, trace, accepted):
        self.trace_outer.pack(fill=tk.X, pady=(10, 0))

        tc = self.trace_canvas
        tc.delete("all")

        x = 8
        for i, step in enumerate(trace):
            state = step['state']
            char  = step['char']
            is_last = (i == len(trace) - 1)

            # Arrow + char
            if i > 0:
                tc.create_text(x, 18, text=f"─{char}→", font=("Courier New", 9),
                               fill=FG2, anchor="w")
                x += 30

            # State pill
            style = NODE_STYLES[state]
            if is_last:
                fill = C_GREEN if accepted else C_RED
                text_c = "white"
                outline = fill
            else:
                fill = style['fill']
                text_c = style['text']
                outline = style['outline']

            w = 28
            tc.create_rectangle(x, 4, x+w, 32, fill=fill,
                                 outline=outline, width=1.5)
            tc.create_text(x + w//2, 18, text=state, font=("Courier New", 10, "bold"),
                           fill=text_c)
            x += w + 4

        tc.config(width=max(x+8, 200))

    def _animate_trace(self, trace, accepted, index=0):
        """Opsional: Animasi transisi state satu per satu."""
        if index >= len(trace):
            return
        step = trace[index]
        mode = 'active'
        if index == len(trace) - 1:
            mode = 'accept' if accepted else 'reject'
        self._draw_fsm(highlight_state=step['state'], mode=mode)
        if index < len(trace) - 1:
            self.after(400, lambda: self._animate_trace(trace, accepted, index+1))


# ──────────────────────────────────────────────
# CLI Mode (fallback tanpa GUI)
# ──────────────────────────────────────────────

def cli_mode():
    print("=" * 55)
    print("  FSM Simulator — Bahasa L")
    print("  L = { x | karakter terakhir 1, tidak ada '00' }")
    print("=" * 55)
    print("Ketik 'keluar' untuk berhenti.\n")

    while True:
        raw = input("Masukkan string (kosong = ε): ").strip()
        if raw.lower() == 'keluar':
            break

        err = validate_input(raw)
        if err:
            print(f"  Error: {err}\n")
            continue

        accepted, trace = run_fsm(raw)
        disp = f'"{raw}"' if raw else 'ε'

        trace_str = ""
        for i, step in enumerate(trace):
            if i > 0:
                trace_str += f" --{step['char']}--> "
            trace_str += step['state']

        print(f"  Jejak    : {trace_str}")
        if accepted:
            print(f"  Hasil    : {disp} DITERIMA ✓")
        else:
            print(f"  Hasil    : {disp} DITOLAK ✗")
        print()


# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if "--cli" in sys.argv:
        cli_mode()
    else:
        try:
            app = FSMApp()
            app.mainloop()
        except tk.TclError:
            print("Tidak dapat membuka GUI. Beralih ke mode CLI...\n")
            cli_mode()