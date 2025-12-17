import wx
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def image_path(name):
    return os.path.join(BASE_DIR, name)


class HorrorGameFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Adventure of Mind", size=(900,800))

        self.has_key = False

        # ---------------- MAIN PANEL ----------------
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(5, 5, 5))
        self.panel = panel

        main = wx.BoxSizer(wx.VERTICAL)

        # -------- IMAGE --------
        self.image_ctrl = wx.StaticBitmap(panel)
        main.Add(self.image_ctrl, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        # -------- TITLE --------
        self.title_text = wx.StaticText(panel, label="")
        self.title_text.SetForegroundColour(wx.Colour(180, 0, 0))
        self.title_text.SetFont(
            wx.Font(28, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)
        )
        main.Add(self.title_text, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        # -------- STORY TEXT --------
        self.text = wx.StaticText(panel)
        self.text.SetForegroundColour(wx.Colour(230, 230, 230))
        self.text.SetFont(
            wx.Font(13, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        )
        self.text.Wrap(820)
        main.Add(self.text, 0, wx.ALL | wx.ALIGN_CENTER, 15)

        # -------- STATUS --------
        self.status = wx.StaticText(panel)
        self.status.SetForegroundColour(wx.Colour(255, 180, 0))
        main.Add(self.status, 0, wx.BOTTOM | wx.ALIGN_CENTER, 10)

        # ================= LEFT INSTRUCTION + RIGHT BUTTONS =================
        bottom_row = wx.BoxSizer(wx.HORIZONTAL)

        self.left_instruction = wx.StaticText(
            panel, label="Click on\nbuttons\nto navigate"
        )
        self.left_instruction.SetForegroundColour(wx.Colour(160, 160, 160))
        self.left_instruction.SetFont(
            wx.Font(11, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)
        )

        left_box = wx.BoxSizer(wx.VERTICAL)
        left_box.AddStretchSpacer(1)
        left_box.Add(self.left_instruction, 0, wx.ALIGN_CENTER)
        left_box.AddStretchSpacer(1)

        bottom_row.Add(left_box, 0, wx.LEFT | wx.RIGHT, 20)

        self.buttons = wx.BoxSizer(wx.VERTICAL)
        bottom_row.Add(self.buttons, 1, wx.EXPAND | wx.RIGHT, 20)

        main.Add(bottom_row, 0, wx.EXPAND | wx.BOTTOM, 20)
        panel.SetSizer(main)

        # ---------------- STORY ----------------
        self.story = {

            "start": {
                "text": (
                    "You were almost home.\n"
                    "Then the forest called."
                ),
                "image": "forest_gate.png",
                "choices": [("Enter the woods", "crossroads")]
            },

            "crossroads": {
                "text": "Three paths stretch into darkness.",
                "image": "crossroads.png",
                "choices": [
                    ("Cabin", "cabin_exterior"),
                    ("Graveyard", "graveyard"),
                    ("Well", "well")
                ]
            },

            # ---------- CABIN ----------
            "cabin_exterior": {
                "text": "An abandoned cabin stands alone.\nThe door creaks in the wind.",
                "image": "cabin_exterior.png",
                "choices": [
                    ("Enter the cabin", "cabin_inside"),
                    ("Go back", "crossroads")
                ]
            },

            "cabin_inside": {
                "text": "The door slams shut.\nA cupboard rattles.\nAnother door leads outside.",
                "image": "cabin_interior.png",
                "choices": [
                    ("OPEN CUPBOARD", "cupboard_end"),
                    ("OPEN DOOR", "magician_spell")
                ]
            },

            "cupboard_end": {
                "text": "A ghost lunges out.\nYou are dragged inside.\n\n🔴 BAD ENDING 🔴",
                "image": "monster.png",
                "end": True
            },

            "magician_spell": {
                "text": "A horrifying magician appears.\nHe casts a spell.",
                "image": "magician.png",
                "choices": [("Fall into darkness", "crossroads")]
            },

            # ---------- GRAVEYARD ----------
            "graveyard": {
                "text": "A silent graveyard.\nOne grave is freshly dug.",
                "image": "graveyard.png",
                "choices": [
                    ("Dig the grave", "grave_dig"),
                    ("Pray", "fake_grave_end"),
                    ("Run back", "crossroads")
                ]
            },

            "fake_grave_end": {
                "text": "A warm light surrounds you.\n🟡 ENDING 🟡",
                "image": "tombstone_closeup.png",
                "choices": [("Accept fate", "fake_grave_reveal")]
            },

            "fake_grave_reveal": {
                "text": (
                    "The light fades.\n"
                    "A whisper laughs:\n"
                    "\"Not yet.\""
                ),
                "image": "monster.png",
                "choices": [("Wake up", "crossroads")]
            },

            "grave_dig": {
                "text": "The soil is loose.",
                "image": "grave_dig.png",
                "choices": [("Dig deeper", "grave_end")]
            },

            "grave_end": {
                "text": "Hands grab you.\nThe lid slams shut.\n\n🔴 GRAVE ENDING 🔴",
                "image": "buried_dark.png",
                "end": True
            },

            # ---------- WELL ----------
            "well": {
                "text": "A stone well.\nA bucket hangs from a rope.",
                "image": "well.png",
                "choices": [
                    ("Lower the bucket", "well_bucket"),
                    ("Run blindly", "forest_run"),
                    ("Back away", "crossroads")
                ]
            },

            "well_bucket": {
                "text": "Inside the bucket is a rusted key.",
                "image": "key_in_bucket.png",
                "action": "get_key",
                "choices": [("Take key", "well")]
            },

            # ---------- RUN → GATE ----------
            "forest_run": {
                "text": "You run through the forest.",
                "image": "forest_run.png",
                "choices": [("Keep running", "gate")]
            },

            "gate": {
                "text": "",
                "image": "gate_escape.png",
                "dynamic": True
            },

            "road_escape": {
                "text": "🟢 ESCAPE ENDING 🟢",
                "image": "road_escape.png",
                "end": True
            }
        }

        self.load_scene("start")
        self.Centre()
        self.Show()

    # ---------------- HELPERS ----------------
    def load_image(self, name):
        path = image_path(name)
        if os.path.exists(path):
            img = wx.Image(path).Scale(650, 420)
            self.image_ctrl.SetBitmap(wx.Bitmap(img))
        else:
            self.image_ctrl.SetBitmap(wx.NullBitmap)

    def clear_buttons(self):
        self.buttons.Clear(True)

    def load_scene(self, scene):
        if scene not in self.story:
            self.load_scene("crossroads")
            return

        data = self.story[scene]
        self.clear_buttons()

        # -------- TITLE / INSTRUCTION --------
        if scene == "start":
            self.title_text.SetLabel("🩸 ADVENTURE OF MIND 🩸")
            self.left_instruction.Show(True)
        else:
            self.title_text.SetLabel("")
            self.left_instruction.Show(False)

        if data.get("action") == "get_key":
            self.has_key = True

        # -------- GATE LOGIC --------
        if scene == "gate":
            self.load_image("gate_escape.png")

            if self.has_key:
                self.text.SetLabel("The key fits.\nThe gate creaks open.")
                btn = wx.Button(self.panel, label="Run to the road", size=(-1, 45))
                btn.Bind(wx.EVT_BUTTON, lambda e: self.load_scene("road_escape"))
            else:
                self.text.SetLabel("The gate is locked.\nYou need something to open it.")
                btn = wx.Button(self.panel, label="Return to the well", size=(-1, 45))
                btn.Bind(wx.EVT_BUTTON, lambda e: self.load_scene("well"))

            self.buttons.Add(btn, 0, wx.EXPAND | wx.ALL, 6)
            self.status.SetLabel(f"Inventory: {'Key' if self.has_key else 'Empty'}")
            self.panel.Layout()
            return

        # -------- NORMAL SCENES --------
        self.load_image(data.get("image", ""))
        self.text.SetLabel(data.get("text", ""))
        self.text.Wrap(820)
        self.status.SetLabel(f"Inventory: {'Key' if self.has_key else 'Empty'}")

        # -------- ENDINGS --------
        if data.get("end"):
            if scene == "road_escape":
                self.has_key = False

            btn = wx.Button(self.panel, label="Restart", size=(-1, 45))
            btn.Bind(wx.EVT_BUTTON, lambda e: self.load_scene("start"))
            self.buttons.Add(btn, 0, wx.EXPAND | wx.ALL, 6)
            self.panel.Layout()
            return

        for label, nxt in data.get("choices", []):
            btn = wx.Button(self.panel, label=label, size=(-1, 45))
            btn.Bind(wx.EVT_BUTTON, lambda e, s=nxt: self.load_scene(s))
            self.buttons.Add(btn, 0, wx.EXPAND | wx.ALL, 6)

        self.panel.Layout()


class HorrorApp(wx.App):
    def OnInit(self):
        HorrorGameFrame()
        return True


if __name__ == "__main__":
    app = HorrorApp()
    app.MainLoop()
