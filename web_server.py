#!/usr/bin/env python3
"""
Simple web server with frontend and API
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import mimetypes

class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve frontend files
        if self.path == '/' or self.path == '/index.html':
            self.serve_file('static/index.html', 'text/html')
        elif self.path.startswith('/static/'):
            file_path = self.path[1:]  # Remove leading slash
            self.serve_file(file_path)
        # API endpoints
        elif self.path == '/api/health':
            self.send_json_response({"status": "healthy", "service": "SDLC Orchestrator"})
        elif self.path == '/api/agents':
            self.send_json_response({
                "agents": [
                    {"id": "claude", "name": "Claude", "status": "active"},
                    {"id": "gemini", "name": "Gemini", "status": "active"},
                    {"id": "openai", "name": "OpenAI", "status": "active"}
                ]
            })
        else:
            self.send_json_response({"error": "Not found"}, 404)
    
    def serve_file(self, file_path, content_type=None):
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            if not content_type:
                content_type, _ = mimetypes.guess_type(file_path)
                content_type = content_type or 'application/octet-stream'
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_json_response({"error": "File not found"}, 404)
    
    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 5000), WebHandler)
    print("🚀 SDLC Orchestrator running at:")
    print("   http://localhost:5000")
    print("   http://127.0.0.1:5000")
    print("   http://0.0.0.0:5000")
    server.serve_forever()