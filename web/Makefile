all: recent

recent:
	@git log -3  --abbrev-commit --pretty="format:%ai: %h %s (%an)" > shortlog
	./actualize.py
	rm shortlog

clean:
	rm -f index.html
