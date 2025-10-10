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
    "качество",
    "доступность",
    "завершенность",
    "устойчивость к ошибкам",
    "восстановляемость",
    "ошибки надежды",
    "сбои и отказы при работы системы",
    "ошибки завершенности",
    "отказы при работе программного обеспечения",
    "сбои при работе программного обеспечения",
    "отсутствие требований по восстановлению данных при отказах операционной системы и аппаратного обеспечения",
    "потери данных при отказах операционной системы и аппаратного обеспечения",
    "ошибка восстановления предшествующего состояния системы после повторного запуска программного обеспечения",
    "отсутствие требований по восстановлению вычислительного процесса в случае сбоя операционной системы и аппаратного обеспечения",
    "ошибка восстановления процесса в случае сбоев оборудования",
    "ошибка восстановления данных в случае их искажений или разрушения",
    "несоответствие требованиям стандартов, соглашений, законов или других предписаний, связанных с качеством",
    "неполнота обработки ошибочных ситуаций",
    "неполнота контроля корректности, полноты и непротиворечивости входных, выходных данных и баз данных",
    "отсутствие возможности функционирования в сокращенном объеме в случае ошибок или помех",
    "недостатки средств контроля работоспособности и диагностирования аппаратных и программных средств",
    "отсутствие диагностического сообщения в случае сбоя или отказа",
    "неполнота контроля непротиворечивости входных и баз данных",
]


def _fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('ascii')


def create_graphic(t, data, faks):
    fig, axs = plt.subplots(figsize=(15, 10))
    plt.subplot(111)
    colors_styles = (
        ('g', '-'), ('c', '-'), ('r', '-'), ('y', '-'), ('m', '-'), ('b', '-'),
        ('teal', '-'), ('gray', '-'), ('olive', '-'), ('g', '--'), ('c', '--'),
        ('r', '--'), ('y', '--'), ('m', '--'), ('b', '--'), ('teal', '--'),
        ('gray', '--'), ('olive', '--'), ('g', '-.'), ('c', '-.'), ('r', '-.'),
        ('y', '-.'), ('m', '-.'),
    )
    for i in range(23):
        color, style = colors_styles[i]
        plt.plot(t, [0 if v < 0 else v for v in data[:, i]], color=color, linestyle=style, label=f"X{i + 1}")
    plt.xlabel("t, время", fontsize=14)
    plt.ylabel("Характеристики", fontsize=14)
    labelLines(plt.gca().get_lines(), fontsize=14)
    plt.xlim([0, 1])
    plt.ylim(bottom=0)
    plt.draw()
    # Also draw faks figure
    fig_x = fig
    fig2 = draw_faks(t, faks)
    return _fig_to_base64(fig_x), _fig_to_base64(fig2)


def draw_faks(t, faks):
    fig, axs = plt.subplots(figsize=(15, 10))
    plt.subplot(1, 1, 1)
    y1, y2, y3, y4, y5, y6 = [], [], [], [], [], []
    for v in t:
        y1.append(fak_1(v, faks[0]))
        y2.append(fak_2(v, faks[1]))
        y3.append(fak_3(v, faks[2]))
        y4.append(fak_4(v, faks[3]))
        y5.append(fak_6(v, faks[4]))
        y6.append(fak_7(v, faks[5]))
    plt.plot(t, y1, label='Fak1')
    plt.plot(t, y2, label='Fak2')
    plt.plot(t, y3, label='Fak3')
    plt.plot(t, y4, label='Fak4')
    plt.plot(t, y5, label='Fak6')
    plt.plot(t, y6, label='Fak7')
    plt.xlabel("t, время", fontsize=14)
    plt.ylabel("Возмущения", fontsize=14)
    labelLines(plt.gca().get_lines(), fontsize=14)
    plt.legend(loc='best')
    plt.draw()
    return fig


def draw_radar_series(data, initial_equations, restrictions):
    radar = RadarDiagram()
    imgs = []
    imgs.append(base64.b64encode(radar.draw_bytes(initial_equations, U_LABELS, "Характеристики системы в начальный момент времени", restrictions)).decode('ascii'))
    imgs.append(base64.b64encode(radar.draw_bytes(data[int(len(data) / 4)], U_LABELS, "Характеристики системы в 1 четверти", restrictions)).decode('ascii'))
    imgs.append(base64.b64encode(radar.draw_bytes(data[int(len(data) / 2)], U_LABELS, "Характеристики системы во 2 четверти", restrictions)).decode('ascii'))
    imgs.append(base64.b64encode(radar.draw_bytes(data[int(len(data) / 4 * 3)], U_LABELS, "Характеристики системы в 3 четверти", restrictions)).decode('ascii'))
    imgs.append(base64.b64encode(radar.draw_bytes(data[-1, :], U_LABELS, "Характеристики системы в последний момент времени", restrictions)).decode('ascii'))
    return imgs


def run_simulation(initial_equations, faks, equations, restrictions):
    t = np.linspace(0, 1)
    data_sol = odeint(pend, initial_equations, t, args=(faks, equations))
    fig1_b64, fig2_b64 = create_graphic(t, data_sol, faks)
    radar_imgs = draw_radar_series(data_sol, initial_equations, restrictions)
    return {
        'images_b64': {
            'figure': fig1_b64,
            'figure2': fig2_b64,
            'diagram': radar_imgs[0],
            'diagram2': radar_imgs[1],
            'diagram3': radar_imgs[2],
            'diagram4': radar_imgs[3],
            'diagram5': radar_imgs[4],
        }
    }


def build_default_inputs():
    rng = np.random.default_rng()
    defaults = {
        'u': [round(float(rng.random() * 0.7 + 0.01), 2) for _ in range(23)],
        'u_restrictions': [1.0 for _ in range(23)],
        'faks': [],
        'equations': []
    }
    for _ in [1, 2, 3, 4, 6, 7]:
        defaults['faks'].append([
            round(float(rng.random() * 0.7 + 0.01), 2),
            round(float(rng.random() * 0.7 + 0.01), 2),
            round(float(rng.random() * 0.7 + 0.01), 2),
            round(float(rng.random() * 0.7 + 0.01), 2),
        ])
    for _ in range(316):
        defaults['equations'].append([
            round(float(rng.random() * 0.7 + 0.01), 2),
            round(float(rng.random() * 0.7 + 0.01), 2),
            round(float(rng.random() * 0.7 + 0.01), 2),
            round(float(rng.random() * 0.7 + 0.01), 2),
        ])
    return defaults


def parse_form(form):
    # Parse initial equations u1..u23 and restrictions
    u = []
    u_restrictions = []
    for i in range(1, 24):
        u.append(float(form.get(f'u{i}', '0') or 0))
        u_restrictions.append(float(form.get(f'u_restrictions{i}', '1') or 1))

    # Parse faks: for ids [1,2,3,4,6,7], each has _1.._4
    fak_ids = [1, 2, 3, 4, 6, 7]
    faks = []
    for fid in fak_ids:
        a = float(form.get(f'fak{fid}_1', '0') or 0)
        b = float(form.get(f'fak{fid}_2', '0') or 0)
        c = float(form.get(f'fak{fid}_3', '0') or 0)
        d = float(form.get(f'fak{fid}_4', '0') or 0)
        faks.append([a, b, c, d])

    # Parse equations f1_1..f316_4
    equations = []
    for i in range(1, 317):
        a = float(form.get(f'f{i}_1', '0') or 0)
        b = float(form.get(f'f{i}_2', '0') or 0)
        c = float(form.get(f'f{i}_3', '0') or 0)
        d = float(form.get(f'f{i}_4', '0') or 0)
        equations.append([a, b, c, d])

    return u, faks, equations, u_restrictions


def build_random_inputs():
    # mimic the desktop UI defaults
    rng = np.random.default_rng()
    initial_equations = [round(float(rng.random() * 0.7 + 0.01), 2) for _ in range(23)]
    restrictions = [1.0 for _ in range(23)]
    faks = []
    for _ in [1, 2, 3, 4, 6, 7]:
        faks.append([
            round(float(rng.random() * 0.7 + 0.01), 2),
            round(float(rng.random() * 0.7 + 0.01), 2),
            round(float(rng.random() * 0.7 + 0.01), 2),
            round(float(rng.random() * 0.7 + 0.01), 2),
        ])
    equations = []
    for _ in range(316):
        equations.append([
            round(float(rng.random() * 0.7 + 0.01), 2),
            round(float(rng.random() * 0.7 + 0.01), 2),
            round(float(rng.random() * 0.7 + 0.01), 2),
            round(float(rng.random() * 0.7 + 0.01), 2),
        ])
    return initial_equations, faks, equations, restrictions


