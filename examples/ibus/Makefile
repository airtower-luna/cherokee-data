#!/usr/bin/make

# Makefile to build the ibus-table database for Cherokee input, by
# Thomas Klute <thomas2.klute@uni-dortmund.de>.
#
# Licensed as CC0 (see
# https://creativecommons.org/publicdomain/zero/1.0/), use as you
# wish!
#
# Please see "help" target for usage.

# Installation prefix (commonly "/usr" or "/usr/local")
PREFIX ?= /usr/local
# Installation directory for ibus-table databases relative to PREFIX
TABLES_DIR ?= $(PREFIX)/share/ibus-table/tables
# Installation directory for the icon relative to PREFIX
ICONS_DIR ?= $(PREFIX)/share/ibus-table/icons
# Icon to use
DEFAULT_ICON = chr.png
ICON ?= $(DEFAULT_ICON)
REL_ICON = $(notdir $(ICON))

CSV = ../../data/full.csv
DB = chr.db
CLEANFILES = chr.txt $(DB)

all: $(DB)

chr.txt: $(CSV) csv-to-ibus.py
ifneq ("$(wildcard $(REL_ICON))", "")
	./csv-to-ibus.py --icon $(REL_ICON) < $< > $@
else
	./csv-to-ibus.py < $< > $@
endif

%.db: %.txt
	ibus-table-createdb -s $< -n $@

clean:
	rm $(CLEANFILES) || true

install: all
	if ! [ -d $(TABLES_DIR) ]; then \
		mkdir -p $(TABLES_DIR); \
	fi
	install --mode=0644 $(DB) $(TABLES_DIR)/
ifneq ("$(wildcard $(REL_ICON))", "")
	if ! [ -d $(ICONS_DIR) ]; then \
		mkdir -p $(ICONS_DIR); \
	fi
	install --mode=0644 $(REL_ICON) $(ICONS_DIR)/
endif

uninstall:
	if [ -e $(TABLES_DIR)/$(DB) ]; then \
		rm $(TABLES_DIR)/$(DB); \
	fi
ifneq ("$(wildcard $(REL_ICON))", "")
	if [ -e $(ICONS_DIR)/$(REL_ICON) ]; then \
		rm $(ICONS_DIR)/$(REL_ICON); \
	fi
endif

help:
	@echo "Makefile to build the ibus-table database for Cherokee syllabary"
	@echo ""
	@echo "Environment variables:"
	@echo "  PREFIX\tInstallation prefix, default: $(PREFIX)"
	@echo "  TABLES_DIR\tInstallation directory for tables, default:\n\t\t\$${PREFIX}/share/ibus-table/tables/"
	@echo "  ICON\t\tIcon for the input method, default: $(DEFAULT_ICON). Must exist in the\n\t\tcurrent directory."
	@echo "  ICONS_DIR\tInstallation directory for icons, default:\n\t\t\$${PREFIX}/share/ibus-table/icons/"
	@echo ""
	@echo "Please not that environment variables are not stored accross make runs, for\nconsistent results you have to pass the same variables each time."

.PHONY: all clean install uninstall help
