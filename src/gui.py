"""Interface desktop para visualizar o Problema do Caixeiro Viajante."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tsp import ALGORITHMS, selected_graph, solve


class TSPGui(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Caixeiro Viajante — Visualizador")
        self.geometry("1180x760")
        self.minsize(900, 620)
        self.result = None
        self.graph = None
        self.positions = None
        self.animating = False

        self._build_style()
        self._build_layout()

    def _build_style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("TkDefaultFont", 20, "bold"))
        style.configure("Muted.TLabel", foreground="#64748b")
        style.configure("Run.TButton", font=("TkDefaultFont", 11, "bold"))

    def _build_layout(self) -> None:
        header = ttk.Frame(self, padding=(22, 18, 22, 8))
        header.pack(fill="x")
        ttk.Label(header, text="Problema do Caixeiro Viajante", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Compare algoritmos e acompanhe a construção da rota.", style="Muted.TLabel").pack(anchor="w", pady=(4, 0))

        body = ttk.Frame(self, padding=12)
        body.pack(fill="both", expand=True)
        controls = ttk.LabelFrame(body, text="Configuração", padding=14)
        controls.pack(side="left", fill="y", padx=(0, 12))
        viewer = ttk.Frame(body)
        viewer.pack(side="left", fill="both", expand=True)

        ttk.Label(controls, text="Algoritmo").pack(anchor="w")
        self.algorithm = ttk.Combobox(controls, state="readonly", values=list(ALGORITHMS), width=25)
        self.algorithm.current(0)
        self.algorithm.pack(fill="x", pady=(5, 14))
        ttk.Label(controls, text="Grafo").pack(anchor="w")
        self.graph_size = tk.IntVar(value=5)
        ttk.Radiobutton(controls, text="Grafo pequeno (5 vértices)", variable=self.graph_size, value=5).pack(anchor="w", pady=3)
        ttk.Radiobutton(controls, text="Grafo grande (18 vértices)", variable=self.graph_size, value=18).pack(anchor="w", pady=3)
        ttk.Button(controls, text="Executar algoritmo", style="Run.TButton", command=self.run).pack(fill="x", pady=(22, 8))
        ttk.Button(controls, text="Limpar resultado", command=self.clear).pack(fill="x")
        ttk.Button(controls, text="▶ Animar caminho", command=self.start_animation).pack(fill="x", pady=(8, 0))
        ttk.Button(controls, text="Ⅱ Pausar animação", command=self.pause_animation).pack(fill="x", pady=(5, 0))
        ttk.Label(controls, text="Velocidade").pack(anchor="w", pady=(16, 3))
        self.speed = tk.DoubleVar(value=600)
        ttk.Scale(controls, from_=100, to=1500, variable=self.speed, orient="horizontal").pack(fill="x")
        ttk.Separator(controls).pack(fill="x", pady=20)
        self.cost = ttk.Label(controls, text="Custo total: —")
        self.time = ttk.Label(controls, text="Tempo: —")
        self.steps = ttk.Label(controls, text="Passos: —")
        for label in (self.cost, self.time, self.steps):
            label.pack(anchor="w", pady=3)
        self.route = ttk.Label(controls, text="Rota: —", wraplength=230, justify="left")
        self.route.pack(anchor="w", pady=(16, 0))

        self.figure, self.ax = plt.subplots(figsize=(8, 6), facecolor="white")
        self.canvas = FigureCanvasTkAgg(self.figure, master=viewer)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.slider = ttk.Scale(viewer, from_=0, to=0, orient="horizontal", command=self._on_slider)
        self.slider.pack(fill="x", padx=18, pady=(8, 0))
        self.step_label = ttk.Label(viewer, text="Execute um algoritmo para visualizar a rota.", style="Muted.TLabel")
        self.step_label.pack(pady=(3, 8))
        self._draw_empty()

    def run(self) -> None:
        if self.graph_size.get() == 18 and self.algorithm.get() == "Força Bruta":
            messagebox.showwarning("Execução demorada", "A força bruta pode ser muito lenta para 18 vértices. Prefira Held-Karp ou uma heurística.")
            return
        self.config(cursor="watch")
        self.update_idletasks()
        try:
            self.graph = selected_graph(self.graph_size.get())
            self.result = solve(self.graph, self.algorithm.get())
            self.positions = nx.spring_layout(self.graph, seed=42)
            self.cost.config(text=f"Custo total: {self.result.cost:.2f}")
            self.time.config(text=f"Tempo: {self.result.elapsed * 1000:.3f} ms")
            self.steps.config(text=f"Passos: {len(self.result.steps)}")
            shown_route = self.result.steps[-1] if self.result.steps else self.result.route
            self.route.config(text="Caminho real: " + " → ".join(map(str, shown_route)))
            self.slider.configure(to=max(0, len(self.result.steps) - 1))
            self.slider.set(max(0, len(self.result.steps) - 1))
            self._draw(max(0, len(self.result.steps) - 1))
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))
        finally:
            self.config(cursor="")

    def clear(self) -> None:
        self.pause_animation()
        self.result = self.graph = None
        self.cost.config(text="Custo total: —")
        self.time.config(text="Tempo: —")
        self.steps.config(text="Passos: —")
        self.route.config(text="Rota: —")
        self.slider.configure(to=0)
        self.slider.set(0)
        self.step_label.config(text="Execute um algoritmo para visualizar a rota.")
        self._draw_empty()

    def _on_slider(self, value: str) -> None:
        if self.result:
            self._draw(int(float(value)))

    def start_animation(self) -> None:
        if self.result and self.result.steps:
            self.animating = True
            self._animate_step(0)

    def pause_animation(self) -> None:
        self.animating = False

    def _animate_step(self, step: int) -> None:
        if not self.animating or not self.result:
            return
        self.slider.set(step)
        self._draw(step)
        if step + 1 < len(self.result.steps):
            self.after(max(100, int(self.speed.get())), lambda: self._animate_step(step + 1))
        else:
            self.animating = False

    def _draw_empty(self) -> None:
        self.ax.clear()
        self.ax.text(0.5, 0.5, "Selecione as opções e execute um algoritmo", ha="center", va="center", color="#64748b")
        self.ax.axis("off")
        self.canvas.draw_idle()

    def _draw(self, step: int) -> None:
        shown = self.result.steps[step]
        self.ax.clear()
        nx.draw_networkx(self.graph, self.positions, ax=self.ax, node_color="#dbeafe", edge_color="#cbd5e1", node_size=650, with_labels=True, font_weight="bold")
        nx.draw_networkx_edges(self.graph, self.positions, edgelist=list(zip(shown, shown[1:])), edge_color="#ef4444", width=3, ax=self.ax)
        nx.draw_networkx_edge_labels(self.graph, self.positions, edge_labels=nx.get_edge_attributes(self.graph, "weight"), ax=self.ax, font_size=8)
        self.ax.set_title(f"Rota — passo {step + 1}/{len(self.result.steps)}")
        self.ax.axis("off")
        self.step_label.config(text=f"Passo {step + 1} de {len(self.result.steps)}")
        self.canvas.draw_idle()


if __name__ == "__main__":
    TSPGui().mainloop()
