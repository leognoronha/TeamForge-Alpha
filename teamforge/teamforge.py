from itertools import combinations

# Base de freelancers fixa
freelancers = [
    {"nome": "Ana", "especializacao": "Back-end", "tecnologias": ["Node", "Express", "PostgreSQL", "Redis"], "custo": 800, "qualidade": 4.7},
    {"nome": "Bruno", "especializacao": "Back-end", "tecnologias": ["Node", "Express", "Python", "MongoDB"], "custo": 1000, "qualidade": 4.9},
    {"nome": "Clara", "especializacao": "Front-end", "tecnologias": ["React", "Javascript", "Tailwind CSS", "Vite"], "custo": 600, "qualidade": 4.5},
    {"nome": "Diego", "especializacao": "Front-end", "tecnologias": ["React", "Tailwind CSS", "Webhook"], "custo": 700, "qualidade": 4.8},
    {"nome": "Eva", "especializacao": "Design", "tecnologias": ["Figma", "Adobe XD"], "custo": 500, "qualidade": 4.6},
    {"nome": "Fernanda", "especializacao": "Design", "tecnologias": ["Figma", "Adobe XD", "Sketch"], "custo": 600, "qualidade": 4.8},
    {"nome": "Carol", "especializacao": "Design", "tecnologias": ["Figma", "Adobe XD", "Illustrator"], "custo": 900, "qualidade": 4.9}
]

# Função para verificar compatibilidade de tecnologias
def verifica_tecnologias(freelancer, tecnologias_requeridas):
    return all(tecnologia in freelancer["tecnologias"] for tecnologia in tecnologias_requeridas)

# Função para simular equipes com flexibilidade total
def simular_equipes(projeto, freelancers_disponiveis, fixos=None):
    equipes = []
    candidatos = {}
    
    # Verifica se há freelancers suficientes e cria candidatos por especialização
    for requisito in projeto["requisitos"]:
        especializacao = requisito["especializacao"]
        quantidade = requisito["quantidade"]
        candidatos_validos = [
            freelancer for freelancer in freelancers_disponiveis 
            if freelancer["especializacao"] == especializacao and verifica_tecnologias(freelancer, requisito["tecnologias"])
        ]
        if len(candidatos_validos) < quantidade:
            return None  # Retorna None se não houver freelancers suficientes
        candidatos[especializacao] = list(combinations(candidatos_validos, quantidade))

    # Função recursiva para combinar todas as especializações dinamicamente
    def combinar_combinacoes(combinacoes, index=0, equipe_atual=[]):
        if index == len(projeto["requisitos"]):
            if equipe_atual:  # Só calcula se equipe_atual não estiver vazia
                custo_total = sum(freelancer["custo"] for freelancer in equipe_atual)
                if custo_total <= projeto["orcamento"]:
                    qualidade_media = sum(freelancer["qualidade"] for freelancer in equipe_atual) / len(equipe_atual)
                    equipe_dict = {"equipe": equipe_atual[:], "custo": custo_total, "qualidade": qualidade_media}
                    if fixos:
                        nomes_equipe = [membro["nome"] for membro in equipe_atual]
                        if all(fixo["nome"] in nomes_equipe for fixo in fixos):
                            equipes.append(equipe_dict)
                    else:
                        equipes.append(equipe_dict)
            return
        
        especializacao = projeto["requisitos"][index]["especializacao"]
        for combo in candidatos[especializacao]:
            combinar_combinacoes(combinacoes, index + 1, equipe_atual + list(combo))

    # Inicia a combinação
    combinar_combinacoes(candidatos)
    return equipes

# Função para otimizar equipes com critério dinâmico
def otimizar_equipes(equipes, criterio):
    if criterio == "1":  # Menor Preço
        equipes.sort(key=lambda x: (x["custo"], -x["qualidade"]))
    elif criterio == "2":  # Melhor Qualidade
        equipes.sort(key=lambda x: (-x["qualidade"], x["custo"]))
    return equipes[:3] if len(equipes) >= 3 else equipes

# Função para exibir equipe
def exibir_equipe(equipe):
    print("\nEquipe:")
    for pessoa in equipe["equipe"]:
        print(f"{pessoa['nome']} ({pessoa['especializacao']}, Custo: R${pessoa['custo']}, Qualidade: {pessoa['qualidade']}/5, Tecnologias: {', '.join(pessoa['tecnologias'])})")
    print(f"Total: R${equipe['custo']}, Qualidade Média: {equipe['qualidade']:.2f}/5, Prazo: {projeto['prazo']} dias")

# Entrada de dados do projeto
print("=== TeamForge - Criação de Projeto ===")
nome_projeto = input("Nome do projeto: ")
orcamento = int(input("Orçamento (R$): "))
prazo = int(input("Prazo (dias): "))

# Escolha das especializações
print("\nQuais áreas vai precisar para o projeto?")
print("[1] Back-end, [2] Front-end, [3] Design")
areas_escolhidas = input("Digite os números das áreas (separadas por vírgula) :").split(",")

especializacoes = {"1": "Back-end", "2": "Front-end", "3": "Design"}
requisitos = []
for area in areas_escolhidas:
    area = area.strip()
    if area in especializacoes:
        especializacao = especializacoes[area]
        quantidade = int(input(f"Quantos {especializacao}? "))
        print(f"\nEspecialização: {especializacao}")
        tecnologias = input(f"Tecnologias necessárias (separadas por vírgula) : ").split(", ")
        requisitos.append({"especializacao": especializacao, "tecnologias": tecnologias, "quantidade": quantidade})

projeto = {"nome": nome_projeto, "requisitos": requisitos, "orcamento": orcamento, "prazo": prazo}

# Escolha do critério
print("\nQual Critério deseja seguir?")
print("[1] Menor Preço")
print("[2] Melhor Qualidade")
criterio = input("Escolha [1 ou 2]: ")

# Simulação inicial
equipes_viaveis = simular_equipes(projeto, freelancers)
if equipes_viaveis is None:
    print("\nNão foi possível realizar a busca: número de freelancers insuficiente para a especialização solicitada.")
else:
    sugestoes = otimizar_equipes(equipes_viaveis, criterio)
    if not sugestoes:
        print("\nNenhuma combinação viável encontrada com o orçamento e requisitos fornecidos.")
    else:
        print("\n=== Sugestões de Equipe ===")
        for i, equipe in enumerate(sugestoes, 1):
            print(f"\nSugestão {i}:")
            exibir_equipe(equipe)

        # Escolha da equipe
        while True:
            num_sugestoes = len(sugestoes)
            opcoes = [str(i) for i in range(1, num_sugestoes + 1)]
            escolha_prompt = f"Qual equipe deseja? [{', '.join(opcoes)}]: "
            escolha = input(f"\n{escolha_prompt}")
            
            if escolha in opcoes:
                equipe_escolhida = sugestoes[int(escolha) - 1]
                print(f"\nEquipe escolhida:")
                exibir_equipe(equipe_escolhida)
                
                if num_sugestoes == 1:
                    print("\nEsta é a única combinação possível.")
                    confirmar = input("Deseja confirmar esta equipe? [y/n]: ").lower()
                    if confirmar == "y":
                        print("\nEquipe confirmada!")
                        exibir_equipe(equipe_escolhida)
                        break
                    elif confirmar == "n":
                        print("\nSimulação encerrada sem confirmação.")
                        break
                    else:
                        print("Digite 'y' ou 'n'.")
                else:
                    editar = input("Deseja editar algum membro da equipe? [y/n]: ").lower()
                    if editar == "y":
                        print("\nMembros da equipe:")
                        nomes_membros = [membro["nome"] for membro in equipe_escolhida["equipe"]]
                        print(", ".join(nomes_membros))
                        membros_rejeitados = input("Digite os nomes de quem deseja remover (separados por vírgula): ").split(",")
                        membros_rejeitados = [nome.strip() for nome in membros_rejeitados]  # Remove espaços extras
                        
                        # Remove todos os rejeitados
                        equipe_fixa = [membro for membro in equipe_escolhida["equipe"] if membro["nome"] not in membros_rejeitados]
                        freelancers_disponiveis = [freelancer for freelancer in freelancers if freelancer["nome"] not in membros_rejeitados]
                        
                        equipes_viaveis = simular_equipes(projeto, freelancers_disponiveis, equipe_fixa)
                        if equipes_viaveis is None:
                            print("\nNão foi possível realizar a busca: número de freelancers insuficiente para a especialização solicitada após a rejeição.")
                            print("Retornando à equipe original.")
                            confirmar = input("Deseja confirmar esta equipe? [y/n]: ").lower()
                            if confirmar == "y":
                                print("\nEquipe confirmada!")
                                exibir_equipe(equipe_escolhida)
                                break
                            elif confirmar == "n":
                                print("\nSimulação encerrada sem confirmação.")
                                break
                            else:
                                print("Digite 'y' ou 'n'.")
                        else:
                            novas_sugestoes = otimizar_equipes(equipes_viaveis, criterio)
                            if not novas_sugestoes:
                                print("\nNenhuma combinação viável encontrada com o orçamento e requisitos fornecidos após a rejeição.")
                                print("Retornando à equipe original.")
                                confirmar = input("Deseja confirmar esta equipe? [y/n]: ").lower()
                                if confirmar == "y":
                                    print("\nEquipe confirmada!")
                                    exibir_equipe(equipe_escolhida)
                                    break
                                elif confirmar == "n":
                                    print("\nSimulação encerrada sem confirmação.")
                                    break
                                else:
                                    print("Digite 'y' ou 'n'.")
                            else:
                                print("\n=== Nova Sugestão ===")
                                for i, equipe in enumerate(novas_sugestoes, 1):
                                    print(f"\nSugestão {i}:")
                                    exibir_equipe(equipe)
                                sugestoes = novas_sugestoes
                    elif editar == "n":
                        print("\nEquipe confirmada!")
                        exibir_equipe(equipe_escolhida)
                        break
                    else:
                        print("Digite 'y' ou 'n'.")
            else:
                print(f"Digite um número entre {opcoes[0]} e {opcoes[-1]}.")