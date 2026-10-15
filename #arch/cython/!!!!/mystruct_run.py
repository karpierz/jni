import mystruct
from mystruct import MyStruct

print("XXXXX", dir(mystruct))
print("XXXXX", dir(mystruct.MyStruct))

obj = MyStruct(10, 3.14, "Hello")

print(obj.x)      # 10
print(obj.y)      # 3.14
print(obj.name)   # Hello

obj.x = 99
obj.name = "World"
