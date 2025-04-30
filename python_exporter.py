#!/usr/bin/env python3
import time
import psutil
from prometheus_client import start_http_server, Gauge
from http.server import BaseHTTPRequestHandler, HTTPServer

# Define Gauges
cpu_gauge = Gauge('system_cpu_percent', 'System CPU usage (%)')
mem_gauge = Gauge('system_memory_percent', 'System memory usage (%)')
disk_read = Gauge('system_disk_read_bytes', 'Disk read bytes')
disk_write = Gauge('system_disk_write_bytes', 'Disk write bytes')
net_sent = Gauge('system_network_bytes_sent', 'Network bytes sent')
net_recv = Gauge('system_network_bytes_recv', 'Network bytes received')

class StatusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK\n')
        else:
            self.send_response(404)
            self.end_headers()

def collect_metrics():
    cpu_gauge.set(psutil.cpu_percent(interval=1))
    mem_gauge.set(psutil.virtual_memory().percent)
    io = psutil.disk_io_counters()
    disk_read.set(io.read_bytes)
    disk_write.set(io.write_bytes)
    net = psutil.net_io_counters()
    net_sent.set(net.bytes_sent)
    net_recv.set(net.bytes_recv)

def run_http_server():
    status_server = HTTPServer(('', 8001), StatusHandler)
    status_server.serve_forever()

if __name__ == '__main__':
    # Start Prometheus metrics server on :8000/metrics
    start_http_server(8000)
    
    # Start status server in a separate thread
    from threading import Thread
    Thread(target=run_http_server, daemon=True).start()
    
    # Main metrics collection loop
    while True:
        collect_metrics()
        time.sleep(5)