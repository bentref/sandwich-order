import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# class createwindow(Gtk.Window):
	# def __init__(self, wintitle, buttonname):
		# Gtk.Window.__init__(self, title=wintitle)
		# self.button = Gtk.Button(label=buttonname)
		# self.button.connect("clicked", self.showaux)
		# self.add(self.button)
	
	# def showaux(self, widget):
		# auxwindow = self.createwindow("Auxilliary Window", "Close")

def show_aux_window(self):
	auxwindow = createwindow("Aux Window", "No Way")
	auxwindow.show_all()

def print_text(self):
	text_to_print = main.textentry.get_text()
	print(text_to_print)
		
class createwindow(Gtk.Window):
	def __init__(self, wintitle, buttonname):
		Gtk.Window.__init__(self, title=wintitle)
		
		self.uicontainer = Gtk.Box(spacing=2, orientation=Gtk.Orientation.VERTICAL)
		self.add(self.uicontainer)
		
		self.button1 = Gtk.Button(label=buttonname)
		self.button1.connect("clicked", show_aux_window)
		self.uicontainer.pack_start(self.button1, True, True, 0)
		
		self.button2 = Gtk.Button(label="Print Text")
		self.button2.connect("clicked", print_text)
		self.uicontainer.pack_end(self.button2, True, True, 0)
		
		self.textlabel = Gtk.Label("Some Text Entry, My Good Man!!!")
		self.uicontainer.pack_start(self.textlabel, True, True, 5)
		
		self.textentry = Gtk.Entry()
		self.uicontainer.pack_start(self.textentry, True, True, 0)
		
		self.radiobox = Gtk.Box(spacing=2, orientation=Gtk.Orientation.VERTICAL)
		self.uicontainer.pack_end(self.radiobox, True, True, 5)
		
		self.radiolabel = Gtk.Label("Bread Type:")
		self.radiobox.pack_start(self.radiolabel, True, True, 0)
		
		self.radio1 = Gtk.RadioButton.new_with_label_from_widget(None, "Sourdough")
		self.radiobox.pack_start(self.radio1, True, True, 0)
		self.radio2 = Gtk.RadioButton.new_from_widget(self.radio1)
		self.radio2.set_label("Wheat")
		self.radiobox.pack_start(self.radio2, True, True, 0)
		self.radio3 = Gtk.RadioButton.new_from_widget(self.radio1)
		self.radio3.set_label("Italian Flatbread")
		self.radiobox.pack_start(self.radio3, True, True, 0)
		
		self.radio4 = Gtk.RadioButton.new_with_label_from_widget(self.radio1, "Austrian Seed")
		self.radiobox.pack_start(self.radio4, True, True, 0)
		

main = createwindow("Ginsterville Soul Tango", "Keyboard Solo")
main.connect("delete-event", Gtk.main_quit)
main.show_all()

Gtk.main()
