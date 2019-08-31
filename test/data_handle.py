import collections

class Data_handle:

    def __init__(self, data):
        self.data = data

    def count_all(self):
        cnt = collections.Counter();
        for x in self.data:
          cnt[x] += 1
        return cnt.most_common(cnt.__len__())









