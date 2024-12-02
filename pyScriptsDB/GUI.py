import wx
import mysql.connector

class DBInterface(wx.Frame): # dbinterface extends wx.frame

    def __init__(self):
        #Frame() Frame(parent, id=ID_ANY, title=EmptyString, pos=DefaultPosition, size=DefaultSize, style=DEFAULT_FRAME_STYLE, name=FrameNameStr)
        super(DBInterface, self).__init__(None, title="Coffee Shop", size=(600, 600))

        self.conn = None
        self.curr = None

        try:
            self.conn = mysql.connector.connect(user = 'root',
                                password = ' ',
                                host = 'localhost',
                                database = 'MyCoffeeShop'
                                )
            self.curr = self.conn.cursor()
        except Exception as e:
            print(f"Failed to connect: {e}")

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL) # this will put buttons vert

        # eventually can make a button func within the class that will control all these but
        button = wx.Button(pnl, label="Run Vegan Chicken Baugette Query")
        button.Bind(wx.EVT_BUTTON, self.button_click_baguette) # this is what creates the 'event' for the button to run on click
        vbox.Add(button, flag=wx.EXPAND | wx.ALL, border=10)

        button = wx.Button(pnl, label="Run Vegan Pastry")
        button.Bind(wx.EVT_BUTTON, self.button_click_pastry)
        vbox.Add(button, flag=wx.EXPAND | wx.ALL, border=10)

        pnl.SetSizer(vbox)
    
    def button_click_baguette(self, event):
        try:
            button = event.GetEventObject()
        
            query = """
            SELECT M.ItemName, I.IngredientName
            FROM Recipes as R
            JOIN Menu AS M ON R.MenuItemSkew = M.MenuItemSkew
            JOIN Ingredients AS I ON R.IngredientSkew = I.IngredientSkew
            WHERE M.ItemName = 'Vegan Chicken Baguette';
            """

            self.curr.execute(query)
            result = (self.curr.fetchall())

            query_frame = wx.Frame(self, title="Ingredients in Vegan Chicken Baguette", size=(400, 300))
            query_pnl = wx.Panel(query_frame)
            vbox = wx.BoxSizer(wx.VERTICAL)

            text = wx.TextCtrl(query_pnl, style=wx.TE_MULTILINE | wx.TE_READONLY)

            for row in result:
                ingredient = row[1]
                text.AppendText(f"{ingredient}\n")

            vbox.Add(text, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
            query_pnl.SetSizer(vbox)

            query_frame.Show()
        
        except Exception as e:
            print(f"error {e}")

    def button_click_pastry(self, event):
        try:
            button = event.GetEventObject()
        
            query = """
            SELECT PastryName
            FROM Pastries
            WHERE PastryName LIKE 'vegan%';
            """

            self.curr.execute(query)
            result = (self.curr.fetchall())

            query_frame = wx.Frame(self, title="Vegan Pastries:", size=(400, 300))
            query_pnl = wx.Panel(query_frame)
            vbox = wx.BoxSizer(wx.VERTICAL)

            text = wx.TextCtrl(query_pnl, style=wx.TE_MULTILINE | wx.TE_READONLY)

            for row in result:
                pastry = row[0]
                text.AppendText(f"{pastry}\n")

            vbox.Add(text, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
            query_pnl.SetSizer(vbox)

            query_frame.Show()
        
        except Exception as e:
            print(f"error {e}")


if __name__ == "__main__":
    app = wx.App()
    frm = DBInterface()
    frm.Show()
    app.MainLoop()