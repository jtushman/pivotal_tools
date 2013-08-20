SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
BUILDDIR      = _build

ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) .

.PHONY: clean html all livehtml browsehtml

all: clean html

clean:
	-rm -rf $(BUILDDIR)/*

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

livehtml: html
	livereload $(BUILDDIR)/html -p 33233

browsehtml: html
	livereload -b $(BUILDDIR)/html -p 33233
