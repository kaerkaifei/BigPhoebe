"""本地开发服务器:带 no-cache 头,改完代码刷新即生效。用法:python serve.py [端口]"""
import http.server
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


class Handler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"  # keep-alive:页面启动并发请求多,少建连接

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write(fmt % args + "\n")
        sys.stderr.flush()


if __name__ == "__main__":
    # 线程版:页面启动会并发拉 11 张贴图 + 音效,单线程 TCPServer(backlog=5)会拒掉部分连接
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"serving http://127.0.0.1:{PORT}/")
    httpd.serve_forever()
