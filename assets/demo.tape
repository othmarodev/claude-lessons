# vhs tape for never-again's demo GIF.
# Install vhs (https://github.com/charmbracelet/vhs):  brew install vhs
# Render:  cd ~/Desktop/claude-lessons && vhs assets/demo.tape   →  assets/demo.gif
# Then reference it in README.md instead of (or above) prevention-moment.svg.

Output assets/demo.gif

Set Shell "bash"
Set FontSize 20
Set Width 1200
Set Height 640
Set Padding 24
Set Theme { "name": "nevergain", "background": "#0d1117", "foreground": "#c9d1d9", "cursor": "#0d1117", "black": "#0d1117", "red": "#ff5f56", "green": "#7ee787", "yellow": "#e3b341", "blue": "#58a6ff", "magenta": "#a371f7", "cyan": "#39c5cf", "white": "#c9d1d9", "brightBlack": "#6e7681", "brightWhite": "#f0f6fc" }

Hide
Type "bash assets/demo.sh" Enter
Show
Sleep 18s
