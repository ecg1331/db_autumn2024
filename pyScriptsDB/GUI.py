import wx
import mysql.connector

# need to create more images for queries
# create query map

class DBInterface(wx.Frame): # dbinterface extends wx.frame

    def __init__(self):
        #Frame() Frame(parent, id=ID_ANY, title=EmptyString, pos=DefaultPosition, size=DefaultSize, style=DEFAULT_FRAME_STYLE, name=FrameNameStr)
        super(DBInterface, self).__init__(None, title="Coffee Shop", size=(850, 750))

        # attributes
        self.conn = None
        self.curr = None
        self.orange = wx.Colour(217, 89, 58) # orange color
        self.font = wx.Font(16, wx.BOLD, wx.NORMAL, wx.NORMAL, False, "Roboto Mini")

        # connecting
        self.connect_to_db()

        # panel
        self.pnl = wx.Panel(self)
        self.welcome_screen("imgs/logoLarge.png")



    def home_screen(self, event):
        '''
        enters to query menu upon mouse event
        '''

        mX, mY = event.GetPosition()
        print(f"{mX, mY}")


        event.Skip(False)
        self.pnl.Destroy()        # destroy old panel
        self.pnl = wx.Panel(self) # create new one
        self.pnl = wx.Panel(self, size=(850, 750))

        self.bg_bitmap = wx.StaticBitmap(self.pnl, bitmap = self.image_helper("imgs/hs2.png"))
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(self.bg_bitmap, 1, wx.ALIGN_CENTER, border=5)

        # Button panel
        button_panel = wx.Panel(self.pnl, size=(700, 475))
        button_panel.SetPosition((72, 90))
        button_panel.SetBackgroundColour(wx.Colour(247, 247, 244))

        # layout of buttons with the panel
        button_layout = wx.FlexGridSizer(2, 2, 10, 10)

        button1 = self.create_button(button_panel, "Name of Ingredients in Vegan Chicken Baguette", "Run Query", self.button_click_baguette)
        button_layout.Add(button1, 0, wx.ALIGN_CENTER  | wx.ALL, border=5)

        button2 = self.create_button(button_panel, "Name of Gluten Free Pastries", "Run Query", self.button_click_pastry)
        button_layout.Add(button2, 0, wx.ALIGN_CENTER | wx.ALL, border=5)

        button3 = self.create_button(button_panel, "Fantasy Books sold in 2023", "Run Query", self.button_click_fantasy_books)
        button_layout.Add(button3, 0, wx.ALIGN_CENTER | wx.ALL, border=5)

        button4 = self.create_button(button_panel, "Count of Number of Ingredients Per Item", "Run Query", self.button_click_ingredient)
        button_layout.Add(button4, 0, wx.ALIGN_CENTER | wx.ALL, border=5)

        button_panel.SetSizer(button_layout) 
        button_panel.Layout() 

        # Finalize the layout
        self.pnl.SetSizer(main_sizer)
        self.pnl.Layout()
        self.Centre()




    def create_button(self, button_panel, label_text, button_label, button_handler):
        '''
        Creates the button
        '''

        label = wx.StaticText(button_panel, label=label_text)
        label.SetForegroundColour(wx.Colour(180, 60, 58)) # has to be darker
        label.SetFont(self.font)

        button = wx.Button(button_panel, label=button_label, size = (100, 30))
        button.Bind(wx.EVT_BUTTON, button_handler)

        label_button = wx.BoxSizer(wx.VERTICAL)
        label_button.Add(label, 0, wx.EXPAND | wx.ALL, border=5)
        label_button.Add(button, 0, wx.ALIGN_CENTER, border= 10)

        return label_button
    


    def button_click_pastry(self, event):
        '''
        runs query for dietary pastries (can be used in place of allergens table)
        '''

        try:
            query = """
            SELECT PastryName
            FROM Pastries
            WHERE PastryName LIKE 'Gluten-Free%';
            """

            self.curr.execute(query)
            result = (self.curr.fetchall())

            query_frame = wx.Frame(self, title="Gluten Free Pastries:", size=(400, 300))
            query_pnl = wx.Panel(query_frame)
            query_pnl.SetBackgroundColour(self.orange)
            vbox = wx.BoxSizer(wx.VERTICAL)

            text = wx.TextCtrl(query_pnl, style=wx.TE_MULTILINE | wx.TE_READONLY)

            for row in result:
                pastry = row[0]
                text.AppendText(f"{pastry}\n")

            vbox.Add(text, proportion=2, flag=wx.EXPAND | wx.ALL, border=10)
            query_pnl.SetSizer(vbox)

            query_frame.Centre()
            query_frame.Show()
        
        except Exception as e:
            print(f"error {e}")
    
    
    def button_click_baguette(self, event):
        '''
        runs query for vegan chicken baguette
        '''

        try:
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
            query_pnl.SetBackgroundColour(self.orange)
            vbox = wx.BoxSizer(wx.VERTICAL)

            text = wx.TextCtrl(query_pnl, style=wx.TE_MULTILINE | wx.TE_READONLY)

            for row in result:
                ingredient = row[1]
                text.AppendText(f"{ingredient}\n")

            vbox.Add(text, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
            query_pnl.SetSizer(vbox)


            query_frame.Centre()
            query_frame.Show()
        
        except Exception as e:
            print(f"error {e}")
    

    def button_click_fantasy_books(self, event):
        '''
        runs query for fantasy books
        '''

        try:
            query = """
            SELECT B.Title
            FROM Books as B
            JOIN Skews AS S ON S.Skew = B.ISBN
            JOIN Sales_Item AS SI on SI.Item = S.Skew
            JOIN Sales AS SAL on SAL.Sale_ID = SI.Sale_ID
            WHERE B. Genre = 'Fantasy' AND YEAR(SAL.Sale_Date) = 2023;
            """
            self.curr.execute(query)
            result = (self.curr.fetchall())

            query_frame = wx.Frame(self, title="Fantasy Books Bought in 2023:", size=(400, 300))
            query_pnl = wx.Panel(query_frame)
            query_pnl.SetBackgroundColour(self.orange)
            vbox = wx.BoxSizer(wx.VERTICAL)

            text = wx.TextCtrl(query_pnl, style=wx.TE_MULTILINE | wx.TE_READONLY)

            for row in result:
                book = row[0]
                text.AppendText(f"{book}\n")

            vbox.Add(text, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
            query_pnl.SetSizer(vbox)

            query_frame.Centre()
            query_frame.Show()
        
        except Exception as e:
            print(f"error {e}")
    

    def button_click_ingredient(self, event):
        '''
        runs query for dietary pastries (can be used in place of allergens table)
        '''

        try:
            query = """
            SELECT M.ItemName, COUNT(I.IngredientName) AS IngredientCount
            FROM Recipes AS R
            JOIN Menu AS M ON R.MenuItemSkew = M.MenuItemSkew
            JOIN Ingredients AS I ON R.IngredientSkew = I.IngredientSkew
            GROUP BY M.ItemName
            ORDER BY M.ItemName;
            """

            self.curr.execute(query)
            result = (self.curr.fetchall())

            query_frame = wx.Frame(self, title="Number of Ingredients in Each Menu Item:", size=(400, 300))
            query_pnl = wx.Panel(query_frame)
            query_pnl.SetBackgroundColour(wx.Colour(217, 89, 58))
            vbox = wx.BoxSizer(wx.VERTICAL)

            text = wx.TextCtrl(query_pnl, style=wx.TE_MULTILINE | wx.TE_READONLY)

            for row in result:
                name = row[0]
                count = row[1]
                text.AppendText(f"{name}: {count}\n")

            vbox.Add(text, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
            query_pnl.SetSizer(vbox)

            query_frame.Centre()
            query_frame.Show()
        
        except Exception as e:
            print(f"error {e}")
    

    def image_helper(self, imgPath):
        '''
        helps load images - will add more images.
        '''
        
        img = wx.Image(imgPath, wx.BITMAP_TYPE_PNG)
        return wx.Bitmap(img)
    
    def connect_to_db(self):
        '''
        connects to database
        '''

        try:
            self.conn = mysql.connector.connect(user = 'root',
                                password = '',
                                host = 'localhost',
                                database = 'MyCoffeeShop'
                                )
            self.curr = self.conn.cursor()
        except Exception as e:
            print(f"Failed to connect: {e}")


    def welcome_screen(self, imgPath):
        '''
        loads welcome image and screen
        '''

        self.bg_bitmap = wx.StaticBitmap(self.pnl, bitmap = self.image_helper(imgPath))
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(self.bg_bitmap, 1, wx.ALIGN_CENTER, border=20)

        self.pnl.SetSizer(main_sizer)
        self.pnl.Layout()
        self.Centre()

        # binding to mouse event bc of img - cant make button transparent
        self.bg_bitmap.Bind(wx.EVT_LEFT_DOWN, self.home_screen)
    

if __name__ == "__main__":
    app = wx.App()
    frm = DBInterface()
    frm.Show()
    app.MainLoop()