from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
 
class Server(Protocol):
  name = ""
  clname = ""
  def getName(self):
	if self.name!="":
		return self.name
	return self.transport.getPeer().host

  def connectionMade(self):
	self.sendLine( "New connection from "+self.getName())
	self.factory.sendtoall(self.getName()+" has joined the chat.")
	self.factory.clientsProtocols[0].append(self)
	self.factory.clientsProtocols[1].append(self.getName())
	self.clname = self.getName()

  def sendLine(self, line):
	self.transport.write(line+"\r\n")

  def connectionLost(self, reason):
	print 'connecition lost from '+self.getName()
	self.factory.clientsProtocols[0].remove(self)
	self.factory.clientsProtocols[1].remove(self.getName())
	self.factory.sendtoall(self.getName()+" has left the chat..")
    
  def dataReceived(self, data):
	if data[:5] == "/exit":
		self.transport.loseConnection()
	elif data[:4] == "/to/":
		spl = data[4:].split(">")
		self.factory.sendprivate(spl[0], spl[1])
	elif data[:4] == "/me/":
		spl = data[4:].split("\r\n")
		self.clname = spl[0]
		
	else:
		self.factory.sendtoall("["+self.clname+"]"+data)
		
 
class ServerFactory(Factory):
	protocol = Server
	def __init__(self, quote=None):
		self.clientsProtocols = [[],[]]
		self.quote = quote 
	def sendtoall(self, msg):
		for client in self.clientsProtocols[0]:
			client.sendLine(msg)
	def sendprivate(self, cl, msg):
		index = self.clientsProtocols[2].index(cl)
		self.clientsProtocols[0][index].sendLine(msg)


reactor.listenTCP(8989, ServerFactory("quote"))
reactor.run()
