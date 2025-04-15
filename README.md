# Ecossistema

**Conteúdo da Disciplina**: Grafos1<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 222024579  |  Filipe Bressanelli |
| 200028626  |  Vitor Borges dos Santos |

## Sobre 
O projeto "Ecossistema" é uma simulação interativa de uma cadeia alimentar modelada como um grafo direcionado, utilizando a biblioteca NetworkX em Python. O objetivo é demonstrar conceitos de grafos, como nós (espécies), arestas (relações predador-presa) e propagação de efeitos em redes, visando assim mostrar como um ecossistema pode ser delicado e dinâmico.

## Screenshots
Adicione 3 ou mais screenshots do projeto em funcionamento.

## Instalação 
**Linguagem**: Python<br>
### Pré-requisitos:
* Python 3: Certifique-se de ter o Python instalado. Baixe em python.org se necessário.
* Bibliotecas: As dependências do projeto estão listadas no arquivo requirements.txt:
    * networkx: Para manipulação de grafos.
    * matplotlib: Para visualização gráfica.

### Passos para Instalação:
1. Clone ou baixe o repositório do projeto para sua máquina.
2. Navegue até o diretório do projeto:
```bash
    cd Grafos1-Ecossistema
```
3. Crie um ambiente virtual (opcional, mas recomendado):
```bash
    python -m venv env
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
```
4. Instale as dependências listadas no requirements.txt
```bash
    pip install -r requirements.txt
```

## Uso 
1. Execute o programa:
```bash
    python interativo.py
```
2. Siga o menu interativo:
* Digite 1 para extinguir uma espécie (ex.: "Coelhos").
* Digite 2 para adicionar uma nova espécie, informando nome, energia e conexões.
* Digite 3 para listar as espécies atuais.
* Digite 4 para visualizar o grafo (salvo como ecossistema.png no diretório atual).
* Digite 5 para sair.
