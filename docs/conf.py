# -*- coding: utf-8 -*-
from better import better_theme_path

extensions = []
templates_path = []
source_suffix = '.rst'
master_doc = 'index'

project = u'pivotal_tools'
copyright = u'2013 Jonathan Tushman and pivotal_tools contributors'
# The short X.Y version.
version = '0.13'
# The full version, including alpha/beta/rc tags.
release = '0.13'
exclude_patterns = ['_build']
pygments_style = 'sphinx'

html_theme_path = [better_theme_path]
html_theme = 'better'
html_theme_options = {
    'inlinecss': """
        #commands h4 {
            font-family: Monaco, Consolas, "Lucida Console", monospace;
        }
    """,
    'cssfiles': [],
    'scriptfiles': [],
    'enablesidebarsearch': False,
    'showrelbartop': False,
    'showrelbarbottom': False,
    'showheader': False,
}
html_title = "{} {}".format(project, release)
html_short_title = "Home"

html_logo = None
html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []
html_show_sphinx = True
html_show_copyright = True
# Output file base name for HTML help builder.
htmlhelp_basename = 'pivotal_toolsdoc'
