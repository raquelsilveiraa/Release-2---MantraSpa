from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import json

class Servico:
    def __init__(self, nome, descricao, beneficios, local):
        self.nome = nome
        self.descricao = descricao
        self.beneficios = beneficios
        self.local = local

    def __str__(self):
        return f"Nome: {self.nome}\nDescrição: {self.descricao}\nBenefícios: {self.beneficios}\nLocalização: {self.local}"

class Funcionario:
    def __init__(self, nome, cargo, disponivel=True):
        self.nome = nome
        self.cargo = cargo
        self.disponivel = disponivel

    def __str__(self):
        return f"Nome: {self.nome}\nCargo: {self.cargo}\nDisponível: {'Sim' if self.disponivel else 'Não'}"

class Agenda:
    def __init__(self):
        self.horarios_disponiveis = {}
        self.agendamentos = self.carregar_agendamentos()

    def carregar_agendamentos(self):
        try:
            with open("dados.json", "r") as file:
                dados = json.load(file)
                return dados.get("agendamentos", [])
        except FileNotFoundError:
            return []

    def agendar_servico(self, servico, data, horario, cliente):
        if data in self.horarios_disponiveis and horario in [horario_agendado for horario_agendado, _, _ in self.horarios_disponiveis[data]]:
            return "Este horário já está ocupado. Por favor, selecione outro horário."

        data_atual = datetime.now().date()
        data_agendamento = datetime.strptime(data, "%d/%m/%Y").date()
        if data_agendamento <= data_atual:
            return "Não é possível agendar para uma data passada ou presente."
        
        try:
            datetime.strptime(horario, "%H:%M")
        except ValueError:
            return "Formato de horário inválido. Use HH:MM."

        if data not in self.horarios_disponiveis:
            self.horarios_disponiveis[data] = []
        self.horarios_disponiveis[data].append((horario, servico, cliente))

        novo_agendamento = {
            "data": data,
            "horario": horario,
            "servico": vars(servico),
            "cliente": cliente
        }
        self.agendamentos.append(novo_agendamento)
        return "Serviço agendado com sucesso."

class Vendas:
    def __init__(self):
        self.fluxo_de_caixa = []

    def registrar_venda(self, valor, servico):
        self.fluxo_de_caixa.append({"valor": valor, "servico": servico.nome})
        return "Venda registrada com sucesso."

    def exibir_fluxo_de_caixa(self):
        registros = []
        if self.fluxo_de_caixa:
            for venda in self.fluxo_de_caixa:
                registros.append(f"Serviço: {venda['servico']}, Valor: R${venda['valor']}")
        return registros

class GerenciadorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Gerenciamento")
        self.master.geometry("800x600")
        self.master.configure(bg="#f0f0f0")

        self.servicos = []
        self.funcionarios = []
        self.agenda = Agenda()
        self.vendas = Vendas()
        self.avaliacoes = []
        self.promocoes = []

        self.carregar_dados()
        self.menu_login()
        self.data_var = StringVar()
        self.horario_var = StringVar()
        self.cliente_var = StringVar()

    def carregar_dados(self):
        try:
            with open("dados.json", "r") as file:
                dados = json.load(file)
                self.servicos = [Servico(**servico) for servico in dados["servicos"]]
                self.funcionarios = [Funcionario(**funcionario) for funcionario in dados["funcionarios"]]
                self.vendas.fluxo_de_caixa = dados.get("vendas", [])
                self.avaliacoes = dados.get("avaliacoes", [])
                self.promocoes = dados.get("promocoes", [])
        except FileNotFoundError:
            pass

    def salvar_dados(self):
        dados = {
            "servicos": [vars(servico) for servico in self.servicos],
            "funcionarios": [vars(funcionario) for funcionario in self.funcionarios],
            "vendas": self.vendas.fluxo_de_caixa,
            "avaliacoes": self.avaliacoes,
            "promocoes": self.promocoes,
            "agendamentos": []
        }
        for data, horarios in self.agenda.horarios_disponiveis.items():
            for horario, servico, cliente in horarios:
                agendamento = {
                    "data": data,
                    "horario": horario,
                    "servico": vars(servico),
                    "cliente": cliente
                }
                dados["agendamentos"].append(agendamento)
        with open("dados.json", "w") as file:
            json.dump(dados, file, indent=4)

    def ver_horarios_agendados(self):
        agendamentos = self.agenda.carregar_agendamentos()
        if agendamentos:
            window = Toplevel(self.master)
            window.title("Horários Agendados")
            window.geometry("400x400")
            window.configure(bg="#f0f0f0")

            frame_agendamentos = Frame(window, bg="#f0f0f0")
            frame_agendamentos.pack(padx=20, pady=20)

            lbl_titulo = Label(frame_agendamentos, text="Horários Agendados", font=("Albert Sans", 18, "bold"), bg="#f0f0f0")
            lbl_titulo.pack(pady=10)

            for agendamento in agendamentos:
                lbl_agendamento = Label(frame_agendamentos, text=f"{agendamento['data']} às {agendamento['horario']}: {agendamento['servico']['nome']} - Cliente: {agendamento['cliente']}", font=("Albert Sans", 12), bg="#f0f0f0")
                lbl_agendamento.pack(anchor="w", padx=10, pady=5)
        else:
            messagebox.showinfo("Informação", "Não há horários agendados.")

    def menu_login(self):
        self.limpar_tela()

        lbl_titulo = Label(self.master, text="Mantra SPA - Login", font=("Albert Sans", 36, "bold"), bg="#FFC0CB", fg="black", padx=20, pady=10)
        lbl_titulo.pack(fill=X)

        frame_login = Frame(self.master, bg="#f0f0f0", padx=20, pady=20)
        frame_login.pack(pady=20)

        lbl_usuario = Label(frame_login, text="Usuário:", font=("Albert Sans", 18), bg="#f0f0f0")
        lbl_usuario.grid(row=0, column=0, pady=10, sticky=E)

        entry_usuario = Entry(frame_login, font=("Albert Sans", 18))
        entry_usuario.grid(row=0, column=1, pady=10, padx=10)

        lbl_senha = Label(frame_login, text="Senha:", font=("Albert Sans", 18), bg="#f0f0f0")
        lbl_senha.grid(row=1, column=0, pady=10, sticky=E)

        entry_senha = Entry(frame_login, font=("Albert Sans", 18), show="*")
        entry_senha.grid(row=1, column=1, pady=10, padx=10)

        btn_login = Button(frame_login, text="Login", font=("Albert Sans", 18), command=lambda: self.validar_login(entry_usuario.get(), entry_senha.get()), bg="#FFC0CB", fg="black", padx=20, pady=10, bd=0, relief=FLAT)
        btn_login.grid(row=2, column=0, columnspan=2, pady=20)

    def validar_login(self, usuario, senha):
        if usuario == "admin" and senha == "123456":
            self.menu_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def menu_principal(self):
        self.limpar_tela()

        lbl_titulo = Label(self.master, text="Mantra SPA", font=("Albert Sans", 36, "bold"), bg="#FFC0CB", fg="black", padx=20, pady=10)
        lbl_titulo.pack(fill=X)

        frame_botoes = Frame(self.master, bg="#f0f0f0", padx=20, pady=20)
        frame_botoes.pack(pady=20)

        btn_servicos = Button(frame_botoes, text="Gerenciar Serviços", font=("Albert Sans", 18), command=self.menu_servicos, bg="#FFC0CB", fg="black", padx=20, pady=10, bd=0, relief=FLAT)
        btn_servicos.grid(row=0, column=0, padx=10)

        btn_agendamentos = Button(frame_botoes, text="Gerenciar Agendamentos", font=("Albert Sans", 18), command=self.menu_agendamentos, bg="#FFC0CB", fg="black", padx=20, pady=10, bd=0, relief=FLAT)
        btn_agendamentos.grid(row=0, column=1, padx=10)

        btn_funcionarios = Button(frame_botoes, text="Gerenciar Funcionários", font=("Albert Sans", 18), command=self.menu_funcionarios, bg="#FFC0CB", fg="black", padx=20, pady=10, bd=0, relief=FLAT)
        btn_funcionarios.grid(row=1, column=0, padx=10, pady=10)

        btn_vendas = Button(frame_botoes, text="Gerenciar Vendas", font=("Albert Sans", 18), command=self.menu_vendas, bg="#FFC0CB", fg="black", padx=20, pady=10, bd=0, relief=FLAT)
        btn_vendas.grid(row=1, column=1, padx=10, pady=10)

        btn_ver_horarios = Button(frame_botoes, text="Ver Horários Agendados", font=("Albert Sans", 18), command=self.ver_horarios_agendados, bg="#FFC0CB", fg="black", padx=20, pady=10, bd=0, relief=FLAT)
        btn_ver_horarios.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        btn_promocoes = Button(frame_botoes, text="Gerenciar Promoções", font=("Albert Sans", 18), command=self.menu_promocoes, bg="#FFC0CB", fg="black", padx=20, pady=10, bd=0, relief=FLAT)
        btn_promocoes.grid(row=3, column=0, padx=10, pady=10)

        btn_avaliacoes = Button(frame_botoes, text="Ver Avaliações", font=("Albert Sans", 18), command=self.menu_avaliacoes, bg="#FFC0CB", fg="black", padx=20, pady=10, bd=0, relief=FLAT)
        btn_avaliacoes.grid(row=3, column=1, padx=10, pady=10)

        self.master.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)

    def fechar_aplicacao(self):
        self.salvar_dados()
        self.master.destroy()

    def limpar_tela(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def menu_servicos(self):
        self.limpar_tela()

        lbl_titulo = Label(self.master, text="Gerenciamento de Serviços", font=("Albert Sans", 36, "bold"), bg="#FFC0CB", fg="black", padx=20, pady=10)
        lbl_titulo.pack(fill=X)

        frame_botoes = Frame(self.master, bg="#f0f0f0", padx=20, pady=20)
        frame_botoes.pack(pady=20)

        btn_adicionar_servico = Button(frame_botoes, text="Adicionar Serviço", font=("Albert Sans", 14), command=self.adicionar_servico)
        btn_adicionar_servico.grid(row=0, column=0, padx=10)

        btn_listar_servicos = Button(frame_botoes, text="Listar Serviços", font=("Albert Sans", 14), command=self.listar_servicos)
        btn_listar_servicos.grid(row=0, column=1, padx=10)

        btn_remover_servico = Button(frame_botoes, text="Remover Serviço", font=("Albert Sans", 14), command=self.remover_servico)
        btn_remover_servico.grid(row=1, column=0, columnspan=2, pady=10)

        btn_voltar = Button(frame_botoes, text="Voltar", font=("Albert Sans", 14), command=self.menu_principal)
        btn_voltar.grid(row=2, column=0, columnspan=2, pady=10)

    def adicionar_servico(self):
        def adicionar():
            nome = entry_nome.get()
            descricao = entry_descricao.get("1.0", "end-1c")
            beneficios = entry_beneficios.get("1.0", "end-1c")
            local = entry_localizacao.get("1.0", "end-1c")

            if not nome or not descricao or not beneficios:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
                return

            servico = Servico(nome, descricao, beneficios, local)
            self.servicos.append(servico)
            messagebox.showinfo("Sucesso", "Serviço adicionado com sucesso.")
            self.salvar_dados()
            window_add_servico.destroy()

        window_add_servico = Toplevel(self.master)
        window_add_servico.title("Adicionar Serviço")
        window_add_servico.geometry("400x400")
        window_add_servico.configure(bg="#f0f0f0")

        lbl_nome = Label(window_add_servico, text="Nome:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_nome.pack(pady=10)

        entry_nome = Entry(window_add_servico, font=("Albert Sans", 12))
        entry_nome.pack()

        lbl_descricao = Label(window_add_servico, text="Descrição:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_descricao.pack(pady=10)

        entry_descricao = Text(window_add_servico, font=("Albert Sans", 12), height=5, width=30)
        entry_descricao.pack()

        lbl_beneficios = Label(window_add_servico, text="Benefícios:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_beneficios.pack(pady=10)

        entry_beneficios = Text(window_add_servico, font=("Albert Sans", 12), height=5, width=30)
        entry_beneficios.pack()

        lbl_localizacao = Label(window_add_servico, text="Localização:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_localizacao.pack(pady=10)

        entry_localizacao = Text(window_add_servico, font=("Albert Sans", 12), height=5, width=30)
        entry_localizacao.pack()

        btn_adicionar = Button(window_add_servico, text="Adicionar", font=("Albert Sans", 14), command=adicionar)
        btn_adicionar.pack(pady=20)

    def listar_servicos(self):
        self.limpar_tela()

        lbl_titulo = Label(self.master, text="Lista de Serviços", font=("Albert Sans", 24, "bold"), bg="#FFC0CB", fg="black", padx=20, pady=10)
        lbl_titulo.pack(fill=X)

        frame_servicos = Frame(self.master, bg="#f0f0f0", padx=20, pady=20)
        frame_servicos.pack()

        if self.servicos:
            for i, servico in enumerate(self.servicos):
                servico_info = Label(frame_servicos, text=servico.__str__(), font=("Albert Sans", 12), bg="#f0f0f0")
                servico_info.grid(row=i, column=0, sticky="w", pady=5)
        else:
            lbl_aviso = Label(frame_servicos, text="Não há serviços cadastrados.", font=("Albert Sans", 14), bg="#f0f0f0")
            lbl_aviso.grid(row=0, column=0, padx=10, pady=5)

        btn_voltar = Button(self.master, text="Voltar", font=("Albert Sans", 14), command=self.menu_principal)
        btn_voltar.pack()

    def remover_servico(self):
        def remover():
            servico_selecionado = listbox_servicos.curselection()
            if not servico_selecionado:
                messagebox.showerror("Erro", "Por favor, selecione um serviço.")
                return
            indice = servico_selecionado[0]
            self.servicos.pop(indice)
            messagebox.showinfo("Sucesso", "Serviço removido com sucesso.")
            self.salvar_dados()
            window_remover_servico.destroy()
            self.menu_servicos()

        window_remover_servico = Toplevel(self.master)
        window_remover_servico.title("Remover Serviço")
        window_remover_servico.geometry("400x300")
        window_remover_servico.configure(bg="#f0f0f0")

        lbl_selecione = Label(window_remover_servico, text="Selecione o serviço:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_selecione.pack(pady=10)

        listbox_servicos = Listbox(window_remover_servico, font=("Albert Sans", 12), selectmode=SINGLE)
        listbox_servicos.pack(expand=True, fill=BOTH)

        for servico in self.servicos:
            listbox_servicos.insert(END, servico.nome)

        btn_remover = Button(window_remover_servico, text="Remover", font=("Albert Sans", 14), command=remover)
        btn_remover.pack(pady=20)

    def menu_agendamentos(self):
        self.limpar_tela()

        lbl_titulo = Label(self.master, text="Gerenciamento de Agendamentos", font=("Albert Sans", 36, "bold"), bg="#FFC0CB", fg="black", padx=20, pady=10)
        lbl_titulo.pack(fill=X)

        frame_botoes = Frame(self.master, bg="#f0f0f0", padx=20, pady=20)
        frame_botoes.pack(pady=20)

        btn_agendar_servico = Button(frame_botoes, text="Agendar Serviço", font=("Albert Sans", 18), command=self.agendar_servico, bg="#FFC0CB", fg="black", padx=20, pady=10, bd=0, relief=FLAT)
        btn_agendar_servico.grid(row=0, column=0, padx=10)

        btn_ver_horarios = Button(frame_botoes, text="Ver Horários Agendados", font=("Albert Sans", 18), command=self.ver_horarios_agendados, bg="#FFC0CB", fg="black", padx=20, pady=10, bd=0, relief=FLAT)
        btn_ver_horarios.grid(row=0, column=1, padx=10)

        btn_voltar = Button(frame_botoes, text="Voltar", font=("Albert Sans", 18), command=self.menu_principal, bg="#FFC0CB", fg="black", padx=20, pady=10, bd=0, relief=FLAT)
        btn_voltar.grid(row=1, column=0, columnspan=2, pady=10)

    def agendar_servico(self):
        def agendar():
            servico_selecionado = listbox_servicos.curselection()
            if not servico_selecionado:
                messagebox.showerror("Erro", "Por favor, selecione um serviço.")
                return
            servico = self.servicos[servico_selecionado[0]]
            data = entry_data.get()
            horario = entry_horario.get()
            cliente = entry_cliente.get()

            if not data or not horario or not cliente:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
                return

            mensagem = self.agenda.agendar_servico(servico, data, horario, cliente)

            if "sucesso" in mensagem:
                self.salvar_dados()
                window_agendar.destroy()
            messagebox.showinfo("Informação", mensagem)

        window_agendar = Toplevel(self.master)
        window_agendar.title("Agendar Serviço")
        window_agendar.geometry("400x400")
        window_agendar.configure(bg="#f0f0f0")

        lbl_selecione_servico = Label(window_agendar, text="Selecione o serviço:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_selecione_servico.pack(pady=10)

        listbox_servicos = Listbox(window_agendar, font=("Albert Sans", 12), selectmode=SINGLE)
        listbox_servicos.pack(expand=True, fill=BOTH)

        for servico in self.servicos:
            listbox_servicos.insert(END, servico.nome)

        frame_data_horario = Frame(window_agendar, bg="#f0f0f0")
        frame_data_horario.pack(pady=20)

        lbl_data = Label(frame_data_horario, text="Data:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_data.grid(row=0, column=0, padx=10, pady=5)
        entry_data = Entry(frame_data_horario, textvariable=self.data_var, font=("Albert Sans", 12))
        entry_data.grid(row=0, column=1, padx=10, pady=5)

        lbl_horario = Label(frame_data_horario, text="Horário:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_horario.grid(row=1, column=0, padx=10, pady=5)
        entry_horario = Entry(frame_data_horario, textvariable=self.horario_var, font=("Albert Sans", 12))
        entry_horario.grid(row=1, column=1, padx=10, pady=5)

        lbl_cliente = Label(frame_data_horario, text="Cliente:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_cliente.grid(row=2, column=0, padx=10, pady=5)
        entry_cliente = Entry(frame_data_horario, textvariable=self.cliente_var, font=("Albert Sans", 12))
        entry_cliente.grid(row=2, column=1, padx=10, pady=5)

        btn_agendar = Button(window_agendar, text="Agendar", font=("Albert Sans", 14), command=agendar)
        btn_agendar.pack(pady=20)

    def menu_funcionarios(self):
        self.limpar_tela()

        lbl_titulo = Label(self.master, text="Gerenciamento de Funcionários", font=("Albert Sans", 24, "bold"), bg="#FFC0CB", fg="black", padx=20, pady=10)
        lbl_titulo.pack(fill=X)

        frame_botoes = Frame(self.master, bg="#f0f0f0", padx=20, pady=20)
        frame_botoes.pack(pady=20)

        btn_adicionar_funcionario = Button(frame_botoes, text="Adicionar Funcionário", font=("Albert Sans", 14), command=self.adicionar_funcionario)
        btn_adicionar_funcionario.grid(row=0, column=0, padx=10)

        btn_listar_funcionarios = Button(frame_botoes, text="Listar Funcionários", font=("Albert Sans", 14), command=self.listar_funcionarios)
        btn_listar_funcionarios.grid(row=0, column=1, padx=10)

        btn_remover_funcionario = Button(frame_botoes, text="Remover Funcionário", font=("Albert Sans", 14), command=self.remover_funcionario)
        btn_remover_funcionario.grid(row=1, column=0, columnspan=2, pady=10)

        btn_voltar = Button(frame_botoes, text="Voltar", font=("Albert Sans", 14), command=self.menu_principal)
        btn_voltar.grid(row=2, column=0, columnspan=2, pady=10)

    def adicionar_funcionario(self):
        def adicionar():
            nome = entry_nome.get()
            cargo = entry_cargo.get()
            if nome and cargo:
                funcionario = Funcionario(nome, cargo)
                self.funcionarios.append(funcionario)
                messagebox.showinfo("Sucesso", "Funcionário adicionado com sucesso.")
                self.salvar_dados()
                window.destroy()
            else:
                messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

        window = Toplevel(self.master)
        window.title("Adicionar Funcionário")
        window.geometry("400x300")
        window.configure(bg="#f0f0f0")

        frame = Frame(window, bg="#f0f0f0")
        frame.pack(pady=20)

        lbl_nome = Label(frame, text="Nome:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_nome.grid(row=0, column=0, padx=10, pady=5)
        entry_nome = Entry(frame, font=("Albert Sans", 14))
        entry_nome.grid(row=0, column=1, padx=10, pady=5)

        lbl_cargo = Label(frame, text="Cargo:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_cargo.grid(row=1, column=0, padx=10, pady=5)
        entry_cargo = Entry(frame, font=("Albert Sans", 14))
        entry_cargo.grid(row=1, column=1, padx=10, pady=5)

        btn_adicionar = Button(window, text="Adicionar", font=("Albert Sans", 14), command=adicionar)
        btn_adicionar.pack(pady=10)

    def listar_funcionarios(self):
        self.limpar_tela()

        lbl_titulo = Label(self.master, text="Lista de Funcionários", font=("Albert Sans", 24, "bold"), bg="#FFC0CB", fg="black", padx=20, pady=10)
        lbl_titulo.pack(fill=X)

        frame_lista = Frame(self.master, bg="#f0f0f0", padx=20, pady=20)
        frame_lista.pack(pady=20)

        if self.funcionarios:
            for i, funcionario in enumerate(self.funcionarios):
                lbl_funcionario = Label(frame_lista, text=funcionario, font=("Albert Sans", 14), bg="#f0f0f0", wraplength=600, justify="left")
                lbl_funcionario.grid(row=i, column=0, padx=10, pady=5, sticky="w")
        else:
            lbl_aviso = Label(frame_lista, text="Não há funcionários cadastrados.", font=("Albert Sans", 14), bg="#f0f0f0")
            lbl_aviso.grid(row=0, column=0, padx=10, pady=5)

        btn_voltar = Button(self.master, text="Voltar", font=("Albert Sans", 14), command=self.menu_funcionarios)
        btn_voltar.pack()

    def remover_funcionario(self):
        def remover():
            index = combo_funcionarios.current()
            if index >= 0:
                del self.funcionarios[index]
                messagebox.showinfo("Sucesso", "Funcionário removido com sucesso.")
                self.salvar_dados()
                window.destroy()
            else:
                messagebox.showwarning("Erro", "Por favor, selecione um funcionário.")

        window = Toplevel(self.master)
        window.title("Remover Funcionário")
        window.geometry("300x150")
        window.configure(bg="#f0f0f0")

        frame = Frame(window, bg="#f0f0f0")
        frame.pack(pady=20)

        lbl_funcionario = Label(frame, text="Selecione o funcionário:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_funcionario.grid(row=0, column=0, padx=10, pady=5)
        combo_funcionarios = ttk.Combobox(frame, values=[funcionario.nome for funcionario in self.funcionarios], font=("Albert Sans", 14))
        combo_funcionarios.grid(row=0, column=1, padx=10, pady=5)

        btn_remover = Button(window, text="Remover", font=("Albert Sans", 14), command=remover)
        btn_remover.pack(pady=10)

    def menu_vendas(self):
        self.limpar_tela()

        lbl_titulo = Label(self.master, text="Gerenciamento de Vendas", font=("Albert Sans", 24, "bold"), bg="#FFC0CB", fg="black", padx=20, pady=10)
        lbl_titulo.pack(fill=X)

        frame_botoes = Frame(self.master, bg="#f0f0f0", padx=20, pady=20)
        frame_botoes.pack(pady=20)

        btn_registrar_venda = Button(frame_botoes, text="Registrar Venda", font=("Albert Sans", 14), command=self.registrar_venda)
        btn_registrar_venda.grid(row=0, column=0, padx=10)

        btn_exibir_fluxo_de_caixa = Button(frame_botoes, text="Exibir Fluxo de Caixa", font=("Albert Sans", 14), command=self.exibir_fluxo_de_caixa)
        btn_exibir_fluxo_de_caixa.grid(row=0, column=1, padx=10)

        btn_voltar = Button(frame_botoes, text="Voltar", font=("Albert Sans", 14), command=self.menu_principal)
        btn_voltar.grid(row=1, column=0, columnspan=2, pady=10)

    def registrar_venda(self):
        def registrar():
            valor = entry_valor.get()
            servico = self.servicos[combo_servicos.current()]
            if valor and servico:
                resultado = self.vendas.registrar_venda(valor, servico)
                messagebox.showinfo("Sucesso", resultado)
                self.salvar_dados()
                window.destroy()
            else:
                messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

        window = Toplevel(self.master)
        window.title("Registrar Venda")
        window.geometry("400x200")
        window.configure(bg="#f0f0f0")

        frame = Frame(window, bg="#f0f0f0")
        frame.pack(pady=20)

        lbl_servico = Label(frame, text="Serviço:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_servico.grid(row=0, column=0, padx=10, pady=5)
        combo_servicos = ttk.Combobox(frame, values=[servico.nome for servico in self.servicos], font=("Albert Sans", 14))
        combo_servicos.grid(row=0, column=1, padx=10, pady=5)

        lbl_valor = Label(frame, text="Valor:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_valor.grid(row=1, column=0, padx=10, pady=5)
        entry_valor = Entry(frame, font=("Albert Sans", 14))
        entry_valor.grid(row=1, column=1, padx=10, pady=5)

        btn_registrar = Button(window, text="Registrar", font=("Albert Sans", 14), command=registrar)
        btn_registrar.pack(pady=10)

    def exibir_fluxo_de_caixa(self):
        self.limpar_tela()

        lbl_titulo = Label(self.master, text="Fluxo de Caixa", font=("Albert Sans", 24, "bold"), bg="#FFC0CB", fg="black", padx=20, pady=10)
        lbl_titulo.pack(fill=X)

        frame_lista = Frame(self.master, bg="#f0f0f0", padx=20, pady=20)
        frame_lista.pack(pady=20)

        registros = self.vendas.exibir_fluxo_de_caixa()

        if registros:
            for i, registro in enumerate(registros):
                lbl_registro = Label(frame_lista, text=registro, font=("Albert Sans", 14), bg="#f0f0f0", wraplength=600, justify="left")
                lbl_registro.grid(row=i, column=0, padx=10, pady=5, sticky="w")
        else:
            lbl_aviso = Label(frame_lista, text="Não há registros de vendas.", font=("Albert Sans", 14), bg="#f0f0f0")
            lbl_aviso.grid(row=0, column=0, padx=10, pady=5)

        btn_voltar = Button(self.master, text="Voltar", font=("Albert Sans", 14), command=self.menu_vendas)
        btn_voltar.pack()

    def menu_promocoes(self):
        self.limpar_tela()

        lbl_titulo = Label(self.master, text="Gerenciamento de Promoções", font=("Albert Sans", 24, "bold"), bg="#FFC0CB", fg="black", padx=20, pady=10)
        lbl_titulo.pack(fill=X)

        frame_botoes = Frame(self.master, bg="#f0f0f0", padx=20, pady=20)
        frame_botoes.pack(pady=20)

        btn_adicionar_promocao = Button(frame_botoes, text="Adicionar Promoção", font=("Albert Sans", 14), command=self.adicionar_promocao)
        btn_adicionar_promocao.grid(row=0, column=0, padx=10)

        btn_listar_promocoes = Button(frame_botoes, text="Listar Promoções", font=("Albert Sans", 14), command=self.listar_promocoes)
        btn_listar_promocoes.grid(row=0, column=1, padx=10)

        btn_remover_promocao = Button(frame_botoes, text="Remover Promoção", font=("Albert Sans", 14), command=self.remover_promocao)
        btn_remover_promocao.grid(row=1, column=0, columnspan=2, pady=10)

        btn_voltar = Button(frame_botoes, text="Voltar", font=("Albert Sans", 14), command=self.menu_principal)
        btn_voltar.grid(row=2, column=0, columnspan=2, pady=10)

    def adicionar_promocao(self):
        def adicionar():
            descricao = entry_descricao.get("1.0", "end-1c")
            if descricao:
                self.promocoes.append(descricao)
                messagebox.showinfo("Sucesso", "Promoção adicionada com sucesso.")
                self.salvar_dados()
                window.destroy()
            else:
                messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

        window = Toplevel(self.master)
        window.title("Adicionar Promoção")
        window.geometry("400x200")
        window.configure(bg="#f0f0f0")

        lbl_descricao = Label(window, text="Descrição:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_descricao.pack(pady=10)

        entry_descricao = Text(window, font=("Albert Sans", 12), height=5, width=30)
        entry_descricao.pack()

        btn_adicionar = Button(window, text="Adicionar", font=("Albert Sans", 14), command=adicionar)
        btn_adicionar.pack(pady=10)

    def listar_promocoes(self):
        self.limpar_tela()

        lbl_titulo = Label(self.master, text="Lista de Promoções", font=("Albert Sans", 24, "bold"), bg="#FFC0CB", fg="black", padx=20, pady=10)
        lbl_titulo.pack(fill=X)

        frame_lista = Frame(self.master, bg="#f0f0f0", padx=20, pady=20)
        frame_lista.pack(pady=20)

        if self.promocoes:
            for i, promocao in enumerate(self.promocoes):
                lbl_promocao = Label(frame_lista, text=promocao, font=("Albert Sans", 14), bg="#f0f0f0", wraplength=600, justify="left")
                lbl_promocao.grid(row=i, column=0, padx=10, pady=5, sticky="w")
        else:
            lbl_aviso = Label(frame_lista, text="Não há promoções cadastradas.", font=("Albert Sans", 14), bg="#f0f0f0")
            lbl_aviso.grid(row=0, column=0, padx=10, pady=5)

        btn_voltar = Button(self.master, text="Voltar", font=("Albert Sans", 14), command=self.menu_promocoes)
        btn_voltar.pack()

    def remover_promocao(self):
        def remover():
            index = listbox_promocoes.curselection()
            if index:
                del self.promocoes[index[0]]
                messagebox.showinfo("Sucesso", "Promoção removida com sucesso.")
                self.salvar_dados()
                window.destroy()
            else:
                messagebox.showwarning("Erro", "Por favor, selecione uma promoção.")

        window = Toplevel(self.master)
        window.title("Remover Promoção")
        window.geometry("400x300")
        window.configure(bg="#f0f0f0")

        lbl_selecione = Label(window, text="Selecione a promoção:", font=("Albert Sans", 14), bg="#f0f0f0")
        lbl_selecione.pack(pady=10)

        listbox_promocoes = Listbox(window, font=("Albert Sans", 12), selectmode=SINGLE)
        listbox_promocoes.pack(expand=True, fill=BOTH)

        for promocao in self.promocoes:
            listbox_promocoes.insert(END, promocao)

        btn_remover = Button(window, text="Remover", font=("Albert Sans", 14), command=remover)
        btn_remover.pack(pady=20)

    def menu_avaliacoes(self):
        self.limpar_tela()

        lbl_titulo = Label(self.master, text="Avaliações dos Serviços", font=("Albert Sans", 24, "bold"), bg="#FFC0CB", fg="black", padx=20, pady=10)
        lbl_titulo.pack(fill=X)

        frame_lista = Frame(self.master, bg="#f0f0f0", padx=20, pady=20)
        frame_lista.pack(pady=20)

        if self.avaliacoes:
            for i, avaliacao in enumerate(self.avaliacoes):
                lbl_avaliacao = Label(frame_lista, text=f"{avaliacao['cliente']}: {avaliacao['avaliacao']}", font=("Albert Sans", 14), bg="#f0f0f0", wraplength=600, justify="left")
                lbl_avaliacao.grid(row=i, column=0, padx=10, pady=5, sticky="w")
        else:
            lbl_aviso = Label(frame_lista, text="Não há avaliações cadastradas.", font=("Albert Sans", 14), bg="#f0f0f0")
            lbl_aviso.grid(row=0, column=0, padx=10, pady=5)

        btn_voltar = Button(self.master, text="Voltar", font=("Albert Sans", 14), command=self.menu_principal)
        btn_voltar.pack()

root = Tk()
app = GerenciadorApp(root)
root.mainloop()
