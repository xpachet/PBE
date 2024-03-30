import threading
import Rfid_PN532
import gi

gi.require_version('Gtk', '3.0') #Tria la versió 3.0 de GTK
from gi.repository import Gtk, Gdk, Gio, Glib

class Window(Gtk.Window):

	def __init__(self):
        
		self.PN532 = Rfid_PN532.Rfid_PN532()
		Gtk.Window.__init__(self, title = "PN532")
		Gtk.Window.set_default_size(self, 300, 50)
		self.set_resizable(False)
		self.connect("destroy", Gtk.main_quit)
		self.set_border_width(4)
        
        	#Estil
		self.style = Gtk.CssProvider()
		self.style.load_from_file(Gio.File.new_for_path("color.css"))
		self.screen = Gdk.Screen.get_default()
		self.context = Gtk.StyleContext()
		self.context.add_provider_for_screen(self.screen, self.style, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


		#Caixa principal
		self.caixa = Gtk.Box(orientation = "vertical")
		self.add(self.caixa)

		#Caixa label
		self.label_box = Gtk.Box()
		self.label_box.get_style_context().add_class("label-box-blue")
		self.label = Gtk.Label(label = "\nPlease, log in with your university card\n")
		self.label_box.pack_start(self.label, True, True, 0)

		#Caixa clear
		self.button_box = Gtk.Box()
		self.clear_button = Gtk.Button(label = "Clear")
		self.clear_button.connect("clicked", self.clear)
		self.button_box.pack_start(self.clear_button, True, True, 0)

		#Coloquem tot a la caixa principal
		self.caixa.pack_start(self.label_box, True, True,0)
		self.caixa.pack_start(self.button_box, True, True, 0)

		self.thread = threading.Thread(target = self.print_uid)
		self.thread.daemon = True
		self.thread.start()

	def clear(self, widget):

		self.label.set_label('\nPlease, log in with your university card\n')
		self.thread = threading.Thread(target = self.print_uid)
		self.thread.start()
		self.label_box.get_style_context().remove_clas("label-box-red")
		self.label_box.get_style_context().add_class("label-box-blue")

	def read_uid(self):
		uid = self.PN532.read_uid()
		GLib.idle_add(self.print_uid, uid)
	def print_uid(self, uid):
		self.label.set_label("\nUID: " + uid + "\n")
		self.label_box.get_style_context().remove_class("label-box-blue")
		self.label_box.get_style_context().add_class("label-box-red")

if __name__ == "__main__":

	win = Window()
	win.show_all()
	Gtk.main()
