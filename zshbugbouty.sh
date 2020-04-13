# Fuente: https://www.youtube.com/watch?v=MF4qRSedmEs
# Fuente: https://awesomelists.net/275-ZSH%20Plugins/0-All--page1--sortBy-stars/
# Fuente: https://github.com/nahamsec/bbht

sudo apt install curl wget man zsh
wget https://github.com/Peltoche/lsd/releases/download/0.17.0/lsd-musl_0.17.0_amd64.deb
wget https://github.com/sharkdp/bat/releases/download/v0.13.0/bat_0.13.0_amd64.deb
sudo dpkg -i lsd-musl_0.17.0_amd64.deb
sudo dpkg -i bat_0.13.0_amd64.deb
sudo apt install zsh-autosuggestions zsh-syntax-highlighting -y 
git clone https://github.com/nahamsec/bbht.git
cd bbht
chmod +x install.sh
./install.sh
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k
echo 'source ~/powerlevel10k/powerlevel10k.zsh-theme' >> ~/.zshrc
mkdir ~/.zshplugins
cd
curl https://raw.githubusercontent.com/virtualshoot/scriptsPersonales/master/p10k.zsh -o .p10k.zsh
echo "function rmk(){
scrub -p dod \$1; shred -zun 10 -v \$1
}" >> .zshrc
source .zshrc
rmk lsd-musl_0.17.0_amd64.deb
rmk bat_0.13.0_amd64.deb
echo "SAVEHIST=5000" >> .zshrc
echo "HISTFILE=~/.zsh_history" >> .zshrc
echo "export HISTTIMEFORMAT='%F %T : '" >> .zshrc
echo "alias history='history -E'" >> .zshrc
echo "alias ll='lsd -lh --group-dirs=first'" >> .zshrc
echo "alias la='lsd -a --group-dirs=first'" >> .zshrc
echo "alias l='lsd --group-dirs=first'" >> .zshrc
echo "alias ls='lsd -lha --group-dirs=first'" >> .zshrc
echo "alias man='/usr/bin/man'" >> .zshrc
source .zshrc
curl https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/plugins/colored-man-pages/colored-man-pages.plugin.zsh -o ~/.zshplugins/colored-man-pages.plugin.zsh
curl https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/plugins/sudo/sudo.plugin.zsh -o ~/.zshplugins/sudo.plugin.zsh 
echo "source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh" >> .zshrc
echo "source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> .zshrc
echo "source ~/.zshplugins/colored-man-pages.plugin.zsh" >> .zshrc
echo "source ~/.zshplugins/sudo.plugin.zsh" >> .zshrc
