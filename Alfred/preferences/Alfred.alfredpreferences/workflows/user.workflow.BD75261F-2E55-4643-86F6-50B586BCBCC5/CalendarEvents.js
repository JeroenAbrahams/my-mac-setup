#!/usr/bin/osascript -l JavaScript

// Copyright (c) 2020 Dean Jackson <deanishe@deanishe.net>
// MIT Licence applies http://opensource.org/licenses/MIT

ObjC.import('AppKit')
ObjC.import('EventKit')

const store = $.EKEventStore.alloc.init


// check for/request access to user's calendars
function haveAccess() {
	let ok = null

	store.requestAccessToEntityTypeCompletion($.EKEntityTypeEvent, function(granted, err) {
		ok = granted
	})
	while (ok === null) {
		delay(0.01)
	}
	return ok
}


// convert an NSColor to an array
function convertColour(colour) {
	colour = colour.colorUsingColorSpace($.NSColorSpace.deviceRGBColorSpace)
	let r = ObjC.unwrap(colour.redComponent),
		g =	ObjC.unwrap(colour.greenComponent),
		b =	ObjC.unwrap(colour.blueComponent),
		a =	ObjC.unwrap(colour.alphaComponent)

	return [r, g, b, a]
}


// load events for number of coming days
function getEvents(days) {
	// retrieve all accounts & their calendars
	let calendars = $.NSMutableArray.alloc.init,
		colours = {}

	ObjC.unwrap(store.sources).forEach(source => {
		console.log(`${ObjC.unwrap(source.title)}`)

		let cals = source.calendarsForEntityType($.EKEntityTypeEvent).allObjects
		ObjC.unwrap(cals).forEach(calendar => {
			console.log(`  +-- ${ObjC.unwrap(calendar.title)}`)
			colours[ObjC.unwrap(calendar.calendarIdentifier)] = convertColour(calendar.color)
			calendars.addObject(calendar)
		})
	})

	// retrieve all events from start of today until n days from now
	var endDateComponents = $.NSDateComponents.alloc.init
	endDateComponents.day = days
	let endDate = $.NSCalendar.currentCalendar.dateByAddingComponentsToDateOptions(endDateComponents, $.NSDate.now, 0)
	let predicate = store.predicateForEventsWithStartDateEndDateCalendars($.NSCalendar.currentCalendar.startOfDayForDate($.NSDate.now), endDate, calendars)

	let events = ObjC.unwrap(store.eventsMatchingPredicate(predicate))
	return [events, colours]
}


// execute script
function run(argv) {
	if (!haveAccess()) {
		return JSON.stringify({error: 'No Access to Calendars', events: []})
	}

	let days = 7,
		events = [],
		formatter = $.NSISO8601DateFormatter.alloc.init

	// convert all times to local time because Python sucks at timezones
	formatter.timeZone = $.NSTimeZone.localTimeZone

	if (argv.length > 0) days = parseInt(argv[0], 10)

	let arr = getEvents(days),
		ekEvents = arr[0],
		colours = arr[1]

	ekEvents.forEach(event => {
		if (event.status === $.EKEventStatusCanceled) return
		if (event.allDay) return

		let title = ObjC.unwrap(event.title),
			url = ObjC.unwrap(event.URL.absoluteString),
			notes = ObjC.unwrap(event.notes),
			location = ObjC.unwrap(event.location)

		// ensure these have values otherwise they'll be omitted from
		// JSON output because they're undefined
		title = title ? title : ''
		url = url ? url : ''
		notes = notes ? notes : ''
		location = location ? location : ''

		events.push({
			uid: ObjC.unwrap(event.eventIdentifier),
			title: title,
			url: url,
			notes: notes,
			location: location,
			account: ObjC.unwrap(event.calendar.source.title),
			calendar: ObjC.unwrap(event.calendar.title),
			calendar_id: ObjC.unwrap(event.calendar.calendarIdentifier),
			start_date: ObjC.unwrap(formatter.stringFromDate(event.startDate)),
			end_date: ObjC.unwrap(formatter.stringFromDate(event.endDate)),
			colour: colours[ObjC.unwrap(event.calendar.calendarIdentifier)],
		})
	})

	events.sort((a, b) => {
		if (a.start_date < b.start_date) return -1
		if (a.start_date > b.start_date) return 1
		if (a.title < b.title) return -1
		if (a.title > b.title) return 1
		return 0
	})

	console.log(`${events.length} event(s)`)

	return JSON.stringify({error: null, events: events})
}