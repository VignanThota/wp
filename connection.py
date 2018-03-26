from http.server import BaseHTTPRequestHandler, HTTPServer
from connectionDB import *
import cgi

class Articles(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			print(self.path)
			if self.path.endswith("/new_post"):
				print(self.path)
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				htmlCode = ""
				htmlCode='''
				<html>
					<head>
						<title>Micro Blog</title>
						<meta charset="utf-8" />
						<meta http-equiv="X-UA-Compatible" content="IE=edge">
						<title>Students</title>
						<meta name="viewport" content="width=device-width, initial-scale=1">
						<link rel="stylesheet" type="text/css" media="screen" href="main.css" />
						<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
						<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
						<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
						<link href="https://fonts.googleapis.com/css?family=Aclonica" rel="stylesheet">
					</head>
					<body>
						<form action='/new_post' method='POST'enctype='multipart/form-data'>
							<div class="container">
								<div class="row form-group" style="height: 75%">
									<h3>Micro Blog</h3>
									<input type="text" name="title" class="form-control" placeholder="Title"><br>
									<input type="text" name="message" class="form-control" placeholder="Message" style="height:300px ">
									<br><button type="submit" class="btn btn-warning">Submit</button>
								</div>
								<div class="row" style="height: 25%;background-color: yellow">
									<h3>Blog Posts</h3>
								</div>
									
							</div>
						</form>
					</body>
				</html>'''
				self.wfile.write(bytes(htmlCode,"UTF-8"))
				return
			if self.path.endswith("/show_entries"):
				# posts = session.query(Blog_Posts).all()
				output = ""
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				for i in session.query(Blog_Posts).order_by(Blog_Posts.Title):
					output += i.Title
					output += i.Message+'<br>'
					# output += i.Date+'<br>'
					output += "</br>"
					output += "</br></br></br>"
				output += "</body></html>"
				self.wfile.write(output.encode())
				return
		except IOError:
			self.send_error(404, 'File Not Found: %s' % self.path)

	def do_POST(self):
		try:
			if self.path.endswith('/new_post'):
				self.send_response(301)
				self.send_header('Content-type','text/html')
				self.end_headers()
				ctype, pdict = cgi.parse_header(self.headers['content-type'])
				pdict['boundary']=bytes(pdict['boundary'],"utf-8")
				if ctype == 'multipart/form-data':

					fields = cgi.parse_multipart(self.rfile,pdict)
					p_title = fields.get('title')
					p_msg =fields.get('message')
				t=p_title[0].decode()
				m=p_msg[0].decode()
				# print(t)
				# print(m)
				htmlCode=""
				htmlCode+="<html><head></head><body>"
				if len(t) == 0 or len(m) == 0:
					htmlCode+='''<h1 style ="color:red">Some details are missing</h1></body></html>'''
					self.wfile.write(bytes(htmlCode,"utf-8"))
					print(htmlCode)
				else:
					htmlCode = '<html><body>Data entered is stored and secured in DB</body></html>'
					self.wfile.write(bytes(htmlCode, "utf-8"))
					addPost(t,m)
					self.wfile.write(bytes(htmlCode, "utf-8"))
		except:
			pass



def main():
	try:
		port = 8800
		server = HTTPServer(('',port),Articles)
		print( "Web Server running on port %s" % port)
		server.serve_forever()
	except KeyboardInterrupt:
		print(" ^C entered, stopping web server....")
		server.socket.shutdown()

if __name__ == '__main__':
	main()