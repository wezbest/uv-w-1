#!/usr/bin/env fish
echo -e ""
echo -e "This will install the following"
echo -e "1. Rust "
echo -e "2. Fish "
echo -e "3. Rust - eza fd-find starship"
echo -e ""
# Rust Installation
yes | curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup update
cargo --version

# Fish Install
sudo apt-add-repository ppa:fish-shell/release-3 -y
sudo apt install libwebkit2gtk-4.0-dev libgtk-3-dev libappindicator3-dev -y
sudo apt-get install fish -y

# Brwe Install
brew install fzf
yes | /home/linuxbrew/.linuxbrew/opt/fzf/install
fzf_key_bindings

# Cargo Installs
echo "Cargo Installs "
echo "eza = exa alternative"
echo "fd-find = find alternative"
echo "starship = starship prompt"
echo "ripgrep = grep alternative"
echo "cfonts = Text banner"
echo "artem = Image to color ascii"
echo "bat = cat alternative"
echo "lolcrab = Rainbow text generator"

cargo install eza fd-find starship ripgrep cfonts artem bat lolcrab image-to-ascii

# Starship init and preset
echo "starship init fish | source" >~/.config/fish/config.fish
starship preset pure-preset >~/.config/starship.toml
cp ./wz/config2.fish ~/.config/fish/config.fish
