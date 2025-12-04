from typing import Any, List, Dict,Tuple,Callable, Union, TypeAlias, ReadOnly
from time import sleep
import os

ActionFunction: TypeAlias = Callable[..., str | None]
Escolha: TypeAlias = Tuple[str, Tuple[ActionFunction, List[Any]]]

# Define a estrutura do único diálogo
# Dialogue é uma Tupla contendo 3 elementos
# 1. str: O texto principal do diálogo.
# 2. str | None: O ID do próximo diálogo na sequência (str) ou None se este for o final da sequência.
# 3. List[Choice]: A lista de opções de escolha para o usuário
Dialogue: TypeAlias = Tuple[str, str | None, List[Escolha]]



class DialogueManager:
    _instance = None
    
    dialogues: Dict[str, Dialogue] = {}
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DialogueManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        
    def _addDialogue(cls, id: str,content: str, nextDialogue: str | None=None, options: List[Escolha] = []):
        if cls.dialogues.get(id, None):
            return
        
        cls.dialogues[id] = (content, nextDialogue, options)
        
    def limpar_terminal(self):
        
        comando = 'cls' if os.name == 'nt' else 'clear'
        os.system(comando)
        
    def showDialogue(self, dialogueId: str):
        dialogue: Dialogue = self.dialogues.get(dialogueId, None)
        
        if not dialogue:
            return
        
        self.limpar_terminal()
        if dialogue[0]:
            for char in dialogue[0]:
                print(char,end="",flush=True)
                sleep(0.05)
            
        
            
        print("\n")
        
        next_id_from_action: str | None = None
        
        options = dialogue[2]
        if options:
            print("--- Escolha uma opção: ---")
            for i, (text, _) in enumerate(options):
                print(f"[{i + 1}] {text}")
                
            while True:
                try:
                    choice_index = int(input("Sua escolha; ")) - 1
                    
                    if 0 <= choice_index < len(options):
                        _, (func, args) = options[choice_index]
                    
                    next_id_from_action = func(*args) # Chama a função com todos os argumentos
                    
                    break
                except ValueError:
                    print("Entrada inválida. Digite o número da opção.")
                    
                    
        next_dialogue_id = next_id_from_action if next_id_from_action is not None else dialogue[1]
                    
        if next_dialogue_id:
            if not options:
                input("Pressione Enter para continuar...")
                
            self.showDialogue(next_dialogue_id)
        elif not options:
            input("Pressione Enter para encerrar a conversa...")
                

        
        
        
def coletar_item(item: str, quantidade: int) -> str | None:
    print(f"\n Você coletou {quantidade}x de {item}! A busca foi bem sucedida!")
    sleep(1.5)
    # NOVO: Retorna o ID do diálogo de sucesso
    return "sucesso_coleta" 

def iniciar_combate(inimigo: str, dificuldade: int) -> str | None:
    print(f"\n Combatendo {inimigo} na dificuldade {dificuldade}!")
    sleep(1.5)
    # NOVO: Retorna o ID do diálogo de combate
    return "combate_iniciado"

def fechar_jogo() -> str | None:
    print("\n Fim de jogo. Game Over seu NOOOOOOOOOB! 6767 676 7 67 67 BONBARDIRO CROCODIRO 67 67 67 SUBWAYSURFEER FREE MOBILE FEET PHOTO GRATIS 2025")
    exit()
    # Retorna None, pois o jogo será encerrado
    return None

def beber_pocao() -> str | None:
    pass


#DialogueManager._addDialogue(DialogueManager,"ID DO DIALOGO","TEXTO DO DIALOGO", "ID DO PRÒXIMO DIALOGO SE HOUVER", [("TEXTO ESCOLHA 1", FUNCAO_ESCOLHA_1), ("TEXTO ESCOLHA 2", FUNCAO_ESCOLHA_2)])        

add = DialogueManager._addDialogue

add(DialogueManager,"tutorial.1", "Seja bem vindo ao tutorial caro guerreiro!", "tutorial.2")
add(DialogueManager,"tutorial.2", "Aqui nesse reino perdemos muitas vidas anualmente", "tutorial.3")
        
        
# Dialogue 3: Com opções, cada uma chamando uma função com argumentos diferentes
# Note a nova estrutura: ("Texto", (funcao, [arg1, arg2, ...]))
add(
    DialogueManager,
    "tutorial.3",
    None, # Fim do fluxo após a escolha, ou a função de ação pode ditar o próximo
    options=[
        ("Procurar uma Espada na floresta (Coletar item)", (coletar_item, ["Espada Longa", 1])),
        ("Enfrentar o Lobo da montanha (Combate)", (iniciar_combate, ["Lobo Alfa", 5])),
        ("Desistir e voltar para casa (Fim)", (fechar_jogo, [])) # Lista de argumentos vazia se não houver args
    ]
)


add(DialogueManager, "sucesso_coleta", "Você agora tem uma arma melhor. Siga em frente!", "tutorial.fim")
add(DialogueManager, "combate_iniciado", "O combate será difícil. Prepare-se para lutar!", "tutorial.fim")
add(DialogueManager, "tutorial.fim", "Parabéns, o tutorial terminou.", None)
