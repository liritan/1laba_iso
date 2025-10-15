import os
import base64
import io
import numpy as np

# Use non-GUI backend for matplotlib in web context
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

try:
    from labellines import labelLines
except ImportError:
    def labelLines(*args, **kwargs):
        return None
from scipy.integrate import odeint

from functions import pend, fak_1, fak_2, fak_3, fak_4, fak_6, fak_7
from radar_diagram import RadarDiagram


U_LABELS = [
    "X1: качество",
    "X2: доступность", 
    "X3: завершенность",
    "X4: устойчивость к ошибкам",
    "X5: восстановляемость",
    "X6: сбои и отказы при работы системы",
    "X7: ошибки завершенности",
    "X8: отказы при работе программного обеспечения",
    "X9: сбои при работе программного обеспечения",
    "X10: отсутствие требований по восстановлению данных при отказах операционной системы и аппаратного обеспечения",
    "X11: потери данных при отказах операционной системы и аппаратного обеспечения",
    "X12: ошибка восстановления предшествующего состояния системы после повторного запуска программного обеспечения",
    "X13: отсутствие требований по восстановлению вычислительного процесса в случае сбоя операционной системы и аппаратного обеспечения",
    "X14: ошибка восстановления процесса в случае сбоев оборудования",
    "X15: ошибка восстановления данных в случае их искажений или разрушения",
    "X16: несоответствие требованиям стандартов, соглашений, законов или других предписаний, связанных с качеством",
    "X17: неполнота обработки ошибочных ситуаций",
    "X18: неполнота контроля корректности, полноты и непротиворечивости входных, выходных данных и баз данных",
    "X19: отсутствие возможности функционирования в сокращенном объеме в случае ошибок или помех",
    "X20: недостатки средств контроля работоспособности и диагностирования аппаратных и программных средств",
    "X21: отсутствие диагностического сообщения в случае сбоя или отказа",
    "X22: неполнота контроля непротиворечивости входных и баз данных",
    "X23: надежность системы"
]


def _fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('ascii')


def create_split_graphics(t, data, faks):
    """Create multiple smaller graphs instead of one large one"""
    figs_b64 = []
    
    # Graph 1: X1-X8
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    colors = plt.cm.tab10(np.linspace(0, 1, 8))
    for i in range(8):
        y_data = [max(0, v) for v in data[:, i]]
        ax1.plot(t, y_data, color=colors[i], label=f'X{i+1}', linewidth=1.5)
    ax1.set_xlabel("Время (t)")
    ax1.set_ylabel("Значения характеристик")
    ax1.set_title("Характеристики X1-X8")
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(bottom=0)
    figs_b64.append(_fig_to_base64(fig1))
    plt.close(fig1)
    
    # Graph 2: X9-X16  
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    colors = plt.cm.tab10(np.linspace(0, 1, 8))
    for i in range(8, 16):
        y_data = [max(0, v) for v in data[:, i]]
        ax2.plot(t, y_data, color=colors[i-8], label=f'X{i+1}', linewidth=1.5)
    ax2.set_xlabel("Время (t)")
    ax2.set_ylabel("Значения характеристик")
    ax2.set_title("Характеристики X9-X16")
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(bottom=0)
    figs_b64.append(_fig_to_base64(fig2))
    plt.close(fig2)
    
    # Graph 3: X17-X23
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    colors = plt.cm.tab10(np.linspace(0, 1, 7))
    for i in range(16, 23):
        y_data = [max(0, v) for v in data[:, i]]
        ax3.plot(t, y_data, color=colors[i-16], label=f'X{i+1}', linewidth=1.5)
    ax3.set_xlabel("Время (t)")
    ax3.set_ylabel("Значения характеристик")
    ax3.set_title("Характеристики X17-X23")
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(bottom=0)
    figs_b64.append(_fig_to_base64(fig3))
    plt.close(fig3)
    
    # Fak graph
    fig4 = draw_faks(t, faks)
    figs_b64.append(_fig_to_base64(fig4))
    plt.close(fig4)
    
    return figs_b64


def draw_faks(t, faks):
    fig, ax = plt.subplots(figsize=(10, 5))
    
    fak_functions = [fak_1, fak_2, fak_3, fak_4, fak_6, fak_7]
    fak_names = ['Fak1', 'Fak2', 'Fak3', 'Fak4', 'Fak6', 'Fak7']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for i, (fak_func, color, name) in enumerate(zip(fak_functions, colors, fak_names)):
        y_values = []
        for v in t:
            calculated_value = fak_func(v, faks[i])
            limited_value = max(0.0, min(1.0, calculated_value))
            y_values.append(limited_value)
        
        ax.plot(t, y_values, color=color, label=name, linewidth=1.5)
    
    ax.set_xlabel("Время (t)")
    ax.set_ylabel("Значения")
    ax.set_title("Графики возмущений")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.0)
    
    plt.tight_layout()
    return fig


def draw_radar_series(data, initial_equations, restrictions):
    radar = RadarDiagram()
    imgs = []
    
    # Use initial_equations for the red line (starting values)
    imgs.append(base64.b64encode(radar.draw_bytes(
        initial_equations, 
        [f"X{i+1}" for i in range(23)], 
        "Характеристики системы в начальный момент времени", 
        restrictions,
        initial_equations  # Pass initial values for red curve
    )).decode('ascii'))
    
    imgs.append(base64.b64encode(radar.draw_bytes(
        data[int(len(data) / 4)], 
        [f"X{i+1}" for i in range(23)], 
        "Характеристики системы в 1 четверти", 
        restrictions,
        initial_equations
    )).decode('ascii'))
    
    imgs.append(base64.b64encode(radar.draw_bytes(
        data[int(len(data) / 2)], 
        [f"X{i+1}" for i in range(23)], 
        "Характеристики системы во 2 четверти", 
        restrictions,
        initial_equations
    )).decode('ascii'))
    
    imgs.append(base64.b64encode(radar.draw_bytes(
        data[int(len(data) / 4 * 3)], 
        [f"X{i+1}" for i in range(23)], 
        "Характеристики системы в 3 четверти", 
        restrictions,
        initial_equations
    )).decode('ascii'))
    
    imgs.append(base64.b64encode(radar.draw_bytes(
        data[-1, :], 
        [f"X{i+1}" for i in range(23)], 
        "Характеристики системы в последний момент времени", 
        restrictions,
        initial_equations
    )).decode('ascii'))
    
    return imgs


def run_simulation(initial_equations, faks, equations, restrictions):
    t = np.linspace(0, 1, 100)
    data_sol = odeint(pend, initial_equations, t, args=(faks, equations))
    
    # Ensure no negative values
    data_sol = np.maximum(data_sol, 0)
    
    # Create split graphics
    figure_b64 = create_split_graphics(t, data_sol, faks)
    
    # Create radar diagrams
    radar_imgs = draw_radar_series(data_sol, initial_equations, restrictions)
    
    return {
        'images_b64': {
            'figure1': figure_b64[0],
            'figure2': figure_b64[1], 
            'figure3': figure_b64[2],
            'figure4': figure_b64[3],
            'diagram': radar_imgs[0],
            'diagram2': radar_imgs[1],
            'diagram3': radar_imgs[2],
            'diagram4': radar_imgs[3],
            'diagram5': radar_imgs[4],
        },
        'success': 'Расчет выполнен успешно!'
    }


def build_default_inputs():
    rng = np.random.default_rng()
    defaults = {
        'u': [round(float(rng.random() * 0.5 + 0.1), 2) for _ in range(23)],
        'u_restrictions': [round(float(rng.random() * 0.3 + 0.7), 2) for _ in range(23)],
        'faks': [],
        'equations': []
    }
    
    # Generate faks with values strictly in [0, 1] range
    for _ in [1, 2, 3, 4, 6, 7]:
        defaults['faks'].append([
            round(float(rng.random() * 0.8), 2),      # a: 0-0.8
            round(float(rng.random() * 0.6), 2),      # b: 0-0.6  
            round(float(rng.random() * 0.4), 2),      # c: 0-0.4
            round(float(rng.random() * 0.2 + 0.1), 2), # d: 0.1-0.3
        ])
    
    # Generate equations with smaller coefficients
    for _ in range(316):
        defaults['equations'].append([
            round(float(rng.random() * 0.1), 2),      # a: 0-0.1
            round(float(rng.random() * 0.15), 2),     # b: 0-0.15
            round(float(rng.random() * 0.2), 2),      # c: 0-0.2
            round(float(rng.random() * 0.1 + 0.05), 2), # d: 0.05-0.15
        ])
    
    return defaults


def parse_form(form):
    u = []
    u_restrictions = []
    for i in range(1, 24):
        u.append(float(form.get(f'u{i}', '0.1') or 0.1))
        u_restrictions.append(float(form.get(f'u_restrictions{i}', '1.0') or 1.0))

    fak_ids = [1, 2, 3, 4, 6, 7]
    faks = []
    for fid in fak_ids:
        a = float(form.get(f'fak{fid}_1', '0') or 0)
        b = float(form.get(f'fak{fid}_2', '0') or 0)
        c = float(form.get(f'fak{fid}_3', '0') or 0)
        d = float(form.get(f'fak{fid}_4', '0') or 0)
        faks.append([a, b, c, d])

    equations = []
    for i in range(1, 317):
        a = float(form.get(f'f{i}_1', '0') or 0)
        b = float(form.get(f'f{i}_2', '0') or 0)
        c = float(form.get(f'f{i}_3', '0') or 0)
        d = float(form.get(f'f{i}_4', '0') or 0)
        equations.append([a, b, c, d])

    return u, faks, equations, u_restrictions