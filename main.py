import network as nw

from tkinter import *
from tkinter import ttk

class PathFinder():
    def __init__(self, root):
        building_names = ("MC", "SLC", "M3", "DC", "PAC", "C2", "ESC", "B1", "B2", "STC", "QNC",
            "PHY", "EIT", "E3", "E2", "E5", "E7", "E6", "RCH", "CPH", "DWE", "NH",
            "ML", "AL", "HH", "TC", "SCH", "EV1", "EV2", "EV3",
            "GH", "LIB", "PAS", "COM", "GSC", "CSB", "ERC", "BMH", "EXP", "LHI")
        bridge_names = (
            ("SLC","PAC"), ("MC","DC"), ("MC","M3"), ("SLC","MC"), ("MC","DC"), ("DC","M3"),
            ("MC","QNC"), ("QNC","B2"), ("B2","STC"), ("B2","B1"), ("B1","STC"), ("B1","ESC"),
            ("DC","C2"), ("C2","ESC"), ("ESC","EIT"), ("EIT","E3"), ("DC","E3"), ("STC","NH"),
            ("E3","E5"), ("E5","E7"), ("E7","E6"), ("EIT","PHY"), ("E3","E2"), ("RCH","E2"),
            ("RCH","DWE"), ("DWE","E2"), ("E2","CPH"), ("DWE","CPH"), ("ML","AL"), ("ML","EV1"),
            ("EV1","AL"), ("EV1","EV2"), ("EV2","EV3"), ("ML","AL"), ("AL","HH"), ("AL","TC"),
            ("AL","TC"), ("HH","TC"), ("TC", "SCH"), ("BMH","EXP"), ("EXP","LHI"), ("CSB","GSC")
        )
        path_names = (
            ("LHI","SLC"), ("BMH","SLC"), ("BMH","M3"), ("BMH","ERC"), ("ERC","CSB"), ("CSB","M3"),
            ("ERC","M3"), ("CSB","COM"), ("COM","GSC"), ("GSC","DC"), ("NH","LIB"), ("NH","ML"),
            ("ML","LIB"), ("AL","LIB"), ("TC","LIB"), ("STC","LIB"), ("B1","LIB"), ("PHY","LIB"),
            ("RCH","LIB"), ("GH","LIB"), ("SCH","GH"), ("GH","DWE"), ("GH","RCH"), ("SCH","DWE"),
            ("PAS","HH"), ("EV2","PAS")
        )

        self.uw = nw.BuildingNetwork()
        self.uw.set_buildings([nw.Building(name) for name in building_names])
        self.uw.set_connections([self.make_bridge(self.uw, c[0], c[1]) for c in bridge_names]
            + [self.make_path(self.uw, c[0], c[1]) for c in path_names])

        edge_pad = 12
        global_pad = 3

        root.title("Waterloo Path Finder")

        mainframe = ttk.Frame(root, padding=(edge_pad))

        entry_title_label = ttk.Label(mainframe, text="Find path staying inside as much as possible")
        from_label = ttk.Label(mainframe, text="from")
        self.from_var = StringVar()
        from_entry = ttk.Entry(mainframe, textvariable=self.from_var)
        to_label = ttk.Label(mainframe, text="to")
        self.to_var = StringVar()
        to_entry = ttk.Entry(mainframe, textvariable=self.to_var)
        find_path_btn = ttk.Button(mainframe, text="Find shortest path", command=self.find_path)
        self.path_var = StringVar()
        result_title_label = ttk.Label(mainframe, text="Shortest path:")
        result_label = ttk.Label(mainframe, textvariable=self.path_var)

        mainframe.grid(column=0, row=0, sticky=(N,S,E,W))

        entry_title_label.grid(column=0, row=0, columnspan=2)
        from_label.grid(column=0, row=1, sticky=(E))
        from_entry.grid(column=1, row=1, sticky=(E,W))
        to_label.grid(column=0, row=2, sticky=(E))
        to_entry.grid(column=1, row=2, sticky=(E,W))
        find_path_btn.grid(column=0, row=3, columnspan=2)
        result_title_label.grid(column=0, row=4, sticky=(N,E))
        result_label.grid(column=1, row=4, sticky=(N))

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0,weight=1)
        mainframe.columnconfigure(1,weight=2)
        mainframe.rowconfigure(4,weight=1)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=global_pad,pady=global_pad)

    def make_bridge(self, network, b1, b2):
        return nw.Connection(network.get_building(b1), network.get_building(b2), 1)
    
    def make_path(self, network, b1, b2):
        return nw.Connection(network.get_building(b1), network.get_building(b2), 5)

    def find_path(self):
        try:
            b1 = self.uw.get_building(self.from_var.get())
            b2 = self.uw.get_building(self.to_var.get())
            path = self.uw.find_shortest_path(b1, b2)
            if path:
                path_str = " -> ".join([str(b) for b in path])
                self.path_var.set(path_str)
            else:
                self.path_var.set("No path found!")
        except:
            pass

def main():
    root = Tk()
    PathFinder(root)
    root.mainloop()

main()