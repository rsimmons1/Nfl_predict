with open('/usr/share/dict/american-english', 'r') as f:
	words = map(lambda word: word.upper(), f.read().split('\n'))
