from itertools import product, combinations

# Base de freelancers fixa
freelancers_disponiveis = [
    {"nome": "Ana", "especializacao": "Back-end", "tecnologias": ["Node", "Express", "PostgreSQL", "Redis"], "custo": 800, "qualidade": 4.7},
    {"nome": "Bruno", "especializacao": "Back-end", "tecnologias": ["Node", "Express", "Python", "MongoDB"], "custo": 1000, "qualidade": 4.9},
    {"nome": "Clara", "especializacao": "Front-end", "tecnologias": ["React", "Javascript", "Tailwind CSS", "Vite"], "custo": 600, "qualidade": 4.5},
    {"nome": "Diego", "especializacao": "Front-end", "tecnologias": ["React", "Tailwind CSS", "Webhook"], "custo": 700, "qualidade": 4.8},
    {"nome": "Eva", "especializacao": "Design", "tecnologias": ["Figma", "Adobe XD"], "custo": 500, "qualidade": 4.6},
    {"nome": "Fernanda", "especializacao": "Design", "tecnologias": ["Figma", "Adobe XD", "Sketch"], "custo": 600, "qualidade": 4.8},
    {"nome": "Carol", "especializacao": "Design", "tecnologias": ["Figma", "Adobe XD", "Illustrator"], "custo": 900, "qualidade": 4.9}
]

# Definindo critérios de otimização
CRITERIO_CUSTO = 1
CRITERIO_QUALIDADE = 2

def gerar_combinacoes_especializacao(combinacoes_por_especializacao):
    """
    Gera todas as combinações possíveis entre as especializações necessárias para o projeto.

    Utiliza o método `product` da biblioteca `itertools` para criar um produto cartesiano das combinações de freelancers previamente filtrados por especialização, permitindo a formação de equipes completas.Por exemplo, se houver 2 combinações de Back-end e 2 de Front-end, o resultado será um iterador com 2 x 2 = 2 combinações totais.

    Args:combinacoes_por_especializacao (dict): Dicionário onde as chaves são especializações (ex.: "Back-end") e os valores são listas de combinações de freelancers válidos para cada especialização.

    Returns:iterator: Um iterador contendo todas as combinações possíveis entre as especializações fornecidas. Cada iteração retorna uma tupla contendo uma combinação única de grupos de freelancers, uma especialização por vez.
    """
    return product(*combinacoes_por_especializacao.values())

def simular_equipes(projeto, freelancers_disponiveis, membros_fixos=None):
    """
    Simula equipes viáveis para um projeto com base nos requisitos, orçamento e membros fixos.

    Filtra freelancers disponíveis por especialização e tecnologias exigidas, gera combinações possíveis e retorna equipes que respeitem o orçamento e incluam membros fixos, se especificados. Retorna None se não houver freelancers suficientes para atender a quantidade solicitada.

    Args:projeto (dict): Dicionário com informações do projeto, incluindo "requisitos" (lista de dicionários com "especializacao", "tecnologias" e "quantidade") e "orcamento". freelancers_disponiveis (list): Lista de dicionários com dados dos freelancers disponíveis (nome, especialização, tecnologias, custo, qualidade). membros_fixos (list, opcional): Lista de dicionários dos freelancers que devem obrigatoriamente estar na equipe. Default é None.

    Returns: list or None: Lista de equipes viáveis, onde cada equipe é um dicionário com "equipe" (lista de membros), "custo" (int) e "qualidade" (float). Retorna None se a simulação for inviável.
    """
    equipes_viaveis = []
    combinacoes_por_especializacao = {}
    
    for requisito in projeto["requisitos"]:
        especializacao = requisito["especializacao"]
        quantidade_necessaria = requisito["quantidade"]
        
        # Filtra freelancers válidos para a especialização
        candidatos_validos = [
            freelancer for freelancer in freelancers_disponiveis 
            if freelancer["especializacao"] == especializacao and 
            set(requisito["tecnologias"]).issubset(freelancer["tecnologias"])
        ]
        if len(candidatos_validos) < quantidade_necessaria:
            return None
        
        combinacoes_por_especializacao[especializacao] = list(combinations(candidatos_validos, quantidade_necessaria))
    
    # Gera todas as combinações entre especializações
    for combinacao_especializacao in gerar_combinacoes_especializacao(combinacoes_por_especializacao):
        membros_equipe = [membro for grupo in combinacao_especializacao for membro in grupo]
        custo_total = sum(membro["custo"] for membro in membros_equipe)
        
        if custo_total > projeto["orcamento"]:
            continue
        
        # Verifica membros fixos obrigatórios
        if membros_fixos and not all(membro_fixo in membros_equipe for membro_fixo in membros_fixos):
            continue
        
        qualidade_media = sum(membro["qualidade"] for membro in membros_equipe) / len(membros_equipe)
        equipes_viaveis.append({
            "equipe": membros_equipe,
            "custo": custo_total,
            "qualidade": round(qualidade_media, 2)
        })
    
    return equipes_viaveis

def otimizar_equipes(equipes_viaveis, criterio):
    """
    Ordena as equipes viáveis com base no critério de otimização escolhido e retorna até 3 melhores opções.

    Suporta dois critérios: CRITERIO_CUSTO (ordena por custo crescente, qualidade decrescente como desempate) e CRITERIO_QUALIDADE (ordena por qualidade decrescente, custo crescente como desempate).

    Args: equipes_viaveis (list): Lista de dicionários com informações das equipes (equipe, custo, qualidade). criterio (int): Critério de otimização (CRITERIO_CUSTO ou CRITERIO_QUALIDADE).

    Returns: list: Lista ordenada com até 3 equipes, mantendo o formato original dos dicionários.
    """
    if criterio == CRITERIO_CUSTO:
        equipes_viaveis.sort(key=lambda equipe: (equipe["custo"], -equipe["qualidade"]))
    elif criterio == CRITERIO_QUALIDADE:
        equipes_viaveis.sort(key=lambda equipe: (-equipe["qualidade"], equipe["custo"]))
    return equipes_viaveis[:3] if len(equipes_viaveis) >= 3 else equipes_viaveis

def exibir_equipe(detalhes_equipe):
    """
    Exibe os detalhes completos de uma equipe no terminal de forma formatada.
    Mostra informações de cada membro (nome, especialização, custo, qualidade, tecnologias) e os totais
    da equipe (custo total, qualidade média, prazo do projeto).
    Args: detalhes_equipe (dict): Dicionário com "equipe" (lista de membros), "custo" (int) e "qualidade" (float).
    """
    print("\nEquipe:")
    for membro in detalhes_equipe["equipe"]:
        print(f"{membro['nome']} ({membro['especializacao']}, Custo: R${membro['custo']}, " +
              f"Qualidade: {membro['qualidade']}/5, Tecnologias: {', '.join(membro['tecnologias'])})")
    print(f"Total: R${detalhes_equipe['custo']}, Qualidade Média: {detalhes_equipe['qualidade']:.2f}/5, " +
          f"Prazo: {projeto['prazo']} dias")

def validar_entrada_numerica(mensagem, valor_minimo=1):
    """
    Valida e retorna uma entrada numérica do usuário, garantindo que seja um inteiro válido e >= valor_minimo.

    Solicita repetidamente até que uma entrada válida seja fornecida, tratando exceções de conversão e valores inválidos.
    
    Args: mensagem (str): Texto exibido para solicitar a entrada do usuário valor_minimo (int, opcional): Valor mínimo aceitável para a entrada. Default é 1.

    Returns: int: O valor numérico validado fornecido pelo usuário.
    """
    while True:
        try:
            valor = int(input(mensagem))
            return valor if valor >= valor_minimo else print(f"Valor deve ser ≥ {valor_minimo}")
        except ValueError:
            print("Erro: Insira um número válido.")

# Interface principal
print("=== TeamForge - Criação de Projeto ===")
nome_projeto = input("Nome do projeto: ")
orcamento = validar_entrada_numerica("Orçamento (R$): ")
prazo = validar_entrada_numerica("Prazo (dias): ")

# Seleção de especializações
print("\nSelecione as áreas necessárias:")
print("[1] Back-end, [2] Front-end, [3] Design")
codigos_areas = input("Digite os números das áreas (separados por vírgula): ").split(",")

mapeamento_especializacoes = {"1": "Back-end", "2": "Front-end", "3": "Design"}
requisitos_projeto = []
for codigo in codigos_areas:
    codigo = codigo.strip()
    if codigo in mapeamento_especializacoes:
        especializacao = mapeamento_especializacoes[codigo]
        quantidade = validar_entrada_numerica(f"Quantos {especializacao}? ")
        tecnologias = input(f"Tecnologias necessárias para {especializacao} (separadas por vírgula): ").split(", ")
        requisitos_projeto.append({
            "especializacao": especializacao,
            "tecnologias": [tech.strip() for tech in tecnologias],
            "quantidade": quantidade
        })

projeto = {
    "nome": nome_projeto,
    "requisitos": requisitos_projeto,
    "orcamento": orcamento,
    "prazo": prazo
}

# Seleção de critério de otimização
print("\nCritério de otimização:")
print("[1] Menor Custo")
print("[2] Melhor Qualidade")
while True:
    try:
        criterio_otimizacao = int(input("Escolha (1/2): "))
        if criterio_otimizacao in [CRITERIO_CUSTO, CRITERIO_QUALIDADE]:
            break
        else:
            print("Opção inválida. Escolha 1 ou 2.")
    except ValueError:
        print("Erro: Digite um número válido.")

# Processamento inicial
equipes_viaveis = simular_equipes(projeto, freelancers_disponiveis)
if not equipes_viaveis:
    print("\nNão foi possível formar equipes com os requisitos fornecidos.")
else:
    sugestoes = otimizar_equipes(equipes_viaveis, criterio_otimizacao)
    print("\n=== Sugestões de Equipe ===")
    for indice, sugestao in enumerate(sugestoes, 1):
        print(f"\nSugestão {indice}:")
        exibir_equipe(sugestao)

    # Seleção e ajuste da equipe
    while True:
        opcoes_validas = [str(numero) for numero in range(1, len(sugestoes) + 1)]
        escolha_equipe = input(f"\nEscolha uma equipe [{', '.join(opcoes_validas)}]: ")
        
        if escolha_equipe not in opcoes_validas:
            print(f"Opção inválida! Digite entre {opcoes_validas[0]} e {opcoes_validas[-1]}")
            continue
            
        equipe_selecionada = sugestoes[int(escolha_equipe) - 1]
        exibir_equipe(equipe_selecionada)
        
        if input("\nDeseja ajustar esta equipe? (s/n): ").lower() == "s":
            nomes_rejeitados = input("Nomes para remover (separados por vírgula): ").split(",")
            nomes_rejeitados = [nome.strip() for nome in nomes_rejeitados]
            
            # Atualiza lista de freelancers disponíveis
            freelancers_disponiveis = [freelancer for freelancer in freelancers_disponiveis if freelancer["nome"] not in nomes_rejeitados]
            membros_fixos = [membro for membro in equipe_selecionada["equipe"] if membro["nome"] not in nomes_rejeitados]
            
            novas_equipes = simular_equipes(projeto, freelancers_disponiveis, membros_fixos)
            if novas_equipes:
                sugestoes = otimizar_equipes(novas_equipes, criterio_otimizacao)
                print("\n=== Novas Sugestões ===")
                for indice, sugestao in enumerate(sugestoes, 1):
                    print(f"\nSugestão {indice}:")
                    exibir_equipe(sugestao)
            else:
                print("\nNão há outras combinações possíveis com os membros restantes.")
                confirmar = input("Deseja manter a equipe atual? (s/n): ").lower()
                if confirmar == "s":
                    print("\nEquipe confirmada com sucesso!")
                    print("\n=== EQUIPE FINAL ===")
                    exibir_equipe(equipe_selecionada)
                    break
                else:
                    print("\nSimulação encerrada sem confirmação.")
                    break
        else:
            print("\nEquipe confirmada com sucesso!")
            break