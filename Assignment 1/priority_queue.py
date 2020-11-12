
class PriorityQueue(object):

    def __init__(self, f):
        self.queue = []
        self.f = f

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # for checking if the queue is empty
    def is_empty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)
# for popping an element based on Priority
    def pop(self):
        if self.is_empty():
            return None
        min_element_index = 0
        for i in range(len(self.queue)):
            if self.f(self.queue[i]) < self.f(self.queue[min_element_index]):
                min_element_index = i
        item = self.queue[min_element_index]
        del self.queue[min_element_index]
        return item
