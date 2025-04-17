import networkx as nx
import matplotlib.pyplot as plt

# ----------------------------------------
# Configuração Inicial do Ecossistema
# ----------------------------------------

def criar_ecossistema():
    eco = nx.DiGraph()
    
    # Adiciona espécies e energia
    especies = {
        "Plantas": 10,
        "Coelhos": 5,
        "Lobos": 3,
        "Insetos": 4,
        "Sapos": 3,
        "Decompositores": 2,
        "Ratos": 2,
        "Aguias": 2
    }
    
    for especie, energia in especies.items():
        eco.add_node(especie, energia=energia)
    
    # Relações
    eco.add_edge("Plantas", "Coelhos", weight=3)
    eco.add_edge("Coelhos", "Lobos", weight=1)
    eco.add_edge("Plantas", "Insetos", weight=2)
    eco.add_edge("Insetos", "Sapos", weight=1)
    eco.add_edge("Decompositores", "Plantas", weight=2)
    eco.add_edge("Lobos", "Decompositores", weight=1)
    eco.add_edge("Coelhos", "Decompositores", weight=1)
    eco.add_edge("Sapos", "Decompositores", weight=1)
    eco.add_edge("Plantas", "Ratos", weight=1)
    eco.add_edge("Ratos", "Aguias", weight=2)
    eco.add_edge("Sapos", "Aguias", weight=1)
    
    return eco

# ----------------------------------------
# Funções de Extinção e Energia (já existentes)
# ----------------------------------------

def extincao_cascata(grafo, especie_alvo):
    if especie_alvo not in grafo:
        return
    
    fila = [especie_alvo]
    extintas = []
    
    while fila:
        atual = fila.pop(0)
        if atual not in grafo:
            continue
        
        # Coleta dependentes antes de remover o nó
        dependentes = list(grafo.successors(atual))
        atualizar_energia(grafo, atual)
        # Remove a espécie e adiciona à lista de extintas
        grafo.remove_node(atual)
        extintas.append(atual)
        
        # Verifica dependentes sem outras fontes de alimento
        for dep in dependentes:
            # Se não tem mais predecessores (fontes de energia), entra na fila
            if len(list(grafo.predecessors(dep))) == 0 or grafo.nodes[dep]["energia"] <= 0:
                fila.append(dep)
    
    print(f"Extinção em cascata: {extintas}")

def atualizar_energia(grafo, especie_extinta):
    dependentes_extintos = []
    # Reduz energia de dependentes diretos
    for dependente in grafo.successors(especie_extinta):
        if "energia" in grafo.nodes[dependente]:
            peso_perdido = grafo[especie_extinta][dependente]["weight"]
            
            grafo.nodes[dependente]["energia"] -= peso_perdido
            # Se energia <= 0, marca para extinção
            if grafo.nodes[dependente]["energia"] <= 0:
                dependentes_extintos.append(dependente)

# ----------------------------------------
# Função de Visualização
# ----------------------------------------

def plot_ecossistema(grafo):
    plt.close('all')  # Fecha gráficos anteriores
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(grafo, seed=42)
    cores = [grafo.nodes[nodo].get('energia', 1) for nodo in grafo.nodes()]
    
    nx.draw(
        grafo, pos, 
        with_labels=True, 
        node_color=cores, 
        cmap=plt.cm.Greens, 
        node_size=2000,
        arrows=True
    )
    
    edge_labels = nx.get_edge_attributes(grafo, "weight")
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels)
    plt.savefig("ecossistema.png")
    # plt.show() so deve ser utilizado em ambientes interativos
    # plt.show(block=False)  # Não bloqueia a execução
    # plt.pause(2)  # Exibe o gráfico por 2 segundos

# ----------------------------------------
# Novas Funções para Interação Avançada
# ----------------------------------------

def adicionar_especie(grafo):
    # Solicitar nome único para a nova espécie
    while True:
        nome = input("Nome da nova espécie: ").strip()
        if nome not in grafo.nodes():
            break
        print(f"Erro: {nome} já existe! Tente novamente.")
    
    # Solicitar energia inicial com validação
    while True:
        try:
            energia = int(input("Energia inicial (ex: 5): "))
            if energia >= 0:  # Garantir que a energia não seja negativa
                break
            print("Erro: A energia deve ser um número inteiro não negativo.")
        except ValueError:
            print("Erro: Insira um número inteiro para a energia.")
    
    # Adicionar o nó ao grafo
    grafo.add_node(nome, energia=energia)
    
    # Mostrar espécies existentes para referência
    print("\nEspécies existentes:", list(grafo.nodes()))
    
    # Adicionar predecessores (espécies que ela come)
    while True:
        pred_input = input("Espécies que ela come (separadas por vírgula, ou 'fim' para terminar): ").strip()
        if pred_input.lower() == 'fim':
            break
        if not pred_input:  # Caso o usuário pressione Enter sem digitar nada
            break
        predecessores = pred_input.split(",")
        for pred in predecessores:
            pred = pred.strip()
            if pred in grafo.nodes():
                while True:
                    try:
                        peso = int(input(f"Peso de {pred} para {nome}: "))
                        if peso > 0:  # Garantir peso positivo
                            grafo.add_edge(pred, nome, weight=peso)
                            break
                        print("Erro: O peso deve ser um número inteiro positivo.")
                    except ValueError:
                        print("Erro: Insira um número inteiro para o peso.")
            else:
                print(f"Aviso: {pred} não encontrada no ecossistema.")
    
    # Adicionar sucessores (espécies que a comem)
    while True:
        suc_input = input("Espécies que a comem (separadas por vírgula, ou 'fim' para terminar): ").strip()
        if suc_input.lower() == 'fim':
            break
        if not suc_input:  # Caso o usuário pressione Enter sem digitar nada
            break
        sucessores = suc_input.split(",")
        for suc in sucessores:
            suc = suc.strip()
            if suc in grafo.nodes():
                while True:
                    try:
                        peso = int(input(f"Peso de {nome} para {suc}: "))
                        if peso > 0:  # Garantir peso positivo
                            grafo.add_edge(nome, suc, weight=peso)
                            break
                        print("Erro: O peso deve ser um número inteiro positivo.")
                    except ValueError:
                        print("Erro: Insira um número inteiro para o peso.")
            else:
                print(f"Aviso: {suc} não encontrada no ecossistema.")
    
    print(f"{nome} adicionada com sucesso!")

# ----------------------------------------
# Loop Principal com Menu
# ----------------------------------------

def main():
    eco = criar_ecossistema()

    while True:
        print("\n=== Menu ===")
        print("1. Extinguir espécie")
        print("2. Adicionar espécie")
        print("3. Listar espécies")
        print("4. Visualizar ecossistema")
        print("5. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            especie = input("Espécie a extinguir: ").strip()
            if especie in eco.nodes():
                extincao_cascata(eco, especie)
            else:
                print("Espécie não encontrada!")
        
        elif opcao == "2":
            adicionar_especie(eco)
        
        elif opcao == "3":
            print("\nEspécies existentes:", list(eco.nodes()))
        
        elif opcao == "4":
            plot_ecossistema(eco)
        
        elif opcao == "5":
            break
        
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()