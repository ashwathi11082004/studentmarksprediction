import urllib.parse, webbrowser, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
data = pd.DataFrame({'hours': [3, 5, 7, 9, 10], 'marks': [50, 70, 80, 90, 100]})
x = data[['hours']]
y = data[['marks']]
model = LinearRegression()
model.fit(x, y)
class App(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/plot.png':
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(open('plot.png', 'rb').read())
            return
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        out = ""
        if 'hours' in q:
            h = float(q['hours'][0])
            result = model.predict([[h]])[0]
            print("predicted marks :", result)
            plt.scatter(x, y)
            plt.plot(x, model.predict(x))
            plt.scatter([h], [result], color='red')
            plt.xlabel('hours')
            plt.ylabel('marks')
            plt.savefig('plot.png')
            plt.clf()
            out = f"<h2>predicted marks : {result}</h2><img src='plot.png'>"

        page = f"<html><body><h1>student marks prediction</h1><form>enter study hours : <input type='number' step='any' name='hours' required><button>predict</button></form>{out}</body></html>"
        open('result.html', 'w').write(page)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(page.encode())

    def log_message(self, *args):
        pass

threading.Timer(0.5, lambda: webbrowser.open('http://localhost:8000')).start()
HTTPServer(('localhost', 8000), App).serve_forever()