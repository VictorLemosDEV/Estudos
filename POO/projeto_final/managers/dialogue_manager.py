from typing import List, Dict,Tuple,Callable, Union, TypeAlias, ReadOnly
from time import sleep
import os

# Define a estrutura do único diálogo
# Dialogue é uma Tupla contendo 3 elementos
# 1. str: O texto principal do diálogo.
# 2. str | None: O ID do próximo diálogo na sequência (str) ou None se este for o final da sequência.
# 3. List[Tuple[str, Callable]]: A lista de opções de escolha para o usuário. 
#    - Cada opção é uma Tupla de 2 elementos:
#      - str: O texto da escolha que será exibido.
#      - Callable: A função (que pode ser chamada) que será executada quando o usuário escolher esta opção.
Dialogue: TypeAlias = Tuple[str, str | None, List[Tuple[str, Callable]]]

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
        
    def _addDialogue(cls, id: str,content: str, nextDialogue: str | None=None, options: List[Tuple[str, Callable]] = []):
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
        for char in dialogue[0]:
            print(char,end="",flush=True)
            sleep(0.05)
            
        input()
        if (dialogue[1]):
            self.showDialogue(dialogue[1]) # Mostra o próximo dialogo
        
        
        



#DialogueManager._addDialogue(DialogueManager,"ID DO DIALOGO","TEXTO DO DIALOGO", "ID DO PRÒXIMO DIALOGO SE HOUVER", [("TEXTO ESCOLHA 1", FUNCAO_ESCOLHA_1), ("TEXTO ESCOLHA 2", FUNCAO_ESCOLHA_2)])        

add = DialogueManager._addDialogue

add(DialogueManager,"tutorial.1", "Seja bem vindo ao tutorial caro guerreiro!", "tutorial.2")
add(DialogueManager,"tutorial.2", "Aqui nesse reino perdemos muitas vidas anualmente")
        
        
        
        
   