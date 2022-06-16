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
	brew install --cask alfred
	brew install --cask google-chrome
	brew install --cask postman

brew_installs: ## Install all Brew packages
	brew tap espanso/espanso
	brew install espanso
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
