greenbot:
	python2 -OO main.py

clean:
	find . -name "*.py[co]" -delete
	find . -name "*~" -delete
