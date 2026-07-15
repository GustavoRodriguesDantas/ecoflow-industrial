# EcoFlow Industrial 🌿🔄

> **EcoFlow Industrial** é um simulador interativo de processos e linhas de produção sustentáveis inspirado no visual de ferramentas modernas de automação *low-code* (como n8n e Node-RED). Desenvolvido como projeto prático para a disciplina de **Lógica de Programação** na **UniLaSalle**, o simulador une a visão analítica da Engenharia de Produção ao desenvolvimento de software para calcular o impacto ambiental e financeiro de operações industriais em tempo real.

---

## 📌 Sumário
- [🎯 Objetivos do Projeto](#-objetivos-do-projeto)
- [💼 Visão de Produto & Engenharia de Produção](#-visão-de-produto--engenharia-de-produção)
- [🎨 O Grande Desafio Técnico: Engine Vetorial Própria](#-o-grande-desafio-técnico-engine-vetorial-própria)
- [⚙️ Arquitetura Computacional & Dados](#-arquitetura-computacional--dados)
- [📊 Dashboard de KPIs em Tempo Real](#-dashboard-de-kpis-em-tempo-real)
- [🚀 Onde o EcoFlow Pode Ser Usado?](#-onde-o-ecoflow-pode-ser-usado)
- [💻 Como Executar o Simulador](#-como-executar-o-simulador)
- [🔮 Roadmap de Dados (Futuras Integrações)](#-roadmap-de-dados-futuras-integrações)

---

## 🎯 Objetivos do Projeto

O EcoFlow Industrial nasceu com a missão de conectar a eficiência operacional à sustentabilidade. O software desafia o usuário a desenhar fluxos logicamente viáveis enquanto equilibra métricas ecológicas e financeiras:

1. **Promover a Sustentabilidade:** Incentivar decisões industriais que mitiguem o impacto ambiental.
2. **Simular Processos Complexos:** Prototipar esteiras completas (coleta, processamento, reciclagem e distribuição).
3. **Monitorar Indicadores:** Apresentar o impacto imediato de escolhas de infraestrutura através de dados visuais.
4. **Desenvolver Lógica Estratégica:** Utilizar desvios condicionais ($IF/ELSE$) para criar rotas alternativas inteligentes de refugo e retrabalho.
5. **Incentivar a Economia Circular:** Validar o papel da logística reversa nos resultados do negócio.

---

## 💼 Visão de Produto & Engenharia de Produção

Como idealizador da visão de produto e líder técnico do projeto, estruturei o EcoFlow para resolver um problema real de gestão industrial: a opacidade de dados ambientais no chão de fábrica. 

Para demonstrar o potencial da ferramenta, implementamos um fluxo padrão de **Logística Reversa de Polímeros**:
$$\text{Coletar PET} \longrightarrow \text{Processar} \longrightarrow \text{Verificar Qualidade (IF/ELSE)} \longrightarrow \begin{cases} \text{OK} \longrightarrow \text{Reciclar} \longrightarrow \text{Distribuir} \\ \text{NÃO} \longrightarrow \text{Descartar} \end{cases}$$

Essa modelagem permite que gestores analisem exatamente o trade-off financeiro de se investir em uma etapa de triagem de qualidade rigorosa vs. o custo de descarte de matéria-prima.

---

## 🎨 O Grande Desafio Técnico: Engine Vetorial Própria

Um dos maiores desafios identificados no desenvolvimento da interface gráfica em Pygame foi a gestão de *assets* externos. Depender de caminhos de arquivos locais para carregar imagens de ícones tornaria o software altamente instável e difícil de rodar em diferentes sistemas operacionais na apresentação do MVP.

**A Solução de Engenharia:** Desenvolvi um mecanismo de renderização puramente matemático. Todos os elementos visuais do canvas foram desenhados programaticamente através de primitivas geométricas (`pygame.draw`):
*   **Ícones de Blocos:** As engrenagens, caminhões de distribuição e símbolos de reciclagem são gerados por cálculos vetoriais em tempo real.
*   **Linhas de Conexão:** A amarração lógica dos blocos utiliza **Curvas de Bézier Cúbicas**, garantindo o visual fluido de ferramentas de mercado.

Com isso, o projeto tornou-se **100% autônomo, portátil e leve**.

---

## ⚙️ Arquitetura Computacional & Dados

O backend do simulador foi construído sobre conceitos estruturados de **Teoria dos Grafos**:

### 1. Motor de Simulação via BFS (Busca em Largura)
O fluxo montado no canvas é interpretado como um Grafo Direcionado. Quando a execução é disparada ("Run Flow"), o algoritmo mapeia os nós raiz (Fontes) e utiliza uma estratégia de **Busca em Largura (BFS)** para navegar pelo processo. Isso garante que nenhuma etapa seja calculada antes que suas dependências anteriores tenham sido processadas.

### 2. Acúmulo Dinâmico de Impacto
Cada bloco adicionado possui um dicionário de propriedades contendo cargas de dados estáticas. À medida que o pulso da simulação transita pelas Curvas de Bézier, os valores são agregados matematicamente e filtrados por limites realistas:

$$KPI_{\text{final}} = \max\left(\text{Min}, \min\left(\text{Max}, \sum_{n \in \text{Caminho}} \Delta KPI_n\right)\right)$$

---

## 📊 Dashboard de KPIs em Tempo Real

Abaixo estão as métricas industriais monitoradas e consolidadas dinamicamente no painel inferior do simulador:

| Indicador | Unidade | Descrição Técnica | Foco de Análise |
| :--- | :--- | :--- | :--- |
| **Pegada de CO₂** | kg | Emissão total de carbono equivalente gerada pelo maquinário e transporte. | Descarbonização / ESG |
| **Custo de Produção**| R$ | Gastos operacionais fixos e variáveis acumulados no ciclo. | Viabilidade Financeira |
| **Taxa de Reuso** | % | Percentual de matéria-prima reaproveitada e reinserida na cadeia. | Economia Circular |
| **OEE** | % | *Overall Equipment Effectiveness* (Eficiência Global do Equipamento). | Produtividade e Gargalos |

---

## 🚀 Onde o EcoFlow Pode Ser Usado?

O simulador possui uma arquitetura versátil projetada para atender diferentes frentes de mercado:
*   **Educação:** Ferramenta didática para ensinar sustentabilidade e lógica de programação em universidades.
*   **Indústrias:** Auxílio rápido no planejamento macro de processos para testar cenários ecológicos.
*   **Consultoria:** Suporte visual para consultores apresentarem cenários de transição verde para clientes.
*   **Governo & ONGs:** Formulação de dinâmicas para programas de incentivo à reciclagem e conscientização pública.

---

## 💻 Como Executar o Simulador

### Pré-requisitos
*   Python 3.10 ou superior instalado.
*   Biblioteca Pygame.

### Instalação e Execução
1. Clone este repositório para sua máquina local:
   ```bash
   git clone [https://github.com/seu-usuario/ecoflow-industrial.git](https://github.com/seu-usuario/ecoflow-industrial.git)
