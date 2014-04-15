alpha = ['A','B','C','D','E','F','G','H','I','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def get_key():
	k = raw_input().upper()
	key = []
	for char in k:
		if char in alpha and char not in key: # add the character to the matrix if it's valid and not already in the matrix
			key.append(char)
		elif char is "J": # handle the case when the letter J appears in the key
			key.append("I")
	for char in alpha:
		if char not in key: # add the rest of the alphahet not appearing in the key to the matrix
			key.append(char)
	return key

def gen_matrix(key):
	matrix = []
	counter = 0
	if key == '': # create a blank matrix
		for xcounter in xrange(5):
			x = []
			for ycounter in xrange(5):
				x.append(alpha[counter])
				counter += 1
			matrix.append(x)
	else: # create a keyed matrix
		for xcounter in xrange(5):
			x = []
			for ycounter in xrange(5):
				x.append(key[counter])
				counter += 1
			matrix.append(x)
	return matrix


def print_matrix(matrix):
	for counter in xrange(5):
		print "%c %c %c %c %c" % (matrix[counter][0], matrix[counter][1], matrix[counter][2], matrix[counter][3], matrix[counter][4])
	print "\n"


def get_message():
	m = raw_input()
	m2 = []
	for char in m.upper():
		if char in alpha: # handle valid characters in the message
			m2.append(char)
		elif char == "J": # handle the case when "J" appears in the message
			m2.append("I") 
		elif char == ".": # swap out the period with an x, for convenience
			m2.append("X")
	return ''.join(m2)


def encrypt(message, key_matrix):
	coords = []
	ciphertext = []
	digraphs = parse_message(message)

	for d in digraphs:
		swap = []
		temp = []
		coords = get_coords(d, key_matrix)
		if coords[0][0] == coords[1][0]: # digraph lies on same x axis
			x,y  = ((coords[0][0], (coords[0][1] + 1) % 5))
			swap.append((x,y))
			x,y  = ((coords[1][0], (coords[1][1] + 1) % 5))
			swap.append((x,y))
		elif coords[0][1] == coords[1][1]: # digraph lies on same y axis
			x,y  = (((coords[0][0] + 1) % 5), coords[0][1])
			swap.append((x,y))
			x,y  = (((coords[1][0] + 1) % 5), coords[1][1])
			swap.append((x,y))
		else: # digraph lies on different x & y axis
			swap.append((coords[0][0], coords[1][1]))
			swap.append((coords[1][0], coords[0][1]))

		for x,y in swap:
			ciphertext.append(key_matrix[x][y])

	print "Your encrypted message is: %s " % ''.join(ciphertext)


def decrypt(message, key_matrix):
	coords = []
	plaintext = []
	digraphs = parse_message(message)

	for d in digraphs:
		swap = []
		temp = []
		coords = get_coords(d, key_matrix)
		if coords[0][0] == coords[1][0]: # digraph lies on same x axis
			x,y  = ((coords[0][0], (coords[0][1] - 1) % 5))
			swap.append((x,y))
			x,y  = ((coords[1][0], (coords[1][1] - 1) % 5))
			swap.append((x,y))
		elif coords[0][1] == coords[1][1]: # digraph lies on same y axis
			x,y  = (((coords[0][0] - 1) % 5), coords[0][1])
			swap.append((x,y))
			x,y  = (((coords[1][0] - 1) % 5), coords[1][1])
			swap.append((x,y))
		else: # digraph lies on different x & y axis
			swap.append((coords[0][0], coords[1][1]))
			swap.append((coords[1][0], coords[0][1]))

		for x,y in swap:
				plaintext.append(key_matrix[x][y])

	print "Your decrypted message is: %s " % ''.join(plaintext)


def parse_message(message):
	digraphs = []
	while len(message) > 0:
		digraph = message[:2]
		if len(digraph) == 1: # trailing single chracter at the end of the message
			digraph = digraph = "%c%c" % (digraph[0], "X")
			digraphs.append(digraph)
			message = message[1:]
		elif digraph[0] == digraph[1]: # handle double letters appearing in the same digraph
			digraph = "%c%c" % (digraph[0], "X")
			digraphs.append(digraph)
			message = message[1:]
		else: # add the digraph to the list
			digraphs.append(digraph)
			message = message[2:]

	return digraphs 


def get_coords(digraph, key_matrix):
	coords = []
	for char in digraph:
		for x in xrange(5):
			for y in xrange(5):
				if key_matrix[x][y] == char:
					coords.append((x,y))
	return coords


def main():
	m = gen_matrix('')
	print "\nInitial PLAYFAIR matrix:\n"
	print_matrix(m)

	print "Enter a key:"
	k = get_key()

	print "\nKeyed PLAYFAIR matrix:\n"
	m = gen_matrix(k)
	print_matrix(m)

	decision = ""
	while decision is not "1" and decision is not "2":
		print "Would you like to encrypt or decrypt a message?"
		print "1 - Encrypt message"
		print "2 - Decrypt Message"
		print "\nDecision:"
		decision = raw_input()

	if decision == "1":
		print "\nEncrypt Message:"
		print "Enter the message you would like to encrypt. \nThe only valid characters are the letters A-Z. \nPeriods may be denoted with an X"
		message = get_message()
		print "The message you entered was: %s" % message
		ciphertext = encrypt(message, m)

	elif decision == "2":
		print "\nDecrypt Message:"
		print "Enter the message you would like to decrypt. \nThe only valid characters are the letters A-Z."
		message = get_message()
		print "The message you entered was: %s" % message
		plaintext = decrypt(message, m)

	else:
		print "Invalid Entry"


if __name__ == "__main__":
	main()