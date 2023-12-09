# ========= PREAMBLE ========= #
# pylint: disable=C0111
from qutebrowser.config.configfiles import ConfigAPI  # noqa: F401
from qutebrowser.config.config import ConfigContainer  # noqa: F401
config = config  # type: ConfigAPI # noqa: F821 pylint: disable=E0602,C0103
c = c  # type: ConfigContainer # noqa: F821 pylint: disable=E0602,C0103

import re
import os
from datetime import date

config.load_autoconfig(False)

DOWNLOAD_DIR = os.path.join(os.path.expandvars("$HOME"),
                            'inbox', 'downloads', 'Firefox',
                            date.today().strftime("%y-%m"))
LATEST_DIR = os.path.join(os.path.expandvars("$HOME"), 'inbox', 'downloads', 'Firefox', 'LATEST')

if os.readlink(LATEST_DIR) != DOWNLOAD_DIR:
    os.remove(LATEST_DIR)
    os.symlink(DOWNLOAD_DIR, LATEST_DIR)

QUTEBROWSER = os.path.join(os.path.expandvars("$HOME"), '.config', 'qutebrowser')
USERSCRIPTS = os.path.join(QUTEBROWSER, 'userscripts')

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# ========= SETTINGS ========= #

c.fonts.default_size = "10pt"

c.content.headers.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"

c.content.pdfjs = False

# Always restore open sites when qutebrowser is reopened
c.session.default_name = "personal"
c.auto_save.session = True
c.session.lazy_restore = True

# Search settings
c.search.ignore_case = 'always'

c.content.local_content_can_access_remote_urls = True

# Downloads setting
c.downloads.location.directory = DOWNLOAD_DIR
c.downloads.open_dispatcher = 'mv {} ~/{}'

c.downloads.position = 'bottom'
c.downloads.remove_finished = 30000 # in ms

# Spellcheck
c.spellcheck.languages = ['en-US', 'fr-FR']

# Don't play media automatically
c.content.autoplay = False

# Always open help / history in a new tab
c.aliases['help'] = 'help -t'
c.aliases['history'] = 'history -t'

# Rename qutebrowser windows (to allow i3 to map different browser windows)
c.window.title_format = '{id}{title_sep}{current_title}{title_sep}qutebrowser'

# Configure search engines
c.url.searchengines = {
    "DEFAULT": "https://duckduckgo.com/?q={}",
    "a": "https://www.amazon.com/search/s?k={}",
    "afr": "https://www.amazon.fr/search/s?k={}",
    "allo": "https://www.allocine.fr/rechercher/?q={}",
    "allocine": "https://www.allocine.fr/rechercher/?q={}",
    "annual": "https://www.annualreviews.org/action/doSearch?AllField={}&ConceptID=",
    "arch": "https://wiki.archlinux.org/index.php?search={}",
    "archive": "https://web.archive.org/web/*/{}",
    "aur": "https://aur.archlinux.org/packages/?K={}",
    "bs": "https://www.crummy.com/software/BeautifulSoup/bs4/doc/search.html?q={}&check_keywords=yes&area=default",
    "cairn": "https://www.cairn.info/resultats_recherche.php?searchTerm={}",
    "crisco": "https://crisco2.unicaen.fr/des/synonymes/{}",
    "cnrtl": "https://www.cnrtl.fr/definition/{}",
    "d": "https://duckduckgo.com/?q={}",
    "deepl": "https://www.deepl.com/translator#xx/en/{}",
    "imdb": "https://www.imdb.com/find?s=all&q={}",
    "img": "https://www.google.com/search?tbm=isch&q={}",
    "g": "https://www.google.com/search?hl=en&q={}",
    "ged": "https://campus-condorcet.primo.exlibrisgroup.com/discovery/search?query=any,contains,{}&tab=ALL&search_scope=ALL&vid=33CCP_INST:CCP&lang=fr&offset=0",
    "gfr": "https://www.google.fr/search?hl=fr&q={}",
    "gs": "https://scholar.google.com/scholar?q={}",
    "fa": "https://fontawesome.com/icons?q={}",
    "libg": "https://libgen.unblockit.pw/search.php?req={}",
    "libf": "https://libgen.unblockit.pw/search.php?req={}",
    "m": "https://money.batpi.net/search?search={}&go=",
    "maps": "https://www.google.com/maps?hl=en&q={}",
    "maxi": "https://www.maxicoffee.com/search.php?target=catalog&q={}",
    "sep": "https://plato.stanford.edu/search/searcher.py?query={}",
    "scholar": "https://scholar.google.com/scholar?q={}",
    "sci": "https://sci-hub.se/{}",
    "t": "https://twitter.com/search?q={}",
    "tr": "https://www.deepl.com/translator#xx/en/{}",
    "theses": "https://www.theses.fr/?q={}",
    "unsplash": "https://unsplash.com/s/photos/{}",
    "w": "https://en.wikipedia.org/wiki/Special:Search/{}",
    "wfr": "https://fr.wikipedia.org/wiki/Special:Search/{}",
    "ygg": "https://www2.yggtorrent.si/engine/search?name={}&do=search",
    "yt": "https://www.youtube.com/results?search_query={}",
    "yts": "https://yts.movie/browse-movies/{}/all/all/0/latest",
}

# Reload config file (useful when tweaking stuff)
config.bind('l', 'config-source;; message-info "Config successfully reloaded!"')

# Bindings
config.bind('c', 'scroll left')
config.bind('t', 'scroll down')
config.bind('s', 'scroll up')
config.bind('r', 'scroll right')

config.bind('C', 'back')
config.bind('R', 'forward')
config.bind('h', 'back -t')

config.bind('T', 'tab-prev')
config.bind('S', 'tab-next')
config.bind('g0', 'tab-focus 1')
config.bind('g$', 'tab-focus -1')
config.bind('g#', 'tab-focus -1')

for i in range(1, 20):
    config.bind(f'g{i}', f'tab-focus {i}')

config.bind('<Ctrl-O>', 'tab-focus stack-prev')
config.bind('<Ctrl-I>', 'tab-focus stack-next')

config.bind('<Ctrl-R>', 'reload -f')
config.bind('<Ctrl-R>', 'reload -f', mode='insert')

# Detach and move tabs between windows
config.bind('<Ctrl-Shift-N>', 'tab-give') # Detach tab
config.bind('<Ctrl-Shift-R>', 'set-cmd-text -s :tab-give') # Send tab to other window
config.bind('p', 'tab-clone --private') # Open tab in private window

# Navigate website
config.bind(';s', 'navigate up') # Go up a level in URL
config.bind(';c', 'navigate prev') # Follow prev link
config.bind(';r', 'navigate next') # Follow next link
config.bind(';o', 'open {url:domain}') # Go to top domain

# Caret mode
config.bind('C', 'scroll left', mode='caret')
config.bind('T', 'scroll down', mode='caret')
config.bind('S', 'scroll up', mode='caret')
config.bind('R', 'scroll right', mode='caret')
config.bind(')', 'move-to-start-of-prev-block', mode='caret')
config.bind('(', 'move-to-start-of-next-block', mode='caret')
config.bind('<Ctrl-N>', 'enter-mode normal', mode='caret')
config.bind('é', 'move-to-end-of-word', mode='caret')
config.bind('c', 'move-to-prev-char', mode='caret')
config.bind('t', 'move-to-next-line', mode='caret')
config.bind('s', 'move-to-prev-line', mode='caret')
config.bind('r', 'move-to-next-char', mode='caret')
config.bind('É', 'move-to-next-word', mode='caret')
config.bind('{', 'move-to-end-of-prev-block', mode='caret')
config.bind('}', 'move-to-end-of-next-block', mode='caret')

#  config.bind('A', f'spawn --userscript {USERSCRIPTS}/add_bookmark')
config.bind('A', 'spawn alacritty -e buku -a {url} --title {title} -w nvim')
config.bind('a', 'quickmark-save')
config.bind('b', 'set-cmd-text -s :tab-focus')

config.bind('<Ctrl-N>', 'set-cmd-text -s :open -w')

# Command mode
config.bind('<Ctrl-N>', 'completion-item-focus next', mode='command')
config.bind('<Ctrl-P>', 'completion-item-focus prev', mode='command')
config.bind('<Ctrl-D>', 'completion-item-del', mode='command')

# Open in another browser
config.bind(';f', 'spawn firefox --new-tab {url}')
config.bind(';c', 'spawn chromium {url}')

# BIB
config.bind(',a', f'spawn --userscript {USERSCRIPTS}/getdoi.py')
config.bind(',e', f'spawn --userscript {USERSCRIPTS}/getemail.py')
config.bind(',s', f'spawn --userscript {USERSCRIPTS}/dl_pdf.py')

# Wallabag
config.bind('B', 'spawn -v -m wallabag add {url}')

# MPV
config.bind(',my', f'spawn --userscript {USERSCRIPTS}/mpv')
config.bind(',fy', f'hint links userscript {USERSCRIPTS}/mpv')

config.bind(',ms', f'spawn --userscript {USERSCRIPTS}/streamlink')
config.bind(',fs', f'hint links userscript {USERSCRIPTS}/streamlink')

# Pass
config.bind('zl', 'spawn --userscript qute-pass')
config.bind('zul', 'spawn --userscript qute-pass --username-only')
config.bind('zpl', 'spawn --userscript qute-pass --password-only')
config.bind('zc', f'spawn --userscript {USERSCRIPTS}/create_pass')

config.bind('<Ctrl-L>', 'download-clear;; clear-messages')

c.colors.tabs.odd.bg = "#1d1f21"
c.colors.tabs.odd.fg = "#969896"
c.colors.tabs.even.bg = "#373b41"
c.colors.tabs.even.fg = "#969896"

c.colors.hints.bg = "#eab700"
c.colors.hints.fg = "#1d1f21"
