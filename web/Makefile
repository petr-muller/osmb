.PHONY: all recent clean

all: recent

recent:
	@git log -3  --abbrev-commit --pretty="format:<li>%ad: %h %s (%an)</li>" > shortlog
	./actualize.py
	rm shortlog

clean:
	rm -f index.html
