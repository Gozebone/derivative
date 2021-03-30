import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


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
        self.add_widget(Label(text='Output:', font_size=fsize))

        self.add_widget(Label(text='Result', font_size=fsize))

# buttons of functions
        self.cos = Button(text='Cos()', font_size=fsize)
        self.inside.add_widget(self.cos)

        self.sin = Button(text='Sin()', font_size=fsize)
        self.inside.add_widget(self.sin)

        self.tg = Button(text='Tg()', font_size=fsize)
        self.inside.add_widget(self.tg)

        self.ctg = Button(text='Ctg()', font_size=fsize)
        self.inside.add_widget(self.ctg)

        self.log = Button(text='Log()', font_size=fsize)
        self.inside.add_widget(self.log)

        self.ln = Button(text='Ln()', font_size=fsize)
        self.inside.add_widget(self.ln)

        self.exp = Button(text='Exp()', font_size=fsize)
        self.inside.add_widget(self.exp)

        self.powN = Button(text='n^x', font_size=fsize)
        self.inside.add_widget(self.powN)

        self.powX = Button(text='x^n', font_size=fsize)
        self.inside.add_widget(self.powX)

        self.powFX = Button(text='f(x)^n', font_size=fsize)
        self.inside.add_widget(self.powFX)

        self.add_widget(self.inside)


class MyApp(App):
    def build(self):
        return MainGrid()
