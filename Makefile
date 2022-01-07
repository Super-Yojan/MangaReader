PREFIX := /usr/local

all: install
	cp src/main.py $(DESTDIR)$(PREFIX)/bin/readmanga
	chmod 0755 $(DESTDIR)$(PREFIX)/bin/readmanga

uninstall:
	$(RM) $(DESTDIR)$(PREFIX)/bin/readmanga

.PHONY: all install uninstall


