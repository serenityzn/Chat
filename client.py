import gtk
from twisted.internet.protocol import Protocol, ClientCreator
from twisted.internet import gtk2reactor # for gtk-2.0
gtk2reactor.install() #this installs the gtk reactor

class MyProg(Protocol):
	button_send_data = []
	larr = ""
	text = ""

	def sendMessage(self, msg):
                self.transport.write("%s\n" % msg)

        def dataReceived(self, data):
                self.larr.get_buffer().insert_at_cursor(data)

	def window(self):
#                app_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		app_window =gtk.Dialog()
                app_window.set_size_request(500, 350)
                app_window.set_border_width(10)
                app_window.set_title("Chat Client")
                app_window.connect("delete_event", lambda w,e: gtk.main_quit())
                app_window.show()
                return app_window

	def entry(self, w):
                entry = gtk.Entry()
                entry.set_max_length(80)
                entry.set_width_chars(50)
                entry.connect("changed", self.enter_callback, entry)
                entry.show()
                w.vbox.pack_start(entry, True, True, 0)
		return entry

	def hbox(self,w):
		hb = gtk.HBox(False, 2)	
		w.add(hb)
		hb.show()
		return hb

	def table(self,w):
		tbl = gtk.Table(10, 10, False)
		tbl.set_row_spacings(10)
		tbl.set_col_spacings(10)
		w.add_with_viewport(tbl)
		tbl.show()
		return tbl

	def scroll(self,w):
		scroll_w = gtk.ScrolledWindow()
		scroll_w.set_border_width(1)
		scroll_w.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_ALWAYS)
		w.vbox.pack_start(scroll_w, True, True, 0)
		scroll_w.show()
		return scroll_w

	def button(self,w):
		btn = gtk.ToggleButton("Send Message")
		data_a = "btn_test"
		btn.connect("clicked", self.button_send_callback, data_a)
                btn.set_flags(gtk.CAN_DEFAULT)
		w.vbox.pack_start(btn, True, True, 2)
		btn.show()
		return btn
	
	def label(self,w):
		txt = gtk.TextView()
		txt.get_buffer().insert_at_cursor('asfsafa asfas \n')
		w.add(txt)
		txt.show()
		return txt
		
	def __init__(self):
		w = self.window()
		s = self.scroll(w)
		l = self.label(s)
		self.larr = l
		e = self.entry(w)
		b = self.button(w)
		
		return
	
	def enter_callback(self, widget, entry):
		text = entry.get_text()
		self.button_send_data = text
#		print "text entry: %s\n"%text
		return
		
	def button_send_callback(self, widget, data_a):
		self.sendMessage(self.button_send_data)
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

