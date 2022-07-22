#!/usr/bin/env osascript

#<editor-fold desc="Preamble">
(*
    F Beccaria
    Copyright (C) 2020
	https://www.beccaria.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
*)
#</editor-fold>

# ------------------------------------------
on run (argv)
	if count of argv < 2 then
   		showAlert("Ooops. Missing required workflow environment variables!")
		return
	end if

	# parse passthrough parameters (the workflow environment variables), where:
	#     argv[0] (required):  is the Xcode version (actual filename minus file extension)
	#     argv[1] (required):  is the full path to the destination folder
	#     argv[2] (optional):  is the name of the playground to be created (timestamp if missing)
	set xcVersion to "blank"
	set xcVersionExists to false
	set pgFolder to "blank"
	set pgFolderExists to false
	try
		set xcVersion to item 1 in argv
		set pgFolder to item 2 in argv
		set xcTargetPath to (path to applications folder as text) & xcVersion & ".app"
		tell application "Finder"
			if (exists file xcTargetPath) then
				set xcVersionExists to true
			end if
			if (exists folder (pgFolder as POSIX file as text)) then
				set pgFolderExists to true
			end if
		end tell
	end try

	# validate parameters & create playground
	if xcVersionExists then
		if pgFolderExists then
			try
				set pgName to item 3 in argv
			on error
				set pgName to getDefaultName()
			end try

			# create playground
			createNewPlayground(POSIX path of xcTargetPath, pgFolder, pgName)

		else
			showAlert("Ooops! Unable to find destination folder: " & pgFolder)
		end if
	else
		showAlert("Ooops! Unable to find file Xcode version: " & xcVersion)
	end if
end run

# ------------------------------------------
on createNewPlayground(xcPath, pgPath, pgName)
	try
		# bring up Xcode
		activate application xcPath
		repeat until application xcPath is running
			delay 0.1
		end repeat
		delay 0.1

		# tell Xcode to create new playground file
		tell application "System Events"
			set xcProcess to the first process whose POSIX path of application file is equal to xcPath
			tell xcProcess

				# Select "File" -> "New" -> "Playground" in Xcode
				click menu item 9 of menu 1 of menu item "New" of menu 1 of menu bar item "File" of menu bar 1
				delay 0.02

				# click "Next" to advance to the save dialog screen
				click button "Next" of sheet 1 of window 1
				delay 0.1

				# change dir to PG save folder
				keystroke "g" using {shift down, command down}
				delay 0.5
				keystroke pgPath
				delay 0.02
				click button "Go" of sheet 1 of sheet 1 of sheet 1 of window 1
				delay 0.1

				# set filename
				set value of text field 1 of sheet 1 of sheet 1 of window 1 to pgName & ".playground"
				delay 0.02

				# "press" Create
				click button "Create" of sheet 1 of sheet 1 of window 1
			end tell
		end tell

	on error
		showAlert("Ooops! Unable to launch " & xcPath)
	end try
end createNewPlayground

# ------------------------------------------
on getDefaultName()
	set isDate to getDate()
	set isTime to getTime()
	return "PG_" & isDate & "__" & isTime
end getDefaultName

# ------------------------------------------
on getDate()
	set isToday to short date string of (current date)
	set [_day, _month, _year] to [day, month, year] of date isToday
	set _month to _month * 1 --> 3
	set _month to text -1 thru -2 of ("0" & _month) --> "03"

	set the text item delimiters to "-"
	set isToday to {_year, _month, _day} as string
	return isToday as string
end getDate

# ------------------------------------------
on getTime()
	set isNow to time string of (current date)
	set [_hours, _minutes, _seconds] to [hours, minutes, seconds] of date isNow
	set isHour to (_hours as string)
	if _hours < 10 then
		set isHour to "0" & isHour
	end if
	set isMin to (_minutes as string)
	if _minutes < 10 then
		set isMin to "0" & isMin
	end if
	set isSec to (_seconds as string)
	if (_seconds < 10) then
		set isSec to "0" & isSec
	end if
	return isHour & "-" & isMin & "-" & isSec
end getTime

# ------------------------------------------
on showAlert(alertText)
	tell application "Finder"
		activate
		display alert alertText
	end tell
end showAlert
