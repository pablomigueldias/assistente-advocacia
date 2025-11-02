# 🧠 Assistente Jurídico com RAG e Agente Inteligente

Um sistema completo de **IA Jurídica** desenvolvido em **Python + FastAPI + React**, integrando:
- **RAG (Retrieval-Augmented Generation)** para busca contextual em documentos reais;
- **Agente Jurídico** pronto para treinar e ser executado.
- **Interface de chat moderna** para testar o comportamento da IA em tempo real.

> 💡 O objetivo é simular o funcionamento de um **assistente jurídico corporativo (BPO jurídico)** — capaz de ler, entender e agir sobre contratos, cláusulas e solicitações reais.

---

## 📚 Sumário
- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Tecnologias Usadas](#-tecnologias-usadas)
- [Como Rodar Localmente](#-como-rodar-localmente)
- [Como Treinar e Atualizar o Conhecimento](#-como-treinar-e-atualizar-o-conhecimento)
- [Como Testar pelo Chat](#-como-testar-pelo-chat)
- [Pontos de Destaque Técnicos](#-pontos-de-destaque-técnicos)
- [Possíveis Expansões Futuras](#-possíveis-expansões-futuras)
- [Autor](#-autor)

---

## 🧩 Visão Geral

O projeto é um **laboratório jurídico de IA**, combinando:
- **LLM (modelo de linguagem)** para interpretar textos;
- **RAG (banco vetorial)** para buscar respostas baseadas em PDFs e textos jurídicos;
- **Agente jurídico** que classifica pedidos, extrai campos (nome, e-mail, SLA, assunto) e gera ações automáticas como roteamento e checklist.

A interface permite testar:
- `/chat` → respostas puras do LLM;
- `/rag/query` → respostas baseadas nos documentos locais;
- `/agent/route` → classificação e extração jurídica com ações.

---

## ⚙️ Funcionalidades

| Módulo | Descrição |
|--------|------------|
| **RAG** | Indexa PDFs e textos jurídicos e responde consultas com base neles |
| **Agente Jurídico** | Classifica o tipo do pedido e gera ações (checklist, prazos, roteamento) |
| **Chat UI** | Interface moderna feita em React + Tailwind para testes rápidos |
| **Ingestão Automática** | Detecta modelos de contrato (com lacunas “____”) e textos explicativos |
| **Armazenamento Vetorial** | Usa embeddings (Ollama / SentenceTransformer) no ChromaDB |

---

## Tecnologias Usadas

### Backend
- **Python 3.11+**
- **FastAPI**
- **LangChain / ChromaDB**
- **Ollama (Llama 3 / Mistral / Nomic Embed)**
- **pypdf** para leitura de PDFs
- **Regex + dataclasses** para extração de dados
- **Uvicorn** (servidor local)

### Frontend
- **React (Vite)**
- **Tailwind CSS**
- **Fetch API** (sem libs externas)
- **Chat UI customizado** para testes do backend
- 

## Como Rodar Localmente

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/seuusuario/assistente_advocacia.git
cd assistente_advocacia
```
### 2️⃣ Crie o ambiente virtual
```bash
python -m venv venv
.\venv\Scripts\activate     # Windows
source venv/bin/activate    # Linux/Mac
```
### 3️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```
### 4️⃣ Suba o backend
```bash
cd app/api
uvicorn app.api.main:app --reload
```
### 5️⃣ Suba o frontend
```bash
cd ../../front
npm install
npm run dev
```


