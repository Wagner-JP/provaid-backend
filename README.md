# 🚀 ProvaID

Plataforma de certificação e verificação de autenticidade de conteúdos digitais utilizando hash SHA-256.

---

## 📌 Sobre o projeto

O **ProvaID** é uma aplicação desenvolvida com foco em validar a autenticidade de arquivos digitais através da geração de hash (SHA-256), permitindo registrar e verificar conteúdos de forma segura.

A ideia do projeto surgiu como parte da minha transição de carreira para a área de tecnologia, com foco em backend e segurança.

---

## ⚙️ Funcionalidades

- 📤 Upload de arquivos
- 🔐 Geração de hash SHA-256
- 🧾 Registro em banco de dados
- 🔍 Verificação de autenticidade por hash
- ♻️ Detecção de arquivos duplicados
- 🔗 Geração de link de verificação
- 🌐 Integração completa entre frontend e backend
- 🔐 (em desenvolvimento) Autenticação com JWT

---

## 🧱 Tecnologias utilizadas

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite

### Frontend
- HTML
- CSS
- JavaScript

### Segurança
- SHA-256 (hashing)
- (em evolução) JWT

---

## 📂 Estrutura do projeto 

Minha jornada (aprendizados reais)

Durante o desenvolvimento do ProvaID, enfrentei diversos desafios que foram fundamentais para o aprendizado:

🔴 Problemas enfrentados
Erros de importação no FastAPI
Estrutura incorreta de pastas (organização do projeto)
Erros de banco de dados (SQLite desatualizado)
Falha ao enviar arquivos (Expected UploadFile, received str)
Problemas de CORS entre frontend e backend
Erros 500 (Internal Server Error)
Frontend não conectando com a API (Failed to fetch)
Servidor frontend não iniciado (connection refused)
Ordem incorreta de inicialização no FastAPI (app não definido)

🟢 Como resolvi
Reorganização da estrutura do projeto (arquitetura modular)
Correção dos imports e separação de camadas (routes, services, schemas)
Reset do banco SQLite (provaid.db)
Ajuste correto do envio de arquivos com UploadFile
Configuração de CORS no FastAPI
Debug com DevTools (Network)
Uso do Swagger para testes diretos da API
Correção da ordem de inicialização do FastAPI
Execução correta de servidores (backend + frontend)
