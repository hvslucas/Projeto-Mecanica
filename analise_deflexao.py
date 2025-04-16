import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Parâmetros do material
E = 100e9  # Pa
A = 1e-4   # m²
L = 0.3    # m

# Coordenadas dos nós
nos = np.array([
    [0, 0],   [0, L],
    [L, 0],   [L, L],
    [2*L, 0], [2*L, L],
    [3*L, 0], [3*L, L],
    [4*L, 0], [4*L, L],
    [5*L, 0], [5*L, L],
    [6*L, 0], [6*L, L]
])

# Elementos conectando os nós (usando índices de 0 a 13)
elementos = [
    # Barras horizontais inferiores (de baixo)
    (0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 12),

    # Barras horizontais superiores (de cima)
    (1, 3), (3, 5), (5, 7), (7, 9), (9, 11), (11, 13),

    # Barras verticais (baixo para cima)
    (0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13),

    # Diagonais corrigidas (de baixo para cima à direita)
    (0, 3), (2, 5), (4, 7), (6, 9), (8, 11), (10, 13)
]


def matriz_rigidez_barra(nó_i, nó_j, E, A):
    xi, yi = nos[nó_i]
    xj, yj = nos[nó_j]
    dx = xj - xi
    dy = yj - yi
    # Módulo de L
    L = np.sqrt(dx**2 + dy**2)
    c = dx / L
    s = dy / L
    k = (E * A / L) * np.array([
        [c*c, c*s, -c*c, -c*s],
        [c*s, s*s, -c*s, -s*s],
        [-c*c, -c*s, c*c, c*s],
        [-c*s, -s*s, c*s, s*s]
    ])
    return k

def resolver_trelica(caso_nome, forcas):
    n_nos = len(nos)
    gl = 2 * n_nos
    K = np.zeros((gl, gl))

    # Montar a matriz de rigidez global
    for e in elementos:
        i, j = e
        ke = matriz_rigidez_barra(i, j, E, A)
        indices = [2*i, 2*i+1, 2*j, 2*j+1]
        for a in range(4):
            for b in range(4):
                K[indices[a], indices[b]] += ke[a, b]

    # Condições de contorno: nós 0 e 1 são engastados
    nos_fixos = [0, 1]
    gl_fixos = []
    for n in nos_fixos:
        gl_fixos.extend([2*n, 2*n+1])

    # Reduzir K e F
    F = np.zeros(gl)
    for g, valor in forcas.items():
        F[g] = valor

    K_red = np.delete(K, gl_fixos, axis=0)
    K_red = np.delete(K_red, gl_fixos, axis=1)
    F_red = np.delete(F, gl_fixos)

    # Resolver sistema
    U_red = np.linalg.solve(K_red, F_red)
    U = np.zeros(gl)
    U[np.setdiff1d(np.arange(gl), gl_fixos)] = U_red

    # DataFrame para armazenar as forças internas
    colunas = ['Nó', 'Deflexão X (m)', 'Deflexão Y (m)']
    deflexoes_nos = []

    # Cálculo das deflexões nos nós
    for i in range(n_nos):
        deflexao_x = U[2*i]  # Deflexão na direção X
        deflexao_y = U[2*i + 1]  # Deflexão na direção Y
        deflexoes_nos.append([i, deflexao_x, deflexao_y])

   # DataFrame para as deflexões nos nós
    df_deflexoes_nos = pd.DataFrame(deflexoes_nos, columns=colunas)

    # Configuração para exibir em notação científica completa
    pd.set_option('display.float_format', lambda x: '%.15e' % x)
    pd.set_option('display.max_columns', None)

    # Função para destacar valores significativos
    def highlight_significant(val):
        if isinstance(val, (float, np.floating)):
            return 'font-weight: bold' if abs(val) > 1e-10 else ''
        return ''

    # Estilização com notação científica
    styled_deflexoes = (df_deflexoes_nos.style
                       .format({'Deflexão X (m)': '{:.2e}',
                               'Deflexão Y (m)': '{:.2e}'})
                       .map(highlight_significant)
                       .set_properties(**{
                           'text-align': 'center',
                           'font-family': 'monospace',
                           'background-color': '#121212'
                       })
                       .set_table_styles([{
                           'selector': 'caption',
                           'props': [
                               ('font-size', '14px'),
                               ('font-weight', 'bold'),
                               ('color', '#121212')
                           ]
                       }, {
                           'selector': 'th',
                           'props': [
                               ('background-color', '#6a9eff20'),
                               ('color', '#4fc3f7')
                           ]
                       }]))

    display(styled_deflexoes)

    # Plotando a treliça original e deformada apenas nos nós
    amplificacao = 1 if "Caso B" in caso_nome else 51
    plt.figure(figsize=(10, 4))

    # Plotando os nós
    for i, (x, y) in enumerate(nos):
        plt.plot(x, y, 'bo')  # Nós originais (azul)
        plt.text(x + 0.01, y + 0.01, str(i), fontsize=9, color='blue')

    # Plotando os nós deformados
    for i in range(len(nos)):
        dx = U[2*i] * amplificacao
        dy = U[2*i + 1] * amplificacao
        x_def = nos[i][0] + dx
        y_def = nos[i][1] + dy
        plt.plot(x_def, y_def, 'ro', markersize=5)  # Nós deformados (vermelho)
        plt.text(x_def + 0.01, y_def + 0.01, f'{i}d', fontsize=9, color='red')

    # Adicionando título e configurações do gráfico
    plt.title(f'Treliça - {caso_nome}')
    plt.axis('equal')
    plt.grid(True)
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.show()

    return U


    # Casos de carregamento
casos = {
    "Caso A (Fx13 = Fx14 = 10kN)": {
        2*12: 10e3,  # Fx13
        2*13: 10e3   # Fx14
    },
    "Caso B (Fy13 = Fy14 = 10kN)": {
        2*12+1: 10e3,  # Fy13
        2*13+1: 10e3   # Fy14
    },
    "Caso C (Fx13 = 10kN, Fx14 = -10kN)": {
        2*12: 10e3,    # Fx13
        2*13: -10e3    # Fx14
    }
}

resultados = {}

for nome, forcas in casos.items():
    # Para visualização, escolhemos uma amplificação (use 1 para Caso B se desejar ver os deslocamentos reais)
    amplif = 1 if "Caso B" in nome else 51
    U = resolver_trelica(nome, forcas)
    resultados[nome] = U