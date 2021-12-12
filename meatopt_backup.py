        meatopt1 = Gtk.RadioButton("Roast Beef")
        meat_box.pack_start(meatopt1, True, True, 1)

        meatopt2 = Gtk.RadioButton.new_with_label_from_widget(meatopt1, "Turkey")
        meat_box.pack_start(meatopt2, True, True, 1)

        meatopt3 = Gtk.RadioButton.new_with_label_from_widget(meatopt1, "Ham")
        meat_box.pack_start(meatopt3, True, True, 1)

        meatopt4 = Gtk.RadioButton.new_with_label_from_widget(meatopt1, "Tuna")
        meat_box.pack_start(meatopt4, True, True, 1)

#############################################
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def optionslist(listtype, options):
    num = 1
    if listtype == "Radio":
        for a in options:
            uicontainer.pack_start(label_meat, True, True, 0)
    if listtype == "Checkbox":
        for a in options:
            print(a)

class orderwindow(Gtk.Window):

   
    def __init__(self, wintitle, main):
        Gtk.Window.__init__(self, title=wintitle)
        
        uicontainer = Gtk.Box(spacing=0, margin=12, orientation=Gtk.Orientation.VERTICAL)
        self.add(uicontainer)
        
        headlabel = Gtk.Label()
        headlabel.set_markup("<big><b>Build Your Sandwich</b></big>\n")
        uicontainer.pack_start(headlabel, True, True, 5)
        
        bread_box = Gtk.Box(spacing=0, orientation=Gtk.Orientation.HORIZONTAL)
        bread_box.set_halign(Gtk.Align.START)
        uicontainer.pack_start(bread_box, True, True, 1)
        
        label_bread = Gtk.Label()
        label_bread.set_markup("<b>Bread Type:</b>")
        bread_box.pack_start(label_bread, True, False, 1)
        
        breadopt1 = Gtk.RadioButton.new_with_label_from_widget(None, "Sourdough")
        bread_box.pack_start(breadopt1, True, True, 1)
        
        breadopt2 = Gtk.RadioButton.new_with_label_from_widget(breadopt1, "Whole Wheat")
        bread_box.pack_start(breadopt2, True, True, 1)
        
        breadopt3 = Gtk.RadioButton.new_with_label_from_widget(breadopt1, "Italian Flatbread")
        bread_box.pack_start(breadopt3, True, True, 1)
        
        cheese_box = Gtk.Box(spacing=0, orientation=Gtk.Orientation.HORIZONTAL)
        cheese_box.set_halign(Gtk.Align.START)
        uicontainer.pack_start(cheese_box, True, True, 0.5)
        
        label_cheese = Gtk.Label()
        label_cheese.set_markup("<b>Cheese:</b>")
        cheese_box.pack_start(label_cheese, True, False, 1)
        
        cheeseopt1 = Gtk.RadioButton("Cheddar")
        cheese_box.pack_start(cheeseopt1, True, True, 1)
        
        cheeseopt2 = Gtk.RadioButton.new_with_label_from_widget(cheeseopt1, "Pepperjack")
        cheese_box.pack_start(cheeseopt2, True, True, 1)
        
        cheeseopt3 = Gtk.RadioButton.new_with_label_from_widget(cheeseopt1, "Swiss")
        cheese_box.pack_start(cheeseopt3, True, True, 1)
        
        meat_box = Gtk.Box(spacing=0, orientation=Gtk.Orientation.HORIZONTAL)
        meat_box.set_halign(Gtk.Align.START)
        uicontainer.pack_start(meat_box, True, True, 1)

        
        label_meat = Gtk.Label()
        label_meat.set_justify(Gtk.Justification.LEFT)
        label_meat.set_markup("<b>Meat: </b>")
#        meat_box.pack_start(label_meat, True, True, 1)
        
        meat_options = ["Roast Beef", "Turkey", "Grilled Chicken", "Ham"]
        optionslist("Radio", meat_options)
        
mainwindow = orderwindow("Main Sandwich Window", True)
mainwindow.connect("delete-event", Gtk.main_quit)
mainwindow.show_all()

Gtk.main()
