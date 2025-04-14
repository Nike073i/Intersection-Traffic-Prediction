#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import psutil
import json
import time
from collections import deque

history = deque(maxlen=1000)

class MetricsHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        metrics = {
            "timestamp": int(time.time()),
            "cpu_usage": psutil.cpu_percent(),
            "ram_usage": psutil.virtual_memory().percent
        }
        history.append(metrics)
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(list(history)).encode()) 

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 9100), MetricsHandler)
    print("Сервер метрик запущен на http://localhost:9100")
    server.serve_forever()