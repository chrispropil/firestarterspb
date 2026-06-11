import os
import http.server
import socketserver
import sys

PORT = 8765
DIRECTORY = os.path.abspath("C:/firestarterspb/reports/html/pulled_143_evidence_viewer")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    # Disable caching to ensure browser fetches the fresh json
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def main():
    if not os.path.exists(DIRECTORY):
        print(f"Error: Directory {DIRECTORY} does not exist. Rebuild the viewer first.")
        sys.exit(1)
        
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("======================================================")
            print(f" FIRESTARTERSPB LOCAL VIEWER SERVER RUNNING")
            print(f" URL: http://127.0.0.1:{PORT}/index.html")
            print(f" Serving from: {DIRECTORY}")
            print(" Press Ctrl+C to stop.")
            print("======================================================")
            httpd.serve_forever()
    except OSError as e:
        print(f"[ERROR] Port {PORT} is already in use or socket error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStopping server...")
        sys.exit(0)

if __name__ == "__main__":
    main()
