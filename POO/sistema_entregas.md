# Sistema de Entregas

Documentação do sistema de pedidos e entregas implementado em `sistemaentrega.py`.

## Visão geral

O sistema é composto por três classes principais:

- Pedido
  - Atributos: `numero` (int), `cliente` (str), `endereco` (str), `valor` (float), `status` (enum: PENDENTE, SAIU_PARA_ENTREGA, ENTREGUE)
- Entregador
  - Atributos: `nome` (str), `telefone` (str), `veiculo` (str), `pedidos` (list[Pedido]) — pedidos atualmente atribuídos ao entregador
  - Regras: cada entregador pode ter no máximo 3 pedidos ao mesmo tempo
- SistemaEntregas
  - Atributos: `pedidos` (list[Pedido]), `entregadores` (list[Entregador])
  - Métodos principais: atribuir pedidos automaticamente, listar pedidos por status, resumo (total/pendentes/entregues)


## Regras e validações importantes

- Um `Pedido` só pode ser aceito por um entregador se seu `status` for `PENDENTE`.
- Quando um entregador aceita um pedido, o pedido passa para `SAIU_PARA_ENTREGA`.
- Um entregador não pode ter mais que 3 pedidos simultâneos; tentativas adicionais são rejeitadas.
- Ao finalizar a entrega, o pedido passa para `ENTREGUE` e é removido da lista de pedidos do entregador.


## API (resumo das classes)

### Classe Pedido
Construtor: `Pedido(numero: int, cliente: str, endereco: str, valor: float, status: Status)`

Métodos utilitários:
- `Pedido.get_by_numero(numero)` — retorna instância ou `None`
- `Pedido.get_instances()` — lista de todas as instâncias criadas (uso interno)

### Classe Entregador
Construtor: `Entregador(nome: str, telefone: str, veiculo: str)`

Métodos:
- `aceitar_pedido(pedido: Pedido)` — valida e altera status do pedido para `SAIU_PARA_ENTREGA`; adiciona à lista `pedidos` do entregador
- `finalizar_entrega(pedido: Pedido)` — marca `ENTREGUE` e remove da lista do entregador
- `Entregador.get_by_nome(nome)` — busca por nome
- `Entregador.get_instances()` — lista de todas as instâncias (uso interno)

### Classe SistemaEntregas
Construtor: `SistemaEntregas()` — mantém listas `pedidos` e `entregadores`

Métodos:
- `resumo()` — retorna um dicionário com chaves: `total`, `pendentes`, `entregues`
- `get_pedidos(status_pedido: Status|str = None)` — retorna pedidos filtrados por status ou todos
- `AtribuirPedidos(nomeEntregador=None, numeroDoPedido=None)` — modo manual (quando `nomeEntregador` informado) ou automático (sem argumentos). No modo automático distribui pedidos pendentes para entregadores disponíveis (respeita limite de 3 pedidos por entregador).


## Menu interativo

O arquivo `sistemaentrega.py` contém um menu interativo (classe `Menu`) para:

- Adicionar pedido
- Adicionar entregador
- Atribuir pedidos (manual ou automático)
- Finalizar entrega
- Visualizar resumo

A implementação do menu inclui validações e *retries* (tentativas limitadas) para entradas inválidas ou tentativas de operações inválidas (por exemplo: atribuir um pedido que já saiu para entrega, usar nome de entregador inexistente, etc.).


## Exemplos rápidos de uso (interpretação/execução)

1) Usando interativamente

- Rode o script `sistemaentrega.py` com Python 3.10+ e siga as instruções do menu para criar pedidos e entregadores e realizar atribuições.

2) Usando como módulo (exemplo mínimo):

```python
from sistemaentrega import Pedido, Entregador, SistemaEntregas, Status

sistema = SistemaEntregas()
# Criar entregadores e pedidos
e1 = Entregador('Ana', '1111-2222', 'Moto')
p1 = Pedido(1, 'Cliente A', 'Rua 1', 50.0, Status.PENDENTE)

sistema.entregadores.append(e1)
sistema.pedidos.append(p1)

# Atribuir automaticamente
sistema.AtribuirPedidos()
print(e1.pedidos)  # deverá conter p1 se tudo ok

# Resumo
print(sistema.resumo())
```


## Testes rápidos

- Tente atribuir um pedido já com status `SAIU_PARA_ENTREGA` — o sistema deverá recusar e, nas rotinas de menu, permitir novas tentativas até o limite.
- Crie 4 pedidos e tente atribuí-los ao mesmo entregador — o 4º deverá ser recusado (limite 3).


## Como contribuir / próximos passos

- Melhorar a interface (ex.: adicionar um CLI com argparse ou uma interface web simples).
- Persistência: armazenar pedidos/entregadores em arquivo JSON ou banco de dados pequeno para manter estado entre execuções.
- Adicionar testes unitários para cobrir as regras de negócio (aceitação de pedido, limite de entregas, resumo).


---

Arquivo: `POO/sistema_entregas.md` gerado automaticamente.
