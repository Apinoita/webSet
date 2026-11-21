import http.server

class counterServer(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == "/":
                file = open("client.html","r")
                string = ""
                for line in file:
                    string+=str(line)
                body = bytes(string,"utf-8")
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            elif self.path=="/favicon.ico":
                body = open("favicon.ico", "rb")
                body = body.read()
                self.send_response(200)
                self.send_header("Content-type", "image/x-icon")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            
            elif self.path.split("/")[1] == "cards":
                body = open("cards/"+self.path.split("/")[2], "rb")
                body = body.read()
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            
            else:
                self.send_response(404)
        except:
            self.send_response(404)
            
            

            
    
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        return super().end_headers()

servhttp = http.server.HTTPServer(('0.0.0.0',8000),counterServer)
servhttp.serve_forever()