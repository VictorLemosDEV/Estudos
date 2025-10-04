# Estudo de POO
# Criei uma classe Vetor com todos os métodos principais de um vetor (com excessão de produtos vetorias)

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other) -> 'Vector':
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __sub__(self, other) -> 'Vector':
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    def __mul__(self, scalar: float) -> 'Vector':
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented
    
    def __truediv__(self, scalar: float) -> 'Vector':
        if isinstance(scalar, (int, float)) and scalar != 0:
            return Vector(self.x / scalar, self.y / scalar)
        return NotImplemented
    
    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"
    
    def __getitem__(self,index) -> float:
        if index == 0:
            return self.x
        
        if index == 1:
            return self.y
        
        raise IndexError("Index out of range for Vector")
    
    def magnitude(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5
    
    def normalize(self) -> 'Vector':
        magnitude = self.magnitude()
        if magnitude == 0:
            return Vector(0,0)
        else:
            return self / magnitude
        
    def dot(self, other) -> float:
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        return NotImplemented
    

    


        return NotImplemented
