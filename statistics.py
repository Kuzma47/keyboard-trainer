import matplotlib.pyplot as plt


def add_text(name):
	plt.title(f"{name}'s WPM statistics")
	plt.xlabel("Number of completed texts")
	plt.ylabel("WPM")


def open_statistics(data, name):
	text_counter = len(data)
	plt.plot([i for i in range(1, len(data) + 1)], data)
	plt.hlines(xmin=1, xmax=text_counter, y=sum(data)/text_counter)
	add_text(name)
	plt.text((text_counter + 1) // 2, sum(data)/text_counter + 0.1, "Average WPM")
	plt.show()
