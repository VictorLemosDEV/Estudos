'''

Gostei bastante de desenvolver esse programa

Devo admitir que achei que ia demorar menos tempo, mas no meio do progresso comecei a implementar funcionalidades novas que não foram pedidas
Aprendi algumas coisas bem interessantes como a implementação de enums no python
também utilizei @classmethods que nunca havia utilizado antes

Usei também um map pro menu (algo que aprendi com desenvolvimento de jogos)

Conclusão: Foi um projeto divertido de escrever, e algumas coisas como a classe customizada de Input vai para o meu github Pessoal



'''

from enum import Enum # Para permitir enums no python

class Status(Enum):
    PENDENTE = 1
    SAIU_PARA_ENTREGA = 2
    ENTREGUE = 3


class Pedido:
    instancias = []

    def __init__(self, numero: int, cliente: str, endereco: str, valor: float, status: Status):
        try:
            if (status in Status): # Caso o status seja do tipo Status.ALGUMACOISA
                self.status = status.name
            else:
                Status[status] # Caso o Status seja do tipo PENDENTE, SAIU_PARA_ENTREGA OU ENTREEGUE
            
        except KeyError:
            raise TypeError("Status deve ter um valor válido")
        finally:
            self.status: Status = status

        self.numero = abs(numero)
        self.cliente = cliente
        self.endereco = endereco
        self.valor = valor

        Pedido.instancias.append(self)

    def __str__(self):
        return f"Pedido {self.numero}, Cliente: {self.cliente}, Endereço: {self.endereco}, Valor: {self.valor}, Status: {self.status.name}"



    @classmethod
    def get_by_numero(cls, numero):
        for pedido in cls.instancias:
            if pedido.numero == numero:
                return pedido
        return None


    # Retorna todos os pedidos existentes
    @classmethod
    def get_instances(cls):
        return cls.instancias
    

        

        

class Entregador:
    instancias = []

    def __init__(self, nome: str, telefone: str, veiculo: str):
        self.nome = nome
        self.telefone = telefone
        self.veiculo = veiculo
        self.pedidos: list[Pedido] = []

        Entregador.instancias.append(self)

    def aceitar_pedido(self, pedido: Pedido):
        if pedido is None:
            return ValueError("Pedido deve ser válido")
        
        if pedido.status != Status.PENDENTE:
            return ValueError("Pedido não está pendente")
        
        if len(self.pedidos) >= 3:
            return IndexError("Máximo de pedidos que podem ser aceitos não pode exceder 3")
        
        pedido.status = Status.SAIU_PARA_ENTREGA
        self.pedidos.append(pedido)

    def finalizar_entrega(self, pedido: Pedido):
            if pedido is None or pedido not in self.pedidos:
                return ValueError("Pedido deve ser válido e deve estar na lista")
            
            pedido.status = Status.ENTREGUE
            self.pedidos = [x for x in self.pedidos if x.numero != pedido.numero]


    def __str__(self):
        return f"Nome: {self.nome}, Telefone: {self.telefone}, Veículo: {self.veiculo}, Pedidos: {[p.numero for p in self.pedidos]}"


    # Retorna o entregador pelo nome
    @classmethod
    def get_by_nome(cls, nome: str):
        for entregador in cls.instancias:
            if entregador.nome == nome:
                return entregador
        return None



    # Retorna todos os entregadores existentes
    @classmethod
    def get_instances(cls):
        return cls.instancias

class SistemaEntregas:
    def __init__(self):
        self.pedidos: list[Pedido] = []
        self.entregadores: list[Entregador] = []

    def resumo(self) -> dict:
        """Retorna um dicionário com total de pedidos, pedidos pendentes e pedidos entregues."""
        total = len(self.pedidos)
        pendentes = len([p for p in self.pedidos if p.status == Status.PENDENTE])
        entregues = len([p for p in self.pedidos if p.status == Status.ENTREGUE])
        return {"total": total, "pendentes": pendentes, "entregues": entregues}


    
    def get_pedidos(self, status_pedido: Status = None) -> list[Pedido]:
        if status_pedido is not None:
            pedidos = [pedido for pedido in self.pedidos if (pedido.status == Status[status_pedido] if isinstance(status_pedido, str) else pedido.status == status_pedido)]
            return pedidos
        else:
            return self.pedidos

    def AtribuirPedidos(self, nomeEntregador=None, numeroDoPedido: int = None) -> None:
        if nomeEntregador is not None:
            if numeroDoPedido is None:
                for pedido in self.get_pedidos(Status.PENDENTE):
                    entregador = Entregador.get_by_nome(nomeEntregador)
                    if entregador:
                        entregador.aceitar_pedido(pedido)
            else:
                entregador = Entregador.get_by_nome(nomeEntregador)
                pedido = Pedido.get_by_numero(numeroDoPedido)
                if entregador and pedido:
                    entregador.aceitar_pedido(pedido)
            return

        # Modo automático: distribui pedidos pendentes para entregadores disponíveis
        pedidos_pendentes = self.get_pedidos(Status.PENDENTE)
        for pedido in pedidos_pendentes:
            for entregador in self.entregadores:
                if len(entregador.pedidos) < 3:
                    result = entregador.aceitar_pedido(pedido)
                    if not isinstance(result, Exception):
                        break
        

# InputClass


# Minha Implementação de uma classe customizada de Input com validação automática
class InputCustom:
    def __init__(self, *args):
        self.retries = 10 # Numero máximo de tentativas por input antes de cancelar o programa

        
        self.map = args
        self.results = []

    def from_inputs(self) -> list:
        for label in self.map:
            try:
                result = None
                if issubclass(label[0], str):
                    result = input(label[1])
                else:
                    if label[0] is Status:
                        entrada = input(label[1]).upper().replace(" ", "_")
                        # Tenta converter por nome, depois por valor
                        try:
                            result = Status[entrada]
                        except KeyError:
                            try:
                                result = Status(int(entrada))
                            except (ValueError, KeyError):
                                raise ValueError("Status inválido. Use o nome ou número do status.")
                    else:
                        result = label[0](input(label[1]))


                if result is not None:
                    self.retries = 10
                    self.results.append(result)
                    continue
            except (IndexError):
                while (self.retries > 0):
                    try:
                        if issubclass(label[0], str):
                            result = input(label[1])
                        else:
                            result = label[0](input(label[1]))
                            print(label[0], label[1], result)

                        


                        if result is not None:
                            self.results.append(result)
                    except (ValueError, TypeError):
                        self.retries -= 1
                        continue
                
                raise RecursionError("Máximo números de tentativas esgotadas!") # Se chegar nessa parte o usuário é um imbecil ou é um QA

        return self.results
           

# Menu Interativo

class Menu:

    @classmethod
    def AdicionarPedido(cls):
        max_retries = 3
        attempts = 0
        while attempts < max_retries:
            try:
                numero = InputCustom((int, "Número do Pedido: ")).from_inputs()[0]
            except Exception:
                print(f"Número do pedido inválido. Tentativas restantes: {max_retries - attempts - 1}")
                attempts += 1
                continue

            # verifica unicidade
            if Pedido.get_by_numero(numero) is not None:
                print(f"Já existe um pedido com número {numero}. Tentativas restantes: {max_retries - attempts - 1}")
                attempts += 1
                continue

            # coleta os demais campos
            try:
                cliente, endereco, valor, status = InputCustom((str, "Nome do Cliente: "), (str, "Endereço: "), (float, "Valor: "), (Status, "Status do Pedido: ")).from_inputs()
            except Exception:
                print(f"Entrada inválida. Tentativas restantes: {max_retries - attempts - 1}")
                attempts += 1
                continue

            pedido = Pedido(numero, cliente, endereco, valor, status)
            sistema.pedidos.append(pedido)
            return

        print("Número máximo de tentativas atingido. Voltando ao menu principal.")

    
    @classmethod
    def AdicionarEntregador(cls) -> None:
        max_retries = 3
        attempts = 0
        while attempts < max_retries:
            try:
                nome = InputCustom((str, "Nome do Entregador: ")).from_inputs()[0]
            except Exception:
                print(f"Nome inválido. Tentativas restantes: {max_retries - attempts - 1}")
                attempts += 1
                continue

            if Entregador.get_by_nome(nome) is not None:
                print(f"Já existe um entregador com o nome '{nome}'. Tentativas restantes: {max_retries - attempts - 1}")
                attempts += 1
                continue

            try:
                telefone, veiculo = InputCustom((str, "Telefone do Entregador: "), (str, "Veículo do Entregador: ")).from_inputs()
            except Exception:
                print(f"Entrada inválida. Tentativas restantes: {max_retries - attempts - 1}")
                attempts += 1
                continue

            entregador = Entregador(nome, telefone, veiculo)
            sistema.entregadores.append(entregador)
            return

        print("Número máximo de tentativas atingido. Voltando ao menu principal.")

    @classmethod
    def ListarPedidosPendentes(cls) -> None:
        for pedido in sistema.get_pedidos("PENDENTE"):
            print(pedido)

    @classmethod
    def AtribuirPedidoAEntregador(cls) -> None:
        # Função auxiliar para tentar N vezes validar e atribuir
        def tentar_atribuir(max_retries: int = 3):
            attempts = 0
            while attempts < max_retries:
                entradas = InputCustom(
                    (str, "Nome do Entregador (Aperte ENTER PARA MODO AUTOMÁTICO):"),
                    (str, "Número do Pedido (Aperte ENTER PARA MODO AUTOMÁTICO):")
                ).from_inputs()
                nome = entradas[0] if entradas[0] != "" else None
                numero = int(entradas[1]) if entradas[1] != "" else None

                # Modo automático: delega ao sistema
                if nome is None and numero is None:
                    sistema.AtribuirPedidos()
                    return

                # Se só nome foi informado -> tenta atribuir qualquer pendente ao entregador
                entregador = Entregador.get_by_nome(nome) if nome is not None else None
                pedido = Pedido.get_by_numero(numero) if numero is not None else None

                # Validações
                if nome is not None and entregador is None:
                    print(f"Entregador '{nome}' não encontrado. Tentativas restantes: {max_retries - attempts - 1}")
                    attempts += 1
                    continue

                if numero is not None and pedido is None:
                    print(f"Pedido número {numero} não encontrado. Tentativas restantes: {max_retries - attempts - 1}")
                    attempts += 1
                    continue

                # Se pedido já saiu para entrega ou foi entregue
                if pedido is not None and pedido.status != Status.PENDENTE:
                    print(f"Pedido {pedido.numero} não está pendente (status: {pedido.status.name}). Tentativas restantes: {max_retries - attempts - 1}")
                    attempts += 1
                    continue

                # Se entregador informado e já lotado
                if entregador is not None and len(entregador.pedidos) >= 3:
                    print(f"Entregador '{entregador.nome}' já atingiu o limite de pedidos. Tentativas restantes: {max_retries - attempts - 1}")
                    attempts += 1
                    continue

                # Tudo ok -> chama sistema para atribuir (modo manual)
                sistema.AtribuirPedidos(nome, numero)
                return

            print("Número máximo de tentativas atingido. Voltando ao menu principal.")

        tentar_atribuir()
    
    @classmethod
    def FinalizarEntrega(cls):
        # Permitir várias tentativas ao fornecer dados inválidos
        max_retries = 3
        attempts = 0
        while attempts < max_retries:
            nome = input("Nome do Entregador: ")
            entregador = Entregador.get_by_nome(nome)
            if entregador is None:
                print(f"Entregador '{nome}' não encontrado. Tentativas restantes: {max_retries - attempts - 1}")
                attempts += 1
                continue

            try:
                numero_pedido = InputCustom((int, "Número do Pedido: ")).from_inputs()[0]
            except Exception:
                print(f"Entrada inválida para número do pedido. Tentativas restantes: {max_retries - attempts - 1}")
                attempts += 1
                continue

            pedido = Pedido.get_by_numero(numero_pedido)
            if pedido is None:
                print(f"Pedido número {numero_pedido} não encontrado. Tentativas restantes: {max_retries - attempts - 1}")
                attempts += 1
                continue

            # Verifica se o pedido está realmente com o entregador
            if pedido not in entregador.pedidos:
                print(f"Pedido {numero_pedido} não está atribuído ao entregador '{entregador.nome}'. Tentativas restantes: {max_retries - attempts - 1}")
                attempts += 1
                continue

            # Tudo ok -> finalizar
            entregador.finalizar_entrega(pedido)
            return

        print("Número máximo de tentativas atingido. Voltando ao menu principal.")
    @classmethod
    def Sair(cls):
        exit()

    @classmethod
    def ListarEntregadores(cls) -> None:
        for entregador in sistema.entregadores:
            print(entregador)

    @classmethod
    def MostrarResumo(cls) -> None:
        resumo = sistema.resumo()
        print(f"Total de pedidos: {resumo['total']}")
        print(f"Pedidos pendentes: {resumo['pendentes']}")
        print(f"Pedidos entregues: {resumo['entregues']}")


menu_interativo_map = {"1": Menu.AdicionarPedido,"2": Menu.AdicionarEntregador, "3": Menu.ListarPedidosPendentes,"4": Menu.ListarEntregadores, "5": Menu.AtribuirPedidoAEntregador, "6": Menu.FinalizarEntrega, "7": Menu.MostrarResumo, "8": Menu.Sair}




sistema = SistemaEntregas()


# Hardcoded entregadores e pedidos para testes
entregador1 = Entregador("João", "1111-1111", "Moto")
entregador2 = Entregador("Maria", "2222-2222", "Carro")
sistema.entregadores.extend([entregador1, entregador2])

pedido1 = Pedido(1, "Cliente A", "Rua 1", 50.0, Status.PENDENTE)
pedido2 = Pedido(2, "Cliente B", "Rua 2", 75.0, Status.PENDENTE)
pedido3 = Pedido(3, "Cliente C", "Rua 3", 100.0, Status.PENDENTE)
sistema.pedidos.extend([pedido1, pedido2, pedido3])

while (True):
    print("\n=== SISTEMA DE ENTREGAS ===")
    print("1. Adicionar pedido")
    print("2. Adicionar entregador")
    print("3. Listar pedidos pendentes")
    print("4. Listar entregadores")
    print("5. Atribuir pedido a entregador")
    print("6. Finalizar entrega")
    print("7. Mostrar resumo (totais)")
    print("8. Sair")

    escolha = input()[0]
    menu_interativo_map[escolha]()


