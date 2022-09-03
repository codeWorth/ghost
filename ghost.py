# all_chars = {'a', '\n', "'", 's', 'm', 'd', 'o', 'l', 'w', 'c', 'h', 'e', 'n', 'i', 'y', 'r', 'b', 't', 'u', 'j', 'g', 'p', 'v', 'x', 'f', 'k', 'z', 'q', 'ó', 'ü', 'á', 'ö', 'ñ', 'é', 'ä', 'è', 'ç', 'ô', 'í', 'â', 'û', 'ê', 'å'}
valid_chars = {'a', '\n', "'", 's', 'm', 'd', 'o', 'l', 'w', 'c', 'h', 'e', 'n', 'i', 'y', 'r', 'b', 't', 'u', 'j', 'g', 'p', 'v', 'x', 'f', 'k', 'z', 'q'}
blacklisted_words = {
	"h'm\n",
	"nth\n",
	"mien\n"
}
minimum_word_length = 3

def all_valid(word):
	for char in word:
		if not char in valid_chars:
			return False

	return True

def has_caps(word):
	return word.lower() != word

def is_possessive(word):
	return word[-3:] == "'s\n"

def only_newline(dictionary):
	return len(dictionary) == 1 and '\n' in dictionary

def potential_words(word, dictionary):
	if len(word) == 0:
		return dictionary

	if not word[0] in dictionary:
		return None
	else:
		return potential_words(word[1:], dictionary[word[0]])

def get_words(dictionary):
	if len(dictionary) == 0:
		yield ""
	else:
		for letter in dictionary.keys():
			for frag in get_words(dictionary[letter]):
				yield letter + frag

def play_game(sub_word_len, words, player_turn, player_count):
	winning_player = None
	word_frag = None
	sub_word_len += 1
	for letter in words.keys():
		if letter == '\n':
			continue
		if sub_word_len >= minimum_word_length and '\n' in words[letter]:
			continue
		if only_newline(words[letter]):
			continue

		_winning_player, _word_frag = play_game(sub_word_len, words[letter], (player_turn + 1) % player_count, player_count)
		_word_frag = letter + _word_frag
		if _winning_player == player_turn:
			return (_winning_player, _word_frag)

		# if we can't win, chose the shortest word to get this over with ASAP
		if winning_player is None or len(_word_frag) < len(word_frag):
			winning_player = _winning_player
			word_frag = _word_frag

	if winning_player is None: # if we have no valid options, the previous player wins
		last_letter = next(word for word in words.keys() if word != '\n')
		return ((player_turn - 1) % player_count, last_letter)
	else:
		return (winning_player, word_frag)


with open("/usr/share/dict/american-english", "r") as words_file:
	print("Building dictionary...")
	words = {}
	for line in words_file:
		if has_caps(line):
			continue

		line = line.lower()
		if line in blacklisted_words:
			continue
		if is_possessive(line):
			continue
		if not all_valid(line):
			continue

		sub_words = words
		for char in line:
			if not char in sub_words:
				sub_words[char] = {}

			sub_words = sub_words[char]

	print("Done")
	player_count = int(input("Number of players: "))
	if player_count < 2:
		print("Invalid number of players, must be greater than 1")
		exit(0)

	while True:
		starting_letters = input("Starting letters: ").strip().lower()
		
		if not all_valid(starting_letters):
			print("Invalid starting letters, contains illegal characters")
			exit(0)

		sub_words = potential_words(starting_letters, words)
		if sub_words is None:
			print("Invalid starting letters, does not begin a word")
			exit(0)

		if len(starting_letters) >= minimum_word_length and '\n' in sub_words:
			print("Invalid starting letters, already is a word")
			exit(0)


		winning_player, word_frag = play_game(len(starting_letters), sub_words, len(starting_letters) % player_count, player_count)
		winning_word = starting_letters + word_frag
		print(winning_player, winning_word)
		if len(input("...")) > 0:
			break
