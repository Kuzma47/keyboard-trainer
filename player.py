class Player:
	def __init__(self, name: str, max_wpm: int, wpm: list):
		self.name = name
		self.max_wpm = max_wpm
		self.wpm = wpm

	def get_average_wpm(self):
		if len(self.wpm) == 0:
			return 0
		return int(sum(list(map(int, self.wpm))) / len(self.wpm))
