def validar_combinacao(pessoas, elementos_permitidos):
    print(f"Elementos permitidos: {elementos_permitidos}")
    elementos_coletados = set()
    
    for nome, elementos in pessoas.items():
        elementos_set = set(elementos)
        print(f"\nValidando {nome} com elementos: {elementos_set}")
        
        if not elementos_set:
            print(f"Erro: {nome} não possui elementos.")
            return False
        
        if not elementos_set.issubset(elementos_permitidos):
            print(f"Erro: {nome} possui elementos inválidos: {elementos_set - elementos_permitidos}")
            return False
        
        if len(elementos_set) == len(elementos_permitidos):
            print(f"Erro: {nome} possui todos os elementos permitidos. Não é permitido.")
            return False
        
        elementos_coletados.update(elementos_set)
        print(f"Elementos coletados até agora: {elementos_coletados}")
    
    if elementos_coletados == elementos_permitidos:
        print("\nTodos os elementos permitidos foram utilizados na combinação.")
        return True
    else:
        faltando = elementos_permitidos - elementos_coletados
        print(f"\nErro: Elementos faltando na combinação: {faltando}")
        return False


def obter_elementos_permitidos():
    while True:
        entrada = input("Elementos permitidos (separados por vírgula): ").strip().upper()
        elementos = {e.strip() for e in entrada.split(',') if e.strip()}
        
        if not elementos:
            print("Erro: Insira pelo menos um elemento.")
            continue
        
        print(f"Elementos permitidos definidos: {elementos}")
        return elementos


def obter_nome_pessoa(numero):
    while True:
        nome = input(f"Nome da pessoa {numero}: ").strip()
        if nome:
            return nome
        print("Erro: O nome não pode ser vazio.")


def obter_elementos_pessoa(nome, permitidos):
    while True:
        entrada = input(f"Elementos para {nome} ({', '.join(permitidos)}): ").strip().upper()
        elementos = [e.strip() for e in entrada.split(',') if e.strip()]
        
        if not elementos:
            print("Erro: Insira pelo menos um elemento.")
            continue
        
        invalidos = [e for e in elementos if e not in permitidos]
        if invalidos:
            print(f"Erro: Elementos inválidos: {', '.join(invalidos)}")
            continue
        
        print(f"Elementos registrados para {nome}: {elementos}")
        return elementos


def obter_numero_pessoas():
    while True:
        try:
            num_pessoas = int(input("Número de pessoas: "))
            if num_pessoas < 1:
                print("Erro: O número deve ser maior ou igual a 1.")
                continue
            return num_pessoas
        except ValueError:
            print("Erro: Insira um número válido.")


def main():
    elementos_permitidos = obter_elementos_permitidos()
    
    pessoas = {}
    num_pessoas = obter_numero_pessoas()
    
    for i in range(1, num_pessoas + 1):
        nome = obter_nome_pessoa(i)
        elementos = obter_elementos_pessoa(nome, elementos_permitidos)
        pessoas[nome] = elementos
    
    print("\nDados coletados:")
    for nome, elementos in pessoas.items():
        print(f"{nome}: {elementos}")
    
    valido = validar_combinacao(pessoas, elementos_permitidos)
    print("\nResultado final:", "VÁLIDO" if valido else "INVÁLIDO")


if __name__ == "__main__":
    main()
