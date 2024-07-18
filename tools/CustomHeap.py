class MinHeap:
    # Custom heap class is required
    def __init__(self):
        self.heap = []

    def insert(self, element):
        self.heap.append(element)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if len(self.heap) == 0:
            raise IndexError("extract_min from empty heap")
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def peek_min(self):
        if len(self.heap) == 0:
            raise IndexError("peek_min from empty heap")
        return self.heap[0]

    def is_empty(self):
        if len(self.heap) == 0:
            return True
        return False
    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        if parent_index >= 0 and self.heap[index][0] < self.heap[parent_index][0]: # [0] selects ferst element of 2d array in each element of the heap for comparesement
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._heapify_up(parent_index)

    def _heapify_down(self, index):
        smallest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2

        if left_child < len(self.heap) and self.heap[left_child][0] < self.heap[smallest][0]:  # [0] selects ferst element of 2d array in each element of the heap for comparesement
            smallest = left_child

        if right_child < len(self.heap) and self.heap[right_child][0] < self.heap[smallest][0]:  # [0] selects ferst element of 2d array in each element of the heap for comparesement
            smallest = right_child

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def __str__(self):
        return str(self.heap)
