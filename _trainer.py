import os
import csv
import numpy as np
import math

# get doc from txt file

def getDoc(filename):

	f = open(filename, 'r')
	doc = f.read()
	f.close()
 
	return doc

path = './lemm_stop'

spm_count = 0
nspm_count = 0
all_count = 0

spm_doc = ''
nspm_doc = ''

test_ctr = 0

# - file reading

for folder in os.listdir(path):	# for each part (1-9)

	if folder != 'part10':

		filename = path + '/' + folder

		for txtfile in os.listdir(filename): # for each txtfile

			doc = getDoc(filename + '/' + txtfile)

			if txtfile[0] == 's':	# if spam > all spam msgs start with s
				spm_count += 1
				spm_doc += ' ' + doc

			else:
				nspm_count += 1
				nspm_doc += ' ' + doc

			test_ctr += 1
			print(test_ctr)


all_count = spm_count + nspm_count
spm_prob = spm_count/all_count
nspm_prob = nspm_count/all_count

temp = ''.join(ch for ch in spm_doc if ( ch.isalnum() or ch.isspace() ) )
temp = ' '.join(temp.split())
spm_words = temp.split(' ')

temp = ''.join(ch for ch in nspm_doc if ( ch.isalnum() or ch.isspace() ) )
temp = ' '.join(temp.split())
nspm_words = temp.split(' ')

spm_words_count = len(spm_words)
nspm_words_count = len(nspm_words)

combined = spm_words + nspm_words

vocab = list(set(combined))
v = len(vocab)

denom1 = spm_words_count + v
denom2 = nspm_words_count + v
def_prob1 = 1/denom1
def_prob2 = 1/denom2

f  = open('probs.csv', 'w', newline='')
writer = csv.writer(f, delimiter=',')
writer.writerow(['Class 1 (Spam) Prob.', 'Class 2 (Not Spam) Prob.', 
				'Default (Spam) Prob.', 'Default (Not Spam) Prob.', 
				'(Spam) Log', '(Not Spam) Log'])
writer.writerow([spm_prob, nspm_prob, def_prob1, def_prob2, math.log(def_prob1), math.log(def_prob2)])

f.close()

f  = open('trained4.csv', 'w', newline='')
writer = csv.writer(f, delimiter=',')

test_ctr = 0

# writer.writerow(['Word', 'Spam (Prob.)', 'Not Spam (Prob.)', 'Spam (Log of Prob.)', 'Not Spam (Log of Prob.)'])

for word in vocab:
	p1 = ((spm_words.count(word) + 1) / denom1)
	p2 = ((nspm_words.count(word) + 1) / denom2)
	writer.writerow([word, p1, p2, math.log(p1), math.log(p2)])

	print(test_ctr)
	test_ctr += 1

f.close()

print(';)')