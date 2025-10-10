import os
import random

from flask import Flask, render_template, request, redirect, url_for, session

# Use non-GUI backend for PythonAnywhere
import matplotlib

matplotlib.use('Agg')

from web_core import run_simulation, build_default_inputs, parse_form, U_LABELS


app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'change-me-in-production'


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        # Load or create defaults once per session
        defaults = session.get('defaults')
        if not defaults:
            defaults = build_default_inputs()
            session['defaults'] = defaults

        if request.method == 'POST':
            # Use submitted values; also persist as new defaults
            u, faks, equations, restrictions = parse_form(request.form)
            session['defaults'] = {
                'u': u,
                'faks': faks,
                'equations': equations,
                'u_restrictions': restrictions,
            }
            outputs = run_simulation(u, faks, equations, restrictions)
            return render_template('index.html', **outputs, ran=True, error=None, defaults=session['defaults'], u_labels=U_LABELS, values={
                'u': u, 'faks': faks, 'equations': equations, 'u_restrictions': restrictions
            })

        if request.args.get('run') == '1':
            # Re-generate random inputs and compute once
            defaults = build_default_inputs()
            session['defaults'] = defaults
            u, faks, equations, restrictions = defaults['u'], defaults['faks'], defaults['equations'], defaults['u_restrictions']
            outputs = run_simulation(u, faks, equations, restrictions)
            return render_template('index.html', **outputs, ran=True, error=None, defaults=defaults, u_labels=U_LABELS, values={
                'u': u, 'faks': faks, 'equations': equations, 'u_restrictions': restrictions
            })

        # Plain GET: just show current defaults without computing
        return render_template('index.html', ran=False, error=None, defaults=defaults, u_labels=U_LABELS)
    except Exception as exc:
        return render_template('index.html', ran=False, error=str(exc))


if __name__ == '__main__':
    # For local testing only; on PythonAnywhere, WSGI will import app
    app.run(host='0.0.0.0', port=5000, debug=True)


