# 📝 Estudos de Programação Orientada a Objetos

> Este repositório reúne anotações e exemplos práticos sobre conceitos de POO, com foco em Python.

---

## 📂 Arquivos

- **`vector.py`** Implementação de uma classe para vetores bidimensionais (`Vector`).  
  Inclui métodos para operações matemáticas e utilitárias.
- **`linked_list.py`** Implementação de uma lista encadeada (`LinkedList`).  
  Inclui métodos para manipulação dinâmica de elementos.
- **`sistemaentrega.py`** Implementação de um sistema simples de pedidos e entregas (classes `Pedido`, `Entregador`, `SistemaEntregas`).
- **`Dice.py`** Implementação de uma classe `Dice` para simular rolagens de dados no padrão RPG.  
  Suporta notações como `2d6+3` e rolagens com vantagem.

---

## ✅ Funcionalidades Implementadas

### 📐 Classe Vector

- [x] **Operações básicas:** Soma, subtração, multiplicação e divisão por escalar.
- [x] **Produto escalar:** Calcula o produto escalar entre dois vetores.
- [x] **Outras funções:** Cálculo de módulo, normalização, comparação, etc.
- [ ] **Produto vetorial:** Em desenvolvimento.

### 🔗 Classe LinkedList

- [x] **Lista encadeada:** Inserção, remoção, busca e iteração de elementos na lista encadeada.
- [X] **Outras operações de lista:** Verificação de tamanho, limpeza da lista, conversão para lista buit-in.

### 🎲 Classe Dice

- [x] **Análise de Notação RPG:** Interpreta strings como `2d8+5` usando expressões regulares.
- [x] **Rolagem Simples e Múltipla:** Executa rolagens de um ou múltiplos dados.
- [x] **Suporte a Vantagem:** Implementa a regra de vantagem (rolar múltiplos dados e pegar o maior) com a notação `#`.
- [x] **Criação Flexível:** Permite criar um dado a partir de uma `string` (`Dice("2d6")`) ou um `int` (`Dice(6)`).
- [x] **Métodos Uteis:** Uso de `__str__`, `__repr__`, `__call__` e `__add__` para uma interface mais intuitiva.

---

## ℹ️ Sobre

Este projeto serve como apoio aos estudos de Programação Orientada a Objetos, facilitando a compreensão de conceitos como encapsulamento, herança e polimorfismo através de exemplos práticos.