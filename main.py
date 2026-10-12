import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, Line
from kivy.core.window import Window
from kivy.utils import platform

# Mobile preview window size on PC only (Android-e eta lagbe na)
if platform not in ('android', 'ios'):
    Window.size = (360, 640)

# --- Font setup ---
# DejaVuSans.ttf ta main.py-r pashe rakho (superscript/subscript/symbol er jonno)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_font_path = os.path.join(BASE_DIR, 'DejaVuSans.ttf')
FONT = _font_path if os.path.exists(_font_path) else 'Roboto'

# --- Comprehensive Class 7 to 10 Formula Database ---
MATH_DATABASE = {
    "Class 7 & 8: Arithmetic & Basics": {
        "Percentage & Profit-Loss": [
            ("Percentage Formula", "Percentage = (Value / Total Value) × 100"),
            ("Profit & Loss", "Profit = Selling Price (SP) - Cost Price (CP)\nLoss = CP - SP\nProfit % = (Profit / CP) × 100\nLoss % = (Loss / CP) × 100"),
            ("Simple Interest", "SI = (P × R × T) / 100\n(P = Principal, R = Rate, T = Time)")
        ],
        "Exponents & Radicals": [
            ("Laws of Indices", "aᵐ × aⁿ = aᵐ⁺ⁿ\naᵐ / aⁿ = aᵐ⁻ⁿ\n(aᵐ)ⁿ = aᵐⁿ\na⁰ = 1\na⁻¹ = 1/a")
        ]
    },
    "Class 9: Algebra & Geometry": {
        "Algebraic Identities": [
            ("Basic Squares", "(a + b)² = a² + 2ab + b²\n(a - b)² = a² - 2ab + b²\na² - b² = (a + b)(a - b)"),
            ("Extended Squares", "(a + b + c)² = a² + b² + c² + 2ab + 2bc + 2ca"),
            ("Cubic Identities", "(a + b)³ = a³ + b³ + 3ab(a + b)\n(a - b)³ = a³ - b³ - 3ab(a - b)\na³ + b³ = (a + b)(a² - ab + b²)\na³ - b³ = (a - b)(a² + ab + b²)")
        ],
        "Lines & Triangles": [
            ("Triangle Properties", "Sum of angles in a triangle = 180°\nArea of Triangle = ½ × base × height\nHeron's Formula = √[s(s-a)(s-b)(s-c)]\n(where s = (a+b+c)/2)")
        ]
    },
    "Class 10: Advanced Algebra & Trig": {
        "Quadratic Equations & AP": [
            ("Quadratic Formula", "For ax² + bx + c = 0:\nx = [-b ± √(b² - 4ac)] / 2a\nDiscriminant (D) = b² - 4ac"),
            ("Arithmetic Progression (AP)", "n-th term: aₙ = a + (n - 1)d\nSum of n terms: Sₙ = (n/2)[2a + (n - 1)d]")
        ],
        "Trigonometry": [
            ("Trig Ratios", "sin θ = Perpendicular / Hypotenuse\ncos θ = Base / Hypotenuse\ntan θ = Perpendicular / Base"),
            ("Trig Identities", "sin²θ + cos²θ = 1\n1 + tan²θ = sec²θ\n1 + cot²θ = cosec²θ")
        ],
        "Mensuration (Surface Area & Volume)": [
            ("Cylinder & Cone", "Cylinder Volume = πr²h\nCylinder CSA = 2πrh\nCone Volume = ⅓πr²h\nCone Slant Height (l) = √(r² + h²)"),
            ("Sphere & Cuboid", "Sphere Volume = (4/3)πr³\nSphere Surface Area = 4πr²\nCuboid Volume = l × b × h\nCuboid Total Surface Area = 2(lb + bh + hl)")
        ]
    }
}


class NotebookWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(NotebookWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Notebook Paper Background & Rules Drawing
        with self.canvas.before:
            Color(0.98, 0.96, 0.90, 1)  # Cream paper color
            self.bg = Rectangle(pos=self.pos, size=self.size)

            # Red Margin Line (bamer lal dag)
            Color(0.9, 0.3, 0.3, 1)
            self.margin_line = Line(points=[35, 0, 35, 3000], width=1.5)

            # Blue Ruled Lines (kagojer horizontal lines)
            Color(0.7, 0.8, 0.9, 0.4)
            self.ruled_lines = []
            for y in range(0, 3000, 30):
                ln = Line(points=[0, y, 3000, y], width=1)
                self.ruled_lines.append(ln)

        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


class MathApp(App):
    def build(self):
        self.title = 'Smart Math Notebook'
        self.root_layout = NotebookWidget()
        self.show_main_menu()
        return self.root_layout

    def clear_screen(self):
        self.root_layout.clear_widgets()

    def show_main_menu(self):
        self.clear_screen()
        main_box = BoxLayout(orientation='vertical', padding=[45, 20, 20, 20], spacing=15)

        # Title
        title = Label(
            text='[b]Smart Math Notebook[/b]\n[i]Class 7 to 10 Complete Formulas[/i]',
            markup=True, font_size=18, color=(0.1, 0.2, 0.5, 1),
            size_hint_y=None, height=70, halign='center', valign='middle',
            font_name=FONT
        )
        title.bind(size=title.setter('text_size'))
        main_box.add_widget(title)

        scroll = ScrollView()
        box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15)
        box.bind(minimum_height=box.setter('height'))

        for level in MATH_DATABASE.keys():
            btn = Button(
                text=level, font_size=15, size_hint_y=None, height=60,
                background_color=(0.2, 0.4, 0.7, 1), font_name=FONT
            )
            btn.bind(on_press=lambda x, lvl=level: self.show_sub_menu(lvl))
            box.add_widget(btn)

        scroll.add_widget(box)
        main_box.add_widget(scroll)
        self.root_layout.add_widget(main_box)

    def show_sub_menu(self, level_name):
        self.clear_screen()
        main_box = BoxLayout(orientation='vertical', padding=[45, 20, 20, 20], spacing=15)

        back_btn = Button(
            text='<  Back to Main Menu', size_hint_y=None, height=45,
            background_color=(0.8, 0.3, 0.3, 1), font_name=FONT
        )
        back_btn.bind(on_press=lambda x: self.show_main_menu())
        main_box.add_widget(back_btn)

        scroll = ScrollView()
        box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15)
        box.bind(minimum_height=box.setter('height'))

        for branch in MATH_DATABASE[level_name].keys():
            # branch naam e markup lagbe na, tai plain text
            lbl = Label(
                text='-- {} --'.format(branch), markup=False, font_size=16,
                color=(0.2, 0.2, 0.2, 1), size_hint_y=None, height=40,
                font_name=FONT
            )
            box.add_widget(lbl)

            for title, formula in MATH_DATABASE[level_name][branch]:
                btn = Button(
                    text=title, font_size=14, size_hint_y=None, height=50,
                    background_color=(0.3, 0.6, 0.4, 1), font_name=FONT
                )
                btn.bind(on_press=lambda x, t=title, f=formula: self.show_formula_detail(t, f, level_name))
                box.add_widget(btn)

        scroll.add_widget(box)
        main_box.add_widget(scroll)
        self.root_layout.add_widget(main_box)

    def show_formula_detail(self, title, formula, level_name):
        self.clear_screen()
        main_box = BoxLayout(orientation='vertical', padding=[45, 20, 20, 20], spacing=20)

        back_btn = Button(
            text='<  Back', size_hint_y=None, height=45,
            background_color=(0.8, 0.3, 0.3, 1), font_name=FONT
        )
        back_btn.bind(on_press=lambda x: self.show_sub_menu(level_name))
        main_box.add_widget(back_btn)

        detail_layout = BoxLayout(orientation='vertical', spacing=10)

        lbl_title = Label(
            text=title, markup=False, font_size=18,
            color=(0.1, 0.2, 0.5, 1), size_hint_y=None, height=40,
            halign='left', valign='middle', font_name=FONT
        )
        lbl_title.bind(size=lbl_title.setter('text_size'))
        detail_layout.add_widget(lbl_title)

        # markup=False zoruri: formula te [ ] ache (jemon [-b ± ...])
        lbl_formula = Label(
            text=formula, markup=False, font_size=16,
            color=(0.1, 0.1, 0.1, 1),
            halign='left', valign='top', font_name=FONT
        )
        lbl_formula.bind(size=lbl_formula.setter('text_size'))
        detail_layout.add_widget(lbl_formula)

        main_box.add_widget(detail_layout)
        self.root_layout.add_widget(main_box)


if __name__ == '__main__':
    MathApp().run()
