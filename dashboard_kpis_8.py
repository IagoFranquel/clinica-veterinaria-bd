"""
Dashboard de KPIs – ShopBR E-Commerce
Trabalho Avaliativo – Banco de Dados (3ª Avaliação)

Instalação:
  pip install matplotlib pandas

Execução:
  py dashboard_kpis.py
"""

import sqlite3
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime, timedelta
import random
import os

# ─── BANCO DE DADOS ───────────────────────────────────────────

DB_FILE = "shopbr.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
            cidade TEXT, estado TEXT);
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL,
            preco REAL NOT NULL, estoque INTEGER DEFAULT 0,
            categoria_id INTEGER REFERENCES categorias(id));
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER REFERENCES clientes(id),
            valor_total REAL NOT NULL,
            status TEXT NOT NULL CHECK(status IN
                ('processando','enviado','entregue','cancelado')),
            data_pedido TEXT DEFAULT (datetime('now')));
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER REFERENCES pedidos(id) ON DELETE CASCADE,
            produto_id INTEGER REFERENCES produtos(id),
            quantidade INTEGER NOT NULL, preco_unit REAL NOT NULL,
            subtotal REAL);
    """)
    conn.executescript("""
        INSERT OR IGNORE INTO categorias(nome) VALUES
            ('Eletrônicos'),('Roupas'),('Casa'),('Esporte');
        INSERT OR IGNORE INTO clientes(nome,email,cidade,estado) VALUES
            ('Ana Paula','ana@email.com','São Paulo','SP'),
            ('Bruno Lima','bruno@email.com','Fortaleza','CE'),
            ('Carla Torres','carla@email.com','Curitiba','PR'),
            ('Diego Ramos','diego@email.com','Recife','PE'),
            ('Elisa Nunes','elisa@email.com','Teresina','PI'),
            ('Felipe Costa','felipe@email.com','Belo Horizonte','MG'),
            ('Gisele Fernanda','gisele@email.com','Porto Alegre','RS'),
            ('Hugo Mendes','hugo@email.com','Salvador','BA');
        INSERT OR IGNORE INTO produtos(nome,preco,estoque,categoria_id) VALUES
            ('Notebook Pro 15"',3299.00,45,1),
            ('Fone BT Max 500',449.00,120,1),
            ('Smartwatch Fit',599.90,80,1),
            ('Tablet Ultra 10"',1199.00,60,1),
            ('Mouse Gamer RGB',189.90,200,1),
            ('Camiseta Fit Dry',89.90,350,2),
            ('Calça Slim Jeans',129.90,220,2),
            ('Jaqueta Winter',299.90,90,2),
            ('Panela Smart 5L',189.90,75,3),
            ('Tapete Premium 2m²',249.90,40,3),
            ('Tênis Run Ultra',299.90,130,4),
            ('Garrafa Thermos 1L',89.90,180,4);
    """)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM pedidos")
    if cur.fetchone()[0] == 0:
        status_opts = ['processando','enviado','entregue','entregue','entregue','cancelado']
        hoje = datetime.now()
        for _ in range(120):
            cid = random.randint(1, 8)
            data = (hoje - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d %H:%M:%S")
            status = random.choice(status_opts)
            itens = [(random.randint(1,12), random.randint(1,3)) for _ in range(random.randint(1,4))]
            valor_total = 0
            for pid, qtd in itens:
                preco = cur.execute("SELECT preco FROM produtos WHERE id=?", (pid,)).fetchone()[0]
                valor_total += round(preco * qtd, 2)
            valor_total = round(valor_total, 2)
            cur.execute("INSERT INTO pedidos(cliente_id,valor_total,status,data_pedido) VALUES(?,?,?,?)",
                        (cid, valor_total, status, data))
            pid_novo = cur.lastrowid
            for prod_id, qtd in itens:
                preco = cur.execute("SELECT preco FROM produtos WHERE id=?", (prod_id,)).fetchone()[0]
                cur.execute("INSERT INTO itens_pedido(pedido_id,produto_id,quantidade,preco_unit,subtotal) VALUES(?,?,?,?,?)",
                            (pid_novo, prod_id, qtd, preco, round(preco*qtd,2)))
        conn.commit()
    return conn

# ─── QUERIES SQL ──────────────────────────────────────────────

def filtros(ano, tri, cat):
    conds = ["p.status != 'cancelado'"]
    params = []
    if ano:
        conds.append("strftime('%Y',p.data_pedido)=?"); params.append(ano)
    if tri:
        m = {"T1":("01","03"),"T2":("04","06"),"T3":("07","09"),"T4":("10","12")}[tri]
        conds.append("strftime('%m',p.data_pedido) BETWEEN ? AND ?"); params += list(m)
    if cat and cat != "Todas":
        conds.append("""EXISTS(SELECT 1 FROM itens_pedido x
            JOIN produtos px ON px.id=x.produto_id
            JOIN categorias cx ON cx.id=px.categoria_id
            WHERE x.pedido_id=p.id AND cx.nome=?)"""); params.append(cat)
    return "WHERE " + " AND ".join(conds), params

def q_kpi(conn, ano, tri, cat):
    w, p = filtros(ano, tri, cat)
    return conn.execute(f"""
        SELECT COUNT(DISTINCT p.id), ROUND(SUM(p.valor_total),2),
               ROUND(AVG(p.valor_total),2), MIN(p.valor_total), MAX(p.valor_total)
        FROM pedidos p {w}""", p).fetchone()

def q_mensal(conn, ano, tri, cat):
    w, p = filtros(ano, tri, cat)
    return pd.read_sql_query(f"""
        SELECT strftime('%m/%Y',p.data_pedido) AS mes,
               strftime('%Y-%m',p.data_pedido) AS ordem,
               ROUND(SUM(p.valor_total),2) AS receita
        FROM pedidos p {w}
        GROUP BY strftime('%Y-%m',p.data_pedido)
        ORDER BY ordem ASC""", conn, params=p)

def q_categoria(conn, ano, tri):
    w, p = filtros(ano, tri, None)
    return pd.read_sql_query(f"""
        SELECT cat.nome AS categoria, ROUND(SUM(ip.subtotal),2) AS receita
        FROM itens_pedido ip
        JOIN produtos pr ON pr.id=ip.produto_id
        JOIN categorias cat ON cat.id=pr.categoria_id
        JOIN pedidos p ON p.id=ip.pedido_id {w}
        GROUP BY cat.nome ORDER BY receita DESC""", conn, params=p)

def q_top(conn, ano, tri, cat, ordem):
    w, p = filtros(ano, tri, cat)
    return pd.read_sql_query(f"""
        SELECT pr.nome AS produto, SUM(ip.quantidade) AS total
        FROM itens_pedido ip
        JOIN produtos pr ON pr.id=ip.produto_id
        JOIN pedidos p ON p.id=ip.pedido_id {w}
        GROUP BY pr.nome ORDER BY total {ordem} LIMIT 5""", conn, params=p)

def q_ticket(conn, ano, tri, cat):
    w, p = filtros(ano, tri, cat)
    return pd.read_sql_query(f"""
        SELECT strftime('%m/%Y',p.data_pedido) AS mes,
               strftime('%Y-%m',p.data_pedido) AS ordem,
               ROUND(AVG(p.valor_total),2) AS ticket
        FROM pedidos p {w}
        GROUP BY strftime('%Y-%m',p.data_pedido)
        ORDER BY ordem ASC""", conn, params=p)

def q_pedidos(conn):
    return pd.read_sql_query("""
        SELECT p.id AS "Pedido",
               c.nome AS "Cliente",
               c.cidade||'/'||c.estado AS "Cidade",
               printf('R$ %.2f', p.valor_total) AS "Valor",
               p.status AS "Status",
               strftime('%d/%m/%Y', p.data_pedido) AS "Data"
        FROM pedidos p
        JOIN clientes c ON c.id=p.cliente_id
        ORDER BY p.data_pedido DESC LIMIT 50""", conn)

# ─── CORES ────────────────────────────────────────────────────

AZUL    = "#185FA5"
VERDE   = "#0F6E56"
LARANJA = "#854F0B"
ROXO    = "#534AB7"
ROSA    = "#993556"
AMBER   = "#B45309"
BG      = "#F4F5F7"
BRANCO  = "#FFFFFF"
TEXTO   = "#1A1A2E"
TEXTO2  = "#6B7280"
CORES   = [AZUL, VERDE, LARANJA, ROXO, ROSA]

def brl(v):
    if v is None: return "—"
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

# ─── APP ──────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.title("ShopBR – Dashboard de KPIs")
        self.state("zoomed")          # abre maximizado no Windows
        self.configure(bg=BG)

        self._header()
        self._filtros()
        self._kpis()

        # painel inferior: gráficos à esquerda, tabela à direita
        painel = tk.Frame(self, bg=BG)
        painel.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0,8))
        painel.columnconfigure(0, weight=3)
        painel.columnconfigure(1, weight=2)
        painel.rowconfigure(0, weight=1)

        self._graficos(painel)
        self._tabela(painel)

        self.atualizar()

    # ── Header ────────────────────────────────
    def _header(self):
        f = tk.Frame(self, bg=AZUL, pady=10, padx=18)
        f.pack(fill=tk.X)
        tk.Label(f, text="🛒  ShopBR — Dashboard de KPIs",
                 bg=AZUL, fg=BRANCO, font=("Helvetica",16,"bold")).pack(side=tk.LEFT)
        tk.Label(f, text="E-Commerce · SQLite · SQL + Python",
                 bg=AZUL, fg="#BCD4ED", font=("Helvetica",9)).pack(side=tk.LEFT, padx=16)

    # ── Filtros ───────────────────────────────
    def _filtros(self):
        f = tk.Frame(self, bg=BRANCO, pady=6, padx=18)
        f.pack(fill=tk.X)

        def lbl(t): tk.Label(f, text=t, bg=BRANCO, fg=TEXTO2, font=("Helvetica",9)).pack(side=tk.LEFT)
        def cb(var, vals, w=8):
            c = ttk.Combobox(f, textvariable=var, values=vals, width=w, state="readonly")
            c.pack(side=tk.LEFT, padx=(3,14))
            c.bind("<<ComboboxSelected>>", lambda e: self.atualizar())
            return c

        self.v_ano = tk.StringVar(value="Todos")
        anos = ["Todos"] + sorted({r[0] for r in self.conn.execute(
            "SELECT DISTINCT strftime('%Y',data_pedido) FROM pedidos")}, reverse=True)
        lbl("Período:"); cb(self.v_ano, anos)

        self.v_tri = tk.StringVar(value="Todos")
        lbl("Trimestre:"); cb(self.v_tri, ["Todos","T1","T2","T3","T4"], 6)

        self.v_cat = tk.StringVar(value="Todas")
        cats = ["Todas"] + [r[0] for r in self.conn.execute("SELECT nome FROM categorias ORDER BY nome")]
        lbl("Categoria:"); cb(self.v_cat, cats, 12)

        self.v_ord = tk.StringVar(value="DESC")
        lbl("Top produtos:")
        for t, v in [("↓ Maior","DESC"),("↑ Menor","ASC")]:
            tk.Radiobutton(f, text=t, variable=self.v_ord, value=v, bg=BRANCO,
                           font=("Helvetica",9), command=self.atualizar).pack(side=tk.LEFT, padx=3)

        tk.Button(f, text="⟳ Atualizar", bg=AZUL, fg=BRANCO, relief=tk.FLAT,
                  font=("Helvetica",9,"bold"), padx=10, pady=3,
                  cursor="hand2", command=self.atualizar).pack(side=tk.RIGHT, padx=6)

    # ── KPI Cards ─────────────────────────────
    def _kpis(self):
        self.frm_kpi = tk.Frame(self, bg=BG, padx=12, pady=6)
        self.frm_kpi.pack(fill=tk.X)
        self.kv = {}
        campos = [
            ("rec","Receita Total",AZUL),("ped","Total Pedidos",VERDE),
            ("tck","Ticket Médio",LARANJA),("mn","Menor Pedido",ROXO),
            ("mx","Maior Pedido",ROSA),("canc","Taxa Cancelamento",AMBER),
        ]
        for i,(k,lbl,cor) in enumerate(campos):
            card = tk.Frame(self.frm_kpi, bg=BRANCO, padx=14, pady=10,
                            highlightthickness=1, highlightbackground="#E5E7EB")
            card.grid(row=0, column=i, sticky="nsew", padx=5)
            self.frm_kpi.columnconfigure(i, weight=1)
            tk.Frame(card, bg=cor, width=3).place(relx=0, rely=0, relheight=1)
            tk.Label(card, text=lbl, bg=BRANCO, fg=TEXTO2,
                     font=("Helvetica",8), anchor="w").pack(anchor="w", padx=5)
            v = tk.StringVar(value="—")
            self.kv[k] = v
            tk.Label(card, textvariable=v, bg=BRANCO, fg=cor,
                     font=("Helvetica",14,"bold")).pack(anchor="w", padx=5)

    # ── Gráficos ──────────────────────────────
    def _graficos(self, painel):
        f = tk.Frame(painel, bg=BG)
        f.grid(row=0, column=0, sticky="nsew", padx=(0,6))

        self.fig, axes = plt.subplots(2, 2, figsize=(9, 6), facecolor=BG)
        self.fig.subplots_adjust(wspace=0.35, hspace=0.45,
                                 left=0.08, right=0.97, top=0.93, bottom=0.12)
        self.ax_lin, self.ax_piz = axes[0]
        self.ax_bar, self.ax_are = axes[1]
        for ax in [self.ax_lin, self.ax_piz, self.ax_bar, self.ax_are]:
            ax.set_facecolor(BRANCO)

        self.cv = FigureCanvasTkAgg(self.fig, master=f)
        self.cv.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ── Tabela ────────────────────────────────
    def _tabela(self, painel):
        f = tk.Frame(painel, bg=BG)
        f.grid(row=0, column=1, sticky="nsew")
        f.rowconfigure(1, weight=1)
        f.columnconfigure(0, weight=1)

        tk.Label(f, text="📋  Últimos Pedidos", bg=BG, fg=TEXTO,
                 font=("Helvetica",10,"bold")).grid(row=0, column=0, columnspan=2,
                                                    sticky="w", pady=(4,4), padx=2)

        cols = ["Pedido","Cliente","Cidade","Valor","Status","Data"]
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("T.Treeview", background=BRANCO, foreground=TEXTO,
                        rowheight=22, fieldbackground=BRANCO, font=("Helvetica",8))
        style.configure("T.Treeview.Heading", background=AZUL, foreground=BRANCO,
                        font=("Helvetica",8,"bold"), relief="flat")
        style.map("T.Treeview", background=[("selected","#DBEAFE")])

        self.tree = ttk.Treeview(f, columns=cols, show="headings", style="T.Treeview")
        larguras = {"Pedido":55,"Cliente":130,"Cidade":110,"Valor":90,"Status":80,"Data":80}
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=larguras[col], anchor="center", stretch=True)

        sb = ttk.Scrollbar(f, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.grid(row=1, column=0, sticky="nsew")
        sb.grid(row=1, column=1, sticky="ns")

        self.tree.tag_configure("entregue",    background="#D1FAE5", foreground="#065F46")
        self.tree.tag_configure("enviado",     background="#FEF3C7", foreground="#78350F")
        self.tree.tag_configure("processando", background="#EDE9FE", foreground="#3730A3")
        self.tree.tag_configure("cancelado",   background="#FEE2E2", foreground="#7F1D1D")

        tk.Label(f,
                 text="SELECT p.id, c.nome, p.valor_total, p.status\n"
                      "FROM pedidos p JOIN clientes c ON c.id=p.cliente_id\n"
                      "ORDER BY p.data_pedido DESC LIMIT 50",
                 bg=BG, fg=TEXTO2, font=("Courier",7), justify="left"
                 ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(4,0))

    # ── Atualizar ─────────────────────────────
    def atualizar(self):
        ano = self.v_ano.get() if self.v_ano.get() != "Todos" else None
        tri = self.v_tri.get() if self.v_tri.get() != "Todos" else None
        cat = self.v_cat.get() if self.v_cat.get() != "Todas" else None
        ord_ = self.v_ord.get()

        # KPIs
        r = q_kpi(self.conn, ano, tri, cat)
        if r:
            self.kv["rec"].set(brl(r[1]))
            self.kv["ped"].set(str(r[0]))
            self.kv["tck"].set(brl(r[2]))
            self.kv["mn"].set(brl(r[3]))
            self.kv["mx"].set(brl(r[4]))
        tot = self.conn.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
        can = self.conn.execute("SELECT COUNT(*) FROM pedidos WHERE status='cancelado'").fetchone()[0]
        self.kv["canc"].set(f"{round(100*can/tot,1)}%" if tot else "—")

        # Gráficos
        for ax in [self.ax_lin, self.ax_piz, self.ax_bar, self.ax_are]:
            ax.clear(); ax.set_facecolor(BRANCO)
            for s in ax.spines.values(): s.set_color("#E5E7EB")

        tc = TEXTO2

        # 1. Linha – Receita mensal
        dm = q_mensal(self.conn, ano, tri, cat)
        if not dm.empty:
            x = range(len(dm))
            self.ax_lin.plot(list(x), dm["receita"].tolist(), color=AZUL,
                             linewidth=2, marker="o", markersize=4)
            self.ax_lin.fill_between(list(x), dm["receita"].tolist(), alpha=0.1, color=AZUL)
            self.ax_lin.set_xticks(list(x))
            self.ax_lin.set_xticklabels(dm["mes"].tolist(), rotation=45, fontsize=6, ha="right")
            self.ax_lin.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"R${v/1000:.0f}k"))
        self.ax_lin.set_title("Receita por Mês", fontsize=9, fontweight="bold", color=TEXTO)
        self.ax_lin.tick_params(labelsize=6, colors=tc)
        self.ax_lin.grid(axis="y", linestyle="--", alpha=0.3)

        # 2. Pizza – Categorias
        dc = q_categoria(self.conn, ano, tri)
        if not dc.empty:
            wedges, texts, autos = self.ax_piz.pie(
                dc["receita"], labels=dc["categoria"], autopct="%1.1f%%",
                colors=CORES[:len(dc)], startangle=140,
                wedgeprops=dict(width=0.6, edgecolor=BRANCO, linewidth=1.5),
                pctdistance=0.78)
            for t in texts: t.set_fontsize(7)
            for a in autos: a.set_fontsize(6); a.set_color(BRANCO); a.set_fontweight("bold")
        self.ax_piz.set_title("Vendas por Categoria", fontsize=9, fontweight="bold", color=TEXTO)

        # 3. Barras – Top produtos
        dt = q_top(self.conn, ano, tri, cat, ord_)
        if not dt.empty:
            nomes = [n[:16]+"…" if len(n)>16 else n for n in dt["produto"]]
            bars = self.ax_bar.barh(nomes, dt["total"].tolist(), color=VERDE,
                                    edgecolor=BRANCO, linewidth=0.5)
            for b in bars:
                w = b.get_width()
                self.ax_bar.text(w+0.3, b.get_y()+b.get_height()/2,
                                 str(int(w)), va="center", fontsize=6, color=tc)
        self.ax_bar.invert_yaxis()
        self.ax_bar.set_title("Top 5 Produtos", fontsize=9, fontweight="bold", color=TEXTO)
        self.ax_bar.tick_params(labelsize=6, colors=tc)
        self.ax_bar.grid(axis="x", linestyle="--", alpha=0.3)

        # 4. Área – Ticket médio
        dk = q_ticket(self.conn, ano, tri, cat)
        if not dk.empty:
            x = range(len(dk))
            self.ax_are.plot(list(x), dk["ticket"].tolist(), color=LARANJA,
                             linewidth=2, marker="s", markersize=3, linestyle="--")
            self.ax_are.fill_between(list(x), dk["ticket"].tolist(), alpha=0.12, color=LARANJA)
            self.ax_are.set_xticks(list(x))
            self.ax_are.set_xticklabels(dk["mes"].tolist(), rotation=45, fontsize=6, ha="right")
            self.ax_are.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"R${v:.0f}"))
        self.ax_are.set_title("Ticket Médio por Mês", fontsize=9, fontweight="bold", color=TEXTO)
        self.ax_are.tick_params(labelsize=6, colors=tc)
        self.ax_are.grid(axis="y", linestyle="--", alpha=0.3)

        self.cv.draw()

        # Tabela
        for row in self.tree.get_children():
            self.tree.delete(row)
        df = q_pedidos(self.conn)
        for _, r in df.iterrows():
            status = r["Status"].lower()
            self.tree.insert("", tk.END, values=list(r), tags=(status,))


# ─── MAIN ─────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Iniciando ShopBR Dashboard...")
    conn = init_db()
    print("Banco OK:", os.path.abspath(DB_FILE))
    app = App(conn)
    app.mainloop()
    conn.close()
