import bisect  
  
class SortedQueue:  
    def __init__(self):  
        self.queue = []  
    def __str__(self) -> str:
        return self.queue.__str__()
    
    def enqueue(self, value):  
        bisect.insort(self.queue, value)  
  
    def dequeue(self):  
        if self.is_empty():  
            raise IndexError("Dequeue from an empty queue")  
        return self.queue.pop(0)  
  
    def is_empty(self):  
        return len(self.queue) == 0  
  
    def size(self):  
        return len(self.queue)  
  
    def peek(self):  
        if self.is_empty():  
            raise IndexError("Peek from an empty queue")  
        return self.queue[0]
    
    def clear(self):
        if self.is_empty() == False:
            self.queue.clear()
    
    def get_list(self):
        return self.queue

if __name__ == '__main__':
    q = SortedQueue()
    q.enqueue(3)
    q.enqueue(1)
    print(q)
    q.enqueue(2)
    print(q)
    q.dequeue()
    print(q)