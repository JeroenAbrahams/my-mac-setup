help: ## This help dialog.
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//'`); \
	for help_line in $${help_lines[@]}; do \
		IFS=$$'#' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf "%-30s %s\n" $$help_command $$help_info ; \
	done

espanso_setup:
	cp ./Espanso/base.yml ~/Library/Application\ Support/espanso/match/base.yml

brew_cask_installs:
## Default
	brew install --cask google-chrome
	brew install --cask 1password
## Development
	brew install --cask iterm2
	brew install --cask postman
	brew install --cask visual-studio-code
## brew install --cask appcleaner
## Productivity
	brew install --cask grammarly
	brew install --cask espanso
	brew install --cask monitorcontrol
	brew install --cask alfred
## brew install --cask raycast
##Uses to automatic open google links in a google App
	brew install --cask finicky
## Aviobook
	brew install --cask iexplorer
	brew install --cask bitwarden
	brew install --cask tunnelblick
	brew install --cask mongodb-realm-studio

## brew install --cask cheatsheet
## brew install --cask alt-tab

brew_installs: ## Install all Brew packages
## brew tap espanso/espanso
## brew install espanso
	brew install zsh
	brew install plantuml
	brew install robotsandpencils/made/xcodes
## Fuck automatic correct command
	brew install thefuck
## TBC IF NEEDED	
## brew install pyenv
## brew install rbenv
## Swift specifics
## brew install cocoapods
## brew install sourcery
## brew install xcodegen
## Aviobook
## brew install ansible
## brew install dependency-check
## brew install swiftplantumlapp
## brew install mitmproxy
## Tools
## brew install node


zsh:
	sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
