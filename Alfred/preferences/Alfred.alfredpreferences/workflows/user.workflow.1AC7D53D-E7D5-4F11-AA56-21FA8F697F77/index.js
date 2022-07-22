'use strict';
const alfy = require('alfy');

const KEY = process.env.KEY;
const TOKEN = process.env.TOKEN;

if (KEY.length == 0) {
	alfy.output([{
		title: 'You need to set your key and token.',
		subtitle: 'Press [Enter ↵] to see instructions.',
		arg: 'https://gistpreview.github.io/?ee0586bba9d9e3ec13d5ad32ebf75ba5',
	}])
} else {
	const defaultNullResults = {
		title: `Nothing found for "${alfy.input}"`,
		subtitle: 'Try changing the search query.'
	}
	
	alfy.fetch('https://api.trello.com/1/search', {
			query: {
				query: `-is:archived ${alfy.input}`,
				key: KEY,
				token: TOKEN
			}
		})
		.then(data => {
			const items = data.cards.map(x => ({
				uid: x.id,
				title: x.name,
				autocomplete: x.name,
				subtitle: x.desc,
				arg: x.url
			}));
			alfy.output(items.length ? items : [defaultNullResults])
		});
}

