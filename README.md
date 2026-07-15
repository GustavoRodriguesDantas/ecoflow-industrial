# EcoFlow Industrial 🌱🏭

**Simulador de Linha de Produção Sustentável | Foco em Gestão de KPIs e Engenharia de Produção**

![Foto da Equipe](./Foto%20da%20Equipe.jpeg)

*Apresentação do projeto na Semana de Engenharia da UniLaSalle.*

O **EcoFlow** é um projeto desenvolvido para a disciplina de **Lógica de Programação** (3º período de Engenharia de Produção), que une o desenvolvimento de software à análise de dados industriais. O projeto simula uma esteira de produção onde cada decisão logística impacta diretamente na sustentabilidade e viabilidade financeira da operação.

## 🏆 Reconhecimento Acadêmico

Este projeto teve a honra de ser apresentado e participar da **Semana de Engenharia da UniLaSalle**, um evento que celebra a inovação e o desenvolvimento de soluções práticas na área. A participação reforça o impacto e a relevância do EcoFlow no contexto acadêmico e industrial.

## 🎯 Objetivos do Jogo (e do Projeto)

Com base nos objetivos acadêmicos e práticos definidos para o EcoFlow Industrial, o simulador visa:

1. **Promover a Sustentabilidade:** Incentivar a adoção de práticas industriais que reduzam o impacto ambiental.

1. **Simular Processos Industriais:** Permitir a montagem e gestão de linhas de produção, abrangendo desde a coleta de matérias-primas até a distribuição.

1. **Monitorar Indicadores:** Acompanhar em tempo real KPIs essenciais como CO2, Custo, Reuso e OEE para avaliar o desempenho do processo.

1. **Desenvolver Lógica Estratégica:** Estimular o uso de decisões inteligentes e estruturas condicionais para otimizar resultados.

1. **Incentivar a Economia Circular:** Valorizar o reuso de materiais e a logística reversa, transformando resíduos em recursos.

## 💡 Visão de Produto e Gestão (PM/PO Mindset)

Como líder do projeto e principal desenvolvedor, foquei em criar uma ferramenta que não apenas "funcionasse", mas que entregasse **valor analítico**. A arquitetura foi pensada para resolver o problema de visualização de trade-offs em processos industriais:

- **Modelagem de KPIs:** Definição e implementação de métricas críticas (CO2, Custo, OEE, Reuso) para fornecer feedback imediato ao "gestor" da linha.

- **User Experience (UX):** Interface intuitiva baseada em fluxos (Drag-and-Drop) para facilitar a prototipagem de diferentes cenários produtivos.

- **Escalabilidade:** O sistema de blocos foi projetado para permitir a adição de novos processos e materiais sem necessidade de refatoração do motor de simulação.

## 📊 Análise de Dados e Indicadores

O motor de simulação utiliza o algoritmo de **Busca em Largura (BFS)** para percorrer o grafo de produção e realizar a agregação de dados em tempo real:

| KPI | Descrição | Objetivo Analítico |
| --- | --- | --- |
| **OEE** | Eficiência Global do Equipamento | Medir a produtividade e qualidade do fluxo. |
| **CO2** | Pegada de Carbono | Analisar o impacto ambiental de cada matéria-prima. |
| **Custo** | Custo Operacional | Avaliar a viabilidade econômica das escolhas. |
| **Reuso** | Taxa de Circularidade | Monitorar a eficiência da logística reversa e reciclagem. |

## 🛠️ Tecnologias e Conceitos

- **Linguagem:** Python 3.x (Pygame)

- **Engenharia de Software:** Programação Orientada a Objetos (POO), Teoria dos Grafos.

- **Engenharia de Produção:** Gestão de Processos, Sustentabilidade Industrial, Logística Reversa, Análise de KPIs.

## 🚀 Como Executar

1. Instale o Pygame: `pip install pygame`

1. Clone o repositório: `git clone https://github.com/seu-usuario/ecoflow.git`

1. Execute: `python ecoflow.py`

---

*Este projeto reflete minha paixão por transformar dados em decisões estratégicas, unindo os fundamentos da Engenharia de Produção com a potência da tecnologia.*
