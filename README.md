# ✈️ Sistema de Monitoramento e Gerenciamento de Tráfego Aéreo Simulado

## 📌 Sobre o Projeto

Este projeto consiste no desenvolvimento de um sistema acadêmico completo para monitoramento e gerenciamento de tráfego aéreo simulado, com foco na aplicação de conceitos de Engenharia de Software, modelagem de sistemas e simulação de eventos em tempo real.

O sistema tem como objetivo simular o comportamento de aeronaves em voo, desde a decolagem até o pouso, utilizando um motor de simulação baseado em eventos discretos. A partir disso, é possível acompanhar a posição das aeronaves em tempo real, gerenciar operações aeroportuárias e identificar possíveis conflitos de tráfego aéreo.

Diferente de sistemas reais de controle de tráfego aéreo, este projeto utiliza dados reais estáticos combinados com telemetria simulada, garantindo viabilidade acadêmica sem perder o realismo operacional.

---

## 🎯 Objetivo

Desenvolver uma plataforma capaz de:

* Monitorar aeronaves em tempo real em um mapa interativo
* Simular voos com base em rotas entre aeroportos
* Gerenciar operações de pouso e decolagem
* Gerar alertas de proximidade e conflito entre aeronaves
* Registrar histórico de voos e eventos operacionais

---

## 🧠 Conceito Principal

O sistema utiliza um modelo híbrido:

* **Dados reais estáticos**
  Informações de aeroportos, pistas e aeronaves para aumentar o realismo

* **Simulação de eventos (SimPy)**
  Cada voo é tratado como um processo que evolui ao longo do tempo, passando por diferentes fases operacionais

* **Telemetria simulada (GPS virtual)**
  A posição das aeronaves é gerada dinamicamente (latitude, longitude, altitude, velocidade e direção)

---

## ⚙️ Funcionalidades

### ✈️ Gestão de Entidades

* Cadastro de aeronaves
* Cadastro de aeroportos e pistas
* Cadastro e controle de voos
* Sistema de usuários com autenticação

### 📡 Monitoramento em Tempo Real

* Visualização das aeronaves em mapa
* Atualização contínua da posição (telemetria simulada)
* Exibição da fase atual do voo

### 🧭 Simulação de Voo

* Controle de estados do voo:

  * Agendado
  * Taxiando
  * Decolando
  * Cruzeiro
  * Aproximação
  * Pouso
  * Finalizado

* Geração de trajetória entre origem e destino

* Evolução baseada em eventos discretos

### 🚨 Sistema de Alertas

* Detecção de proximidade entre aeronaves
* Geração de alertas com níveis de severidade
* Registro de eventos operacionais

### 📊 Histórico e Rastreamento

* Armazenamento de posições ao longo do tempo
* Visualização da rota percorrida
* Consulta de histórico de voos

---

## 🏗️ Arquitetura

O sistema é estruturado em camadas:

* **Backend (API)**
  Responsável pelas regras de negócio, persistência de dados e integração com o simulador

* **Simulador (SimPy)**
  Motor responsável por controlar os eventos e gerar a telemetria das aeronaves

* **Banco de Dados**
  Armazena entidades, posições, voos e alertas

* **Frontend (Interface Web)**
  Responsável pela visualização dos dados, incluindo mapa interativo e dashboard

---

## 🛠️ Tecnologias Utilizadas

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL

### Simulação

* SimPy
* Geopy

### Frontend

* JavaScript
* Leaflet (mapas interativos)

### Outros

* WebSocket (planejado para tempo real)
* JWT para autenticação

---

## 🗂️ Estrutura do Projeto

```bash
backend/
frontend/
docs/
```

---

## 📚 Aplicação Acadêmica

Este projeto foi desenvolvido como parte da disciplina de Engenharia de Software, com o objetivo de aplicar na prática:

* Levantamento de requisitos
* Modelagem UML
* Arquitetura de sistemas
* Desenvolvimento orientado a camadas
* Simulação de sistemas complexos
* Trabalho em equipe com controle de versão

---

## 🚀 Diferenciais do Projeto

* Uso de simulação de eventos discretos (SimPy)
* Representação realista de operações aéreas
* Integração entre simulação e visualização em tempo real
* Estrutura modular e escalável
* Aplicação prática de conceitos de engenharia

---

## 📌 Status do Projeto

🚧 Em desenvolvimento (MVP em construção)

---

## 👥 Equipe

Projeto desenvolvido por uma equipe de estudantes de Engenharia de Computação.

---

## 📄 Licença

Este projeto possui fins acadêmicos e educacionais.
