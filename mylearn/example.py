"""
简单计算器示例模块

该模块提供了一个 Calculator 类，实现了基本的四则运算功能。
"""


class Calculator:
    """
    简单计算器类
    
    提供基本的数学运算功能，包括加法、减法、乘法和除法。
    """
    
    def add(self, a: float, b: float) -> float:
        """
        加法运算
        
        Args:
            a: 第一个加数
            b: 第二个加数
            
        Returns:
            两个数的和
        """
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """
        减法运算
        
        Args:
            a: 被减数
            b: 减数
            
        Returns:
            差 (a - b)
        """
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """
        乘法运算
        
        Args:
            a: 第一个因数
            b: 第二个因数
            
        Returns:
            两个数的积
        """
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """
        除法运算
        
        Args:
            a: 被除数
            b: 除数
            
        Returns:
            商 (a / b)
            
        Raises:
            ValueError: 当除数为零时抛出异常
        """
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b


# 主程序入口
if __name__ == "__main__":
    # 创建计算器实例
    calc = Calculator()
    
    # 演示加法
    a, b = 10, 5
    result = calc.add(a, b)
    print(f"{a} + {b} = {result}")
    
    # 演示减法
    result = calc.subtract(a, b)
    print(f"{a} - {b} = {result}")
    
    # 演示乘法
    result = calc.multiply(a, b)
    print(f"{a} * {b} = {result}")
    
    # 演示除法
    result = calc.divide(a, b)
    print(f"{a} / {b} = {result}")
    
    # 演示除法错误处理
    try:
        calc.divide(10, 0)
    except ValueError as e:
        print(f"错误: {e}")