import gi
import sendmail
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
# Define a couple global variables:
final_order = []
final_order_price = 0
aux_window_num = 0
aux_window_list = []
sandwich_number = 1
send_bool = False

def cancel_action(*args):
    # The function that is called when you press big red button
    # args[0] is the window that called the action
    if args[1] == main_window:
        main_window.destroy()
        for win in aux_window_list:
            win.destroy()
        Gtk.main_quit()
    else:
        args[1].destroy()

def new_sandwich(*args):
    # This is the function called when we pull up options to create new sandwich.
    # Note: it used to be `new_win = aux_window()` but the new_win variable is not used
    aux_window_list.append(aux_window())
   
def finish_order(*args):
    """
    Create the 'pretty' version of the order that will be emailed off,
    then end and send the order. buildpretty starts out as a list,
    will be converted to a string
    """
    buildpretty = []
    for num, item in enumerate(final_order):
        buildpretty.append(item.format_attrs())
    buildpretty = '\n'.join(buildpretty)
    buildpretty += ("Total Price: $" + str(final_order_price))
    print(buildpretty)
    if send_bool:
        # Send email only if that switch is toggled
        sendmail.send_order(buildpretty)
    Gtk.main_quit()
    main_window.destroy()

class mainwindow(Gtk.Window):
    def update_display_add(self, build_instance):
        """
        This will add a new item to the treeview. Items are added 1 at a time.
        `build_instance` is the instance of sandwich or drink class (current_build) that is passed from
        auxwindow.add_to_final()
        """
        name = build_instance.get_name()
        # Update the treeview: below
        item_to_list = [name, '$' + str(build_instance.price)]
        self.items_to_list.append(item_to_list)
        num = len(self.items_to_list) - 1
        # We assume that the addition is always at the end of the list. Thus, can simply get list length with len()
        item_to_list = [num] + item_to_list
        self.treeview_iters[num] = self.store_model.append(None, None)
        self.store_model.set(self.treeview_iters[num], [0,1,2], item_to_list)
        global final_order_price
        final_order_price += build_instance.price
        final_order_price = round(final_order_price, 2)
        price_label_text = "Total Price: $" + str(final_order_price)
        self.total_price_label.set_text(price_label_text)
        # button_grid.attach(total_price_label, 3, 0, 1, 1)
        self.show_all()
    def update_display_reload(self):
        """
        Basically, clear out the model (deleting all rows) and start over.
        """
        # Need to delete all treeview iters and clear out treestore.
        # Also clearing out items_to_list
        self.treeview_iters = {}
        self.items_to_list = []
        self.store_model.clear()
        # Re-calculate the price and re-create items_to_list based on items in final_order
        global final_order_price
        final_order_price = 0
        for build_instance in final_order:
            final_order_price += build_instance.price
            name = build_instance.get_name()
            item_to_list = [name, '$' + str(build_instance.price)]
            self.items_to_list.append(item_to_list)
        # Right here, still need to do iter on items_to_list to put them in the treeview again
        for num, item_to_list in enumerate(self.items_to_list):
            item_to_list = [num] + item_to_list
            self.treeview_iters[num] = self.store_model.append(None, None)
            self.store_model.set(self.treeview_iters[num], [0,1,2], item_to_list)
        final_order_price = round(final_order_price, 2)
        price_label_text = "Total Price: $" + str(final_order_price)
        self.total_price_label.set_text(price_label_text)
        self.show_all()
        self.resize(200, 100)
    def update_display_remove(self, *args):
        index = self.selected_item_in_tv
        index_int = int(index.to_string())
        del final_order[index_int]
        del self.items_to_list[index_int]
        index = self.store_model.get_iter(index)
        self.update_display_reload()
    def on_treeview_select(self, *args):
        """
        What is done when the selected row (item) in treeview changes.
        self.selected_item_in_tv is an integer, it is the number both in treeview and
        in items_to_list of the item selected.
        """
        self.selected_item_in_tv = args[1]
    def set_send_bool(self, *args):
        global send_bool
        send_bool = args[0].get_active()
    def __init__(self):
        Gtk.Window.__init__(self, title="Ben's BBQ and Foot Massage")
        self.set_default_size(200, 100)
        self.set_icon_from_file("sandwich Logo v2.svg.png")

        self.uicontainer = Gtk.Box(spacing=0, margin=12, orientation=Gtk.Orientation.VERTICAL)
        self.add(self.uicontainer)

        self.main_label = Gtk.Label()
        self.main_label.set_markup("<big><b>Your Items:</b></big>")
        self.uicontainer.pack_start(self.main_label, True, True, 0)

        # Create the liststore DATA and model. Append each item as a row
        self.store_model = Gtk.TreeStore(int, str, str)
        self.items_to_list = []
        self.treeview_iters = {}
        # self.update_treeview()
        # Create the actual view and render it
        self.main_treeview_view = Gtk.TreeView.new_with_model(self.store_model)
        self.main_treeview_view.set_activate_on_single_click(True)
        # self.main_treeview_render = Gtk.CellRendererText()
        self.column_label_list = ["#", "Item", "Price"]
        self.render_columns = []
        for i, label in enumerate(self.column_label_list):
            cell_renderer = Gtk.CellRendererText()
            self.main_treeview_view.append_column(Gtk.TreeViewColumn(label, cell_renderer, text=i))
            # The problem here was that text argument in Gtk.TreeViewColumn. I was binding all the columns
            # to just one item from the list. Actually, it needs to be a variable bc column 2 takes text 2, etc.
        self.uicontainer.pack_start(self.main_treeview_view, True, True, 0)
        self.main_treeview_view.connect("row-activated", self.on_treeview_select)

        self.button_grid = Gtk.Grid(margin_top=11)
        # self.button_grid.set_margin-top(11)
        self.uicontainer.pack_start(self.button_grid, True, True, 0)
        # Create the buttons that appear in the main window.
        # This was moved from the list_actions_buttons functions.
        self.icon_add = Gtk.Image(icon_name='list-add-symbolic')
        self.icon_remove = Gtk.Image(icon_name='list-remove-symbolic')
        self.add_button = Gtk.Button()
        # Add button below treeview: calls func new_sandwich
        self.add_button.connect("clicked", new_sandwich)
        self.add_button.set_image(self.icon_add)
        self.remove_button = Gtk.Button()
        self.remove_button.connect("clicked", self.update_display_remove)
        self.remove_button.set_image(self.icon_remove)
        self.button_grid.attach(self.add_button, 0, 0, 1, 1)
        self.button_grid.attach(self.remove_button, 1, 0, 1, 1)

        self.price_label_text = "Total Price: $" + str(final_order_price)
        self.total_price_label = Gtk.Label.new(self.price_label_text)
        self.total_price_label.set_margin_start(10)
        self.button_grid.attach(self.total_price_label, 3, 0, 1, 1)

        #    uicontainer.pack_start(order_box, True, True, 0)

        # order_view_list = Gtk.Label()# this is unused so I just commented it out. May delete
        self.buttonsbox = Gtk.Box(spacing=0, margin=12, orientation=Gtk.Orientation.HORIZONTAL)
        self.uicontainer.pack_start(self.buttonsbox, True, True, 0)
        
        self.switch = Gtk.Switch()
        self.switch.set_active(send_bool)
        self.switch.connect("notify::active", self.set_send_bool)
        self.switch.set_valign(Gtk.Align.CENTER)
        self.buttonsbox.pack_start(self.switch, True, True, 5)
        
        self.cancel = Gtk.Button(label="Cancel")
        self.cancel.connect("clicked", cancel_action, self)
        self.cancel.get_style_context().add_class("destructive-action")
        self.buttonsbox.pack_start(self.cancel, True, True, 5)
        self.submit = Gtk.Button(label="Submit Order")
        self.submit.connect("clicked", finish_order)
        # submit.connect("clicked", finish_order, True)
        self.submit.get_style_context().add_class("suggested-action")
        self.buttonsbox.pack_start(self.submit, True, True, 5)


class sandwich: 
    """
        available_options: the options that will be created in a new sandwich window.
        A multi-line dictionary. It's a class var b/c all new sandwiches offer
        the same stuff.
        First item in the list indicates whether it's single or multiple select,
        Second item is a dictionary, which functions as options_list.
        Each class has a base price. Values in dictionary add to the base price
        if an option is selected
        -------
        TODO?? Add a tooltip so when you hover over the option in aux_window,
        you see the extra price that a choice adds
    """
    
    available_options = { 
        "Bread": [False, {"Sourdough": 0, "Italian Flatbread": 2.25, "Whole Wheat": 0}],
        "Cheese": [False, {"Cheddar": 0, "Swiss": 0, "Pepperjack": 0, "St. Jorge": .75}],
        "Meat": [True, {"Roast Beef": 0, "Turkey": 0, "Grilled Chicken": 0, "Bat": 7.75}],
        "Toasted": [False, {"Yes": 0, "No": 0}],
        "Condiments": [True, {"Mustard": 0, "Mayo": 0, "Ketchup": 0, "Bacon Bits": 2, "Salt": 0, "Pepper": 0, "Secret Sauce": .5}],
    }
    def get_name(self):
        try:
            name = self.build_attrs['Meat'][0] + ' Sandwich'
        except:
            name = "Meatless Sandwich"
        return name
    def format_attrs(self):
        """ Return the human-readable string of options for the sandwich. There also needs
        to be a way to get the price in there.
        """
        returnstr = "## Sandwich\n"
        for key, value in self.build_attrs.items():
            if isinstance(value, list):
                returnstr += (key + ": ")
                for a in value:
                    returnstr += (a + ", ")
                returnstr += "\n"
            else:
                returnstr += (key + ": " + value + "\n")
        returnstr += ("Item Price: $" + str(self.price) + "\n")
            
        return returnstr
    
    def __init__(self):
        self.build_attrs = {}
        for category in self.available_options:
            if self.available_options[category][0]:
                # if it's a checklist (multiple True) add the category pre-emptively to build_attrs
                self.build_attrs[category] = []
        self.price = 6.99 # The base price, to be added to
        
        
    # added = False  # Has the sandwich actually been added, or is it in progress?

class drink:
    available_options = {
        "Drink": [False, {"Barbeque Water": 0, "McDonalds Sprite": 4.20, "Kombucha": 0}],
        "Size": [False, {"Small": 2.00, "Medium": 3.25, "Large": 4.00, "Big Gulp": 5.75}]
    }
    
    def get_name(self):
        name = self.build_attrs['Size'] + ' ' + self.build_attrs['Drink']
        return name
    def format_attrs(self):
        returnstr = '## ' + self.build_attrs['Size'] + ' Drink: ' + self.build_attrs['Drink'] + '\n'
        returnstr += ("Item Price: $" + str(self.price))
        return returnstr
    def __init__(self):
        self.build_attrs = {}
        for category in self.available_options:
            if self.available_options[category][0]:
                # if it's a checklist (multiple True) add the category pre-emptively to build_attrs
                self.build_attrs[category] = []
        self.price = 0

class aux_window(Gtk.Window):

    
    def destroy_window(self, item_clicked): # self explanatory
        del self.current_build
        self.destroy()    
    def set_val(self, selected_obj, category, label, multiple, list_obj, num):
        """
        Called when any option is clicked in the build window
        What set_val does: it adds the selected option to build_attrs.
        build_attrs is an instance var (dict) created by the sandwich class--
        so it resides inside current_build
        
        Arguments:
        - selected_obj: something like <Gtk.CheckButton object at...>
        - category: the category of the choice, i.e. "Bread"
        - label: the label of the selected option, i.e. "Sourdough"
        - multiple: bool, whether or not it is a multiple-select (checkboxes)
        - list_obj: the list that holds all the checkboxes
        - num: the number within the list that the clicked option is
        """
        # print(str(other_selfs))
        # print(str(category))
        # print(str(label))
        # print(str(multiple))
        if multiple:
            if list_obj[num].get_active():
                self.current_build.build_attrs[str(category)].append(label)
            else:
                if label in self.current_build.build_attrs[str(category)]:
                    self.current_build.build_attrs[str(category)].remove(label)
        else:
            self.current_build.build_attrs[str(category)] = label
        # print (self.current_build.build_attrs)
    
    def add_to_final(self, *args): # Add the item to final order. Tally price
        
        for category, value in self.current_build.build_attrs.items():
            if isinstance(value, str):
                self.current_build.price += self.current_build.available_options[category][1][value]
            if isinstance(value, list):
                for list_item in value:
                    self.current_build.price += self.current_build.available_options[category][1][list_item]
            # Find the price of each selected option, and add it to the price.
            # If the option is a single select, we can just look up the price of the label.
            # If it's a multiple (list) we have to iterate through the list, using each selected as list_item
            # Next: round price to 2 decimal places (money)
        self.current_build.price = round(self.current_build.price, 2)
            
        final_order.append(self.current_build)
        print("Final item added to order is..." + str(self.current_build.build_attrs))
        print("Price of the item is: " + str(self.current_build.price))
        main_window.update_display_add(self.current_build)
        self.destroy()
    def optionslist(self, multiple, options_list, name):
        # The function to list all the options for category: e.g. Meat: Ham, Turkey, etc.
        # Note: optionslist is the function, options_list is actually the dict
        option = []
        num = 0
        self.boxes[name] = Gtk.FlowBox() 
        # Has been switched to a flow box so that long strings of 
        # options will be broken into multiple lines.
        self.labels[name] = Gtk.Label()
        lnm = "<b>" + name + ": </b>"
        self.labels[name].set_markup(lnm)
        self.uicontainer.pack_start(self.labels[name], True, True, 0)
        self.uicontainer.pack_start(self.boxes[name], True, True, 0)
        
        # Instead of packing into a flowbox, we use add()
        #self.boxes[name].add(self.labels[name])
        
        
        if not multiple: # Radio button, single select
            for a in list(options_list.keys()):
                # If the option being added is the first, just add it.
                # If it's not, add it to the already defined one
                if num == 0:
                    option.append(Gtk.RadioButton.new_with_label_from_widget(None, a))
                else:
                    option.append(Gtk.RadioButton.new_with_label_from_widget(option[0], a))
                self.boxes[name].add(option[num])
                option[num].connect("toggled", self.set_val, name, a, False, option, num)
                option[num].set_active(True)
                option[0].set_active(True)
                num += 1
        if multiple: # Checklist
            for a in options_list:
            # Append the checkboxes to the list for that option so they are displayed in GUI
                option.append(Gtk.CheckButton.new_with_label(a))
                self.boxes[name].add(option[num])
                option[num].connect("toggled", self.set_val, name, a, True, option, num)
                num += 1
    def set_build_class(self, *args):
        """
        After changing the option in the dropdown build_class_select, this function changes the window
        to accomodate that build class. Args[0] is the clicked item
        """
        build_class = args[0].get_active_id()
        self.combo_box_container.destroy()
        self.populate(build_class)
    def populate(self, build_class):
        self.combo_box_container.destroy()
        self.uicontainer.set_size_request(300, -1)
        # ~ self.options_container = Gtk.Box(spacing=3, margin=15, orientation=Gtk.Orientation.VERTICAL)
        # ~ self.uicontainer.pack_start(self.options_container, False, True, 0)
        if build_class == "sandwich":
            self.current_build = sandwich() # current_build is an instance of sandwich
            # class. Won't be added to final_order until finalized
            self.headlabel = Gtk.Label()
            self.headlabel.set_markup("<big><b>Add a Sandwich</b></big>\n")
        
        if build_class == "drink":
            self.current_build = drink()
            self.headlabel = Gtk.Label()
            self.headlabel.set_markup("<big><b>Add a Drink</b></big>\n")
            
        
        self.boxes = {}
        self.labels = {}
        self.list_of_checked_options = []
        
        
        self.uicontainer.pack_start(self.headlabel, True, True, 5)
        # print(self.uicontainer.query_child_packing(self.headlabel))
        
        for key, value in self.current_build.available_options.items():
            # Instead of multiple optionslist calls, just run through the list provided with sandwich class
            # value[0] will be True or False, passed as multiple parameter
            # value[1] is being passed as the options_list parameter. It should look
            # like [{"Grilled Chicken": 2.00, "Ham": 3.00}] 
            self.optionslist(value[0], value[1], key)
        # TODO: Add a number input for quantity
        self.action_button_box = Gtk.Box(spacing=5, margin=0, orientation=Gtk.Orientation.HORIZONTAL)
        self.uicontainer.pack_end(self.action_button_box, True, True, 0)
        self.button_addsandwich = Gtk.Button.new_with_label("Add")
        self.button_addsandwich.get_style_context().add_class("suggested-action")
        self.button_addsandwich.connect("clicked", self.add_to_final)
        self.button_cancelsandwich = Gtk.Button.new_with_label("Cancel")
        self.button_cancelsandwich.connect("clicked", self.destroy_window)
        self.action_button_box.pack_start(self.button_cancelsandwich, True, True, 0)
        self.action_button_box.pack_start(self.button_addsandwich, True, True, 0)
        
        self.show_all() # Have to call this so it updates the window
    def __init__(self):
        """
        Create just the uicontainer and combo box at first. The other stuff will be created in 
        function populate(), and will be in its own box called options_container
        """
        Gtk.Window.__init__(self, title="Add New Item")
        self.uicontainer = Gtk.Box(spacing=3, margin=15, orientation=Gtk.Orientation.VERTICAL)
        self.add(self.uicontainer)
        self.combo_box_container = Gtk.Box(spacing=3, margin=15, orientation=Gtk.Orientation.VERTICAL)
        self.uicontainer.pack_start(self.combo_box_container, True, True, 5)
        self.build_class_select_label = Gtk.Label()
        self.build_class_select_label.set_markup("<b>Item Type to Add:</b>")
        self.build_class_select = Gtk.ComboBoxText.new()
        self.build_class_select.append("sandwich", "Sandwich")
        self.build_class_select.append("drink", "Drink")
        self.combo_box_container.pack_start(self.build_class_select_label, True, True, 0)
        self.combo_box_container.pack_start(self.build_class_select, False, True, 0)
        self.build_class_select.connect("changed", self.set_build_class)
        self.show_all()
        
        # All the rest of the populating of this window has been moved into the
        # function self.populate()



# Mainwindow has been made into a class. Create it here
main_window = mainwindow()

main_window.connect("delete-event", Gtk.main_quit)
main_window.show_all()


Gtk.main()
