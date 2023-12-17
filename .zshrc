# ###############
# Zsh fig file
# by @gaalcaras
# ###############

# GENERAL {{{

autoload -U zmv

setopt prompt_subst

setopt glob_complete
setopt complete_in_word
setopt completealiases
setopt always_to_end
setopt auto_menu

# Ask to correct commands but not arguments
setopt nocorrectall
setopt correct

# Completion
# Loading completion cache can slow down zsh startup. A quick fix is to only do
# that once a day :
# https://gist.github.com/ctechols/ca1035271ad134841284#gistcomment-2308206
autoload -Uz compinit

for dump in ~/.cache/zsh/.zcompdump(N.mh+24); do
  compinit
done

compinit -C

autoload -U +X bashcompinit && bashcompinit

zstyle ':completion*:default' menu 'select=0'
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}' 'r:|=*' 'l:|=* r:|=*'
zstyle ':completion:*' list-colors ''

# History

# Disable history if NOHISTFILE is passed via environment variable
if [ ! -z $NOHISTFILE ] && $NOHISTFILE; then
  unset HISTFILE
else
  export HISTFILE="$HOME/.zsh_history"
  export SAVEHIST=100000
  export HISTSIZE=100000
  export HISTFILESIZE=100000

  setopt extended_history
  setopt HIST_FIND_NO_DUPS
  setopt inc_append_history_time
fi

source ~/.local/bin/user/zsh/history

# }}}

# EXPORTS {{{

# If TERM is set to xterm-256color mutt has problems redrawing
# after viewing attachments.
# See: https://superuser.com/questions/844058/tmux-mutt-not-redrawing
# export TERM="screen-256color"
# export TERM="alacritty"
# Alacritty advices to set $TERM in alacritty config

export GOPATH="$HOME/faire/programmer/go"
export GOBIN="$GOPATH/bin"

export PATH=$(find $HOME/.local/bin/user/ -type d -printf "%p:")$(find $HOME/.dotfiles/bin/ -type d -printf "%p:")/usr/local/bin:$HOME/.gem/ruby/2.6.0/bin:/bin:/usr/local/bin:/usr/bin:/usr/bin/vendor_perl:/usr/bin/core_perl:$GOBIN:/home/gaalcaras/.gem/ruby/3.0.0/bin:$HOME/.local/bin:$HOME/.local/bin/rsync-time-backup/

export EDITOR="nvim"
export OPENER="xdg-open"
export PDFREADER="/usr/bin/zathura"
export BROWSER="/usr/bin/qutebrowser"
export TERMINAL="/usr/bin/alacritty -e"
export MANPATH="/usr/local/man:$MANPATH"

export BIB_DIR="$HOME/Nextcloud/bib"
export BIB_FILE="$BIB_DIR/master.bib"
export BIB_PDF_DIR="$BIB_DIR/pdf"
export BIB_NOTE_DIR="$HOME/inbox/notes/apprendre/bib"

export SUDO_ASKPASS=$HOME/.config/rofi/modules/rofi_sudo_askpass

# For qutebrowser userscript readability-js
# WARNING : slows down zsh considerably (+0.2s)
# export NODE_PATH=$NODE_PATH:$(npm root -g)

export CHEATCOLORS=true

export WINEPREFIX=$HOME/.adewine/

# ROFI
export ROFICOL=1
export ROFIACCENT=#b294bb # Tomorrow Purple

export LF_ICONS="\
di=:\
ex=:\
*.pdf=:\
*.epub=:\
*.png=:\
*.jpg=:\
*.jpeg=:\
*.doc=󱀾:\
*.docx=󱀾:\
*.odt=󱀾:\
*.xls=:\
*.xlsx=:\
*.ods=:\
*.ppt=:\
*.pptx=:\
*.csv=:\
*.json=:\
*.py=:\
*.R=:\
*.py=:\
*.sh=:\
*.bash=:\
"
# }}}

# VIM KEYBINDING {{{
bindkey -v

# http://zsh.sourceforge.net/Doc/Release/Zsh-Line-Editor.html
bindkey -M vicmd '^' vi-beginning-of-line
bindkey -M vicmd '0' vi-beginning-of-line

bindkey -M vicmd 'c' vi-backward-char
bindkey -M vicmd 'r' vi-forward-char

# Vi mode breaks up and down arrow keys with history search.
# This is the fix:
# https://github.com/robbyrussell/oh-my-zsh/issues/1720#issuecomment-286366959

autoload -U history-search-end
zle -N history-beginning-search-backward-end history-search-end
bindkey "^[[A" history-beginning-search-backward-end

bindkey -M vicmd 'b' backward-word
bindkey -M vicmd 'é' forward-word

bindkey -M vicmd 'yy' vi-yank-whole-line
bindkey -M vicmd 'Y' vi-yank-eol

bindkey -M vicmd 'l' vi-change-eol
bindkey -M vicmd 'L' vi-change-eol
bindkey -M vicmd 'll' vi-change-whole-line

# }}}

# PROMPT {{{

function git_prompt_info() {
  ref=$(git symbolic-ref HEAD 2> /dev/null) || return
  branch=$(basename "$ref")
  gst=''
  color="green"
  unstaged=$(git status --porcelain | cut -c1-3 | grep \? | wc -l)
  changed=$(git status --porcelain | cut -c1-3 | grep -v \? | wc -l)
  (($unstaged > 0)) && unstaged="?" || unstaged=""
  (($changed > 0)) && changed="+" && color="red" || changed=""
  echo "%F{$color}[$branch$changed$unstaged] %f"
}

function pre_prompt() {
  uname=$(whoami)
  [[ "$uname" != "gaalcaras" ]] && echo "$uname"
  hostname=$(hostname)
  [[ "$hostname" != "batcave" ]] && echo "@$hostname"
}

function private_zsh() {
  if [ -z $HISTFILE ]; then
    echo "%K{red}%B%F{black}_>%f%b%K%F{red}"
  else
    echo "$%f"
  fi
}

PROMPT='%F{blue}$(pre_prompt)%(l..:.)%f%F{magenta}%~%f $(git_prompt_info)$(private_zsh) '

# }}}

# ALIASES {{{

alias fig='/usr/bin/git --git-dir=$HOME/.dotfiles_/ --work-tree=$HOME'

# ls aliases
alias ls="ls -F --color=auto --block-size=M"
alias la="ls -a"
alias ll="ls -l"
alias lla="ll -a"
alias ldot="ll -d .*"

# Directories
alias pdw="cd ~/Documents/phd-writing"

# Git aliases
alias glog="git log --graph --pretty=format:'%Cred%h%Creset %an: %s - %Creset %C(yellow)%d%Creset %Cgreen(%cr)%Creset' --abbrev-commit --date=relative"
alias gst='git status -sb'
alias gc='git commit'
alias ga='git add -p'

# Locale stuff
alias git='LC_ALL=C git'
alias khal='LC_TIME=C khal'
alias ikhal='LC_TIME=C ikhal'

# Tools
alias bib="cd $BIB_DIR && $EDITOR $BIB_FILE"
alias nv="nvim"
alias nvimlua="NVIM_APPNAME=nvimlua nvim"
alias mutt='hash tmuxifier 2>/dev/null && tmuxifier load-window mutt || neomutt -n' # Check if tmuxifier exists before loading mutt setup
alias mr='mr -d "$HOME"' # Multi-repos with minimal output and 5 parallel jobs
alias top='gtop'

# Development
alias nvtest='nvim +UpdateRemotePlugins +qall && nvim "+TranscribeAudio ~/Videos/googlepixel.webm"'

# Misc
alias reload='source ~/.zshrc'
alias msmtp-unlock="rm $HOME/.msmtpqueue/.lock"
alias stats="fc -l 1 | awk '{CMD[\$2]++;count++;}END { for (a in CMD)print CMD[a] \" \" CMD[a]/count*100 \"% \" a;}' | grep -v \"./\" | column -c3 -s \" \" -t | sort -nr | nl | head -n20"
alias mmv='noglob zmv -W'

# adestart() { WINEPREFIX="$HOME/.adewine/" wine "$HOME/.adewine" "/drive_c/Program Files/Adobe/Adobe Digital Editions 2.0/DigitalEditions.exe" >/dev/null 2>&1 & }

# }}}}

# DOTFILES {{{

function rc() {
  $EDITOR "$(fig ls-files | fzf)"
}

alias i3rc="$EDITOR ~/.config/i3/config"
alias msmtprc="$EDITOR ~/.msmtprc"
alias muttrc="$EDITOR ~/.config/neomutt/muttrc"
alias qutebrowserrc="$EDITOR ~/.config/qutebrowser/config.py"
alias lfrc="$EDITOR ~/.config/lf/lfrc"
alias rofirc="$EDITOR ~/.config/rofi/config.rasi"
alias vimrc="$EDITOR ~/.vimrc"
alias xinitrc="$EDITOR ~/.xinitrc"
alias zathurarc="$EDITOR ~/.config/zathura/zathurarc"
alias zshrc="$EDITOR ~/.zshrc"

# }}}

# CHECKLIST {{{

function checklist_add {
  local checklist="$1"
  local element="${@:2}"

  if [ "$element" = "" ]; then
    $EDITOR $checklist
  else
    echo "[ ] $element" >> "$checklist"
  fi
}

alias google="checklist_add $HOME/Nextcloud/Checklists/google.txt"
alias book="checklist_add $HOME/Nextcloud/Checklists/books.txt"

# }}}

# NOTE TAKING {{{

zettel() {
  local tmpdir=$(pwd)
  local cmd="Note $@"

  cd "$HOME/Zettelkasten/zettel"
  nvim -c "$cmd"

  cd "$tmpdir"
}

zstyle ':completion:*:*:zettel:*:*' file-sort 'reverse'
compdef '_path_files -W $HOME/Zettelkasten/zettel -g "*"' zettel

zstyle ':completion:*:*:note:*:*' file-sort 'reverse'
compdef '_path_files -W $HOME/Nextcloud/Notes -g "*.md"' note

# }}}

# INIT {{{

if [[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]]; then
#  sway
#  exit 0
fi

if hash register-python-argcomplete 2>/dev/null; then
  eval "$(register-python-argcomplete pubs)"
fi

if hash tmuxifier 2>/dev/null;
then
  eval "$(tmuxifier init -)"
fi

precmd() {
  print -Pn "\e]0;%m:%~\a"
}

function preexec {
  printf "\033]0;%s\a" "$1"
}

# }}}

# vim: fdm=marker fmr={{{,}}} fdl=0 fen
