# Alunos:
# Gabriel Hiroaki da Silva Kanezaki   RA: 179292
# Luiz Felipe Teodoro Monteiro        RA: 177210

# Programa de busca de DNA, pelo método KMP para 
# nos retornar as posições do DNA requisitado
# e juntamente com o algoritmo de força bruta
# para verificarmos a quantidade de comparações
# entre cada algoritmo.

# Funcionamento do programa:
# 1º - Digitar uma cadeia aleatória de DNA
# 2º - Digitar uma cadeia de DNA a ser buscada
# na cadeia aleatória.
# 3º - Clicar em buscar.
# Obs.: Programa funciona com letra minúscula
# e maiúscula. 

# Obs.: o programa só vai conseguir rodar
# se respeitar algumas condições, onde só
# vai dar continuidade, se:
# 1º - A entrada do DNA, tanto no valor aleatório
# quanto no valor a ser buscado, tem que estar 
# dentro dos caracteres permitidos: [A, C, G, T]
# ou seja, se colocar outro caractere o programa 
# não vai ser executado.
# 2º - O DNA a ser buscado não pode ser maior que 
# a cadeia aleatória.
# 3º - Tanto a cadeia aleatória quanto o DNA a ser
# buscado, o tamanho tem que ser maior que zero.

import numpy as np
import tkinter as tk

# ajustes da fonte e cor do fundo do programa
bg = 'gray'
cms = ('terminal', 12, 'bold')

# classe feita para nos auxiliar no desenvolvimento
# do código em geral, desse modo facilitando o 
# armazenamento das váriaveis entre as funções
class Algoritmos():
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern
    # algoritmo da busca de substring kmp

    def kmp(self):
        iteracaoKmp = 0 
        dfa = self.criaDFA(iteracaoKmp)
        print(f'DFA: {dfa}')
        # vetor que vai armazenar os indices das ocorrencias
        ans = []
        # k vai ser o indice da nossa substring
        k = 0
        # percorrendo o texto
        for i in range(len(self.text)):                         
            while k > 0 and self.text[i] != self.pattern[k]:   
                k = dfa[k - 1]                                 
            if self.text[i] == self.pattern[k]:
                k += 1
                iteracaoKmp += 1
                if k == len(self.pattern):
                    # se k (indice do dfa) == tamanho do padrao, significa que chegamos no ultimo estado
                    # portanto, encontramos nossa substring e iremos adicionar o indice a lista ans
                    ans.append(i - (k - 1)) # i - (k - 1) é o indice onde a substring foi encontrada
                    k = dfa[k - 1]  # k = dfa[len(padrao) - 1], pois k sera == len(padrao)
                    iteracaoKmp += 1
        return ans, iteracaoKmp

    def criaDFA(self, iteracaoKmp):
        # primeira posição do dfa será sempre 0
        j = 0
        dfa = [j] 
        # percorre a substring  
        for i in range(1, len(self.pattern)):
            while j > 0 and self.pattern[j] != self.pattern[i]:     
                # se nao estivermos na primeira posicao do dfa e padrao[j] != padrao[i]
                # j ira retroceder para a posicao j-1 do dfa
                j = dfa[j - 1]
            if self.pattern[j] == self.pattern[i]:
                j += 1             
                iteracaoKmp += 1 
            # caso j == 0 e padrao[i] != padrao[j], dfa vai armazenar 0
            # caso j > 0 e padrao[i] != padrao[j], dfa vai armazenar o valor de dfa[j - 1]
            # caso j > 0 e padrao[i] == padrao[j], dfa vai armazenar j + 1       
            dfa.append(j)                   
        return dfa

    # algoritmo da força bruta

    def forcabruta(self):
        # iniciando a variavel onde vamos
        # armazenar a quantidade de comparação
        # do algoritmo da força bruta
        iteracaoBF = 0
        # vetor das posições de substrings válidas
        ans = np.zeros((len(self.text)-len(self.pattern)+1))
        # inicia o algoritmo de força bruta, contando
        # cada if feito nele
        for i in range(len(self.text)-len(self.pattern)+1):
            for j in range(len(self.pattern)):
                iteracaoBF += 1
                if self.text[j+i] != self.pattern[j]:
                    ans[i] = 0
                    break
                else:
                    ans[i] = 1
                    iteracaoBF += 1
        # retorna o vetor com as posições e soma as comparações
        # a mais feitas.
        mostrar_matriz = np.where(ans > 0)
        return mostrar_matriz[0].astype(float), iteracaoBF + len(ans)

# classe que criamos para efetuar todo o 
# desenvolvimento da interface gráfica
# juntamente com a lógica do programa
class window():
    def __init__(self):
        root = tk.Tk()
        root.resizable('False', 'False')
        root['bg'] = bg
        root.title('Busca em DNA')

        titulo = tk.Label(root, text = '\nBusca DNA\nUtilizando o metodo KMP\n', bg = bg, font = cms)
        titulo.grid()

        main_frame = tk.Frame(root, bg = bg)
        main_frame.grid()

        text_label = tk.Label(main_frame, text = 'Sequencia aleatoria:', bg = bg, font = cms)
        self.text_entry = tk.Entry(main_frame, width = 25)
        text_label.grid(row = 1, column = 0, sticky = 'W', padx = 10)
        self.text_entry.grid(row = 2, column = 0, pady = 5, padx = 10, sticky = 'W')

        pattern_label = tk.Label(main_frame, text = 'Digite o DNA:', bg = bg, font = cms)
        self.pattern_entry = tk.Entry(main_frame, width = 25)
        pattern_label.grid(row = 1, column = 1, sticky = 'W', padx = 10)
        self.pattern_entry.grid(row = 2, column = 1, pady = 5, padx = 10)

        enter = tk.Button(main_frame, text = 'Buscar', bg = 'light gray', font = cms, command = self.search)
        enter.grid(row = 3, column = 1, sticky = 'E', padx = 10, pady = 10)

        obs = tk.Label(main_frame, text = '** Caracteres permitidos = A, C, G, T', bg = bg, fg = 'dark red',padx = 10, font = ('arial', 11, 'bold', 'italic'))
        obs.grid(row = 3, column = 0)

        root.mainloop()

    # função que vai validar a sequência de caracteres
    # digitados pelo usuário
    def valida(self, pattern):
        seq = ['A','C','G','T']
        c = 0
        for i in seq:
            c += pattern.count(i)
        return c == len(pattern)

    # funçao matriz, onde vamos utilizar para 
    # fazer o código funcionar, juntando com as 
    # outras funções
    def search(self):
        text = self.text_entry.get().upper().strip().replace(' ', '')
        pattern = self.pattern_entry.get().upper().strip().replace(' ', '')
        valido = self.valida(pattern) and self.valida(text)
        # condição que utilizamos a função valida onde vai
        # verificar se a cadeia digitada corresponde aos valores
        # existentes, e juntamente se for > 0 o tamanho dos 
        # caracteres inseridos, e o DNA digitado (pattern) não 
        # pode ser maior que a cadeia aleatória (text) que criamos
        try:
            self.root_final.destroy()
        except:
            if valido and len(pattern) > 0 and len(text) > 0 and len(pattern) <= len(text):
                algoritmos = Algoritmos(text, pattern)
                KMP = algoritmos.kmp()              
                BF = algoritmos.forcabruta()
                self.root_final = tk.Tk()
                self.root_final.resizable('False', 'False')
                self.root_final['bg'] = bg
                self.root_final.title('Resultado da busca')

                titulo = tk.Label(self.root_final, text = 'Resultado:\n', font = cms, bg = bg)
                titulo.grid()
                
                titulo = tk.Label(self.root_final, text = f'Quantidade de iterações\n --> KMP: {KMP[1]}\n--> BF: {BF[1]}', font = cms, bg = bg)
                titulo.grid()
                if len(KMP[0]) == 0:
                    titulo = tk.Label(self.root_final, text = f'Nenhum padrão encontrado.', font = cms, bg = bg)
                else:
                    titulo = tk.Label(self.root_final, text = f'Padrão encontrado em:\n --> KMP: {KMP[0]}', font = cms, bg = bg)
                    print('Força bruta: ', BF[0]) # para fins de comparação
                titulo.grid()
                if self.root_final.destroy:
                    self.root_final.mainloop()

window()
