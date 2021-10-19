# Preenche notas Portal-Professor-UFES

Script que preenche as notas automagicamente. Precisa de Selenium + GeckoDriver para funcionar.

Script baseado em um fork do [preenche-Minha-UFMG](https://github.com/flaviovdf/preenche-notas-ufmg) desenvolvido pelo Prof. Flávio Figueiredo.


## Dependências

1. Firefox, deve ter em qualquer distribuição linux. Em outros sistemas instale o Firefox.
1. [selenium](https://selenium-python.readthedocs.io)
1. [gecko-driver](https://github.com/mozilla/geckodriver/)
1. [pandas](https://pandas.pydata.org)
1. [click](https://click.palletsprojects.com)


### Instalando o GeckoDriver no Linux

Execute as linhas abaixo como root. Caso prefira, mude os comandos para instalar em um outro local.

Caso esteja em outro sistema operacional, instale o gecko-driver manualmente.

```bash
LATEST=`wget -O - https://github.com/mozilla/geckodriver/releases/latest 2>&1 | grep "Location:" | grep --only-match -e "v[0-9\.]\+"`
wget "https://github.com/mozilla/geckodriver/releases/download/${LATEST}/geckodriver-${LATEST}-linux64.tar.gz"
tar -x geckodriver -zf geckodriver-${LATEST}-linux64.tar.gz -O > /usr/local/bin/geckodriver
chmod +x /usr/local/bin/geckodriver
```

### Instalando as dependências

```bash
pip install selenium pandas click
```


## Como utilizar

Basta rodar:

```
python main.py -h
```

Para ver as opções. O vídeo abaixo mostra um exemplo de uso.

Sempre mantenha um terminal aberto. O mesmo vai perguntar para você qual é a turma, veja o vídeo abaixo.
O vídeo é da minha-UFMG mas a sequencia de comandos se aplica para o portal do professor-UFES.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/Z7yhH-4r8YI/0.jpg)](https://www.youtube.com/watch?v=Z7yhH-4r8YI)


## Formato dos Dados

Como entrada, basta passar um csv que contenha um cabeçalho com matrícula, nota e falta,separado por ;
**A ideia aqui é que o: excell, google-sheets, \*-office, todos permitem salvar planilhas como csv**

```
Matricula;nota;falta
```
## Responsabilidades

Use por sua conta e risco. Verifique as notas antes de salvar de enviar definitivamente.

Vale lembrar que qualquer manutenção no portal do professor pode fazer o script quebrar.

Esse script **não tem** garantias de manutenção e nem suporte. Siga as instruções e seja feliz!

## Known issues

- Não apresenta mais de uma turma de um mesmo curso. Solução atual: Encerrar o lançamento de notas da turma após preenchimento. @ricardocmello
- Exception  em caso de aluno na tabela de frequência no portal não constar no CSV. Solução atual: ter todos os alunos no CSV ou terminar o preenchimento manualmente após crash.
