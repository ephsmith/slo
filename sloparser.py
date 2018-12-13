from io import StringIO
import csv
from flask import Flask
from flask import request
from flask import render_template
from flask import make_response


app = Flask(__name__)


def clone(s):
    headers = ["Name",          # 0
               "Student ID",    # 1
               "Start",         # 2
               "Finish",        # 3
               "Duration",      # 4
               "Correct",       # 5
               "Incorrect",     # 6
               "Not Attempted",  # 7
               ]
    data = []
    for row in s.split('\n'):
        r = [x for x in row.split('\t')]
        data.append(r)
    return headers, data


def logical_to_str(b):
    if b:
        return "0"
    else:
        return "1"


def parse(s):
    headers = ["Name",
               "Student ID",
               "Start",
               ]
    slos = ['SLO-{}.{}'.format(m, n) for m in range(1, 6) for n in range(1, 4)]
    headers.extend(slos)
    data = []

    for row in s.split('\n'):
        r = row.split('\t')
        data_row = [r[0], r[1], r[2]]
        if r[5] == "0" and r[6] == "0":
            incorrect = ["0" for slo in slos]
        else:
            incorrect = [logical_to_str(slo in r[6]) for slo in slos]
        data_row.extend(incorrect)
        data.append(data_row)
    return headers, data


def data_to_csv(d):
    x = [','.join(r) for r in d]
    return '\n'.join(x)


@app.route('/slo', methods=['POST', 'GET'])
def sloparser_app():
    if request.method == 'POST':
        headers, data = parse(request.form['pasted'])
        if request.form['operation'] == 'display':
            return render_template('index.html',
                                   data=data,
                                   headers=headers,
                                   pasted=request.form['pasted'])
        if request.form['operation'] == 'csv':
            si = StringIO()
            cw = csv.writer(si)
            all = [headers]
            all.extend(data)
            cw.writerows(all)
            out = make_response(si.getvalue())
            out.headers["Content-Disposition"] = "attachment;filename=export.csv"
            out.headers["Content-type"] = "text/csv"
            return out
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
