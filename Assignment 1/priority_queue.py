import sys

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
        heuristic_values = dict()
        if self.is_empty():
            return None
        min_element_index = 0
        min_value = self.f(self.queue[0])
        heuristic_values[self.queue[0]] = min_value
        min_element_amount_to_save = self.queue[0].state.amount_to_save()
        for i in range(len(self.queue)):
            queue_i_res = self.f(self.queue[i])
            heuristic_values[self.queue[i]] = queue_i_res
            queue_i_amount_to_save = self.queue[i].state.amount_to_save()
            if queue_i_res < min_value or (queue_i_res == min_value and queue_i_amount_to_save < min_element_amount_to_save):
                min_element_index = i
                min_value = queue_i_res
                min_element_amount_to_save = queue_i_amount_to_save
        item = self.queue[min_element_index]
        del self.queue[min_element_index]
        return item
