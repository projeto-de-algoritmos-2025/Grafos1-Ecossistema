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
        "Decompositores": 6
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
        
        # Remove a espécie e adiciona à lista de extintas
        grafo.remove_node(atual)
        extintas.append(atual)
        
        # Verifica dependentes sem outras fontes de alimento
        for dep in dependentes:
            # Se não tem mais predecessores (fontes de energia), entra na fila
            if len(list(grafo.predecessors(dep))) == 0:
                fila.append(dep)
    
    print(f"Extinção em cascata: {extintas}")

def atualizar_energia(grafo, especie_extinta):
    # Reduz energia de dependentes diretos
    for dependente in grafo.predecessors(especie_extinta):
        if "energia" in grafo.nodes[dependente]:
            peso_perdido = grafo[dependente][especie_extinta]["weight"]
            grafo.nodes[dependente]["energia"] -= peso_perdido
            
            # Se energia <= 0, marca para extinção
            if grafo.nodes[dependente]["energia"] <= 0:
                extincao_cascata(grafo, dependente)

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
    plt.show(block=False)  # Não bloqueia a execução
    plt.pause(2)  # Exibe o gráfico por 2 segundos

# ----------------------------------------
# Novas Funções para Interação Avançada
# ----------------------------------------

def adicionar_especie(grafo):
    nome = input("Nome da nova espécie: ").strip()
    if nome in grafo.nodes():
        print(f"Erro: {nome} já existe!")
        return
    
    energia = int(input("Energia inicial (ex: 5): "))
    grafo.add_node(nome, energia=energia)
    
    # Conectar a outras espécies
    predecessores = input("Espécies que ela come (separadas por vírgula): ").split(",")
    for pred in predecessores:
        pred = pred.strip()
        if pred in grafo.nodes():
            peso = int(input(f"Peso de {pred} para {nome}: "))
            grafo.add_edge(pred, nome, weight=peso)
    
    sucessores = input("Espécies que a comem (separadas por vírgula): ").split(",")
    for suc in sucessores:
            suc = suc.strip()
            if suc in grafo.nodes():
                peso = int(input(f"Peso de {nome} para {suc}: "))
                grafo.add_edge(nome, suc, weight=peso)
    
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
                atualizar_energia(eco, especie)
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