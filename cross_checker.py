import os, csv, math

def getDoc(filename):

	f = open(filename, 'r')
	doc = f.read()
	f.close()
 
	return doc

def check(inside_folder):
	f1 = open('train/trained'+inside_folder+'.csv', 'r')
	reader = csv.reader(f1)
	words = []
	log1 = []
	log2 = []

	for row in reader:
		words.append(row[0])
		log1.append(float(row[3]))
		log2.append(float(row[4]))

	f2 = open('train/probs_'+inside_folder+'.csv', 'r')
	reader2 = csv.reader(f2)
	next(reader2)
	probs = next(reader2)
	cp1 = float(probs[0])
	cp2 = float(probs[1])
	def1 = float(probs[4])
	def2 = float(probs[5])

	f3  = open('results/results'+inside_folder+'.csv', 'w', newline='')
	writer = csv.writer(f3, delimiter=',')
	writer.writerow(['File', 'isSpam', 'isCorrect', 'Spam Probability', 'Not Spam Probability'])



	spam = 0
	notspam = 0
	correct = 0
	cnt = 0

	text_file = open('results/errors'+inside_folder+'.txt', 'w')
	super_results = open('results/super'+inside_folder+'.csv', 'w',newline='')
	super_writer = csv.writer(super_results,delimiter=",")

	filename ='./lemm_stop/'+inside_folder

	for test in os.listdir(filename):

		doc = getDoc(filename + '/' + test)

		doc = ''.join(ch for ch in doc if ( ch.isalnum() or ch.isspace() ) )
		doc = ' '.join(doc.split())
		doc = doc.split(' ')

		s_prob = cp1
		ns_prob = cp2

		for word in doc:
			try:
				i = words.index(word)
				s_prob += log1[i]
				ns_prob += log2[i]
			except:
				s_prob += def1
				ns_prob += def2

		if s_prob > ns_prob:
			isSpam = 1
			spam += 1
		else:
			isSpam = 0
			notspam += 1

		if (test[0] == 's' and isSpam == 1) or (test[0] != 's' and isSpam == 0):
			correctness = 1
			correct += 1
			#print('ok')
		else:
			correctness = 0
			#print('NOOOOOOOOoooooooooooOOOOOOOOOO0000OOOoooooo')
			text_file.write(test + '  ' + str(s_prob) + '  ' + str(ns_prob) + '\n')

		cnt += 1

		writer.writerow([test, isSpam, correctness, s_prob, ns_prob])
	super_writer.writerow(["folder","spam count","not spam count", "Correct","Errors","Total","Correct Percent"])
	super_writer.writerow([inside_folder,spam,notspam,correct,cnt-correct,cnt,round((correct/cnt)*100), 2])
	print('Folder: ', inside_folder)
	print('Spam Count:', spam)
	print('Not Spam Count:', notspam)
	print('Correct:', correct)
	print('Errors:', cnt-correct)
	print('Total:', cnt)
	print('Correct Percent:', round(((correct/cnt)*100), 2), '%')

	f1.close()
	f2.close()
	f3.close()
	text_file.close()
	super_results.close()

def start():
	path = './lemm_stop'
	for folder in os.listdir(path):
		check(folder)
print("Working, this will take awhile")
start()