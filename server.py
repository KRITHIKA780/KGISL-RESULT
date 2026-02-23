import http.server
import socketserver
import os

PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Remove query parameters for file checking
        path = self.path.split('?')[0]
        
        # If the path doesn't have an extension and is not a directory
        if not os.path.splitext(path)[1] and not path.endswith('/'):
            # Check if an .html version exists
            html_path = path.strip('/') + ".html"
            if os.path.exists(html_path):
                self.path = "/" + html_path
                # Keep original query parameters if they existed
                if '?' in self.path:
                    self.path += '?' + self.path.split('?')[1]
                    
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

handler = MyHandler

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"Server started at http://localhost:{PORT}")
    print("This server automatically handles URLs without .html (e.g., /faculty)")
    httpd.serve_forever()
