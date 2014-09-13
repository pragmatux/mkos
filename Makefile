MANPAGES:=$(patsubst %.md,%,$(wildcard *.?.md))

manpages: $(MANPAGES)

%: %.md
	pandoc --standalone --to=man $< -o $@

.PHONY: clean
clean:
	rm -f $(MANPAGES)
