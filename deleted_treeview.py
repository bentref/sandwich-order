treeview_liststore_0 = Gtk.ListStore(int, str, str)
treeview_liststore_0.append([1, "Ham Sandwich", "$6.99"])

treeview_liststore_1 = Gtk.TreeStore(int, str, str)
treeview_liststore_1.append([1, "Turkey Sandwich", "12.49"])
# Create the column renderers for the treeview
renderer_column_0 = Gtk.CellRendererText()
column_0 = Gtk.TreeViewColumn("#", renderer_column_0, text=0)

renderer_column_1 = Gtk.CellRendererText()
column_1 = Gtk.TreeViewColumn("Item", renderer_column_1, text=1)

renderer_column_2 = Gtk.CellRendererText()
column_2 = Gtk.TreeViewColumn("Price", renderer_column_2, text=2)


#Create and populate the treeview by appending columns
sandwichlist_treeview = Gtk.TreeView(model=treeview_liststore_0)
sandwichlist_treeview.append_column(column_0)
sandwichlist_treeview.append_column(column_1)
sandwichlist_treeview.append_column(column_2)
