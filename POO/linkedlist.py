# Estudo de POO
# Criei uma classe Node e uma classe LinkedList


from typing import Optional


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.previous = None

    def delete(self):
        if self.previous:
            self.previous.next = self.next
        if self.next:
            self.next.previous = self.previous

        self.next = None
        self.previous = None

class LinkedList:
    def __init__(self, data):
        self.head = Node(data)

    def __iter__(self):
        lista = []
        next_value = self.head
        lista.append(next_value.data)
        while next_value.next:
            next_value = next_value.next
            lista.append(next_value.data)
        
        return iter(lista)
    
    def __len__(self) -> int:
        count = 0
        next_value = self.head
        count += 1
        
        while next_value.next:
            next_value = next_value.next
            count += 1

        return count


    def __isCircular(self) -> bool:
        hashMap = {}
        next_node = self.head
        hashMap[next_node] = True
        while next_node.next:
            next_node = next_node.next
            try:
                if hashMap[next_node]:
                    return True
            except KeyError:
                hashMap[next_node] = True

        return False
                


    def append(self, data):

        new_node = Node(data)
        next_node: Optional[Node] = None
        if self.head.next:
            next_node = self.head.next
            while next_node.next:
                next_node = next_node.next

            next_node.next = new_node
            new_node.previous = next_node
            return new_node
        
        self.head.next = new_node
        new_node.previous = self.head
        return new_node
    
    def find(self, value) -> tuple[int, Node] | None:
        next_value = self.head
        index = 0

        if next_value.data == value:
            return (index, next_value)

        while next_value.next:
            next_value = next_value.next
            index += 1
            if (value == next_value.data):
                return (index, next_value)
            
    
            

        return None





