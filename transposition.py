import sys

def encrypt(text,key):
	cur=0
	i=0
	arr=[]
	innerlist=[]

	for i in range(0,len(key)):
		innerlist.append((key[i],i))

	arr.append(innerlist)

	while 1:
		innerlist=[]
		for j in xrange(0,len(key)):
			while cur < len(text):
				if text[cur]==' ' or text[cur]=='\t' or text[cur]=='\n':
					cur=cur+1
				else:
					break	

			if cur < len(text):
				innerlist.append(text[cur])
				cur=cur+1
			else:
				innerlist.append('~')

		arr.append(innerlist)		
		if cur >= len(text):
			break

	for i in xrange(1,len(arr)):
		for j in arr[i]:
	  		sys.stdout.write(j)
	  	print

	s=sorted(arr[0], key=lambda k: k[0])
	#print s

	output=""
	for i in xrange(0,len(s)):
		for j in xrange(1,len(arr)):
			output+=str(arr[j][s[i][1]])	

	return output

def decrypt(text,key):
	arr=[]
	for i in xrange(0,len(text)/len(key)):
		innerlist=[]
		for j in xrange(0,len(key)):
			innerlist.append(0)
		arr.append(innerlist)

	innerlist=[]
	for i in range(0,len(key)):
		innerlist.append((key[i],i))
	s=sorted(innerlist, key=lambda k: k[0])

	cur=0
	for i in xrange(0,len(s)):
		for j in xrange(0,len(arr)):
			arr[j][s[i][1]]=text[cur]
			cur=cur+1

	output=""
	for i in xrange(0,len(arr)):
		for j in xrange(0,len(key)):
			output+=str(arr[i][j])	

	return output


sys.stdout.write("Enter text to encrypt : ")
text=raw_input()
text.replace(" ","")

sys.stdout.write("Enter key : ")
key=raw_input()
key.replace(" ","")

output=encrypt(text,key)
print "Encrypted text = " + output

answer=decrypt(output,key)
print "Decrypted text = " + answer
