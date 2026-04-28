from pybeaut import Colorate, Colors, Center, Add, Banner, Write, System
from os import get_terminal_size


def sep(title):
    print(Colorate.Color(Colors.dark_gray, "─" * 55))
    print(Colorate.Color(Colors.white, f"  {title}"))
    print(Colorate.Color(Colors.dark_gray, "─" * 55))
    print()


def wait(label="next"):
    input(Colorate.Color(Colors.dark_gray, f"\n  [ screenshot done? Enter → {label} ] "))
    System.Clear()


# ── 1. Colorate · Static ─────────────────────────────────────────────────────
sep("1 · Colorate — Static color")
print(Colorate.Color(Colors.red,       "  This is red"))
print(Colorate.Color(Colors.green,     "  This is green"))
print(Colorate.Color(Colors.cyan,      "  This is cyan"))
print(Colorate.Color(Colors.orange,    "  This is orange"))
print(Colorate.Color(Colors.purple,    "  This is purple"))
print(Colorate.Color(Colors.yellow,    "  This is yellow"))
print(Colorate.Color(Colors.pink,      "  This is pink"))
print(Colorate.Color(Colors.turquoise, "  This is turquoise"))
print(Colorate.Color(Colors.light_red, "  This is light_red"))
print(Colorate.Color(Colors.dark_blue, "  This is dark_blue"))
wait("Vertical fade")

# ── 2. Colorate · Vertical ───────────────────────────────────────────────────
sep("2 · Colorate — Vertical fade")
text = (
    "Pybeaut vertical fade\n"
    "Every line shifts color\n"
    "Red bleeds into blue\n"
    "Smoothly, line by line"
)
print(Colorate.Vertical(Colors.red_to_blue, text))
wait("Horizontal fade")

# ── 3. Colorate · Horizontal ─────────────────────────────────────────────────
sep("3 · Colorate — Horizontal fade")
print(Colorate.Horizontal(Colors.blue_to_purple,
    "Horizontal fade — every character shifts color across the line!"))
wait("Diagonal fade")

# ── 4. Colorate · Diagonal ───────────────────────────────────────────────────
sep("4 · Colorate — Diagonal fade")
text = (
    "Diagonal color fade\n"
    "The gradient moves\n"
    "Across lines and chars\n"
    "Like a slanted rainbow"
)
print(Colorate.Diagonal(Colors.green_to_blue, text))
wait("Diagonal Backwards")

# ── 5. Colorate · DiagonalBackwards ──────────────────────────────────────────
sep("5 · Colorate — Diagonal Backwards")
text = (
    "Backwards diagonal\n"
    "Gradient reversed\n"
    "Right side is brighter"
)
print(Colorate.DiagonalBackwards(Colors.yellow_to_red, text))
wait("Format")

# ── 6. Colorate · Format ─────────────────────────────────────────────────────
sep("6 · Colorate — Format (accent chars)")
text = (
    "[ Pybeaut ]\n"
    "[ Colors  ]\n"
    "[ Format  ]"
)
print(Colorate.Format(
    text,
    second_chars=["[", "]"],
    mode=Colorate.Vertical,
    principal_col=Colors.blue_to_cyan,
    second_col=Colors.white
))
wait("Center XCenter")

# ── 7. Center · XCenter ──────────────────────────────────────────────────────
sep("7 · Center — XCenter")
logo = (
    "  ____        _                    _   \n"
    " |  _ \\ _   _| |__   ___  __ _ _  _| |_ \n"
    " | |_) | | | | '_ \\ / _ \\/ _` | | | | __|\n"
    " |  __/| |_| | |_) |  __/ (_| | |_| | |_ \n"
    " |_|    \\__, |_.__/ \\___|\\__,_|\\__,_|\\__|\n"
    "        |___/                             "
)
colored = Colorate.Vertical(Colors.blue_to_cyan, logo)
print(Center.XCenter(colored))
wait("TextAlign")

# ── 8. Center · TextAlign ────────────────────────────────────────────────────
sep("8 · Center — TextAlign")
text = "Short\nA longer line here\nMedium line"

print(Colorate.Color(Colors.dark_gray, "  --- CENTER ---"))
print(Colorate.Color(Colors.cyan, Center.TextAlign(text, align=Center.center)))
print()
print(Colorate.Color(Colors.dark_gray, "  --- RIGHT ---"))
print(Colorate.Color(Colors.yellow, Center.TextAlign(text, align=Center.right)))
wait("Add")

# ── 9. Add ───────────────────────────────────────────────────────────────────
sep("9 · Add — blocks side by side")
left = Colorate.Vertical(Colors.red_to_yellow,
    " ██████╗ \n"
    "██╔═══██╗\n"
    "██║   ██║\n"
    "╚██████╔╝\n"
    " ╚═════╝ "
)
right = Colorate.Vertical(Colors.blue_to_cyan,
    "██████╗ \n"
    "██╔══██╗\n"
    "██████╔╝\n"
    "██╔══██╗\n"
    "██████╔╝\n"
    "╚═════╝ "
)
print(Add.Add(left, right, center=True))
wait("Banner Lines")

# ── 10. Banner · Lines ───────────────────────────────────────────────────────
sep("10 · Banner — Lines")
print(Banner.Lines("Welcome to Pybeaut"))
wait("Banner Whale")

# ── 11. Banner · Whale ───────────────────────────────────────────────────────
sep("11 · Banner — ASCII art + centered text")
whale = r"""       .
      ":"
    ___:____     |"\/"|
  ,'        `.    \  /
  |  O        \___/  |
~^~^~^~^~^~^~^~^~^~^~^~^~"""

info = (
    "   Pybeaut    \n"
    "   v1.1.1     \n"
    "              \n"
    "   by Backist "
)
colored_whale = Colorate.Vertical(Colors.blue_to_cyan, whale)
colored_info  = Colorate.Vertical(Colors.cyan_to_blue, info)
print(Center.XCenter(Add.Add(colored_whale, colored_info, center=True)))
wait("Banner Arrow")

# ── 12. Banner · Arrow ───────────────────────────────────────────────────────
sep("12 · Banner — Arrow")
arrow = Banner.Arrow(icon='▶', size=2, number=3, direction='right')
print(Colorate.Vertical(Colors.green_to_cyan, arrow))
wait("Write.Print")

# ── 13. Write · Print ────────────────────────────────────────────────────────
sep("13 · Write — Print (animated typing)")
Write.Print(
    "\nWelcome to Pybeaut!\n"
    "Every character appears one by one\n"
    "with a smooth color fade.\n\n",
    Colors.blue_to_purple,
    interval=0.03
)
wait("Colors StaticRGB + StaticMIX")

# ── 14. Colors · StaticRGB & StaticMIX ──────────────────────────────────────
sep("14 · Colors — StaticRGB & StaticMIX")
salmon     = Colors.StaticRGB(250, 128, 114)
mint       = Colors.StaticRGB(152, 255, 152)
sky        = Colors.StaticRGB(135, 206, 235)
red_blue   = Colors.StaticMIX([Colors.red, Colors.blue])
cyan_green = Colors.StaticMIX([Colors.cyan, Colors.green])

print(Colorate.Color(salmon,     "  StaticRGB(250, 128, 114) — salmon"))
print(Colorate.Color(mint,       "  StaticRGB(152, 255, 152) — mint"))
print(Colorate.Color(sky,        "  StaticRGB(135, 206, 235) — sky"))
print(Colorate.Color(red_blue,   "  StaticMIX([red, blue])   — purple-ish"))
print(Colorate.Color(cyan_green, "  StaticMIX([cyan, green]) — teal-ish"))
wait("Boxes")

# ── 15. Boxes ────────────────────────────────────────────────────────────────
sep("15 · Boxes")
box_simple = Banner.SimpleCube("Hello, Pybeaut!")
print(Colorate.Color(Colors.cyan, box_simple))

box_double = Banner.Box(
    "Pybeaut\nDouble Box",
    up_left="╔═", up_right="═╗",
    down_left="╚═", down_right="═╝",
    left_line="║", right_line="║",
    up_line="═", down_line="═"
)
print(Colorate.Vertical(Colors.blue_to_cyan, box_double))

box_light = Banner.Box(
    "Custom\nBox Style",
    up_left="┌─", up_right="─┐",
    down_left="└─", down_right="─┘",
    left_line="│", right_line="│",
    up_line="─", down_line="─"
)
print(Colorate.Vertical(Colors.purple_to_blue, box_light))
wait("System")

# ── 16. System ───────────────────────────────────────────────────────────────
sep("16 · System")
System.Title("My Pybeaut App")
size = get_terminal_size()
print(Colorate.Color(Colors.cyan,   f"  Terminal size : {size.columns} cols × {size.lines} rows"))
print(Colorate.Color(Colors.yellow, f"  Windows       : {System.Windows}"))
if System.Windows:
    print(Colorate.Color(Colors.green, "  RGB support   : full (Windows 10/11)"))
else:
    print(Colorate.Color(Colors.orange, "  RGB support   : depends on terminal"))

print()
print(Colorate.Color(Colors.white, "  All done!"))
