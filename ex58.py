import tkinter as tk
from tkinter import messagebox
# Variáveis globais do jogo
jogador_atual = 'X'
pontos_x = 0
pontos_o = 0
tabuleiro = [['' for _ in range(3)] for _ in range(3)]
jogo_terminado = False
botoes = [[None for _ in range(3)] for _ in range(3)]
label_x = None
label_o = None
def criar_interface(root):
    global label_x, label_o, botoes
    
    root.title("Jogo da Velha")
    root.geometry("400x500")
    root.configure(bg="lightgray")
    root.resizable(False, False)
    
    # Configurar grid principal
    for i in range(4):  # 4 colunas para botões controle
        root.grid_columnconfigure(i, weight=1)
    root.grid_rowconfigure(0, weight=0)  # Placar
    for i in range(1, 4):  # Linhas do tabuleiro (1,2,3)
        root.grid_rowconfigure(i, weight=1)
    root.grid_rowconfigure(4, weight=0)  # Botões controle
    
    criar_placar(root)
    criar_tabuleiro(root)
    criar_botoes_controle(root)
def criar_placar(root):
    global label_x, label_o
    
    # Frame para placar na linha 0
    placar_frame = tk.Frame(root, bg="silver")
    placar_frame.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")
    
    # Label para X
    label_x = tk.Label(placar_frame, text=f"Jogador X: {pontos_x}", 
                       font=("Bookman Old Style", 14), bg="yellow", fg="olive", 
                       relief="raised", bd=2, padx=20)
    label_x.pack(side="left", padx=20)
    
    # Label para O
    label_o = tk.Label(placar_frame, text=f"Jogador O: {pontos_o}", 
                       font=("Bookman Old Style", 14), bg="hotpink", fg="deeppink", 
                       relief="raised", bd=2, padx=20)
    label_o.pack(side="right", padx=20)
def criar_tabuleiro(root):
    global botoes
    # Criar 3x3 botões nas linhas 1-3, colunas 0-2
    for i in range(3):
        for j in range(3):
            btn = tk.Button(root, text="", font=("Bookman Old Style", 32), 
                            width=5, height=2, bg="white", fg="black",
                            relief="raised", bd=2,
                            command=lambda row=i, col=j: fazer_jogada(row, col))
            btn.grid(row=i+1, column=j, padx=2, pady=2, sticky="nsew")
            botoes[i][j] = btn
def criar_botoes_controle(root):
    # Botão Reiniciar Partida - linha 4, col 0
    btn_reiniciar = tk.Button(root, text="Reiniciar Partida", 
                              font=("Bookman Old Style", 12), bg="lawngreen", fg="green",
                              relief="raised", bd=2, command=reiniciar_partida)
    btn_reiniciar.grid(row=4, column=0, padx=5, pady=10, sticky="ew")
    
    # Botão Zerar Placar - linha 4, col 1
    btn_zerar = tk.Button(root, text="Zerar Placar", 
                          font=("Bookman Old Style", 12), bg="darkorange", fg="orangered",
                          relief="raised", bd=2, command=zerar_placar)
    btn_zerar.grid(row=4, column=1, padx=5, pady=10, sticky="ew")
    
    # Botão Créditos - linha 4, col 2
    btn_creditos = tk.Button(root, text="Créditos", 
                             font=("Bookman Old Style", 12), bg="turquoise", fg="saddlebrown",
                             relief="raised", bd=2, command=mostrar_creditos)
    btn_creditos.grid(row=4, column=2, padx=5, pady=10, sticky="ew")

    # Espaço vazio na col 3 para equilíbrio
    espaco = tk.Label(root, text="", bg="lightgray")
    espaco.grid(row=4, column=3, sticky="ew")
def fazer_jogada(row, col):
    global jogador_atual, jogo_terminado
    if tabuleiro[row][col] != '' or jogo_terminado:
        return  # Casa ocupada ou jogo terminado
    
    # Colocar símbolo
    tabuleiro[row][col] = jogador_atual
    botoes[row][col].config(text=jogador_atual, state="disabled")
    
    # Verificar vitória ou empate
    if verificar_vitoria():
        finalizar_jogo(f"Jogador {jogador_atual} venceu!")
        return
    elif verificar_empate():
        finalizar_jogo("Empate!")
        return
    
    # Alternar jogador
    jogador_atual = 'O' if jogador_atual == 'X' else 'X'
def verificar_vitoria():
    # Linhas
    for i in range(3):
        if tabuleiro[i][0] == tabuleiro[i][1] == tabuleiro[i][2] != '':
             return True
    # Colunas
    for j in range(3):
        if tabuleiro[0][j] == tabuleiro[1][j] == tabuleiro[2][j] != '':
            return True
    # Diagonais
    if (tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] != '') or \
       (tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] != ''):
        return True
    return False
def verificar_empate():
    return all(tabuleiro[i][j] != '' for i in range(3) for j in range(3))
def finalizar_jogo(mensagem):
    global jogo_terminado, pontos_x, pontos_o
    jogo_terminado = True
    messagebox.showinfo("Fim de Jogo", mensagem)
    
    # Atualizar placar
    if "X venceu" in mensagem:
        pontos_x += 1
    elif "O venceu" in mensagem:
        pontos_o += 1
    # Para empate, não incrementa ninguém
    
    atualizar_placar()
def atualizar_placar():
    global label_x, label_o
    label_x.config(text=f"Jogador X: {pontos_x}")
    label_o.config(text=f"Jogador O: {pontos_o}")
def reiniciar_partida():
    global tabuleiro, jogador_atual, jogo_terminado
    tabuleiro = [['' for _ in range(3)] for _ in range(3)]
    jogador_atual = 'X'
    jogo_terminado = False
    for i in range(3):
        for j in range(3):
            botoes[i][j].config(text="", state="normal")
def zerar_placar():
    global pontos_x, pontos_o
    pontos_x = 0
    pontos_o = 0
    atualizar_placar()
    reiniciar_partida()  # Opcional: também reinicia o tabuleiro
def mostrar_creditos():
    creditos = """
    Jogo da Velha - Tic Tac Toe
    
    Desenvolvido por:
    - Duda Cavalcante
    - Turma: Turminha da sala 18
    - Professor: Alexandre Tolentino
    - Data: 09/10/2025
    
    """
    messagebox.showinfo("Créditos", creditos)
if __name__ == "__main__":
    root = tk.Tk()
    criar_interface(root)
    root.mainloop()