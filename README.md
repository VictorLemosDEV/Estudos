# 📚 Repositório Geral de Anotações  
Anotações das matérias do curso de **Ciência da Computação**.

---

## 📅 Organização por Semestre

### 2º Semestre
**Conteúdos Principais:**
- Engenharia de Software I
- Arquitetura de Sistemas Operacionais
- Sistemas Embarcados
- Geometria Analítica e Algebra Linear


---


## ⚙️ Configuração do Ambiente de Desenvolvimento

Esta seção descreve como configurar um ambiente virtual Python para este projeto, permitindo a instalação das dependências e a execução da suíte de testes com o `pytest`.

### Pré-requisitos
- Python 3.8 ou superior instalado.
- O arquivo `requirements.txt` deve existir no repositório.

### Passo a Passo

**1. Crie o Ambiente Virtual**

Na pasta raiz do repositório, execute o comando abaixo para criar uma pasta chamada `.venv` que conterá o ambiente isolado.

```bash
python -m venv .venv
```

**2. Ative o Ambiente Virtual**

Você precisa "entrar" no ambiente antes de usá-lo. O comando varia conforme o seu sistema operacional:

Windows (PowerShell):
```
.\.venv\Scripts\Activate.ps1
```
Windows (CMD):
```
.\.venv\Scripts\activate.bat
```
macOS e Linux:
```
source .venv/bin/activate
```

**3. Instale as Dependências**

Com o ambiente ativo, use o ``pip`` para instalar todas as bibliotecas de teste listadas no arquivo ``requirements.txt`` com um único comando.
```
pip install -r requirements.txt
```

Agora você pode, por exemplo, executar a suíte de testes do repositório usando o comando:
```
pytest
```

> Este repositório serve para centralizar e organizar os estudos ao longo da graduação.