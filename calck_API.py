from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import math
import re

app = FastAPI(title="Modern Calculator API", version="1.0.0")

class CalculationRequest(BaseModel):
    expression: str
    trig_mode: str = "DEG"  # DEG or RAD

class ScientificRequest(BaseModel):
    value: float
    function: str
    trig_mode: str = "DEG"

class CalculationResponse(BaseModel):
    result: float
    expression: str

class CalculatorEngine:
    """Движок калькулятора для обработки вычислений"""
    
    def __init__(self):
        self.current_input = ""
        self.first_number = None
        self.operation = None
        self.waiting_for_second_number = False
        self.trig_mode = "DEG"
    
    def evaluate_expression(self, expression: str, trig_mode: str = "DEG") -> float:
        """Вычисляет математическое выражение"""
        self.trig_mode = trig_mode
        
        # Простая обработка выражения
        # В реальном приложении лучше использовать библиотеку sympy или ast для парсинга выражений
        try:
            # Заменяем специальные символы
            expr = expression.replace('^', '**')
            expr = expr.replace('×', '*')
            expr = expr.replace('÷', '/')
            expr = expr.replace('π', str(math.pi))
            expr = expr.replace('e', str(math.e))
            
            # Обрабатываем научные функции
            expr = self._replace_scientific_functions(expr)
            
            # Безопасное вычисление выражения
            result = eval(expr, {"__builtins__": {}}, {
                'sin': self._safe_sin,
                'cos': self._safe_cos,
                'tan': self._safe_tan,
                'asin': self._safe_asin,
                'acos': self._safe_acos,
                'atan': self._safe_atan,
                'log': self._safe_log10,
                'ln': math.log,
                'sqrt': math.sqrt,
                'abs': abs,
                'factorial': math.factorial,
                'gamma': math.gamma,
                'pi': math.pi,
                'e': math.e
            })
            
            return float(result)
            
        except Exception as e:
            raise ValueError(f"Ошибка вычисления выражения: {str(e)}")
    
    def _replace_scientific_functions(self, expression: str) -> str:
        """Заменяет текстовые функции на вызовы"""
        # Заменяем функции вида f(x)
        replacements = [
            (r'sin\(([^)]+)\)', r'sin(\1)'),
            (r'cos\(([^)]+)\)', r'cos(\1)'),
            (r'tan\(([^)]+)\)', r'tan(\1)'),
            (r'asin\(([^)]+)\)', r'asin(\1)'),
            (r'acos\(([^)]+)\)', r'acos(\1)'),
            (r'atan\(([^)]+)\)', r'atan(\1)'),
            (r'log\(([^)]+)\)', r'log(\1)'),
            (r'ln\(([^)]+)\)', r'ln(\1)'),
            (r'sqrt\(([^)]+)\)', r'sqrt(\1)'),
            (r'x²', r'**2'),
            (r'x³', r'**3'),
            (r'10\^x', r'10**'),
            (r'1/x', r'1/'),
            (r'x!', r'factorial('),
            (r'\|x\|', r'abs('),
        ]
        
        result = expression
        for pattern, replacement in replacements:
            result = re.sub(pattern, replacement, result)
        
        return result
    
    def _safe_sin(self, x):
        if self.trig_mode == "DEG":
            return math.sin(math.radians(x))
        return math.sin(x)
    
    def _safe_cos(self, x):
        if self.trig_mode == "DEG":
            return math.cos(math.radians(x))
        return math.cos(x)
    
    def _safe_tan(self, x):
        if self.trig_mode == "DEG":
            return math.tan(math.radians(x))
        return math.tan(x)
    
    def _safe_asin(self, x):
        if not -1 <= x <= 1:
            raise ValueError("asin требует значения от -1 до 1")
        result = math.asin(x)
        if self.trig_mode == "DEG":
            return math.degrees(result)
        return result
    
    def _safe_acos(self, x):
        if not -1 <= x <= 1:
            raise ValueError("acos требует значения от -1 до 1")
        result = math.acos(x)
        if self.trig_mode == "DEG":
            return math.degrees(result)
        return result
    
    def _safe_atan(self, x):
        result = math.atan(x)
        if self.trig_mode == "DEG":
            return math.degrees(result)
        return result
    
    def _safe_log10(self, x):
        if x <= 0:
            raise ValueError("log требует положительного числа")
        return math.log10(x)

calculator = CalculatorEngine()

@app.get("/")
async def root():
    return {
        "name": "Modern Calculator API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "calculate": "/calculate",
            "scientific": "/scientific",
            "operations": "/operations",
            "constants": "/constants"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "calculator"}

@app.post("/calculate", response_model=CalculationResponse)
async def calculate(request: CalculationRequest):
    """Вычисляет математическое выражение"""
    try:
        result = calculator.evaluate_expression(
            request.expression, 
            request.trig_mode
        )
        return CalculationResponse(
            result=result,
            expression=request.expression
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")

@app.post("/scientific")
async def scientific_function(request: ScientificRequest):
    """Выполняет научную функцию над числом"""
    try:
        value = request.value
        result = None
        
        if request.trig_mode == "DEG" and request.function in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
            angle_value = math.radians(value)
        else:
            angle_value = value
        
        if request.function == 'sin':
            result = math.sin(angle_value)
        elif request.function == 'cos':
            result = math.cos(angle_value)
        elif request.function == 'tan':
            result = math.tan(angle_value)
        elif request.function == 'asin':
            if not -1 <= value <= 1:
                raise ValueError("asin требует значения от -1 до 1")
            result = math.asin(value)
            if request.trig_mode == "DEG":
                result = math.degrees(result)
        elif request.function == 'acos':
            if not -1 <= value <= 1:
                raise ValueError("acos требует значения от -1 до 1")
            result = math.acos(value)
            if request.trig_mode == "DEG":
                result = math.degrees(result)
        elif request.function == 'atan':
            result = math.atan(value)
            if request.trig_mode == "DEG":
                result = math.degrees(result)
        elif request.function == 'log':
            if value <= 0:
                raise ValueError("log требует положительного числа")
            result = math.log10(value)
        elif request.function == 'ln':
            if value <= 0:
                raise ValueError("ln требует положительного числа")
            result = math.log(value)
        elif request.function == 'sqrt':
            if value < 0:
                raise ValueError("sqrt требует неотрицательного числа")
            result = math.sqrt(value)
        elif request.function == 'x²':
            result = value ** 2
        elif request.function == 'x³':
            result = value ** 3
        elif request.function == '10^x':
            result = 10 ** value
        elif request.function == '1/x':
            if value == 0:
                raise ValueError("Деление на ноль")
            result = 1 / value
        elif request.function == 'x!':
            if value < 0:
                raise ValueError("Факториал требует неотрицательного числа")
            if value.is_integer():
                result = math.factorial(int(value))
            else:
                result = math.gamma(value + 1)
        elif request.function == 'abs':
            result = abs(value)
        else:
            raise ValueError(f"Неизвестная функция: {request.function}")
        
        return {
            "function": request.function,
            "input": value,
            "result": result,
            "trig_mode": request.trig_mode
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")

@app.get("/operations")
async def get_operations():
    """Возвращает список поддерживаемых операций"""
    return {
        "basic": ["+", "-", "*", "/", "%", "^"],
        "scientific": [
            "sin", "cos", "tan", "asin", "acos", "atan",
            "log", "ln", "sqrt", "x²", "x³", "10^x", "1/x", "x!", "abs"
        ],
        "constants": ["π", "e"],
        "parentheses": ["(", ")"]
    }

@app.get("/constants")
async def get_constants():
    """Возвращает математические константы"""
    return {
        "pi": math.pi,
        "e": math.e,
        "description": {
            "pi": "Число π (отношение длины окружности к диаметру)",
            "e": "Число Эйлера (основание натурального логарифма)"
        }
    }

@app.get("/mode/{trig_mode}")
async def set_trig_mode(trig_mode: str):
    """Устанавливает режим для тригонометрических функций"""
    if trig_mode.upper() not in ["DEG", "RAD"]:
        raise HTTPException(status_code=400, detail="Режим должен быть DEG или RAD")
    
    calculator.trig_mode = trig_mode.upper()
    return {
        "message": f"Тригонометрический режим установлен в {calculator.trig_mode}",
        "trig_mode": calculator.trig_mode
    }

@app.post("/basic")
async def basic_operation(a: float, b: float, operation: str):
    """Выполняет базовую операцию над двумя числами"""
    try:
        if operation == '+':
            result = a + b
        elif operation == '-':
            result = a - b
        elif operation == '*':
            result = a * b
        elif operation == '/':
            if b == 0:
                raise ValueError("Деление на ноль")
            result = a / b
        elif operation == '%':
            result = a % b
        elif operation == '^':
            result = a ** b
        else:
            raise ValueError(f"Неподдерживаемая операция: {operation}")
        
        return {
            "operation": operation,
            "a": a,
            "b": b,
            "result": result
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")