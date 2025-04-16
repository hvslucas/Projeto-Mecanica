import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Propriedades do material
E = 100e9  # Em pascal (Pa)
A = 1e-4   # Área da seção transversal (m²)
L = 0.3    # Comprimento (m)


# Mapeando os nós
nos = np.array([
    [0, 0], [0, L], [L, 0], [L, L], [2*L, 0], [2*L, L],
    [3*L, 0], [3*L, L], [4*L, 0], [4*L, L], [5*L, 0], [5*L, L],
    [6*L, 0], [6*L, L]
])



# Conexão dos elementos
elementos = [
    (0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 12),
    (1, 3), (3, 5), (5, 7), (7, 9), (9, 11), (11, 13),
    (0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13),
    (0, 3), (2, 5), (4, 7), (6, 9), (8, 11), (10, 13)
]


# Comprimento equivalente da viga
l_eq = 6 * L  # 1.8 m


# Casos a serem analisados:
casos = {
    "Caso A (Fx13 = Fx14 = 10kN)": {
        2*12: 10e3,
        2*13: 10e3
    },
    "Caso B (Fy13 = Fy14 = 10kN)": {
        2*12+1: 10e3,
        2*13+1: 10e3
    },
    "Caso C (Fx13 = 10kN, Fx14 = -10kN)": {
        2*12: 10e3,
        2*13: -10e3
    }
}


# Formatando a exibição do pandas
pd.set_option('display.float_format', '{:.10e}'.format)


# ===============================
# FUNÇÕES DE ANÁLISE DA TRELIÇA
# ===============================


# Fix: Adicionado nós como parâmetros
def matriz_rigidez_barra(no_i, no_j, E, A, nos=nos):
    xi, yi = nos[no_i]
    xj, yj = nos[no_j]
    dx, dy = xj - xi, yj - yi
    L_barra = np.sqrt(dx**2 + dy**2)
    c, s = dx / L_barra, dy / L_barra

    k = (E * A / L_barra) * np.array([
        [ c*c,  c*s, -c*c, -c*s],
        [ c*s,  s*s, -c*s, -s*s],
        [-c*c, -c*s,  c*c,  c*s],
        [-c*s, -s*s,  c*s,  s*s]
    ])
    return k



def montar_matriz_rigidez_global(nos=nos, elementos=elementos):
    n_nos = len(nos)
    gl = 2 * n_nos
    K = np.zeros((gl, gl))
    for i, j in elementos:
        ke = matriz_rigidez_barra(i, j, E, A, nos)
        indices = [2*i, 2*i+1, 2*j, 2*j+1]
        for a in range(4):
            for b in range(4):
                K[indices[a], indices[b]] += ke[a, b]
    return K


def resolver_sistema(K, forcas):
    gl_fixos = [0, 2, 3]  # Restrições: Nó 0 em X; Nó 1 em X e Y
    gl = K.shape[0]
    gl_livres = [i for i in range(gl) if i not in gl_fixos]

    F = np.zeros(gl)
    for gl_forca, valor in forcas.items():
        F[gl_forca] = valor

    K_red = K[np.ix_(gl_livres, gl_livres)]
    F_red = F[gl_livres]
    U_red = np.linalg.solve(K_red, F_red)

    U = np.zeros(gl)
    U[gl_livres] = U_red
    return U


def calcular_forcas_internas(U, nos=nos, elementos=elementos):
    forcas_internas = []
    for idx, (i, j) in enumerate(elementos):
        xi, yi = nos[i]
        xj, yj = nos[j]
        dx, dy = xj - xi, yj - yi
        L_barra = np.sqrt(dx**2 + dy**2)
        c, s = dx / L_barra, dy / L_barra

        u_i, u_j = U[2*i], U[2*j]
        v_i, v_j = U[2*i+1], U[2*j+1]
        delta_L = (u_j - u_i)*c + (v_j - v_i)*s
        N = (E * A / L_barra) * delta_L

        forcas_internas.append([f'B{idx+1}', N])

    return pd.DataFrame(forcas_internas, columns=['Barra', 'Força (N)'])


def plotar_trelica(U, df_forcas, caso_nome, amplificacao=50, nos=nos, elementos=elementos):
    plt.figure(figsize=(14, 7))
    for idx, (i, j) in enumerate(elementos):
        xi, yi = nos[i]
        xj, yj = nos[j]

        # Treliça original
        plt.plot([xi, xj], [yi, yj], 'k--', alpha=0.3)

        # Treliça deformada
        xi_def = xi + U[2*i] * amplificacao
        yi_def = yi + U[2*i+1] * amplificacao
        xj_def = xj + U[2*j] * amplificacao
        yj_def = yj + U[2*j+1] * amplificacao
        plt.plot([xi_def, xj_def], [yi_def, yj_def], 'r-', lw=1.5)

        # Forças internas
        N = df_forcas.iloc[idx, 1]
        cor = 'blue' if N > 0 else 'red'
        meio_x = (xi_def + xj_def)/2
        meio_y = (yi_def + yj_def)/2

        # Desenhando as direções das forças internas
        dx = xj_def - xi_def
        dy = yj_def - yi_def
        L_def = np.sqrt(dx**2 + dy**2)
        plt.arrow(meio_x, meio_y,
        dx/L_def * 0.2 * np.sign(N),
        dy/L_def * 0.2 * np.sign(N),
        color=cor, head_width=0.02)

        if "Caso B" in caso_nome:
            texto = f'{N:.2f} N'  # Notação normal
        else:
            texto = f'{N:.2e} N'  # Notação científica

        plt.text(meio_x, meio_y + 0.02, texto,
                 color=cor, ha='center', fontsize=8, fontweight='bold')

    plt.title(f'{caso_nome}\nTração (azul) e Compressão (vermelho)')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.axis('equal')
    plt.grid(True)
    plt.legend(handles=[
        Line2D([0], [0], color='blue', lw=2, label='Tração (> 0)'),
        Line2D([0], [0], color='red', lw=2, label='Compressão (< 0)')
    ], loc='upper right')
    plt.show()



def formatar_comparacao(titulo, valor_mef, valor_teorico, unidade="m"):
    """Formata a comparação no mesmo estilo das tabelas de forças internas"""
    diferenca = abs((valor_mef - valor_teorico)/valor_teorico)*100

    # Criar um DataFrame estilizado para a comparação
    df_comparacao = pd.DataFrame({
        'Método': ['MEF', 'Teórico', 'Diferença'],
        'Valor': [valor_mef, valor_teorico, diferenca],
        'Unidade': [unidade, unidade, '%']
    })

    # Função de formatação condicional
    def color_diff(val):
        color = 'red' if val > 5 else 'skyblue'  # Destaca diferenças > 5%
        return f'color: {color}; font-weight: bold'

    # Estilização
    styled = (df_comparacao.style
             .format({'Valor': '{:.3e}', 'Unidade': '{}'}, precision=3)
             .map(color_diff, subset=pd.IndexSlice[:, ['Valor']])
             .set_caption(titulo)
             .set_properties(**{'text-align': 'center'})
             .hide(axis='index'))

    display(styled)



def calcular_propriedades_equivalentes(resultados):

    U_A = resultados["Caso A (Fx13 = Fx14 = 10kN)"]
    u_medio_A = (U_A[2*12] + U_A[2*13]) / 2
    EA_eq = (10e3 * l_eq) / u_medio_A

    U_C = resultados["Caso C (Fx13 = 10kN, Fx14 = -10kN)"]
    v_medio_C = (U_C[2*12+1] + U_C[2*13+1]) / 2
    momento = 10e3 * L
    EI_eq = (momento * l_eq**2) / (2 * v_medio_C)

    U_B = resultados["Caso B (Fy13 = Fy14 = 10kN)"]
    v_medio_B = (U_B[2*12+1] + U_B[2*13+1]) / 2
    GA_eq = (10e3 * l_eq) / (v_medio_B - (10e3 * l_eq**3)/(3 * EI_eq))

    # Criar DataFrame com os resultados
    df_propriedades = pd.DataFrame({
        'Propriedade': ['EA equivalente', 'EI equivalente', 'GA equivalente'],
        'Valor': [EA_eq, EI_eq, GA_eq],
        'Unidade': ['N', 'N·m²', 'N']
    })

    # Função de formatação condicional
    def color_prop(val):
        return 'font-weight: black'

    # Estilização
    styled_props = (df_propriedades.style
                   .format({'Valor': '{:.3e}', 'Unidade': '{}'}, precision=3)
                   .map(color_prop)
                   .set_caption("PROPRIEDADES EQUIVALENTES DA TRELIÇA")
                   .set_properties(**{
                       'text-align': 'middle',
                   })
                   .set_table_styles([{
                       'selector': 'caption',
                       'props': [
                           ('font-size', '16px'),
                           ('font-weight', 'black'),
                           ('text-align', 'middle'),
                           ('color', '#0056b3')
                       ]
                   }]))

    display(styled_props)

    return EA_eq, EI_eq, GA_eq



def validar_com_trelica_extendida(resultados, EA_eq, EI_eq, GA_eq):

    # Adicionar 2 painéis extras (totalizando 8 painéis)
    nos_extendidos = np.vstack([nos, [[7*L, 0], [7*L, L], [8*L, 0], [8*L, L]]])
    elementos_extendidos = elementos + [
        (12, 14), (14, 16), (13, 15), (15, 17),
        (12, 13), (14, 15), (16, 17),
        (12, 15), (14, 17)
    ]

    l_extendido = 8 * L  # 2.4 m

    # Casos de carregamento na treliça estendida
    casos_extendidos = {
        "Caso A Extendido (Fx16 = Fx17 = 10kN)": {2*14: 10e3, 2*15: 10e3},
        "Caso B Extendido (Fy16 = Fy17 = 10kN)": {2*14+1: 10e3, 2*15+1: 10e3},
        "Caso C Extendido (Fx16 = 10kN, Fx17 = -10kN)": {2*14: 10e3, 2*15: -10e3}
    }

    # Simular e comparar
    for nome, forcas in casos_extendidos.items():
        K_ext = montar_matriz_rigidez_global(nos_extendidos, elementos_extendidos)
        U_ext = resolver_sistema(K_ext, forcas)

        # Calcular deflexões médias
        if "A" in nome:
            u_medio = (U_ext[2*14] + U_ext[2*15]) / 2
            u_teorico = (10e3 * l_extendido) / EA_eq
            formatar_comparacao(
                "\n\nComparação de Deflexão Axial (Caso A)",
                u_medio, u_teorico
            )

        elif "B" in nome:
            v_medio = (U_ext[2*14+1] + U_ext[2*15+1]) / 2
            v_teorico = (10e3 * l_extendido**3)/(3 * EI_eq) + (10e3 * l_extendido)/GA_eq
            formatar_comparacao(
                "\n\nComparação de Deflexão Transversal (Caso B)",
                v_medio, v_teorico
            )

        elif "C" in nome:
            v_medio = (U_ext[2*14+1] + U_ext[2*15+1]) / 2
            momento = 10e3 * L
            v_teorico = (momento * l_extendido**2)/(2 * EI_eq)
            formatar_comparacao(
                "\n\nComparação de Deflexão por Momento (Caso C)",
                v_medio, v_teorico
            )



# ========================
# EXECUÇÃO DOS CÁLCULOS
# ========================

resultados = {}

# Processar todos os casos de carregamento
for nome, forcas in casos.items():

    # Cálculos principais
    K = montar_matriz_rigidez_global()
    U = resolver_sistema(K, forcas)
    df_forcas = calcular_forcas_internas(U)

    # Armazena os resultados
    resultados[nome] = U

    # Exibição da tabela estilizada
    pd.set_option('display.max_rows', None)

    def color_forca(val):
        color = 'red' if val < 0 else 'skyblue'
        return f'color: {color}; font-weight: bold'

    if "Caso B" in nome:
        styled_df = (df_forcas.style
                    .map(color_forca, subset=['Força (N)'])
                    .format({'Força (N)': '{:.2f}'})
                    .set_caption(f"Forças Internas - {nome}"))
    else:
        styled_df = (df_forcas.style
                    .map(color_forca, subset=['Força (N)'])
                    .format({'Força (N)': '{:.2e}'})
                    .set_caption(f"Forças Internas - {nome}"))

    display(styled_df.set_properties(**{'text-align': 'center'}))

    # Gera os gráficos
    plotar_trelica(U, df_forcas, nome, amplificacao=50 if "Caso B" not in nome else 1)

# Cálculos finais
EA_eq, EI_eq, GA_eq = calcular_propriedades_equivalentes(resultados)

# Chamar a função de validação com a treliça extendida
validar_com_trelica_extendida(resultados, EA_eq, EI_eq, GA_eq)