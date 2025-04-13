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
O Projeto 3 consiste na análise de uma treliça plana com barras horizontais, verticais e inclinadas, submetida a três diferentes casos de carregamento. O objetivo principal é determinar as deflexões (deslocamento) e forças nos elementos da treliça, além de modelá-la como uma viga equivalente para validação dos resultados.

### Objetivos Específicos

1. **Análise dos Casos de Carregamento:**
   - Resolver a treliça para três cenários distintos:
     - **Caso A:** Forças horizontais aplicadas nos nós 13 e 14
     
       $$ F_{x13} = F_{x14} = 10.000 \quad (N) $$

     - **Caso B:** Forças verticais aplicadas nos nós 13 e 14 
     
       $$ F_{y13} = F_{y14} = 10.000 \quad (N) $$

     - **Caso C:** Forças horizontais opostas aplicadas nos nós 13 e 14 
     
       $$ F_{x13} = 10.000 \quad (N) F_{x14} = -10.000\quad (N) $$

2. **Determinação de Propriedades Equivalentes:**
   - Modelar a treliça como uma viga engastada e livre, calculando:
     - Rigidez axial `EA _{eq}`.
     - Rigidez à flexão `EI _{eq}`.
     - Rigidez ao cisalhamento `GA _{eq}`.

3. **Cálculo de Deflexões:**
   - Determinar as deflexões (deslocamento / deformação) na extremidade da treliça para cada caso de carregamento, utilizando as fórmulas da viga equivalente:
     - Deflexão axial: \(u_{\text{ponta}} = \frac{FI}{(EA)_{eq}}\).
     - Deflexão transversal: \(v_{\text{ponta}} = \frac{FI^3}{3(EI)_{eq}} + \frac{FI}{(GA)_{eq}}\).
     - Deflexão devido a um momento: \(V_{\text{ponta}} = \frac{Cl^2}{2(EI)_{eq}}\).

4. **Validação do Modelo:**
   - Comparar os resultados obtidos pelo Método dos Elementos Finitos (MEF) com as deflexões calculadas pelo modelo de viga equivalente.
   - Estender a análise para uma treliça com dois painéis adicionais (\(I = 2,4 \, \text{m}\)) e validar os resultados.

5. **Apresentação dos Resultados:**
   - Organizar os dados em tabelas, incluindo:
     - Deslocamentos nodais.
     - Forças em cada elemento.
     - Comparação entre os resultados do MEF e do modelo de viga equivalente.
   - Representar graficamente a treliça e destacar as regiões críticas.

## :snake: Dependências

## :rescue_worker_helmet: Simulação

## :gear: Como rodar




