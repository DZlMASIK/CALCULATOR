import tkinter as tk
from tkinter import font
import math

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("400x650")
        self.root.configure(bg='#121212')
        self.root.resizable(False, False)
        
        # Цветовая схема (темная тема)
        self.colors = {
            'bg': '#121212',
            'display_bg': '#1e1e1e',
            'display_fg': '#ffffff',
            'num_btn': '#2d2d2d',
            'num_btn_hover': '#3d3d3d',
            'num_text': '#ffffff',
            'op_btn': '#ff9500',
            'op_btn_hover': '#ffaa33',
            'op_text': '#ffffff',
            'special_btn': '#a6a6a6',
            'special_btn_hover': '#bfbfbf',
            'special_text': '#000000',
            'sci_btn': '#4a9eff',
            'sci_btn_hover': '#6ab0ff',
            'sci_text': '#ffffff',
            'toggle_btn': '#5856d6',
            'toggle_btn_hover': '#7876f6',
            'shadow': '#000000'
        }
        
        # Переменные
        self.current_input = ""
        self.result_var = tk.StringVar(value="0")
        self.operation = None
        self.first_number = None
        self.waiting_for_second_number = False
        self.trig_mode = "DEG"
        self.sci_panel_visible = False
        
        # Настройка шрифтов
        try:
            self.display_font = font.Font(family="Segoe UI", size=34, weight="normal")
            self.button_font = font.Font(family="Segoe UI", size=20, weight="normal")
            self.mode_font = font.Font(family="Segoe UI", size=12, weight="normal")
            self.sci_font = font.Font(family="Segoe UI", size=14, weight="normal")
        except:
            self.display_font = font.Font(size=34, weight="normal")
            self.button_font = font.Font(size=20, weight="normal")
            self.mode_font = font.Font(size=12, weight="normal")
            self.sci_font = font.Font(size=14, weight="normal")
        
        self.setup_ui()
        self.bind_keys()
    
    def create_button(self, parent, text, command, bg, fg, hover_bg, row, col, colspan=1, btn_font=None, width=8, height=2):
        """Создание современной кнопки"""
        if btn_font is None:
            btn_font = self.button_font
        
        btn = tk.Button(
            parent,
            text=text,
            font=btn_font,
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=fg,
            borderwidth=0,
            relief='flat',
            cursor='hand2',
            command=command,
            padx=10,
            pady=10,
            width=width,
            height=height
        )
        
        # Эффект наведения
        def on_enter(e):
            btn['bg'] = hover_bg
        
        def on_leave(e):
            btn['bg'] = bg
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        # Размещение кнопки
        btn.grid(
            row=row,
            column=col,
            columnspan=colspan,
            sticky="nsew",
            padx=3,
            pady=3,
            ipadx=5,
            ipady=5
        )
        
        return btn
    
    def setup_ui(self):
        # Основной контейнер
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Индикатор режима
        mode_frame = tk.Frame(main_container, bg=self.colors['bg'])
        mode_frame.pack(fill='x', pady=(0, 15))
        
        self.mode_label = tk.Label(
            mode_frame,
            text=f"Mode: {self.trig_mode}",
            font=self.mode_font,
            bg=self.colors['bg'],
            fg='#888888'
        )
        self.mode_label.pack(side='left')
        
        # Кнопка переключения режима
        mode_btn = tk.Button(
            mode_frame,
            text="DEG/RAD",
            font=self.mode_font,
            command=self.toggle_trig_mode,
            bg=self.colors['toggle_btn'],
            fg='white',
            activebackground=self.colors['toggle_btn_hover'],
            activeforeground='white',
            borderwidth=0,
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=5
        )
        mode_btn.pack(side='right')
        
        # Дисплей
        display_frame = tk.Frame(
            main_container,
            bg=self.colors['display_bg'],
            height=100
        )
        display_frame.pack(fill='x', pady=(0, 20))
        
        display = tk.Label(
            display_frame,
            textvariable=self.result_var,
            font=self.display_font,
            bg=self.colors['display_bg'],
            fg=self.colors['display_fg'],
            anchor='e',
            padx=20,
            pady=25
        )
        display.pack(fill='both', expand=True)
        
        # Кнопка переключения научных функций
        sci_toggle_frame = tk.Frame(main_container, bg=self.colors['bg'])
        sci_toggle_frame.pack(fill='x', pady=(0, 15))
        
        self.sci_toggle_btn = tk.Button(
            sci_toggle_frame,
            text="▼ Scientific Functions",
            font=self.sci_font,
            command=self.toggle_sci_panel,
            bg=self.colors['sci_btn'],
            fg='white',
            activebackground=self.colors['sci_btn_hover'],
            activeforeground='white',
            borderwidth=0,
            relief='flat',
            cursor='hand2',
            pady=10
        )
        self.sci_toggle_btn.pack(fill='x')
        
        # Научная панель (скрыта изначально) - создаем с фиксированной высотой
        self.sci_panel = tk.Frame(main_container, bg=self.colors['bg'], height=250)
        self.sci_panel.pack_propagate(False)  # Запрещаем изменение размера контентом
        
        # Основная клавиатура
        self.keyboard_frame = tk.Frame(main_container, bg=self.colors['bg'])
        self.keyboard_frame.pack(fill='both', expand=True)
        
        # Настройка сетки для основной клавиатуры (5 строк, 4 колонки)
        for i in range(4):
            self.keyboard_frame.grid_columnconfigure(i, weight=1, minsize=80)
        for i in range(5):
            self.keyboard_frame.grid_rowconfigure(i, weight=1, minsize=70)
        
        # Расположение кнопок (теперь 0 занимает одну колонку, точка - другую)
        buttons = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '']  # Последняя пустая, чтобы не было второй кнопки "="
        ]
        
        # Создание кнопок
        self.buttons_dict = {}
        
        for row_idx, row in enumerate(buttons):
            for col_idx, text in enumerate(row):
                if text == '':  # Пропускаем пустые кнопки
                    continue
                    
                # Для кнопки "=" делаем colspan=2, чтобы она была больше
                colspan = 2 if text == '=' else 1
                col = col_idx if text != '=' else 2  # "=" начинается с колонки 2
                
                # Определение стиля кнопки
                if text in ['C', '⌫', '%']:
                    bg = self.colors['special_btn']
                    fg = self.colors['special_text']
                    hover_bg = self.colors['special_btn_hover']
                elif text in ['/', '*', '-', '+', '=']:
                    bg = self.colors['op_btn']
                    fg = self.colors['op_text']
                    hover_bg = self.colors['op_btn_hover']
                else:
                    bg = self.colors['num_btn']
                    fg = self.colors['num_text']
                    hover_bg = self.colors['num_btn_hover']
                
                btn = self.create_button(
                    self.keyboard_frame,
                    text,
                    lambda t=text: self.button_click(t),
                    bg,
                    fg,
                    hover_bg,
                    row_idx,
                    col,
                    colspan,
                    width=10 if colspan == 2 else 8
                )
                
                self.buttons_dict[text] = btn
        
        # Создаем научную панель отдельно
        self.setup_sci_panel()
    
    def setup_sci_panel(self):
        """Настройка научной панели"""
        # Внутренний контейнер для научных функций
        sci_container = tk.Frame(self.sci_panel, bg=self.colors['bg'])
        sci_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Настройка сетки для научных функций
        for i in range(4):
            sci_container.grid_columnconfigure(i, weight=1)
        for i in range(5):
            sci_container.grid_rowconfigure(i, weight=1)
        
        # Расширенный набор научных функций (теперь 5x4)
        sci_buttons = [
            ['sin', 'cos', 'tan', 'π'],
            ['asin', 'acos', 'atan', 'e'],
            ['log', 'ln', '√', 'x²'],
            ['x³', '10^x', '1/x', 'x!'],
            ['(', ')', '|x|', '^']
        ]
        
        for row_idx, row in enumerate(sci_buttons):
            for col_idx, text in enumerate(row):
                btn = tk.Button(
                    sci_container,
                    text=text,
                    font=self.sci_font,
                    bg=self.colors['sci_btn'],
                    fg=self.colors['sci_text'],
                    activebackground=self.colors['sci_btn_hover'],
                    activeforeground=self.colors['sci_text'],
                    borderwidth=0,
                    relief='flat',
                    cursor='hand2',
                    command=lambda t=text: self.sci_button_click(t),
                    padx=5,
                    pady=10
                )
                
                # Эффект наведения
                def on_enter(e, b=btn, h=self.colors['sci_btn_hover']):
                    b['bg'] = h
                
                def on_leave(e, b=btn, bg=self.colors['sci_btn']):
                    b['bg'] = bg
                
                btn.bind("<Enter>", on_enter)
                btn.bind("<Leave>", on_leave)
                
                btn.grid(
                    row=row_idx,
                    column=col_idx,
                    sticky="nsew",
                    padx=2,
                    pady=2
                )
                
                # Для удобства тоже сохраняем в словарь
                self.buttons_dict[text] = btn
    
    def toggle_sci_panel(self):
        """Переключение видимости научной панели"""
        if not self.sci_panel_visible:
            # Показываем панель ПЕРЕД основной клавиатурой
            self.sci_panel.pack(fill='x', pady=(0, 10), before=self.keyboard_frame)
            self.sci_toggle_btn.config(text="▲ Scientific Functions")
            # Увеличиваем размер окна
            self.root.geometry("400x900")
        else:
            # Скрываем панель
            self.sci_panel.pack_forget()
            self.sci_toggle_btn.config(text="▼ Scientific Functions")
            # Возвращаем исходный размер окна
            self.root.geometry("400x650")
        
        self.sci_panel_visible = not self.sci_panel_visible
    
    def toggle_trig_mode(self):
        """Переключение между градусами и радианами"""
        self.trig_mode = "RAD" if self.trig_mode == "DEG" else "DEG"
        self.mode_label.config(text=f"Mode: {self.trig_mode}")
    
    def sci_button_click(self, text):
        """Обработка нажатий научных кнопок"""
        try:
            if self.current_input:
                value = float(self.current_input)
            else:
                value = 0
            
            result = None
            
            # Преобразование в радианы если нужно
            if self.trig_mode == "DEG" and text in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
                angle_value = math.radians(value)
            else:
                angle_value = value
            
            # Тригонометрические функции
            if text == 'sin':
                result = math.sin(angle_value)
            elif text == 'cos':
                result = math.cos(angle_value)
            elif text == 'tan':
                result = math.tan(angle_value)
            elif text == 'asin':
                result = math.asin(value) if -1 <= value <= 1 else None
                if result is not None and self.trig_mode == "DEG":
                    result = math.degrees(result)
            elif text == 'acos':
                result = math.acos(value) if -1 <= value <= 1 else None
                if result is not None and self.trig_mode == "DEG":
                    result = math.degrees(result)
            elif text == 'atan':
                result = math.atan(value)
                if self.trig_mode == "DEG":
                    result = math.degrees(result)
            
            # Математические константы
            elif text == 'π':
                self.current_input = str(math.pi)
                self.update_display()
                return
            elif text == 'e':
                self.current_input = str(math.e)
                self.update_display()
                return
            
            # Математические операции
            elif text == 'log':
                result = math.log10(value) if value > 0 else None
            elif text == 'ln':
                result = math.log(value) if value > 0 else None
            elif text == '√':
                result = math.sqrt(value) if value >= 0 else None
            elif text == 'x²':
                result = value ** 2
            elif text == 'x³':
                result = value ** 3
            elif text == '10^x':
                result = 10 ** value
            elif text == '1/x':
                result = 1 / value if value != 0 else None
            elif text == 'x!':
                if value >= 0 and value.is_integer():
                    result = math.factorial(int(value))
                else:
                    result = math.gamma(value + 1)
            elif text == '|x|':
                result = abs(value)
            elif text == '(':
                self.current_input += '('
                self.update_display()
                return
            elif text == ')':
                self.current_input += ')'
                self.update_display()
                return
            elif text == '^':
                self.handle_operation('^')
                return
            
            # Обработка ошибок
            if result is None:
                self.result_var.set("Error")
                return
            
            # Форматирование результата
            if abs(result) < 1e-10:
                result = 0
            
            if abs(result - round(result, 10)) < 1e-10:
                result = round(result, 10)
            
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            self.current_input = str(result)
            self.update_display()
            
        except Exception as e:
            self.result_var.set("Error")
            self.current_input = ""
    
    def button_click(self, text):
        """Обработка нажатий основных кнопок"""
        # Подсветка кнопки
        self.highlight_button(text)
        
        if text.isdigit() or text == '.':
            self.handle_number_input(text)
        elif text in ['+', '-', '*', '/', '%', '^']:
            self.handle_operation(text)
        elif text == '=':
            self.calculate()
        elif text == 'C':
            self.clear()
        elif text == '⌫':
            self.backspace()
    
    def handle_number_input(self, num):
        """Обработка ввода чисел"""
        if self.waiting_for_second_number:
            self.current_input = ""
            self.waiting_for_second_number = False
        
        if num == '.':
            if '.' not in self.current_input:
                if self.current_input == "":
                    self.current_input = "0."
                else:
                    self.current_input += "."
        else:
            if self.current_input == "0":
                self.current_input = num
            else:
                self.current_input += num
        
        self.update_display()
    
    def handle_operation(self, op):
        """Обработка математических операций"""
        if self.current_input:
            if self.first_number is not None and not self.waiting_for_second_number:
                self.calculate()
            
            self.first_number = float(self.current_input)
            self.operation = op
            self.waiting_for_second_number = True
            
            # Отображение операции
            display_op = op
            if op == '*':
                display_op = '×'
            elif op == '/':
                display_op = '÷'
            elif op == '^':
                display_op = '^'
            
            self.result_var.set(f"{self.current_input} {display_op}")
    
    def calculate(self):
        """Выполнение вычислений"""
        if self.first_number is not None and self.operation and self.current_input:
            try:
                second_number = float(self.current_input)
                
                if self.operation == '+':
                    result = self.first_number + second_number
                elif self.operation == '-':
                    result = self.first_number - second_number
                elif self.operation == '*':
                    result = self.first_number * second_number
                elif self.operation == '/':
                    if second_number == 0:
                        self.result_var.set("Error")
                        self.clear()
                        return
                    result = self.first_number / second_number
                elif self.operation == '%':
                    result = self.first_number % second_number
                elif self.operation == '^':
                    result = self.first_number ** second_number
                
                # Форматирование результата
                if abs(result) < 1e-10:
                    result = 0
                
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
                
                self.result_var.set(str(result))
                self.current_input = str(result)
                self.first_number = None
                self.operation = None
                self.waiting_for_second_number = False
                
            except Exception as e:
                self.result_var.set("Error")
                self.clear()
    
    def clear(self):
        """Очистка калькулятора"""
        self.current_input = ""
        self.result_var.set("0")
        self.first_number = None
        self.operation = None
        self.waiting_for_second_number = False
    
    def backspace(self):
        """Удаление последнего символа"""
        if self.current_input:
            self.current_input = self.current_input[:-1]
            if not self.current_input:
                self.current_input = "0"
            self.update_display()
    
    def update_display(self):
        """Обновление дисплея"""
        if self.current_input == "":
            self.result_var.set("0")
        else:
            # Форматирование длинных чисел
            if len(self.current_input) > 15:
                try:
                    num = float(self.current_input)
                    if abs(num) > 1e12 or (abs(num) < 1e-4 and num != 0):
                        self.result_var.set(f"{num:.4e}")
                    else:
                        self.result_var.set(f"{num:.8g}")
                except:
                    self.result_var.set(self.current_input[:15] + "...")
            else:
                self.result_var.set(self.current_input)
    
    def bind_keys(self):
        """Привязка клавиш клавиатуры"""
        # Цифры
        for key in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            self.root.bind(key, lambda event, k=key: self.key_press(k))
        
        # Операции
        self.root.bind('+', lambda event: self.key_press('+'))
        self.root.bind('-', lambda event: self.key_press('-'))
        self.root.bind('*', lambda event: self.key_press('*'))
        self.root.bind('/', lambda event: self.key_press('/'))
        
        # Специальные клавиши
        self.root.bind('.', lambda event: self.key_press('.'))
        self.root.bind('<Return>', lambda event: self.key_press('='))
        self.root.bind('<BackSpace>', lambda event: self.key_press('⌫'))
        self.root.bind('<Delete>', lambda event: self.key_press('C'))
        self.root.bind('<Escape>', lambda event: self.key_press('C'))
        self.root.bind('c', lambda event: self.key_press('C'))
        self.root.bind('C', lambda event: self.key_press('C'))
        self.root.bind('%', lambda event: self.key_press('%'))
        
        # Научные функции (горячие клавиши)
        self.root.bind('<F2>', lambda event: self.toggle_sci_panel())
    
    def key_press(self, key):
        """Обработка нажатий клавиш"""
        # Преобразование символов
        if key in self.buttons_dict:
            self.highlight_button(key)
        
        # Обработка
        if key.isdigit() or key == '.':
            self.handle_number_input(key)
        elif key in ['+', '-', '*', '/', '%']:
            self.handle_operation(key)
        elif key == '=':
            self.calculate()
        elif key == 'C':
            self.clear()
        elif key == '⌫':
            self.backspace()
    
    def highlight_button(self, key):
        """Подсветка кнопки при нажатии"""
        if key in self.buttons_dict:
            btn = self.buttons_dict[key]
            original_bg = btn.cget('bg')
            
            # Определение цвета подсветки
            if key in ['C', '⌫', '%']:
                highlight_color = self.colors['special_btn_hover']
            elif key in ['+', '-', '*', '/', '=']:
                highlight_color = self.colors['op_btn_hover']
            elif key.isdigit() or key == '.':
                highlight_color = self.colors['num_btn_hover']
            elif key in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'π', 'e', 'log', 'ln', '√', 'x²', 'x³', '10^x', '1/x', 'x!', '(', ')', '|x|', '^']:
                highlight_color = self.colors['sci_btn_hover']
            else:
                return
            
            # Анимация подсветки
            btn.config(bg=highlight_color)
            self.root.after(100, lambda: btn.config(bg=original_bg))

def main():
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()