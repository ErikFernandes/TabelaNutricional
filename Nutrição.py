import requests, sys, re
from bs4 import BeautifulSoup
import PySimpleGUI as sg

sg.theme("dark")

layout = [
    [sg.Text("Tabela Nutricional", expand_x=True, justification="center")],
    [sg.Text("Digite o Alimento:", expand_x=False, justification="left"),
     sg.Input(key="term", size=(40, 0), expand_x=False, justification="left"), sg.Button("Ok", key = "burcarTerm")],
    [sg.Output(size=(60, 20), key="out")],
    [sg.Text("Selecione uma opção", expand_x=True, justification="center")],
    [sg.Text("                                      "),
     sg.Input(size=(10, 0), expand_x=False, justification='center', key="opcaoEsc"), sg.Button("Ok", key="escolheOp")]

]

janela = sg.Window("", layout)



def Grafico():
    try:
        while True:


            evento, valores = janela.read()

            if evento == sg.WIN_CLOSED:
                break

            term = valores["term"]

            if evento == "burcarTerm":

                with requests.Session() as s:

                    requests.packages.urllib3.disable_warnings()
                    page = s.post(f'http://www.tabelanutricional.com.br/pesquisa/{term}')
                    soup = BeautifulSoup(page.text, 'html.parser')
                    divs = soup.find_all("li", class_="cat-item")
                    lista = {}
                    v = 0

                    janela["out"].update("")

                    for item in divs:
                        try:
                            lista[v] = item.a["href"]
                            print(v, item.text)
                            v = v + 1
                        except:
                            pass

                    if v == 0:
                        print('Nenhum resultado encontrado, confira a ortografica!')
                        Grafico()

            if evento == 'escolheOp':

                opcaoEsc = valores["opcaoEsc"]
                opcaoEsc = int(opcaoEsc)


                janela["out"].update("")

                alimento_seleci = lista[opcaoEsc]

                url = ('http://www.tabelanutricional.com.br' + alimento_seleci)
                page = s.post(url)
                soup = BeautifulSoup(page.text, 'html.parser')
                resultado = soup.find_all("div", id="response")
                tabela = {}

                janela["opcaoEsc"].update("")

                for item in resultado:
                    linhas = item.findAll("td")
                    print('Alimento selecionado: ', re.sub(r"[^A-Za-z]+", ' ', alimento_seleci).upper())
                    print('Nutrientes / Quantidade / % VD*')

                    for a, b, c in zip(*[iter(linhas)] * 3):
                        print(a.text + " / ", b.text + " / ", c.text)

    except:
        janela["out"].update("")
        janela["opcaoEsc"].update("")
        janela["term"].update("")
        print("Entrada inválida, digite o nome do alimente novamente...")
        Grafico()


        Grafico()
Grafico()