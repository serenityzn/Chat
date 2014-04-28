import gtk
from twisted.internet.protocol import Protocol, ClientCreator
from twisted.internet import gtk2reactor # for gtk-2.0
gtk2reactor.install() #this installs the gtk reactor

class MyProg(Protocol):

	button_send_data = []
	chat_msg = ""
	srv = ""
	chat = "====="
	
	def sendMessage(self, msg):
                self.transport.write("%s\n" % msg)
        def dataReceived(self, data):
		text=self.chat_msg.get_text()+"\r\n"+data
		self.chat_msg.set_text(text)
                print data

	def window(self):
                app_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
                app_window.set_size_request(500, 350)
                app_window.set_border_width(10)
                app_window.set_title("Chat Client")
                app_window.connect("delete_event", lambda w,e: gtk.main_quit())

                vbox_app = gtk.VBox(False, 0)
                app_window.add(vbox_app)
                vbox_app.show()
                app_window.show()
                return vbox_app
	
	def label(self, v, msg):
		label1 = gtk.Label(msg)
		label1.show()
		v.pack_start(label1, True, True, 0)
		self.chat_msg = label1
		test = label1

	def buttons(self, v):
		button_send = gtk.Button(stock=gtk.STOCK_CLOSE)
		data_a=self.button_send_data
		button_send.connect("clicked", self.button_send_callback, data_a)
		button_send.set_flags(gtk.CAN_DEFAULT)
		button_send.show()
		v.pack_start(button_send, True, True, 0)

	def entry(self, v):
		entry = gtk.Entry()
		entry.set_max_length(80)
		entry.set_width_chars(50)
		entry.connect("changed", self.enter_callback, entry)
		entry.show()
		v.pack_start(entry, True, True, 0)
		
	def __init__(self):
		v=self.window()
		lab=self.label(v,"")
		self.buttons(v)
		self.entry(v)
		return
	
	def enter_callback(self, widget, entry):
		text = entry.get_text()
		self.button_send_data = text
		print "text entry: %s\n"%text
		return
		
	def button_send_callback(self, widget, data_a):
		self.srv.sendMessage(self.button_send_data)
		return

 
def gotProtocol(p):
	MyProg.srv = p	
	
def main():
	from twisted.internet import reactor
	c = ClientCreator(reactor, MyProg)
	c.connectTCP("10.224.53.30", 8989).addCallback(gotProtocol)
	reactor.run()
	return 0

if __name__ == "__main__":
	main()

