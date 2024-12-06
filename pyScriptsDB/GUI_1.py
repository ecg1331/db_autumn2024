import wx
import wx.svg
import wx.lib.buttons as buttons
import mysql.connector
import wx.lib.agw.genericmessagedialog as GMD
from wx import Bitmap
import cairosvg  # Optional, for handling SVG if needed

class DBInterface(wx.Frame):
    def __init__(self, *args, **kw):
        super(DBInterface, self).__init__(*args, **kw)

        # Frame setup
        self.panel = wx.Panel(self)
        self.SetTitle("Coffee Shop")
        self.conn = None
        self.curr = None
        self.SetSize((850, 750))  # Set initial size of the window

        # Image path (replace with your actual image path)
        self.bg_image_path = "imgs/logo.png"  # Ensure this path is correct

        # Connect to the database
        self.connect_to_db()

        # Set up the welcome screen with a static image
        self.pnl = wx.Panel(self)
        self.pnl.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)  # Custom background style

        # Bind the resize event to rescale image
        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)

        # Create the welcome screen with a "Go to Main Screen" button
        self.show_welcome_screen()

        # Timer to transition from welcome to main screen after 3 seconds
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_start_button_click, self.timer)
        self.timer.Start(3000)  # 3-second delay to switch screens

    def connect_to_db(self):
        """Connect to the MySQL database."""
        try:
            self.conn = mysql.connector.connect(user='root',
                                                password='Salt%eeny7',
                                                host='localhost',
                                                database='MyCoffeeShop')
            self.curr = self.conn.cursor()
        except Exception as e:
            print(f"Failed to connect to the database: {e}")

    def show_welcome_screen(self):
        """Display the welcome screen with a background image and a 'Start' button."""
        self.pnl.Destroy()  # Remove any existing panels
        self.pnl = wx.Panel(self)
        self.pnl.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        # Set up the welcome screen content
        welcome_sizer = wx.BoxSizer(wx.VERTICAL)

        # Display welcome image
        self.bg_image = wx.Image(self.bg_image_path, wx.BITMAP_TYPE_PNG)
        self.bg_bitmap = wx.Bitmap(self.bg_image)

        # Display the background image
        wx.StaticBitmap(self.pnl, bitmap=self.bg_bitmap)

        # Add a 'Start' button
        start_button = wx.Button(self.pnl, label="Go to Main Screen", size=(200, 50))
        start_button.Bind(wx.EVT_BUTTON, self.on_start_button_click)

        welcome_sizer.Add(start_button, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        self.pnl.SetSizerAndFit(welcome_sizer)
        self.pnl.Layout()

    def on_erase_background(self, event):
        """Draw the background image on the welcome screen."""
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self.pnl)

        # Load the image and draw it
        img = wx.Image(self.bg_image_path, wx.BITMAP_TYPE_PNG)
        if img.IsOk():
            frame_width, frame_height = self.GetSize()
            img.Rescale(frame_width, frame_height)  # Resize image to fit the window size
            bmp = wx.Bitmap(img)
            dc.DrawBitmap(bmp, 0, 0)

    def on_resize(self, event):
        """Handle window resizing and rescale image accordingly."""
        self.Refresh()  # Trigger an erase event to redraw the background image
        event.Skip()

    def on_start_button_click(self, event):
        """Transition from the welcome screen to the main screen with buttons."""
        self.pnl.Destroy()  # Destroy the welcome panel

        # Create a new panel for the main screen
        self.pnl = wx.Panel(self)
        self.pnl.SetBackgroundColour(wx.Colour(247, 247, 244))  # Light background color

        # Create the main screen layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Add a title (optional)
        # title = wx.StaticText(self.pnl, label="Main Menu")
        # title.SetFont(wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        # title.SetForegroundColour(wx.Colour(0, 0, 0))  # Black text

        # main_sizer.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        # Create a panel for the buttons
        button_panel = wx.Panel(self.pnl)
        button_layout = wx.FlexGridSizer(2, 5, 10, 10)

        # Add 10 buttons with icons, titles, and descriptions
        for i in range(1, 11):
            button_icon = self.load_svg(f"imgs/icon{i}.svg")  # Load SVG icon
            button_title = f"Button {i}"
            button_description = f"Description for Button {i}"  # Customize this for each button
            if button_icon is not None:  # Check if the icon is valid
                icon_button_layout = self.create_icon_button(button_panel, button_icon, button_title, button_description)
                button_layout.Add(icon_button_layout, 0, wx.EXPAND | wx.ALL, border=5)

        button_panel.SetSizer(button_layout)
        button_panel.Layout()

        # Add the button panel to the main sizer
        main_sizer.Add(button_panel, 1, wx.EXPAND | wx.ALL, border=20)

        self.pnl.SetSizerAndFit(main_sizer)
        self.pnl.Layout()

        self.Centre()

    def create_icon_button(self, panel, icon, title, description):
        """Create a button with an icon, title, and description."""
        button = wx.BitmapButton(panel, bitmap=icon, size=(100, 100))
        button.Bind(wx.EVT_BUTTON, self.button_click)

        # Title text
        label = wx.StaticText(panel, label=title)
        label.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        label.SetForegroundColour(wx.Colour(0, 0, 0))  # Black text

        # Description text (smaller font for the description)
        description_label = wx.StaticText(panel, label=description)
        description_label.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        description_label.SetForegroundColour(wx.Colour(100, 100, 100))  # Grey text

        # Layout for the button (icon, title, and description)
        button_layout = wx.BoxSizer(wx.VERTICAL)
        button_layout.Add(label, 0, wx.EXPAND | wx.ALL, border=5)
        button_layout.Add(button, 0, wx.ALIGN_CENTER, border=10)
        button_layout.Add(description_label, 0, wx.EXPAND | wx.ALL, border=5)

        return button_layout

    def load_svg(self, svg_file_path):
        """Load an SVG file directly as a wx.Bitmap."""
        try:
            img = wx.Image(svg_file_path, wx.BITMAP_TYPE_SVG)
            if img.IsOk():
                return wx.Bitmap(img)
            else:
                print(f"Error: Invalid SVG file {svg_file_path}")
                return None
        except Exception as e:
            print(f"Error loading SVG: {e}")
            return None

    def button_click(self, event):
        """Handle button clicks."""
        print("Button clicked!")

if __name__ == "__main__":
    app = wx.App()
    frm = DBInterface(None, title="Coffee Shop", size=(850, 750))
    frm.Show()
    app.MainLoop()
