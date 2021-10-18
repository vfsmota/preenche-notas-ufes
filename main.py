# -*- coding: utf8


from selenium import webdriver

import click
import pandas as pd


URL = 'https://professor.ufes.br/'
NOTAS = URL + 'LancamentoNotas/index.jsp?todas=0&&menu=0'


def parse_turmas(form):
    turmas = {}
    for option in form.find_elements_by_tag_name('tr'):
        cols = option.find_elements_by_tag_name('td')
        if (len(cols) == 3):
            disc = cols[1].text
            #print(cols[1].text)
            link = option.find_elements_by_tag_name('a')
            #print(link[0].get_attribute('href'))
            turmas[disc] = link[0].get_attribute('href')

    return turmas

def pega_turma(turmas):
    while True:
        print()
        escolha_idx = print('Escolha uma turma:')
        escolhas = {}
        for i, turma in enumerate(sorted(turmas)):
            escolhas[str(i)] = turma
            print(i, ':', turma, sep='\t')

        escolha_idx = input()
        if escolha_idx not in escolhas:
            print('Turma inválida!')
        else:
            break

    nome_turma = escolhas[escolha_idx]
    valor_form = turmas[nome_turma]
    return valor_form

def parse_lancarNotas(form):
    link = form[1].find_elements_by_tag_name('a')
    #print(link[0].get_attribute('href'))
    return link[0].get_attribute('href')

@click.command()
@click.option('--usuario', prompt='Digite seu login')
@click.option('--senha', prompt='Digite sua senha', hide_input=True)
@click.argument('arquivo_notas')

def main(usuario, senha, arquivo_notas):

    print('Lendo o arquivo')
    try:
    #     # Lendo como string, mais seguro
        df = pd.read_csv(arquivo_notas, header=0, index_col=None, dtype=str, sep=';')
        df['Matricula'] = pd.to_numeric(df['Matricula'])
        df = df.set_index('Matricula')
        #df = df.sort_index()
        df = df.fillna('0')
        print(df)
    except Exception as e:
        print('Arquivo no formato errado.')
        print('CSV  deve seguir Matricula; Nota; Falta')
        raise e



    # Inicia selenium
    print('Iniciando selenium')
    driver = webdriver.Firefox()
    driver.get(URL)

    # Logando
    #username = driver.find_element_by_name('login')
    username = driver.find_element_by_xpath("//input[1]")
    password = driver.find_element_by_name('senha')

    username.send_keys(usuario)
    password.send_keys(senha)
    driver.find_element_by_xpath("//input[@type='submit']").click()

    # Vamos para a seleção de turma
    driver.get(NOTAS)

    #Pegar as turmas
    form_turma = driver.find_element_by_id("lista_turmas")
    turmas = parse_turmas(form_turma)
    escolha_turma = pega_turma(turmas)
    #print(escolha_turma)

    #Vai para o preenchimento das notas
    driver.get(escolha_turma)

    lancar = driver.find_elements_by_class_name("NoPrint")
    link = parse_lancarNotas(lancar)

    #Aqui vai lançar as notas propriamente
    driver.get(link)

    form_notas = driver.find_element_by_id("formulario")
    for aluno in form_notas.find_elements_by_tag_name('tr'):
        #print(aluno.text)
        matric = aluno.find_elements_by_class_name('matricula')
        if (len(matric) < 1):
            continue

        #removendo os parenteses da matricula no lançamento
        matric = matric[0].text[1:-1]

        notas = aluno.find_elements_by_tag_name('input')
        notaP = notas[1]
        faltaP = notas[2]

        notaDf = df.loc[int(matric)][0]
        notaP.send_keys(notaDf)
        faltaDf = df.loc[int(matric)][1]
        faltaP.send_keys(faltaDf)


    print('Antes de fechar o script, ', end='')
    print('verifique tudo e salve as notas no browser.')
    print('Depois, digite qq coisa aqui para terminar')
    input()
    try:
        driver.close()
    except:
        pass


if __name__ == '__main__':
    main()
