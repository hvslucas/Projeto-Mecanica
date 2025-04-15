# :triangular_ruler::building_construction: Projeto Mecânica - Treliça

- ### [:dart: Objetivo](#dart-objetivo-1)
- ### [:snake: Dependências](#snake-dependências-1)
- ### [:rescue_worker_helmet: Simulação](#rescue_worker_helmet-simulação-1)
- ### [:gear: Como rodar](#gear-como-rodar-1)
- ### [:arrow_down: Baixar o projeto](https://github.com/hvslucas/Projeto-Mecanica/archive/refs/heads/main.zip)

## Disciplina de Mecânica Para Engenharia da Computação

Esse foi um projeto desenvolvido por discentes do curso de *Engenharia da Computação da Universidade Federal da Paraíba*, curso este que pertence ao *[Centro de Informática](http://ci.ufpb.br/)*, localizado na *[Rua dos Escoteiros S/N - Mangabeira - João Pessoa - Paraíba - Brasil](https://g.co/kgs/xobLzCE)*. O código foi desenvolvido em Python com as anotações em Jupyter Notebook e foi avaliado por meio de simulações realizadas no Ansys, permitindo a verificação do funcionamento correto do projeto e a validação dos resultados esperados. A partir dos resultados obtidos por meio da execução do código em Python, validados pelas simulações no Ansys, o professor responsável pela disciplina realizou a avaliação do projeto e do desempenho dos membros da equipe.

### :hammer_and_wrench: Autores:
-  :link:  *[Lucas Henrique Vieira da Silva](https://github.com/hvslucas)*
-  :link:  *[Marco Antonio de Vasconcelos Souza Filho](https://github.com/MarcoFilho1)*
-  :link:  *[Pedro Henrique Araujo De Carvalho](https://github.com/pedroarawj)*
-  :link:  *[Yves Ribeiro De Sena](https://github.com/Yvesena)*

###  :hammer_and_wrench: Docente:

-  :link: *Jairo Rocha de Faria*
<br>

[![premium_photo-1661335257817-4552acab9656](https://github.com/user-attachments/assets/395eddb2-4588-47d2-990c-d02d8dc7aa94)](#triangular_rulerbuilding_construction-projeto-mecânica---treliça)

## :dart: Objetivo

### Objetivo Geral
O Projeto consiste na análise de uma treliça plana com barras horizontais, verticais e inclinadas, submetida a três diferentes casos de carregamento. O objetivo principal é determinar as deflexões (deslocamento) e forças nos elementos da treliça, além de modelá-la como uma viga equivalente para validação dos resultados.

### Objetivos Específicos

1. **Análise dos Casos de Carregamento:**
   - Resolver a treliça para três cenários distintos:
     - **Caso A:** Forças horizontais aplicadas nos nós 13 e 14
     
       F<sub>x13</sub> = F<sub>x14</sub> = 10.000 N

     - **Caso B:** Forças verticais aplicadas nos nós 13 e 14 
     
       F<sub>y13</sub> = F<sub>y14</sub> = 10.000 N

     - **Caso C:** Forças horizontais opostas aplicadas nos nós 13 e 14 
     
       F<sub>x13</sub> = 10.000 N, F<sub>x14</sub> = -10.000 N

2. **Determinação de Propriedades Equivalentes:**
   - Modelar a treliça como uma viga engastada e livre, calculando:
     - Rigidez axial EA<sub>eq</sub>.
     - Rigidez à flexão EI<sub>eq</sub>.
     - Rigidez ao cisalhamento GA<sub>eq</sub>.

3. **Cálculo de Deflexões:**
   - Determinar as deflexões (deslocamento / deformação) na extremidade da treliça para cada caso de carregamento, utilizando as fórmulas da viga equivalente:
     - Deflexão axial: 

$$ u_{ponta} = \frac{FI}{(EA)_{eq}} $$

   - Deflexão transversal: 

$$ v_{ponta} = \frac{FI^3}{3(EI)\_{eq}} + \frac{FI}{(GA)_{eq}} $$

   - Deflexão devido a um momento:
     
$$ V_{ponta} = \frac{Cl^2}{2(EI)_{eq}} $$

4. **Validação do Modelo:**
   - Comparar os resultados obtidos pelo Método dos Elementos Finitos (MEF) com as deflexões calculadas pelo modelo de viga equivalente.
   - Comparar com o resultado adquirido no Software Ansys Workbench[^1] na versão 2025 R1.

[^1]: O [Ansys é um software de simulação computacional para engenharia](https://razor.com.br/blog/engenharia-e-fabricacao/tudo-sobre-o-ansys/) que possui uma versão disponível para estudantes. Mais no próprio site do software: [Site Oficial](https://www.ansys.com/)

5. **Apresentação dos Resultados:**
   - Organizar os dados em tabelas, incluindo:
     - Deslocamentos nodais.
     - Forças em cada elemento.
     - Comparação com o resultado do software
   - Representar graficamente a treliça e destacar as regiões críticas.

## :snake: Dependências

- **`numpy`**: Biblioteca fundamental para computação científica em Python, fornecendo suporte para arrays multidimensionais e operações matemáticas eficientes.
  - **Implementação:** Utilizada para criar e manipular arrays das coordenadas dos nós (`nos`), montar a matriz de rigidez global (`K`), resolver sistemas lineares com `np.linalg.solve`, e realizar cálculos vetoriais como normas (`np.sqrt`) e operações de álgebra linear.

- **`pandas`**: Biblioteca para manipulação e análise de dados, especialmente útil para trabalhar com estruturas tabulares.
  - **Implementação:** Empregada para armazenar e formatar as forças internas das barras em um DataFrame (`df_forcas`), permitindo exibição organizada dos resultados com controle de formatação numérica (`display.float_format`).

- **`matplotlib.pyplot`**: Biblioteca para criação de visualizações estáticas, animadas e interativas em Python.
  - **Implementação:** Usada para plotar a treliça original e deformada (`plt.plot`, `plt.arrow`), adicionar legendas personalizadas (`Line2D`), configurar títulos e eixos (`plt.title`, `plt.xlabel`), e exibir informações textuais sobre as forças internas (`plt.text`).

- **`matplotlib.lines.Line2D`**: Componente específico do matplotlib para criação e customização de linhas em gráficos.
  - **Implementação:** Utilizado para criar elementos personalizados na legenda do gráfico, distinguindo visualmente barras em tração (azul) e compressão (vermelho).

### Relação entre Dependências e Funcionalidades Principais:
1. **Cálculos Estruturais** (`numpy`):
   - Montagem da matriz de rigidez (`matriz_rigidez_barra`, `montar_matriz_rigidez_global`)
   - Solução do sistema linear de deslocamentos (`resolver_sistema`)

2. **Gerenciamento de Resultados** (`pandas`):
   - Tabela de forças internas (`calcular_forcas_internas`)

3. **Visualização** (`matplotlib`):
   - Plotagem da treliça deformada com cores indicativas (`plotar_trelica`)
   - Anotação dos valores de força nas barras e legendas personalizadas

## :rescue_worker_helmet: Simulação

### 🔧 **Pré-Processamento**

1. **Materiais**:
Material: Alumínio (biblioteca ANSYS General Materials), com ajuste no módulo de Young.

   **Parâmetros**:
   - Módulo de Young (E): 100 GPa
   - Coeficiente de Poisson (ν): 0,33

2. **Geometria**:
   **Tipo**: Treliça plana com barras horizontais, verticais e inclinadas.

   **Dimensões das barras**:
   - Horizontais/verticais: L = 0,3 m
   - Inclinadas: √2L ≈ 0,424 m

   **Seção transversal**:
   - Área constante: A = 1,0 cm² (1 × 10⁻⁴ m²)

   **Conectividade seguindo o seguinte modelo**:

![image](https://github.com/user-attachments/assets/2be98100-751d-47a6-ad67-ca1a83fba17a)


### ⚙️ **Solução**


### 📈 **Pós-Processamento**

- Principais resultados obtidos:
  

### 📂 **Arquivos do ANSYS**


## :gear: Como rodar




