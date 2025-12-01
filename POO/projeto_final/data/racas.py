from typing import Protocol, Dict, List

RACA_CATALOGO = {}

class IRaca(Protocol):
    
    nome: str
    attributeBonus: Dict[str, int]
    description: str


class Raca(IRaca):
    
    def __init__(self, nome: str, attributeBonus, descricao: str):
        self.nome = nome
        self.attributeBonus = attributeBonus
        self.description = descricao
        
        RACA_CATALOGO[self.nome] = self
        
    
        
    def __repr__(self):
        return f"Raca('{self.nome}', Mod: {self.attributeBonus})"
       

# --- Definição das Raças ---

# 1. Humano (Versátil)
humano = Raca(
    "Humano", 
    {"forca": 1, "constituicao": 1, "agilidade": 1, "inteligencia": 1},
    "Versátil e adaptável, sem bônus ou penalidades significativas. Bom para qualquer classe."
)

# 2. Dragão (Tank Natural)
dragao = Raca(
    "Dragão", 
    {"forca": 2, "constituicao": 3, "agilidade": 0, "inteligencia": 1},
    "Extremamente robusto, excelente HP. Sua lentidão é compensada por sua resistência."
)

# 3. Elfo Silvestre (Lutador Ágil)
elfo_silvestre = Raca(
    "Elfo Silvestre", 
    {"forca": 0, "constituicao": 1, "agilidade": 3, "inteligencia": 1},
    "Rápido e gracioso. Ideal para classes que dependem de evasão e iniciativa, mas frágil."
)

# 4. Anão da Montanha (Durável e Forte)
anao_montanha = Raca(
    "Anão da Montanha", 
    {"forca": 2, "constituicao": 2, "agilidade": 0, "inteligencia": 1},
    "Forte e resistente a danos. Ideal para guerreiros e defensores."
)

# 5. Gnomo Inventor (Mestre Arcano)
gnomo = Raca(
    "Gnomo Inventor", 
    {"forca": 0, "constituicao": 0, "agilidade": 2, "inteligencia": 3},
    "Poder mágico superior e raciocínio rápido. Possui o HP e Força muito baixos."
)

# 6. Meio-Orc (Bruto Implacável)
meio_orc = Raca(
    "Meio-Orc", 
    {"forca": 3, "constituicao": 1, "agilidade": 0, "inteligencia": 0},
    "Foco total em poder de ataque. Ideal para bárbaros, mas falta sutileza e inteligência."
)

# 7. Sereiano (Vigor Aquático)
sereiano = Raca(
    "Sereiano", 
    {"forca": 1, "constituicao": 2, "agilidade": 1, "inteligencia": 1},
    "Equilibrado com uma leve vantagem em vigor. Útil em ambientes aquáticos."
)

# 8. Felino (Ágil e Sagaz)
felino = Raca(
    "Felino", 
    {"forca": 1, "constituicao": 0, "agilidade": 2, "inteligencia": 2},
    "Combina agilidade e inteligência, bom para ladinos ou magos com foco em movimento."
)

# 9. Golem de Pedra (Fortaleza Ambulante)
# Usa penalidade para balancear o bônus de CON
golem = Raca(
    "Golem de Pedra", 
    {"forca": 1, "constituicao": 3, "agilidade": -1, "inteligencia": 2},
    "Corpo de pedra garante HP extremo, mas penaliza a velocidade e iniciativa."
)

# 10. Vampiro (Equilíbrio Sombrio)
vampiro = Raca(
    "Vampiro", 
    {"forca": 1, "constituicao": 1, "agilidade": 2, "inteligencia": 2},
    "Equilíbrio entre agilidade e intelecto, bom para arquétipos de combate mágico."
)


