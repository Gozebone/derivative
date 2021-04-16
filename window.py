from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from derivative import der
from output import clear_expression

functions = {
    'Sin()': 'sin()',
    'Cos()': 'cos()',
    'Tg()': 'tan()',
    'Ctg()': 'ctg()',
    'Log()': 'log[]()',
    'Ln()': 'ln()',
    'Exp()': 'exp()',
    'x^n': 'x^',
    'f(x)^n': '()^'

}
class MainGrid(GridLayout):
    def __init__(self, **kwargs):
        fsize = 40

        super(MainGrid, self).__init__(**kwargs)

        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 5

# input
        self.add_widget(Label(text='Input:', font_size=fsize))

        self.input_expression = TextInput(multiline=False, font_size=fsize)
        self.add_widget(self.input_expression)

# output
        self.output_expression = Label(text='Result', font_size=fsize)
        self.add_widget(Label(text='Output:', font_size=fsize))

        self.add_widget(self.output_expression)

# buttons of functions
        self.cos = Button(text='Cos()', font_size=fsize)
        self.cos.bind(on_press=self.pressed)
        self.inside.add_widget(self.cos)

        self.sin = Button(text='Sin()', font_size=fsize)
        self.sin.bind(on_press=self.pressed)
        self.inside.add_widget(self.sin)

        self.tg = Button(text='Tg()', font_size=fsize)
        self.tg.bind(on_press=self.pressed)
        self.inside.add_widget(self.tg)

        self.ctg = Button(text='Ctg()', font_size=fsize)
        self.ctg.bind(on_press=self.pressed)
        self.inside.add_widget(self.ctg)

        self.log = Button(text='Log()', font_size=fsize)
        self.log.bind(on_press=self.pressed)
        self.inside.add_widget(self.log)

        self.ln = Button(text='Ln()', font_size=fsize)
        self.ln.bind(on_press=self.pressed)
        self.inside.add_widget(self.ln)

        self.exp = Button(text='Exp()', font_size=fsize)
        self.exp.bind(on_press=self.pressed)
        self.inside.add_widget(self.exp)

        self.powX = Button(text='x^n', font_size=fsize)
        self.powX.bind(on_press=self.pressed)
        self.inside.add_widget(self.powX)

        self.powFX = Button(text='f(x)^n', font_size=fsize)
        self.powFX.bind(on_press=self.pressed)
        self.inside.add_widget(self.powFX)

        self.result_but = Button(text='Result', font_size=fsize)
        self.result_but.bind(on_press=self.result_click)
        self.inside.add_widget(self.result_but)

        self.add_widget(self.inside)

    def pressed(self, instance):
        text = self.input_expression.text
        position = self.input_expression.cursor[0]
        text = text[:position] + functions[instance.text] + text[position:]
        self.input_expression.text = text

    def result_click(self, instance):
        text = self.input_expression.text
        try:
            self.output_expression.text = clear_expression(der(text.lower()))
        except Exception:
            self.output_expression.text = 'none'

class MyApp(App):
    def build(self):
        return MainGrid()
