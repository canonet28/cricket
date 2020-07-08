import random, shutil, datetime, math, os, fnmatch

################# Files and global functions for ball by ball commentary ###################
not_first_run = ''
comm_file = "scorecards/commentary_file.txt"
open(comm_file, "w")

def commentary(comment):
	with open (comm_file, 'a') as f:
		f.write(comment)

#FURTHER TO DO:
#  1. For now commentary file can be generated for only one match at a time. Will need to
#	  enable some batch processing method just like the scorecards
#  2. Could attempt further details in commentary lines, But that could be an overkill
#  3. Match viewer and visualizations based on output.

################# Match Viewer Attempt ###################
matchviewer_file = "scorecards/matchviewer.txt"
open(matchviewer_file, "w")

def matchviewer(comment):
	with open (matchviewer_file, 'a') as f:
		f.write(comment)



######################## Alternate Ball by Ball Commentary ##################################
alt_comm_file = "scorecards/alt_commentary_file.html"
alt_file = open(alt_comm_file, "w")
alt_file.close()


def alt_commentary(alt_comment, batsman0, batsman1):
	global not_first_run
	with open (alt_comm_file, 'a') as f:
		if not_first_run != True:
			first_alt_comment = "<tr><td style = 'border:1px dotted black;' width='8%'>Time</td><td style = 'border:1px dotted black;' width='17%'>Bowler</td><td style = 'border:1px dotted black;' width='20%'>Batsman</td><td style = 'border:1px dotted black;' width='5%'>Rns</td><td style = 'border:1px dotted black;' width='5%'>Bls</td><td style = 'border:1px dotted black;' width='20%'>Batsman</td><td style = 'border:1px dotted black;'  width='5%'>Rns</td><td style = 'border:1px dotted black;' width='5%'>Bls</td><td style = 'border:1px dotted black;' width='5%'>Overs</td><td style = 'border:1px dotted black;' width='5%'>Tot</td><td style = 'border:1px dotted black;' width='5%'>Wk</td></tr><tr><td style = 'border:1px dotted black;' colspan = '2'></td><td style = 'border:1px dotted black;' width='20%'>"  + batsman0 + "</td><td style = 'border:1px dotted black;' colspan = '2'></td><td style = 'border:1px dotted black;' width='20%'>" + batsman1 +  "</td><td style = 'border:1px dotted black;' colspan = '5'></td></tr>" + alt_comment

			f.write(first_alt_comment)
			not_first_run = True
		else:	
			f.write(alt_comment)			
	
############################################################################################




def twodp (x):
	return "%.2f" % round(x,2)

def listshow (x, end = False):
	a = ''
	for i in x:
		if i is not x[-1]: a = a + '{}, '.format(i)
		else:
			if end == False: a = a + '{}'.format(i)
			else: a = a + '{} {}'.format(end, i) 
	return a

def namematch (a, b, z):
	c = [x for x in a if x.name == b]
	if len (c) == 0: return z
	elif len(c) == 1: return c[0]
	else: return random.choice(c)

def playerwrite (a):
	x = "[" + '"' + a.name + '", '

	for i in [a.bat, a.bowl, a.tag, a.first, a.last, a.sr, a.er, a.capt]:
		if i == a.tag:
			x = x + '"'
			x = x + a.tag
			x = x + '", '
		else: x = x + str(i) + ', '
	x = x + "]"
	return x

def scoreformat (x):
	if x[1] == 10: return str(x[0])
	else: return '{}-{}'.format(x[0],x[1])

def showteam (x):
	def keeper (t):
		x = ''
		for i in t:
			if 'WK' in i.tag: x = i
		if x == '':
			for i in t:
				if i.tag in ['Bat', 'OpenBat']: x = i
		if x == '':
			for i in t:
				if quickorder(i.tag) == 1: x = i
		if x == '':
			for i in t: x = [y for y in t if t.bowl == max([z.bowl for z in t])][0]
		return x

	WK = ''
	capt = ''

	WK = keeper (x.xi)
	
	if x.captain in x.xi:
		capt = x.captain
	else:
		capt = x.lastcapt

	a = ''

	n = 1
	for i in x.xi:
		tag = ''
		if WK == i: tag = "†"
		if capt == i: tag = "*" + tag
		if i != x.xi[-1]: a = a + '{} {}{}, '.format(n,tag,i.name)
		else: a = a + '{} {}{}'.format(n,tag,i.name)
		n = n + 1

	return a

def pitchmake (Weather):
	PaceFactor = 1 + 0.5*(random.random() * (random.random()-random.random())) #how good the pitch is for pace. 0.75-1.25, lower is better for bowling
	SpinFactor = 1 + 0.5*(random.random() * (random.random()-random.random())) #same for spin
	Outfield = 1 + 0.25*(random.random() * (random.random()-random.random()))

	Asia = ['India','Pakistan','Sri Lanka','Bangladesh','Afghanistan']

	if Weather in Asia:
	    p = (4 + random.random())/5
	    if Weather == 'Pakistan':
	        p = (1+p)/2
	    PaceFactor = PaceFactor/p
	    SpinFactor = SpinFactor*p

	print ("Pace Factor:", "{:0.2f}".format(PaceFactor), "Spin Factor:", "{:0.2f}".format(SpinFactor), 'Outfield Factor:', "{:0.2f}".format(Outfield))

	return [PaceFactor, SpinFactor, Outfield]

def quickorder (y):
	if 'WK' in y: return 2
	elif "Open" in y: return 0
	elif y == "Spin": return 4
	elif y in ["Fast", "Med"]: return 3
	else: return 1

def excessrpo (b):
	if b.overs == 0: return 0
	elif b.runs / b.overs < 4: return 0
	else: return 4 - (b.runs/b.overs)

def openingbowlers (a):
	x = a.bowl + (a.bat)/3
	if 'WK' in a.tag: x = x + 100
	elif 'Spin' in a.tag or 'Bat' in a.tag: x = x + 50
	elif 'Part' in a.tag: x = x + 25
	return x

def oversballs (x):
	if x.balls == 0: return str(x.overs)
	elif x.balls == 6: return str(x.overs+1)
	else: return '{}.{}'.format(x.overs, x.balls)






class teaminnings:
	def __init__(self, t):
		self.test = t
		self.team = t.tobat
		self.bowlteam = [x for x in [t.home, t.away] if x is not self.team][0]
		self.innings = []
		self.order = []
		self.active = True
		self.onstrike = self.team.xi[0]
		self.batsmen = [self.team.xi[0],self.team.xi[1]]
		self.bowlers = [x for x in self.bowlteam.xi]
		self.bowlers.sort(key = lambda x: openingbowlers (x))
		self.bowler = self.bowlers[0]
		self.otherbowler = self.bowlers[1]
		self.fatigue = []
		self.extras = [0,0,0,0,0]
		######### Alternate Ball by Ball Commentary ######
		self.over_details = ''   
		self.lastbatsman = ''    
		self.lastindex = ''      
		self.default_alt_commentary = '' 
		self.default_alt_commentary_header = ''
		self.default_alt_commentary_batsmen = ''
		self.dismissed_batsmen = []
		self.dismissed_batsmen_names = []
		self.dismissed_batsmen_index = []
		self.dismissed_batsmen_details = []
		self.batsmen0_innings_runs = ''
		self.batsmen1_innings_runs = ''
		self.batsmen0_innings_balls = ''
		self.batsmen1_innings_balls = ''
		self.innings_number = ''
		self.old_innings = ''


	def inningsheader (self):
		if len(self.test.teaminnings) > 2: self.number = '2nd'
		else: self.number = '1st'

		y = (' {} - {} innings'.format(self.team.name, self.number))


		if self.test.odi == True: y = ' {}'.format(self.team.name)

		if len(self.test.teaminnings) == 2 and self.test.odi == True: y = y + ' (Target: {} in {} overs)'.format(self.test.teaminnings[0].runs+1, self.test.overslimit)

		if len(self.test.teaminnings) == 3 and self.test.teaminnings[1].team == self.team: y = y + ' (following on)'
		if len(self.test.teaminnings) == 4: y = y + ' (Target: {} in {} overs)'.format(self.target()+self.runs, self.test.remaining() + self.overs)
		self.test.score (y)
		self.test.newscore (y + "\n")

	

	def run (self):
		self.active = True
		for i in self.team.xi:
			x = innings (i, self.test)
			self.innings.append(x)
			i.innings = x
			x.opposition = self.bowlteam
		for i in self.bowlteam.xi:
			i.bowling = bowling (i, self.test)
			i.bowling.opposition = self.team

		if len(self.test.teaminnings) > 1: self.test.logger('Start of innings')

		while self.wickets < 10 and self.active == True and (self.test.odi == False or self.overs < self.test.overslimit):
			self.test.raincheck()
			self.over()

		self.allout()


	def runsadd (self, n):
		self.runs = self.runs + n
		self.onstrike.innings.runs = self.onstrike.innings.runs + n
		self.bowler.bowling.runs = self.bowler.bowling.runs + n
		if n == 4:
			self.onstrike.innings.fours +=1
		elif n == 6:
			self.onstrike.innings.sixes +=1

		self.overlog.append(str(n))
		self.milestone(n)
		self.partnership(n)
		self.swap(n)


	def pitchfactor (self):
		if 'Spin' in self.bowler.tag: return self.test.pitch[1]
		else: return self.test.pitch[0]

	def bowlchange (self):
		x = excessrpo(self.bowler.bowling)- 5*self.bowler.bowling.wickets

		if 'Fast' in self.bowler.tag:
			x = x + 2*self.bowler.bowling.spell + self.fatigue.count(self.bowler)
		elif 'Med' in self.bowler.tag:
			x = x + self.bowler.bowling.spell + self.fatigue.count(self.bowler)
		else:
			x = x + 0.5*self.bowler.bowling.spell + self.fatigue.count(self.bowler)
		if 'Part' in self.bowler.tag: x = x+4
		elif 'Bat' in self.bowler.tag or 'WK' in self.bowler.tag: x = x+6
		#if 'Fast' in self.bowler.tag: x = 1.5*x
		if self.overs < 20: x = x*0.75
		if x < 1: x = 1
		x = x**1.5

		change = True

		if self.overs < 5: x = 0
		elif quickorder(self.bowler.tag) > 2 and self.bowler.bowling.spell < 3: x = 0
		elif self.overs % 80 < 2: 
			x = 100
			change = False
		elif self.test.overcount() % 30 < 2: 
			x = 100
			change = False

		#self.test.logger ((self.bowler.name, round(x)))

		#if self.test.odi == True: x = self.bowlchangeodi()

		if x >= 10 and random.random() < x/100: 
			b = self.bowlchoice(change = change)
			if b is not self.bowler: self.bowler.bowling.spell = 0
			return b
		else: return self.bowler

	def bowlchoice (self, change = True):
		a = self.bowler
		if change == True: c = [x for x in self.bowlteam.xi if x is not self.bowler and x is not self.otherbowler and x is not self.bowlteam.wk]
		else:  c = [x for x in self.bowlteam.xi if x is not self.otherbowler and x is not self.bowlteam.wk]
		c.sort(key = lambda x: self.bowlvalue(x), reverse = False)

		

		if self.test.bowlingchanges == True and a is not c[0]: 
			if change == True: 
							self.test.logger('Bowling change: {} ({} over spell) replaced by {}'.format(a.name, a.bowling.spell, c[0].name))
							
							##### Ball by Ball Commentary ######
							COMM_bowlingchange = f"...Bowling Change: {a.name} ({a.bowling.wickets}/{a.bowling.runs}) replaced by {c[0].name} ({c[0].bowling.wickets}/{c[0].bowling.runs})\n\n"
							commentary(COMM_bowlingchange)

							##### Alternate Ball by Ball Commentary: ADDITION OF CHANGE OF BOWLER PROMPT ######
							#ALTCOMM_bowlingchange = f"<tr><td colspan='11'>&emsp;Bowling Change: {a.name} ({a.bowling.wickets}/{a.bowling.runs}) replaced by {c[0].name} ({c[0].bowling.wickets}/{c[0].bowling.runs})</td></tr>"
							#alt_commentary(ALTCOMM_bowlingchange, self.batsmen[0].name, self.batsmen[1].name)

							#### MATCH VIEWER #####
							javascript_array_part1 = f'myArray[{self.test.array_counter}] = "'
							javascript_array_content = f'BOWLING CHANGE, BOWLING CHANGE: {a.name} ({a.bowling.wickets}/{a.bowling.runs}) replaced by {c[0].name} ({c[0].bowling.wickets}/{c[0].bowling.runs})'
							javascript_array = javascript_array_part1 + self.javascript_array_part2 + javascript_array_content + self.javascript_array_part3
							self.test.array_counter += 1
							matchviewer(javascript_array)


			else: 
				self.test.logger('Bowling change: {} replaced by {}'.format(a.name, c[0].name))
		return c[0]
		
		



	def bowlvalue (self, p):
		o = self.overs % 80
		t = quickorder(p.tag)

		x = p.bowl + excessrpo(p.bowling) - 5*p.bowling.wickets

		if len(self.fatigue) > 10: y = self.fatigue[-10:]
		else: y = [] 

		if 'Fast' in p.tag:
			x = x + 5*self.fatigue.count(p)**2 + 100*y.count(p)**2
		else:
			x = x + self.fatigue.count(p)**2 + 2*y.count(p)**2

		if 'Part' in p.tag: x = x + 25
		if 'Bat' in p.tag: x = x + 60
		if 'WK' in p.tag: x = x + 100
		if o < 25 and 'Spin' in p.tag: x = x + 100
		if self.overs < 50 and t < 3: x = x + 100
		if self.wickets > 7 and t < 3: x = x + 50
		if self.partnership(0) > 150 and t < 3: x + x - 50
		if 'Spin' in p.tag: x = x * self.det() * self.test.pitch[1]
		else: x = x * self.test.pitch[0]

		x = x - 50*random.random()

		#if self.test.odi == True: x = self.bowlvalueodi(p)

		return x

	def det (self):
		if 'Spin' in self.bowler.tag: daydict = dict({1:1.3, 2:1.2, 3:1.1, 4:0.9, 5:0.7})
		else: daydict = dict({1:1.2, 2:1.1, 3:1, 4:0.9, 5:0.8})

		if self.day() > 5: x = daydict[5]
		else: x = daydict[self.day()]

		if ('Fast' in self.bowler.tag or 'Med' in self.bowler.tag):
			if self.overs%80 < 10: x = x * 0.9
			elif self.overs % 80 > 60: x = x * 1.1

		return x

	def aggfactor (self):
		#f self.test.odi == True: return self.aggfactorodi()

		x = 1
		if len(self.test.teaminnings) < 4:
			if self.runs > 400: x =  x + (self.runs-400)/1000
			if self.wickets > 1 and self.runs/self.wickets < 15: x = x - 0.2

		if len(self.test.teaminnings) == 3 and self.lead() > 200 and (self.wickets < 7 or self.lead() > 250): x = x + (self.lead()-200)/200

		elif len(self.test.teaminnings) == 4 and self.test.remaining() > 0:
			y = self.target() - self.runs
			r = y / self.test.remaining()
			z = 10 - self.wickets

			if 6 > r > 1 and z > 7 and self.test.remaining() < 50:
				x = x + (r)/5
			if r > 4 and z <= 4 and y > 10:
				x = x - self.wickets/20

		if self.onstrike.innings.runs > 150: x = x + (self.onstrike.innings.runs-150)/500

		if x > 1.25 and self.test.weather == 'Timeless': x = 1.25

		o = [x for x in self.batsmen if x is not self.onstrike][0]
		d = self.onstrike.bat/o.bat
		if self.onstrike.bat < 15 or self.wickets < 7 or o.bat > 30 or o.innings.runs > 100: d = 1
		if d > 5: d = 5

		if d > 1: x = x * d**0.5
		else: x = x*d

		return x

	def wicketrate (self):
		y = 1 * self.bowler.mod / self.onstrike.mod
		if 'WK' not in self.bowlteam.wk.tag: y = y * 0.8

		y = y * (self.test.rpo/self.test.base) * (1/6)
		y = y * self.aggfactor() * max (1, self.aggfactor()**0.5)
		y = y / (self.onstrike.bat/30)**0.8
		y = y / (self.bowler.bowl/30)**0.5
		y = y / self.det()**0.5
		y = y / self.onstrike.innings.form()**0.5
		y = y / self.pitchfactor()**0.5
		y = y * self.bowler.er**0.5
		y = y * self.onstrike.sr**0.5
		return y

	def rate (self):
		y = self.test.rpo/6 * self.onstrike.mod / self.bowler.mod
		y = y * self.aggfactor()
		y = y * (self.onstrike.bat/30)**0.2
		y = y * (self.bowler.bowl/30)**0.5
		y = y * self.det()**0.5
		y = y * self.onstrike.innings.form()**0.5
		y = y * self.pitchfactor()**0.5
		y = y * self.bowler.er**0.5
		y = y * self.onstrike.sr**0.5
		y = y * self.test.pitch[2]
		#print (self.onstrike.name, self.onstrike.bat, self.bowler.name, self.bowler.bowl, y)
		return y

	def howout (self):
		def catcher (x):
			y = [y for y in x.xi if y is not self.bowler and y is not self.bowlteam.wk] + [y for y in x.xi[:6] if y is not self.bowler and y is not self.bowlteam.wk]
			return random.choice(y)

		x = random.random()
		if x < 0.2143: return 'b. {}'.format(self.bowler.name)
		elif x < 0.3573: return 'lbw. b. {}'.format(self.bowler.name)
		elif x < 0.52: 
			self.bowlteam.wk.catches += 1
			return 'c. †{} b. {}'.format(self.bowlteam.wk.name, self.bowler.name)
		elif x < 0.9065: 
			y = catcher(self.bowlteam)
			y.catches += 1
			if y == self.bowler:
				return 'c. & b. {}'.format(self.bowler.name)
			else:
				return 'c. {} b. {}'.format(y.name, self.bowler.name)
		elif x < 0.9568:
			if ('Med' in self.bowler.tag or 'Spin' in self.bowler.tag):
				self.bowlteam.wk.stumpings += 1
				return 'st. †{} b. {}'.format(self.bowlteam.wk.name, self.bowler.name)
			else:
				return 'c. †{} b. {}'.format(self.bowlteam.wk.name, self.bowler.name)
		elif x < 0.9983: return 'run out ({})'.format(random.choice(self.bowlteam.xi).name)
		elif x < 0.9999: return 'hit wicket b. {}'.format(self.bowler.name)
		else: return 'obstructed the field b. {}'.format(self.bowler.name)

	def wicket (self):
		self.wickets += 1
		self.onstrike.innings.out = True
		self.onstrike.innings.dismissal = self.howout()

		if 'run out' not in self.onstrike.innings.dismissal:
			self.bowler.bowling.wickets += 1

		if self.partnership(0) >= 0:
			if self.wickets != 10: 
				x = ' - New batsman {}'.format(self.team.xi[self.wickets+1].name)
				self.ALTCOMM_newbatsman = 'New batsman is {}'.format(self.team.xi[self.wickets+1].name)  ######### Alternate Ball by Ball Commentary ######
			else: 
				x = ''
				self.ALTCOMM_newbatsman = ''  ######### Alternate Ball by Ball Commentary ######
			self.test.logger('{} {} {} ({}b) {}x4 {}x6 - partnership {} {}'.format(self.onstrike.name, self.onstrike.innings.dismissal, self.onstrike.innings.runs, self.onstrike.innings.balls, self.onstrike.innings.fours, self.onstrike.innings.sixes, self.partnership(0), x))
			
			##### Ball by Ball Commentary ######
			self.COMM_wicket = 'OUT - {} {} ({}b) {}x4 {}x6 - partnership {} {}'.format(self.onstrike.innings.dismissal, self.onstrike.innings.runs, self.onstrike.innings.balls, self.onstrike.innings.fours, self.onstrike.innings.sixes, self.partnership(0), x)



		
		if self.bowler.bowling.wickets >= 5 and 'run out' not in self.onstrike.innings.dismissal:
			self.test.logger('{} {}'.format(self.bowler.name, self.bowler.bowling.bowlformat()))

		self.onstrike.innings.FOW = [self.onstrike, self.runs,self.wickets]
		

		######### Alternate Ball by Ball Commentary ######
		if self.wickets <= 10:
			self.dismissed_batsmen.append(self.onstrike)
			self.dismissed_batsmen_names.append(self.onstrike.name)
			self.lastindex = self.batsmen.index(self.onstrike)
			self.dismissed_batsmen_details.extend(['OUT - ' + self.onstrike.name, self.lastindex, self.onstrike.innings.dismissal, self.onstrike.innings.runs, self.onstrike.innings.balls, self.overs, self.balls, self.runs, self.wickets])			
			
			
			if self.batsmen[0] == self.onstrike: 
					self.nonstrike_runs = self.batsmen[1].innings.runs
					self.nonstrike_balls = self.batsmen[1].innings.balls
			else: 
					self.nonstrike_runs = self.batsmen[0].innings.runs
					self.nonstrike_balls = self.batsmen[0].innings.balls		
			
				
			if self.wickets < 10:
				self.batsmen.insert(self.lastindex, self.team.xi[self.wickets+1])
				self.batsmen.remove(self.onstrike)
				self.onstrike = self.team.xi[self.wickets+1]
			
				self.dismissed_batsmen_details.append(self.onstrike.name)

				if self.lastindex == 0:
					self.dismissed_batsmen_details.extend([self.onstrike.name, self.batsmen[1].name, self.batsmen[1].innings.runs, self.batsmen[1].innings.balls])
				elif self.lastindex == 1:
					self.dismissed_batsmen_details.extend([self.batsmen[0].name, self.onstrike.name, self.batsmen[0].innings.runs, self.batsmen[0].innings.balls])


				self.declaration()
			
			if self.wickets == 10:
				self.dismissed_batsmen_details.append('x')
				self.dismissed_batsmen_details.extend(['x','x',self.nonstrike_runs,self.nonstrike_balls])



	def extracheck (self):
		e = random.random()
		if e < 0.268: 
			extra = 'b'
			e = random.random()
			if e < 0.2:
				self.runs += 4
				self.extras[0] += 4
				self.partnership(4)
				self.overlog.append('4b')
				return True
			elif e < 0.4:
				self.runs +=1
				self.extras[0] += 1
				self.partnership(1)
				self.overlog.append('b')
				self.swap(1)
				return True

		elif e < 0.632: 
			e = random.random()
			extra = 'lb'
			if e < 1/7:
				self.runs += 4
				self.extras[1] +=4
				self.partnership(4)
				self.overlog.append('4lb')
				return True
			elif e < (1/7 + 1/50):
				self.runs += 2
				self.extras[1] += 2
				self.partnership(2)
				self.overlog.append('2lb')
				return True
			elif e < 193/350:
				self.runs += 1
				self.extras[1] +=1
				self.partnership(1)
				self.overlog.append('lb')
				self.swap(1)
				return True

		elif e < 0.697: 
			extra = 'w'
			if random.random() < 0.1:
				self.runs +=5
				self.extras[2] += 5
				self.bowler.bowling.runs += 5
				self.partnership(5)
				self.balls -= 1
				self.overlog.append('4wd')
				return True
			elif random.random() < 0.7:
				self.runs +=1
				self.extras[2] += 1
				self.bowler.bowling.runs += 4
				self.partnership(4)
				self.overlog.append('wd')
				self.balls -= 1
				return True

		elif e < 0.9979: 
			extra = 'nb'
			self.runs +=1
			self.extras[3] +=1
			self.balls -= 1
			self.bowler.bowling.runs += 1
			self.partnership(1)
			self.overlog.append('nb')
			return False

		else: 
			if random.random() < 1/5:
				extra = 'pen'
				self.runs += 5
				self.extras[4] += 5
				self.balls -= 1
				self.partnership(5)
				self.overlog.append('5pen')
				return True	




	def ball (self):
		#if match_start: self.first_session()
		a = self.onstrike
		b = self.bowler
		extra = ''
		COMM_ball_outcome = ''
		COMM_no_ball = ''
		self.swap_check = False  ######### Alternate Ball by Ball Commentary ######

		z = self.rate()
		y = self.wicketrate()


		four = 0.06*z
		six = 0.003*z
		x = random.random()			

		self.balls += 1 
		self.onstrike.innings.balls += 1

		self.bowler.overcount()
		self.bowler.bowling.balls += 1

		if random.random() < 0.027:
			dead = self.extracheck()
			if dead == True:  
					###### Ball by Ball Commentary ######
					if self.swap_check:
						COMM_ball_by_ball = f"{str(self.overs)}.{str(self.balls)} {b.name} to {a.name}: {self.overlog[-2]}\n"
					else:	
						COMM_ball_by_ball = f"{str(self.overs)}.{str(self.balls)} {b.name} to {a.name}: {self.overlog[-1]}\n"
					commentary(COMM_ball_by_ball)
					return
			else:
				COMM_no_ball = 'No ball'

		if y < x < 3*y: 
			#self.overlog.append('!')
			self.onstrike.innings.chances += 1
			self.bowler.bowling.chances += 1
			if random.random() < 1/10: 
				q = random.choice(self.bowlteam.xi)
				self.test.logger('{} dropped by {} off {} on {}*'.format(self.onstrike.name, q.name, self.bowler.name, self.onstrike.innings.runs))
				self.onstrike.innings.drops.append([q, self.bowler, self.onstrike.innings.runs])

				###### Ball by Ball Commentary ######
				COMM_ball_outcome = '{} dropped by {} off {} on {}*'.format(self.onstrike.name, q.name, self.bowler.name, self.onstrike.innings.runs)

		if x < y: 
			i = self.wicket()
			self.overlog.append('W')
			if len(self.overlog) >= 5 and len(self.overlog[-2]) > 3 and self.overlog[-3] == 'W' and len(self.overlog[-4]) > 3 and self.overlog[-5] == 'W': self.test.logger('Hattrick for {}!'.format(self.bowler.name))
			self.overlog.append(self.onstrike.name)
			COMM_ball_outcome = self.COMM_wicket  ###### Ball by Ball Commentary ######
			COMM_ball_outcome_array = COMM_ball_outcome.split("-")
			if len(COMM_ball_outcome_array) > 3:
				COMM_ball_outcome = COMM_ball_outcome_array[0] + "<br>&emsp;&emsp;&emsp;&emsp;" + COMM_ball_outcome_array[1] + "<br>&emsp;&emsp;&emsp;&emsp;" + COMM_ball_outcome_array[2].title() + ".<br><br>&emsp;&emsp;&emsp;&emsp;" + COMM_ball_outcome_array[3]


		elif x > 1 - six: 
			self.runsadd(6)
			COMM_ball_outcome = 'SIX!'  ###### Ball by Ball Commentary ######
		elif x > 1 - six - four: 
			self.runsadd(4)
			COMM_ball_outcome = 'FOUR!'  ###### Ball by Ball Commentary ######
		elif x > 1 - six - four - z:
			c = random.random()
			if c < 0.4: 
				self.runsadd(1)
				COMM_ball_outcome = '1 run'   ###### Ball by Ball Commentary ######
			elif c < 0.49: 
				self.runsadd(2)
				COMM_ball_outcome = '2 runs'	###### Ball by Ball Commentary ######
			elif c < 0.512: 
				self.runsadd(3)
				COMM_ball_outcome = '3 runs'	###### Ball by Ball Commentary ######
			else: 
				self.overlog.append('.')
				COMM_ball_outcome = 'No run'	###### Ball by Ball Commentary ######
		else: 
			self.overlog.append('.')
			COMM_ball_outcome = 'No run'	###### Ball by Ball Commentary ######



		###### Ball by Ball Commentary ######
		if COMM_no_ball == "No ball" and COMM_ball_outcome == "No run":
			COMM_ball_outcome = COMM_no_ball
		elif COMM_no_ball == "No ball" and COMM_ball_outcome != "No run":
			COMM_ball_outcome = "No ball plus " + COMM_ball_outcome
		COMM_ball_by_ball = f"{str(self.overs)}.{str(self.balls)} {b.name} to {a.name}: {COMM_ball_outcome}\n"		

		

		#### MATCH VIEWER #####
		check_time = str(self.test.time())
		check_time = check_time.replace(":","")

		if int(check_time) <= 1300:
			self.test_session = "1st Session"
		elif int(check_time) > 1300 and int(check_time) < 1600:
			self.test_session = "2nd Session"
		elif int(check_time) > 1600:
			self.test_session = "3rd Session"
		else:
			self.test_session = "1st Session"



		if len(self.test.teaminnings) == 1:
			self.innings_number = '1st Inning'
			self.old_innings = ""
		elif len(self.test.teaminnings) == 2:
			self.innings_number = '1st Inning'
			self.old_innings = f"{self.test.teaminnings[0].team.name},{self.test.teaminnings[0].runs},{self.test.teaminnings[0].wickets}"
		elif len(self.test.teaminnings) == 3:
			self.innings_number = '2nd Inning'			
			self.old_innings = f"{self.test.teaminnings[0].team.name},{self.test.teaminnings[0].runs},{self.test.teaminnings[0].wickets},{self.test.teaminnings[1].team.name},{self.test.teaminnings[1].runs},{self.test.teaminnings[1].wickets}"
		elif len(self.test.teaminnings) == 4:
			self.innings_number = '2nd Inning'			
			self.old_innings = f"{self.test.teaminnings[0].team.name},{self.test.teaminnings[0].runs},{self.test.teaminnings[0].wickets},{self.test.teaminnings[1].team.name},{self.test.teaminnings[1].runs},{self.test.teaminnings[1].wickets},{self.test.teaminnings[2].team.name},{self.test.teaminnings[2].runs},{self.test.teaminnings[2].wickets}"



		## ARRAY [ 0 - Day, 1 - Session, 2 - Innings, 3 - Time, 4 - Overs, 5 - Batting Team, 6 - Bowling Team, 7 - Bowler 1 Name, 8 - Bowler 1 Overs, 9 - Bowler 1 runs, 10 - Bowler 1 Wickets, 11 - Bowler 2 Name, 12 - Bowler 2 Overs, 13 - Bowler 2 runs, 14 - Bowler 2 Wickets, 15 - Batsman 1 Name, 16 - Batsman 1 Runs, 17 - Batsman 1 Balls, 18 - Batsman 1 Fours, 19 - Batsman 1 Sixes, 20 - Batsman 2 Name, 21 - Batsman 2 Runs, 22 - Batsman 2 Balls, 23 - Batsman 2 Fours, 24 - Batsman 2 Sixes, 25 - Total Team Runs, 26 - Total Team Wickets, 27 - Current Partnership, 28 - State of Play, 29 - EVENT, 30 - Batting Team Roster, 31 - Bowling Team Roster, 32 - Lead/Trail, 33 - 41 Previous three innings of Match as Team Name Team Total and Team Wickets]

		javascript_array_part1 = f'myArray[{self.test.array_counter}] = "'

		self.javascript_array_part2 = f'{self.day()},{self.test_session},{self.innings_number},{str(self.test.time())},{str(self.overs)}.{str(self.balls)},{self.team.name},{self.bowlteam.name},{self.bowler.name},{self.bowler.bowling.overs}.{self.bowler.bowling.balls},{self.bowler.bowling.runs},{self.bowler.bowling.wickets},{self.otherbowler.name},{self.otherbowler.bowling.overs}.{self.otherbowler.bowling.balls},{self.otherbowler.bowling.runs},{self.otherbowler.bowling.wickets},{self.batsmen[0].name},{self.batsmen[0].innings.runs},{self.batsmen[0].innings.balls},{self.batsmen[0].innings.fours},{self.batsmen[0].innings.sixes},{self.batsmen[1].name},{self.batsmen[1].innings.runs},{self.batsmen[1].innings.balls},{self.batsmen[1].innings.fours},{self.batsmen[1].innings.sixes},{str(self.runs)},{str(self.wickets)},{self.partnership(0)},'


		javascript_array_content = f'PLAY,{b.name} to {a.name}: <b>{COMM_ball_outcome}</b>'


		self.javascript_array_part3 = f',<b>{self.team.name.upper()}</b><br><table width=\'100%\'><tr><td width=\'60%\'><b>Batsmen</b></td><td width=\'10%\'><b>R</b></td><td width=\'10%\'><b>B</b></td><td width=\'10%\'><b>4s</b></td><td width=\'10%\'><b>6s</b></td></tr><tr><td>{self.team.xi[0].name}</td><td>{self.team.xi[0].innings.runs}</td><td>{self.team.xi[0].innings.balls}</td><td>{self.team.xi[0].innings.fours}</td><td>{self.team.xi[0].innings.sixes}</td></tr><tr><td>{self.team.xi[1].name}</td><td>{self.team.xi[1].innings.runs}</td><td>{self.team.xi[1].innings.balls}</td><td>{self.team.xi[1].innings.fours}</td><td>{self.team.xi[1].innings.sixes}</td></tr><tr><td>{self.team.xi[2].name}</td><td>{self.team.xi[2].innings.runs}</td><td>{self.team.xi[2].innings.balls}</td><td>{self.team.xi[2].innings.fours}</td><td>{self.team.xi[2].innings.sixes}</td></tr><tr><td>{self.team.xi[3].name}</td><td>{self.team.xi[3].innings.runs}</td><td>{self.team.xi[3].innings.balls}</td><td>{self.team.xi[3].innings.fours}</td><td>{self.team.xi[3].innings.sixes}</td></tr><tr><td>{self.team.xi[4].name}</td><td>{self.team.xi[4].innings.runs}</td><td>{self.team.xi[4].innings.balls}</td><td>{self.team.xi[4].innings.fours}</td><td>{self.team.xi[4].innings.sixes}</td></tr><tr><td>{self.team.xi[5].name}</td><td>{self.team.xi[5].innings.runs}</td><td>{self.team.xi[5].innings.balls}</td><td>{self.team.xi[5].innings.fours}</td><td>{self.team.xi[5].innings.sixes}</td></tr><tr><td>{self.team.xi[6].name}</td><td>{self.team.xi[6].innings.runs}</td><td>{self.team.xi[6].innings.balls}</td><td>{self.team.xi[6].innings.fours}</td><td>{self.team.xi[6].innings.sixes}</td></tr><tr><td>{self.team.xi[7].name}</td><td>{self.team.xi[7].innings.runs}</td><td>{self.team.xi[7].innings.balls}</td><td>{self.team.xi[7].innings.fours}</td><td>{self.team.xi[7].innings.sixes}</td></tr><tr><td>{self.team.xi[8].name}</td><td>{self.team.xi[8].innings.runs}</td><td>{self.team.xi[8].innings.balls}</td><td>{self.team.xi[8].innings.fours}</td><td>{self.team.xi[8].innings.sixes}</td></tr><tr><td>{self.team.xi[9].name}</td><td>{self.team.xi[9].innings.runs}</td><td>{self.team.xi[9].innings.balls}</td><td>{self.team.xi[9].innings.fours}</td><td>{self.team.xi[9].innings.sixes}</td></tr><tr><td>{self.team.xi[10].name}</td><td>{self.team.xi[10].innings.runs}</td><td>{self.team.xi[10].innings.balls}</td><td>{self.team.xi[10].innings.fours}</td><td>{self.team.xi[10].innings.sixes}</td></tr></table>,<b>{self.bowlteam.name.upper()}</b><br><table width=\'100%\'><tr><td width=\'60%\'><b>Bowlers</b></td><td width=\'10%\'><b>O</b></td><td width=\'10%\'><b>M</b></td><td width=\'10%\'><b>R</b></td><td width=\'10%\'><b>W</b></td></tr><tr><td>{self.bowlteam.xi[0].name}</td><td>{self.bowlteam.xi[0].bowling.overs}.{self.bowlteam.xi[0].bowling.balls}</td><td>{self.bowlteam.xi[0].bowling.maidens}</td><td>{self.bowlteam.xi[0].bowling.runs}</td><td>{self.bowlteam.xi[0].bowling.wickets}</td></tr><tr><td>{self.bowlteam.xi[1].name}</td><td>{self.bowlteam.xi[1].bowling.overs}.{self.bowlteam.xi[1].bowling.balls}</td><td>{self.bowlteam.xi[1].bowling.maidens}</td><td>{self.bowlteam.xi[1].bowling.runs}</td><td>{self.bowlteam.xi[1].bowling.wickets}</td></tr><tr><td>{self.bowlteam.xi[2].name}</td><td>{self.bowlteam.xi[2].bowling.overs}.{self.bowlteam.xi[2].bowling.balls}</td><td>{self.bowlteam.xi[2].bowling.maidens}</td><td>{self.bowlteam.xi[2].bowling.runs}</td><td>{self.bowlteam.xi[2].bowling.wickets}</td></tr><tr><td>{self.bowlteam.xi[3].name}</td><td>{self.bowlteam.xi[3].bowling.overs}.{self.bowlteam.xi[3].bowling.balls}</td><td>{self.bowlteam.xi[3].bowling.maidens}</td><td>{self.bowlteam.xi[3].bowling.runs}</td><td>{self.bowlteam.xi[3].bowling.wickets}</td></tr><tr><td>{self.bowlteam.xi[4].name}</td><td>{self.bowlteam.xi[4].bowling.overs}.{self.bowlteam.xi[4].bowling.balls}</td><td>{self.bowlteam.xi[4].bowling.maidens}</td><td>{self.bowlteam.xi[4].bowling.runs}</td><td>{self.bowlteam.xi[4].bowling.wickets}</td></tr><tr><td>{self.bowlteam.xi[5].name}</td><td>{self.bowlteam.xi[5].bowling.overs}.{self.bowlteam.xi[5].bowling.balls}</td><td>{self.bowlteam.xi[5].bowling.maidens}</td><td>{self.bowlteam.xi[5].bowling.runs}</td><td>{self.bowlteam.xi[5].bowling.wickets}</td></tr><tr><td>{self.bowlteam.xi[6].name}</td><td>{self.bowlteam.xi[6].bowling.overs}.{self.bowlteam.xi[6].bowling.balls}</td><td>{self.bowlteam.xi[6].bowling.maidens}</td><td>{self.bowlteam.xi[6].bowling.runs}</td><td>{self.bowlteam.xi[6].bowling.wickets}</td></tr><tr><td>{self.bowlteam.xi[7].name}</td><td>{self.bowlteam.xi[7].bowling.overs}.{self.bowlteam.xi[7].bowling.balls}</td><td>{self.bowlteam.xi[7].bowling.maidens}</td><td>{self.bowlteam.xi[7].bowling.runs}</td><td>{self.bowlteam.xi[7].bowling.wickets}</td></tr><tr><td>{self.bowlteam.xi[8].name}</td><td>{self.bowlteam.xi[8].bowling.overs}.{self.bowlteam.xi[8].bowling.balls}</td><td>{self.bowlteam.xi[8].bowling.maidens}</td><td>{self.bowlteam.xi[8].bowling.runs}</td><td>{self.bowlteam.xi[8].bowling.wickets}</td></tr><tr><td>{self.bowlteam.xi[9].name}</td><td>{self.bowlteam.xi[9].bowling.overs}.{self.bowlteam.xi[9].bowling.balls}</td><td>{self.bowlteam.xi[9].bowling.maidens}</td><td>{self.bowlteam.xi[9].bowling.runs}</td><td>{self.bowlteam.xi[9].bowling.wickets}</td></tr><tr><td>{self.bowlteam.xi[10].name}</td><td>{self.bowlteam.xi[10].bowling.overs}.{self.bowlteam.xi[10].bowling.balls}</td><td>{self.bowlteam.xi[10].bowling.maidens}</td><td>{self.bowlteam.xi[10].bowling.runs}</td><td>{self.bowlteam.xi[10].bowling.wickets}</td></tr></table>,{self.test.teaminnings[-1].lead()},{self.old_innings}"\n'

		javascript_array = javascript_array_part1 + self.javascript_array_part2 + javascript_array_content + self.javascript_array_part3


		self.test.array_counter += 1
		commentary(COMM_ball_by_ball)
		matchviewer(javascript_array)




	def over (self):
		COMM_day_break = ''
		ALTCOMM_day_break = ''
		VIEWER_day_break = ''
		self.incomplete_lastover = ''

		if self.test.overcount() % 90 == 0 and self.test.odi == False:
			for i in self.order: i.spell = 0 
			self.fatigue = []

		self.overlog = [self.onstrike.name]
		x = self.runs
		y = self.bowlchange()
		if y != self.bowler:
			self.bowler.bowling.spell == 0
		self.bowler = y

		self.fatigue.append(self.bowler)
		if len(self.fatigue) > 25: self.fatigue.pop(0)

		if self.bowler.bowling not in self.order: self.order.append(self.bowler.bowling)
		self.day()
		while self.balls < 6 and self.wickets < 10 and self.active == True:
			if self.test.remaining() <= 0: 
				self.active = False
				self.result()
				break

			self.ball()
			self.result()
			
		self.day()

		if self.runs - x == 0 and self.balls == 6: 
			self.bowler.bowling.maidens += 1
			self.bowler.maidens += 1


		if (self.balls < 6 and self.wickets == 10) or (self.balls < 6 and self.active == False): self.incomplete_lastover = True  ## Building to check the overlog from incomplete last overs 

		if (self.balls == 6) or self.incomplete_lastover:
			if self.balls == 6:
				self.overs, self.balls = self.overs+1, 0
				self.bowler.bowling.overs +=1
				self.bowler.bowling.spell += 1
				self.bowler.bowling.balls = 0


			###### Ball by Ball Commentary ######
			
			n = self.test.teaminnings[-1].lead()
			if len(self.test.teaminnings) == 1: COMM_score_in_context = ''
			elif len(self.test.teaminnings) in [2,3]:
				if n > 0: COMM_score_in_context = f"(lead by {n})"
				elif n == 0: COMM_score_in_context = f"(scores level)"
				else: COMM_score_in_context = f"(trail by {-n})"
			else: 
				COMM_score_in_context = '(target {})'.format(self.test.teaminnings[3].target()+self.test.teaminnings[3].runs)
			

			if self.test.overcount() % 90 == 30: 
				COMM_day_break = '...LUNCH on Day ' + str(self.day()) +'\n\n\n--Day ' + str(self.day()) + ', 2nd Session--\n\n'	
				ALTCOMM_day_break = '<tr><td colspan = "11"><br>LUNCH on Day ' + str(self.day()) +'<br><br>--Day ' + str(self.day()) + ', 2nd Session--</td></tr>'+ self.default_alt_commentary_header  ###### Alternate Ball by Ball Commentary #####
				VIEWER_day_break = 'LUNCH on Day ' + str(self.day()) + '<br><br>'
			if self.test.overcount() % 90 == 60: 
				COMM_day_break = '...TEA on Day ' + str(self.day()) +'\n\n\n--Day ' + str(self.day()) + ', 3rd Session--\n\n'	
				ALTCOMM_day_break = '<tr><td colspan = "11"><br>TEA on Day ' + str(self.day()) +'<br><br>--Day ' + str(self.day()) + ', 3rd Session--</td></tr>' + self.default_alt_commentary_header	###### Alternate Ball by Ball Commentary #####
				VIEWER_day_break = 'TEA on Day ' + str(self.day()) + '<br><br>'
			COMM_runs_in_over = self.runs - x 
			COMM_wickets_in_over = self.overlog.count("W")
			COMM_end_of_over = f"\n...{str(COMM_runs_in_over)} runs and {COMM_wickets_in_over} wickets in that over. {self.bowler.name} {self.bowler.bowling.wickets}/{self.bowler.bowling.runs} ({self.bowler.bowling.overs}.{self.bowler.bowling.balls})\n...Score: {str(self.runs)}/{str(self.wickets)} {COMM_score_in_context}. {self.batsmen[0].name} {self.batsmen[0].innings.runs}* ({self.batsmen[0].innings.balls}b), {self.batsmen[1].name} {self.batsmen[1].innings.runs}* ({self.batsmen[1].innings.balls}b). Partnership {self.partnership(0)}.\n\n{COMM_day_break}"
			commentary(COMM_end_of_over)

			##########################################


			#### MATCH VIEWER #####
			javascript_array_part1 = f'myArray[{self.test.array_counter}] = "'
			javascript_array_content = f'END OF OVER,{VIEWER_day_break}END OF OVER - {str(COMM_runs_in_over)} runs and {COMM_wickets_in_over} wickets in that over'
			javascript_array = javascript_array_part1 + self.javascript_array_part2 + javascript_array_content + self.javascript_array_part3
			self.test.array_counter += 1
			matchviewer(javascript_array)


			################################## Alternate Ball by Ball Commentary : START OF CORE SCRIPTS ##################################
			

			global on_strike, non_strike, batsman0_balls, batsman1_balls
			batsman0_balls = ''
			batsman1_balls = ''
			overlog_detail_count = 0


			## Frequently used table stuctures (FUTS)

			self.default_alt_commentary_header = f"<tr><td style = 'border:0.5px dotted black;' width='8%'>Time</td><td style = 'border:0.5px dotted black;' width='17%'>Bowler</td><td style = 'border:0.5px dotted black;' width='20%'>Batsman</td><td style = 'border:0.5px dotted black;' width='5%'>Rns</td><td style = 'border:0.5px dotted black;' width='5%'>Bls</td><td style = 'border:0.5px dotted black;' width='20%'>Batsman</td><td style = 'border:0.5px dotted black;' width='5%'>Rns</td><td style = 'border:0.5px dotted black;' width='5%'>Bls</td><td style = 'border:0.5px dotted black;' width='5%'>Overs</td><td style = 'border:0.5px dotted black;' width='5%'>Tot</td><td style = 'border:0.5px dotted black;' width='5%'>Wk</td></tr>"
			
			self.default_alt_commentary_batsmen = f"<tr><td style = 'border:0.5px dotted black;' width='8%' colspan = '2'></td><td style = 'border:0.5px dotted black;' width='20%'>{self.batsmen[0].name}</td><td style = 'border:0.5px dotted black;' width='5%' colspan = '2'></td><td style = 'border:0.5px dotted black;' width='20%'>{self.batsmen[1].name}</td><td style = 'border:0.5px dotted black;' colspan = '5'></td></tr>"


			for overlog_detail in self.overlog:
				overlog_detail_count += 1


				if overlog_detail in self.dismissed_batsmen_names:
					self.playerindex = self.dismissed_batsmen_details.index('OUT - ' + overlog_detail)
					self.lastbatsman = self.dismissed_batsmen_details[self.playerindex]
					self.lastindex = self.dismissed_batsmen_details[self.playerindex + 1]
					self.lastbatsman_dismissal = self.dismissed_batsmen_details[self.playerindex + 2]
					self.lastbatsman_runs = self.dismissed_batsmen_details[self.playerindex + 3]
					self.lastbatsman_balls = self.dismissed_batsmen_details[self.playerindex + 4]
					self.lastbatsman_totalovers = self.dismissed_batsmen_details[self.playerindex + 5]
					self.lastbatsman_totalballs = self.dismissed_batsmen_details[self.playerindex + 6]
					self.lastbatsman_totalruns = self.dismissed_batsmen_details[self.playerindex + 7]
					self.lastbatsman_totalwickets = self.dismissed_batsmen_details[self.playerindex + 8]
					self.nextbatsman = self.dismissed_batsmen_details[self.playerindex + 9]
					self.nextbatsman0 = self.dismissed_batsmen_details[self.playerindex + 10]
					self.nextbatsman1 = self.dismissed_batsmen_details[self.playerindex + 11]

					

					if self.lastindex == 0:
						on_strike = 0
						self.batsmen0_innings_runs = self.lastbatsman_runs
						self.batsmen0_innings_balls = self.lastbatsman_balls
						self.batsmen1_innings_runs = self.dismissed_batsmen_details[self.playerindex + 12]
						self.batsmen1_innings_balls = self.dismissed_batsmen_details[self.playerindex + 13]


					else:
						on_strike = 1	
						self.batsmen1_innings_runs = self.lastbatsman_runs
						self.batsmen1_innings_balls = self.lastbatsman_balls
						self.batsmen0_innings_runs = self.dismissed_batsmen_details[self.playerindex + 12]
						self.batsmen0_innings_balls = self.dismissed_batsmen_details[self.playerindex + 13]


				elif overlog_detail == self.batsmen[0].name:
					on_strike = 0	
					non_strike = 1


				elif overlog_detail == self.batsmen[1].name:
					on_strike = 1
					non_strike = 0



				else:
					if on_strike == 0:
						batsman0_balls += "&nbsp;" + overlog_detail
						batsman1_balls += "&nbsp;&nbsp;"

					if on_strike == 1:
						batsman1_balls += "&nbsp;" + overlog_detail
						batsman0_balls += "&nbsp;&nbsp;"

					self.wicketball = False
				
					if overlog_detail == "W":
					
						if self.lastbatsman_totalwickets < 10:
							self.over_details = f"<tr><td style = 'border:1px dotted black;' width='8%'>{self.test.time()}</td><td style = 'border:1px dotted black;' width='17%'>{self.bowler.name}</td><td style = 'border:1px dotted black;' width='20%'>{batsman0_balls}</td><td style = 'border:1px dotted black;' width='5%'>{self.batsmen0_innings_runs}</td><td style = 'border:1px dotted black;' width='5%'>{self.batsmen0_innings_balls}</td><td style = 'border:1px dotted black;' width='20%'>{batsman1_balls}</td><td style = 'border:1px dotted black;' width='5%'>{self.batsmen1_innings_runs}</td><td style = 'border:1px dotted black;' width='5%'>{self.batsmen1_innings_balls}</td><td style = 'border:1px dotted black;' width='5%'>{str(self.lastbatsman_totalovers)}.{str(self.lastbatsman_totalballs)}</td><td style = 'border:1px dotted black;' width='5%'>{str(self.lastbatsman_totalruns)}</td><td style = 'border:1px dotted black;' width='5%'>{str(self.lastbatsman_totalwickets)}</td></tr><tr><td colspan='11'></td></tr><tr><td colspan='11'>&emsp;{self.lastbatsman} {self.lastbatsman_dismissal} {self.lastbatsman_runs} ({self.lastbatsman_balls}b)<br>&emsp;Score now: {str(self.lastbatsman_totalruns)}/{str(self.lastbatsman_totalwickets)} {COMM_score_in_context}. Next batsman is {self.nextbatsman}</td></tr><tr><td colspan='11'></td></tr><tr><td style = 'border:0.5px dotted black;' width='8%' colspan = '2'></td><td style = 'border:0.5px dotted black;' width='20%'>{self.nextbatsman0}</td><td style = 'border:0.5px dotted black;' width='5%' colspan = '2'></td><td style = 'border:0.5px dotted black;' width='20%'>{self.nextbatsman1}</td><td style = 'border:0.5px dotted black;' colspan = '5'></td></tr>"

						elif self.lastbatsman_totalwickets == 10:
							self.over_details = f"<tr><td style = 'border:1px dotted black;' width='8%'>{self.test.time()}</td><td style = 'border:1px dotted black;' width='17%'>{self.bowler.name}</td><td style = 'border:1px dotted black;' width='20%'>{batsman0_balls}</td><td style = 'border:1px dotted black;' width='5%'>{self.batsmen0_innings_runs}</td><td style = 'border:1px dotted black;' width='5%'>{self.batsmen0_innings_balls}</td><td style = 'border:1px dotted black;' width='20%'>{batsman1_balls}</td><td style = 'border:1px dotted black;' width='5%'>{self.batsmen1_innings_runs}</td><td style = 'border:1px dotted black;' width='5%'>{self.batsmen1_innings_balls}</td><td style = 'border:1px dotted black;' width='5%'>{str(self.lastbatsman_totalovers)}.{str(self.lastbatsman_totalballs)}</td><td style = 'border:1px dotted black;' width='5%'>{str(self.lastbatsman_totalruns)}</td><td style = 'border:1px dotted black;' width='5%'>{str(self.lastbatsman_totalwickets)}</td></tr><tr><td colspan='11'></td></tr><tr><td colspan='11'>&emsp;{self.lastbatsman} {self.lastbatsman_dismissal} {self.lastbatsman_runs} ({self.lastbatsman_balls}b)<br>&emsp;Score now: {str(self.lastbatsman_totalruns)}/{str(self.lastbatsman_totalwickets)} {COMM_score_in_context}.</td></tr><tr><td colspan='11'></td></tr>"
				



						alt_commentary(self.over_details, self.batsmen[0].name, self.batsmen[1].name)

						batsman0_balls = ''
						batsman1_balls = ''
						batsman0_balls = self.lastbatsman_totalballs * "&nbsp;&nbsp;"
						batsman1_balls = self.lastbatsman_totalballs * "&nbsp;&nbsp;"
						self.wicketball = True

			


			if self.wickets < 10 and self.wicketball == False:
				if ALTCOMM_day_break != '':
					ALTCOMM_day_break = ALTCOMM_day_break + self.default_alt_commentary_batsmen
			
				self.over_details = f"<tr><td style = 'border:1px dotted black;' width='8%'>{self.test.time()}</td><td style = 'border:1px dotted black;' width='17%'>{self.bowler.name}</td><td style = 'border:1px dotted black;' width='20%'>{batsman0_balls}</td><td style = 'border:1px dotted black;' width='5%'>{self.batsmen[0].innings.runs}</td><td style = 'border:1px dotted black;' width='5%'>{self.batsmen[0].innings.balls}</td><td style = 'border:1px dotted black;' width='20%'>{batsman1_balls}</td><td style = 'border:1px dotted black;' width='5%'>{self.batsmen[1].innings.runs}</td><td style = 'border:1px dotted black;' width='5%'>{self.batsmen[1].innings.balls}</td><td style = 'border:1px dotted black;' width='5%'>{str(self.overs)}.{str(self.balls)}</td><td style = 'border:1px dotted black;' width='5%'>{str(self.runs)}</td><td style = 'border:1px dotted black;' width='5%'>{str(self.wickets)}</td></tr>{ALTCOMM_day_break}"

				alt_commentary(self.over_details, self.batsmen[0].name, self.batsmen[1].name)
			
			############################################ END OF CORE SCRIPTS   ###################################################





		if self.runs - x > 12:
			y = ''
			for i in self.overlog: 
				if i == 'nb': y = y + str(i)
				else: y = y + str(i) + ' '
			self.test.logger('{} runs from the {} over. ({})'.format(self.runs-x, self.bowler.name, y[:-1]))

		self.declaration()
		if self.wickets < 10 and self.active == True: 
			self.swap(1)
			self.bowler, self.otherbowler = self.otherbowler, self.bowler


	def day (self):
		if self.test.odi == True: return 1

		y = round(1+(self.test.overcount())//90)
		z = self.test.overcount() % 90
		a = '{} {}* ({}b), {} {}* ({}b)'.format(self.batsmen[0].name, self.batsmen[0].innings.runs, self.batsmen[0].innings.balls, self.batsmen[1].name, self.batsmen[1].innings.runs, self.batsmen[1].innings.balls)

		y = min(y, self.test.scheduledovers//90)

		if (z == 30 or z == 60) and self.balls == 0 and self.overs > 0:
			if z == 30:
				self.test.logger('Lunch: ' + a)
			elif z == 60:
				self.test.logger('Tea: ' + a)



		x = 'Day {}'.format(y)
		if y > self.test.daytracker:
			if y > 1:
				#self.test.logger('Close of play: ' + a + '\n' + '\n' + '\n————————————————————————————————————————————————————————————————————————————————————————————-')
				self.test.logger('Close of play: ' + a + '\n\n')

				###### Ball by Ball Commentary ######
				n = self.test.teaminnings[-1].lead()
				if len(self.test.teaminnings) == 1: COMM_score_in_context = ''
				elif len(self.test.teaminnings) in [2,3]:
					if n > 0: COMM_score_in_context = f"(lead by {n})"
					elif n == 0: COMM_score_in_context = f"(scores level)"
					else: COMM_score_in_context = f"(trail by {-n})"
				else: 
					COMM_score_in_context = '(target {})'.format(self.test.teaminnings[3].target()+self.test.teaminnings[3].runs)

				COMM_end_of_day = f"...End of Day {y-1} - {self.team.name} {str(self.runs)}/{str(self.wickets)} {COMM_score_in_context}. {self.batsmen[0].name} {self.batsmen[0].innings.runs}* ({self.batsmen[0].innings.balls}b), {self.batsmen[1].name} {self.batsmen[1].innings.runs}* ({self.batsmen[1].innings.balls}b). {self.bowler.name} {self.bowler.bowling.wickets}/{self.bowler.bowling.runs} ({self.bowler.bowling.overs}.{self.bowler.bowling.balls})\n\n\n\n--{x}, 1st Session--\n\n"
				commentary(COMM_end_of_day)

				#######################################


				#### MATCH VIEWER #####
				javascript_array_part1 = f'myArray[{self.test.array_counter}] = "'
				javascript_array_content = f'END OF DAY,END OF DAY {y-1} <br> {self.team.name} {str(self.runs)}/{str(self.wickets)} {COMM_score_in_context}<br>{self.batsmen[0].name} {self.batsmen[0].innings.runs}* ({self.batsmen[0].innings.balls}b)<br>{self.batsmen[1].name} {self.batsmen[1].innings.runs}* ({self.batsmen[1].innings.balls}b)<br>{self.bowler.name} {self.bowler.bowling.wickets}/{self.bowler.bowling.runs} ({self.bowler.bowling.overs}.{self.bowler.bowling.balls})<br>{self.otherbowler.name} {self.otherbowler.bowling.wickets}/{self.otherbowler.bowling.runs} ({self.otherbowler.bowling.overs}.{self.otherbowler.bowling.balls})'
				javascript_array = javascript_array_part1 + self.javascript_array_part2 + javascript_array_content + self.javascript_array_part3
				self.test.array_counter += 1
				matchviewer(javascript_array)



				### Alternate Ball by Ball Commentary ####

				ALTCOMM_end_of_day = f"<tr><td colspan='11'></td></tr><tr><td colspan='11'><br><br>END OF DAY { y-1}<br>{self.team.name} {str(self.runs)}/{str(self.wickets)} {COMM_score_in_context}. {self.batsmen[0].name} {self.batsmen[0].innings.runs}*, {self.batsmen[1].name} {self.batsmen[1].innings.runs}*. {self.bowler.name} {self.bowler.bowling.wickets}/{self.bowler.bowling.runs}, {self.otherbowler.name} {self.otherbowler.bowling.wickets}/{self.otherbowler.bowling.runs}<br><br><br><br></td></tr><tr><td colspan='11'>--{x}, 1st Session--</td></tr>{self.default_alt_commentary_header}{self.default_alt_commentary_batsmen}"
				alt_commentary(ALTCOMM_end_of_day, self.batsmen[0].name, self.batsmen[1].name)


				##########################################



				#self.scoresheet()
				

			self.test.logger(x)
			self.test.daytracker = y
		return y

	def swap (self, n):
		if n % 2 == 1:
			if self.batsmen[0] == self.onstrike: self.onstrike = self.batsmen[1]
			else: self.onstrike = self.batsmen[0]
			if self.balls < 6: 
				self.overlog.append(self.onstrike.name)
				self.swap_check = True  ######## Alternate Ball by Ball Commentary #########

	def lead (self):
		a = sum([x.runs for x in self.test.teaminnings if x.team == self.team])
		b = sum([x.runs for x in self.test.teaminnings if x.team != self.team])
		return a-b

	def milestone (self, n):
		x = self.onstrike.innings.runs-n

		if x % 50 > 10 and self.onstrike.innings.runs % 50 <= n:
			self.test.logger('{} {}* ({}b) {}x4 {}x6'.format(self.onstrike.name, self.onstrike.innings.runs, self.onstrike.innings.balls, self.onstrike.innings.fours, self.onstrike.innings.sixes))
			self.declaration()
		if self.runs % 50 < n and n != 0 and self.runs >= 50:
			self.test.logger('{} {}* ({}b), {} {}* ({}b).'.format(self.batsmen[0].name, self.batsmen[0].innings.runs, self.batsmen[0].innings.balls, self.batsmen[1].name, self.batsmen[1].innings.runs, self.batsmen[1].innings.balls))
			self.declaration()


	def partnership (self, n):
		try: a = max([x.FOW[1] for x in self.innings if x.FOW is not ''])
		except: a = 0
		y = self.runs-a
		if y % 50 < n and y >= 50:
			z = 50*round(y/50)
			x = '{} partnership between {} and {}.'.format(z,self.batsmen[0].name,self.batsmen[1].name)
			self.test.logger(x)
		return y

	def declaration (self):
		if self.test.odi == True: return False

		if self.test.weather == 'Timeless' or len(self.test.teaminnings) == 4 or self.wickets == 10: return False
		for i in self.batsmen:
			if i.innings.runs % 100 > 89 and (i is not self.team.captain or random.random() < 0.9): return False

		if len(self.test.teaminnings) == 1 and (self.runs > 500 or self.overs > 150) and random.random() < self.runs/50000: 
			self.declare = True
		elif len(self.test.teaminnings) == 2 and self.runs > 500 and self.lead() > -50 and random.random() < 0.01: 
			self.declare = True
		elif len(self.test.teaminnings) == 2 and (self.runs/self.test.teaminnings[0].runs > 2) and self.overs > 100 and self.runs > 350 and random.random() < 0.01:
			self.declare = True
		elif len(self.test.teaminnings) == 2 and self.lead() > 200 and self.runs > 400 and random.random() < 0.01:
			self.declare = True
		elif len(self.test.teaminnings) == 3 and self.lead() > (self.test.remaining()*self.test.rpo + 100) and self.test.remaining() > 35:
			self.declare = True

		if self.declare == True:
			self.test.logger('{} declared with a lead of {}.'.format(self.team.gamecapt.name, self.lead()))
			self.active = False
			#self.allout()
		else:
			return False

	def allout (self):
		a = '{} {}* ({}b), {} {}* ({}b)'.format(self.batsmen[0].name, self.batsmen[0].innings.runs, self.batsmen[0].innings.balls, self.batsmen[1].name, self.batsmen[1].innings.runs, self.batsmen[1].innings.balls)

		if len(self.test.teaminnings) < 4 or self.test.win != '':
			self.test.tobat = self.followon()
			q,w = '',''
			if self.batsmen[0].innings.out == False: q = "*"
			if self.batsmen[1].innings.out == False: w = "*"
			#self.test.logger('End of innings - {} {}{} ({}b), {} {}{} ({}b).\n \n \n————————————————————————————————————————————————————————————————————————————————————————————-'.format(self.batsmen[0].name, self.batsmen[0].innings.runs, q, self.batsmen[0].innings.balls, self.batsmen[1].name, self.batsmen[1].innings.runs, w, self.batsmen[1].innings.balls))
			self.test.logger('End of Innings: ' + a + '\n' + '\n' + '\n')
				
			###### Ball by Ball Commentary ######
			n = self.test.teaminnings[-1].lead()
			if len(self.test.teaminnings) == 1: COMM_score_in_context = ''
			elif len(self.test.teaminnings) in [2,3]:
				if n > 0: COMM_score_in_context = f"(lead by {n})"
				elif n == 0: COMM_score_in_context = f"(scores level)"
				else: COMM_score_in_context = f"(trail by {-n})"
			else: 
				COMM_score_in_context = '(target {})'.format(self.test.teaminnings[3].target()+self.test.teaminnings[3].runs)


			COMM_end_of_innings = f"\n...End of innings - {self.team.name} {str(self.runs)}/{str(self.wickets)} {COMM_score_in_context}. {self.batsmen[0].name} {self.batsmen[0].innings.runs}{q} ({self.batsmen[0].innings.balls}b), {self.batsmen[1].name} {self.batsmen[1].innings.runs}{w} ({self.batsmen[1].innings.balls}b). {self.bowler.name} {self.bowler.bowling.wickets}/{self.bowler.bowling.runs} ({self.bowler.bowling.overs}.{self.bowler.bowling.balls})\n\n\n"
			commentary(COMM_end_of_innings)

			########################################

			#### MATCH VIEWER #####
			javascript_array_part1 = f'myArray[{self.test.array_counter}] = "'
			javascript_array_content = f'END OF INNINGS,END OF INNINGS <br> {self.team.name} {str(self.runs)}/{str(self.wickets)} {COMM_score_in_context}<br>{self.batsmen[0].name} {self.batsmen[0].innings.runs}{q} ({self.batsmen[0].innings.balls}b)<br>{self.batsmen[1].name} {self.batsmen[1].innings.runs}{w} ({self.batsmen[1].innings.balls}b)<br>{self.bowler.name} {self.bowler.bowling.wickets}/{self.bowler.bowling.runs} ({self.bowler.bowling.overs}.{self.bowler.bowling.balls})<br>{self.otherbowler.name} {self.otherbowler.bowling.wickets}/{self.otherbowler.bowling.runs} ({self.otherbowler.bowling.overs}.{self.otherbowler.bowling.balls})'
			javascript_array = javascript_array_part1 + self.javascript_array_part2 + javascript_array_content + self.javascript_array_part3
			self.test.array_counter += 1
			matchviewer(javascript_array)




			###### Alternate Ball by Ball Commentary ######
			ALTCOMM_end_of_innings = f"<tr><td colspan='11'></td></tr><tr><td colspan='11'><br><br>END OF INNINGS<br>{self.team.name} {str(self.runs)}/{str(self.wickets)} {COMM_score_in_context}. {self.batsmen[0].name} {self.batsmen[0].innings.runs}{q} ({self.batsmen[0].innings.balls}b), {self.batsmen[1].name} {self.batsmen[1].innings.runs}{w} ({self.batsmen[1].innings.balls}b). {self.bowler.name} {self.bowler.bowling.wickets}/{self.bowler.bowling.runs} ({self.bowler.bowling.overs}.{self.bowler.bowling.balls})<br><a target='_blank' href='scoresheet{len(self.test.teaminnings)}.txt'>See Full Scorecard</a><br><br><br><br></td></tr><tr><td colspan='11'></td></tr>"
			alt_commentary(ALTCOMM_end_of_innings, self.batsmen[0].name, self.batsmen[1].name)


		self.scoresheet()

		self.changeofinning()



	def scoresheet (self):
		if self.balls == 6:
			self.balls = 0
			self.overs += 1
		if self.bowler.bowling.balls == 6:
			self.bowler.bowling.balls = 0
			self.bowler.bowling.overs += 1
		self.bowler.overcount()


		if len(self.test.teaminnings) < 4 or self.test.win != '':
			q,w = '',''
			if self.batsmen[0].innings.out == False: q = "*"
			if self.batsmen[1].innings.out == False: w = "*"

		#self.test.tobat = self.followon()
		self.test.logprint()
		self.inningsheader()

		for a in self.test.players:
			a.stats(self.test)

		for a in self.innings:
			a.stats()
			if a.out == False: 
				a.dismissal = 'not out'
				FOW = ''
			else:
				if a.FOW[2] == 10:
					FOW = '{}ao'.format(a.FOW[1])
				else:
					FOW = '{}-{}'.format(a.FOW[1],a.FOW[2])

			tag = ''
			if a.player == self.team.gamecapt: tag = tag + '*'
			if a.player == self.team.wk: tag = tag + "†"

			if len(tag) > 1:
				name = a.name.ljust(19)
			else:
				name = a.name.ljust(20)

			if self.test.fullcard == True:
				 a.scorecard = '{}{} {} {} {} FOW:{}      {}'.format(tag.rjust(1),name, a.dismissal.rjust(50), str(a.runs).rjust(3), '({})'.format(a.balls).rjust(5),FOW.rjust(6),a.player.batdesc(self.test.year))
			else:
				a.scorecard = '{}{} {} {} {} FOW:{}'.format(tag.rjust(1),name, a.dismissal.rjust(50), str(a.runs).rjust(3), '({})'.format(a.balls).rjust(5),FOW.rjust(6))
			
			if a.balls > 0:
				self.test.score (a.scorecard)
				self.test.newscore(a.scorecard)

		if sum(self.extras) > 0:
			a = ''
			if self.extras[0] >0: a = a + '{}b, '.format(self.extras[0])
			if self.extras[1] >0: a = a + '{}lb, '.format(self.extras[1])
			if self.extras[2] >0: a = a + '{}w, '.format(self.extras[2])
			if self.extras[3] >0: a = a + '{}nb, '.format(self.extras[3])
			if self.extras[4] >0: a = a + '{}pen, '.format(self.extras[4])

			a = a[:-2]
			self.test.score('{} - extras {}'.format(a, str(sum(self.extras)).rjust(3)).rjust(76))
			self.test.newscore('{} - extras {}'.format(a, str(sum(self.extras)).rjust(3)).rjust(76))
		else:
			self.test.score('extras 0'.rjust(76))
			self.test.newscore('extras 0'.rjust(76))

		if self.overs + self.balls > 0: z = "%.2f" % (self.runs/(self.overs + self.balls/6))
		else: z = ''

		if self.wickets == 10:
			y = '(all out - {} overs) {}   ({} RPO)'.format(oversballs (self), self.runs, z)
		elif self.declare == True:
			y = '({} wickets declared - {} overs) {}   ({} RPO)'.format(self.wickets, oversballs (self), self.runs, z)
		else:
			y = '({} wickets - {} overs) {}   ({} RPO)'.format(self.wickets, oversballs (self), self.runs, z)

		self.test.score (y.rjust(89))
		self.test.newscore (y.rjust(89))

		b = [x.name for x in self.innings if x.balls == 0]

		self.test.score( '{}{}{}{}{}'.format(''.ljust(21),'O'.center(6), 'M'.center(7), 'R'.center(5), 'W'.center(5)))
		self.test.newscore( '{}{}{}{}{}'.format(''.ljust(21),'O'.center(6), 'M'.center(7), 'R'.center(5), 'W'.center(5)))
		for i in self.order:
			i.stats()
			if i.overs == 0 and i.balls == 0:
				continue
			if i.balls > 0: 
				o = i.overs + i.balls/6
			else: o = i.overs

			if o > 0: e = "%.2f" % round(i.runs/o,2)
			else: e = "----" 

			if self.test.fullcard == True:
				y = ' {} {} - {} - {} - {}   {} RPO {} {} {}'.format(i.name.ljust(20), oversballs(i).center(4), str(i.maidens).rjust(2), str(i.runs).rjust(3), str(i.wickets).rjust(2), str(e), i.player.tag.center(15), ''.ljust(28),i.player.bowldesc(self.test.year))
			else:
				y = ' {} {} - {} - {} - {}   {} RPO {}'.format(i.name.ljust(20), oversballs(i).center(4), str(i.maidens).rjust(2), str(i.runs).rjust(3), str(i.wickets).rjust(2), str(e), i.player.tag.center(15))
			self.test.score (y)		
			self.test.newscore (y)	

		
		self.test.decorator()
		self.test.blank()
		self.test.blank()
		self.test.blank()
		self.test.blank()


	def followon (self):
		if self.test.odi == True: return self.bowlteam

		if len(self.test.teaminnings) == 2 and self.lead() <= -200 and self.wickets == 10:
			if (self.test.weather == 'Timeless' and self.lead() <= -300) or -(self.lead())  > self.test.remaining()-self.test.lostovers + self.overs*0.5:
				self.test.logger('{} chose to enforce the follow-on.\n\n'.format(self.bowlteam.gamecapt.name))
				return self.team
			else:
				self.test.logger('{} declined to enforce the follow-on.\n\n'.format(self.bowlteam.gamecapt.name))
		return self.bowlteam

	
	def changeofinning (self):
		#y = self.test.teaminnings[-1]
		y = self.followon()
		if len(self.test.teaminnings) >= 2: inn_number = '2nd'
		else: inn_number = '1st'
		 
		with open (self.test.scorecard, 'a') as f:
			if len(self.test.teaminnings) < 4 and self.test.win == '':
				#x = 'Change of innings'
				x = '{} - {} innings'.format(y.name, inn_number)
				f.write(x)
				commentary('\n' + x + '\n\n') ###### Ball by Ball Commentary ######


				###### Alternate Ball by Ball Commentary ######
				self.batsmen = [y.xi[0],y.xi[1]]

				ALTCOMM_end_of_innings = f"<tr><td colspan='11'>{x}</td></tr><tr><td colspan='11'></td></tr>{self.default_alt_commentary_header}<tr><td style = 'border:0.5px dotted black;' width='8%' colspan = '2'></td><td style = 'border:0.5px dotted black;' width='20%'>{self.batsmen[0].name}</td><td style = 'border:0.5px dotted black;' width='5%' colspan = '2'></td><td style = 'border:0.5px dotted black;' width='20%'>{self.batsmen[1].name}</td><td style = 'border:0.5px dotted black;' colspan = '5'></td></tr>"
				alt_commentary(ALTCOMM_end_of_innings, self.batsmen[0].name, self.batsmen[1].name)	
				#################################################

			else:
				 f.write("Post Match")
		self.test.card.append('')


	def target (self):
		a = sum([x.runs for x in self.test.teaminnings if x.team == self.team])
		b = sum([x.runs for x in self.test.teaminnings if x.team != self.team])
		return b-a+1

	def margin (self):
		if self.test.win in ['Draw', 'Tie']: return self.test.win

		a = sum([x.runs for x in self.test.teaminnings if x.team == self.team])
		b = sum([x.runs for x in self.test.teaminnings if x.team == self.bowlteam])

		if b > a and len(self.test.teaminnings) == 3:
			if b-a != 1: return 'an innings and {} runs'.format(b-a)
			else: return 'an innings and 1 run'
		elif b > a and (len(self.test.teaminnings) == 4 or self.test.odi == True and len(self.test.teaminnings)==2):
			if b-a != 1: return '{} runs'.format(b-a)
			else: return '1 run'
		elif (len(self.test.teaminnings) == 4 or self.test.odi == True and len(self.test.teaminnings)==2) and a > b:
			if self.wickets != 9: return '{} wickets'.format(10-self.wickets)
			else: return '1 wicket'
		else: return ''

	def endofgame (self):
		self.test.blank()
		self.result()
		a, b = [], []
		if self.test.win == '':
			return

		if self.test.win in ['Draw', 'Tie']:
			for i in self.test.teaminnings:
				x = [i.runs, i.wickets]
				if i.team == self.test.teaminnings[0].team: a.append(scoreformat(x))
				else: b.append(scoreformat(x)) 
			
			if self.test.win == 'Draw':
				x = ' {} ({}) drew with {} ({})'.format(self.test.teaminnings[0].team.name, listshow(a), [x for x in [self.test.home, self.test.away] if x is not self.test.teaminnings[0].team][0].name, listshow(b))
			else:
				x = ' {} ({}) tied with {} ({})'.format(self.test.teaminnings[0].team.name, listshow(a), [x for x in [self.test.home, self.test.away] if x is not self.test.teaminnings[0].team][0].name, listshow(b))
		
		else: 
			for i in self.test.teaminnings:
				x = [i.runs, i.wickets]
				if i.team == self.test.win: a.append(scoreformat(x))
				else: b.append(scoreformat(x))
			x = ' {} ({}) beat {} ({}) by {}'.format(self.test.win.name, listshow(a), [x for x in [self.test.home, self.test.away] if x is not self.test.win][0].name, listshow(b), self.test.margin)
		self.test.score(x)
		commentary('...In summary, ' + x)  ###### Ball by Ball Commentary ######

		ALTCOMM_result = x  ### Alternate Ball by Ball Commentary ####


		self.test.resultdesc = x
		if self.test.win in ['Draw', 'Tie']: self.test.winname = self.test.win
		else: self.test.winname = self.test.win.name

		self.test.motmpick()

		x = []

		for i in self.test.teaminnings:
			for j in i.innings:
				if j.player == self.test.motm and j.balls > 0:
					if j.out == True: y = ''
					else: y = '*'
					x.append('{}{}'.format(j.runs, y))
			for j in i.order:
				if j.player == self.test.motm and ((j.balls > 0) or (j.overs > 0)): x.append('{}-{}'.format(j.wickets, j.runs))			

		self.test.score(' Man of the Match: {} ({}) ({})'.format(self.test.motm.name, self.test.motm.team,listshow(x)))

		###### Ball by Ball Commentary ######
		COMM_motm = '. {} ({}) was the Man of the Match for ({}).\n...End of the file. Created from modified version of CricketPy by Jamee.\n'.format(self.test.motm.name, self.test.motm.team,listshow(x))
		commentary(COMM_motm)
		

		### Alternate Ball by Ball Commentary ####
		ALTCOMM_motm = 'Man of the Match: {} ({}) for ({})<br>End of the file. Created from modified version of CricketPy developed by Jamee.'.format(self.test.motm.name, self.test.motm.team,listshow(x))
		ALTCOMM_summary = f"<tr><td colspan='11'>RESULT: {ALTCOMM_result}<br>{ALTCOMM_motm}</td></tr></table></html>"
		alt_commentary(ALTCOMM_summary, a, b)


		#### MATCH VIEWER #####
		javascript_array_part1 = f'myArray[{self.test.array_counter}] = "'
		javascript_array_content = f'END OF MATCH,END OF MATCH<br>{ALTCOMM_result.replace(","," &")}<br>{self.test.motm.name} ({self.test.motm.team}) was the Man of the Match for ({listshow(x).replace(",",";")})'
		last_inning = f',{self.team.name},{self.runs},{self.wickets}"\n'
		javascript_array = javascript_array_part1 + self.javascript_array_part2 + javascript_array_content + self.javascript_array_part3.replace('"\n',last_inning)
		self.test.array_counter += 1
		matchviewer(javascript_array)





		if self.test.lostovers > 0:
			self.test.score(' {} overs lost to bad weather.'.format(self.test.lostovers))
		self.test.score(self.test.pitchdetails())
		#self.test.logger('End of game:'+x)
		self.test.logprint()
		self.test.matchreport()

		##### ONLY SAVE SCORECARDS FROM THIS POINT ON ######

		if self.test.saveallcards == True: self.test.cardsave()

		if len(test.teaminnings) == 4:
			if self.test.win == self.test.teaminnings[1].team == self.test.teaminnings[2].team: self.test.cardsave()

		if any((x.runs >= 700 or (x.runs <=50 and x.wickets ==10)) for x in self.test.teaminnings): self.test.cardsave()
		if any((x.runs >= 250 or (x.runs>=200 and (x.runs/x.balls > 1 or self.test.year < 1900))) for x in self.test.inns): self.test.cardsave()
		if any(x.wickets > 8 and x.runs < 1000 for x in self.test.bowls):self.test.cardsave() 
		if any(x.wickets == 8 and x.runs < 50 for x in self.test.bowls):self.test.cardsave() 
		if any(x.wickets >=6 and x.runs <=10 for x in self.test.bowls): self.test.cardsave()

		if self.test.weather == 'Timeless' and self.test.win == 'Draw': self.test.cardsave()

	def finish (self):
		if self.balls == 6:
			self.overs += 1
			self.balls = 0
		self.active = False

		self.test.margin = self.margin()



	def result (self):
		a = sum([x.runs for x in self.test.teaminnings if x.team == self.team])
		b = sum([x.runs for x in self.test.teaminnings if x.team == self.bowlteam])

		#print (a, b, self.test.remaining())

		if self.test.odi == True: 
			if a > b and len(self.test.teaminnings) == 2:
				self.test.win = self.team
				self.test.lose = self.bowlteam
				self.finish()
				return

			if (self.wickets == 10 or self.overs == self.test.overslimit):
				if b > a:
					self.test.win = self.team
					self.test.lose = self.bowlteam
					self.finish()
					return	
				elif b == a:
					self.test.win, self.test.margin = 'Tie', 'Tie'
					self.finish()
					return

		if self.test.remaining() <= 0 and ((b >= a and self.wickets < 10) or (len(self.test.teaminnings) < 4 and a >= b)):
			self.test.win, self.test.margin = 'Draw', 'Draw'
			self.finish()
			return

		if len (self.test.teaminnings) == 4:
			if a > b: 
				self.test.win = self.team
				self.test.loss = self.bowlteam
				self.finish()
				return
			if self.wickets == 10:
				if b > a:
					self.test.win = self.bowlteam
					self.test.loss = self.team
					self.finish()
					return
				elif a == b:
					self.test.win, self.test.margin = 'Tie', 'Tie'
					self.finish()
					return

		elif len(self.test.teaminnings) == 3:
			if b > a and self.wickets == 10:
				self.test.win = self.bowlteam
				self.test.loss = self.team
				self.finish()
				return

		if b > a and self.wickets < 10: return

	test = ''
	team = ''
	bowlteam = ''
	number = ''
	active = ''
	declare = False

	runs = 0
	wickets = 0
	overs = 0
	balls = 0
	extras = []

	onstrike = ''
	batsmen = ''
	bowler = ''
	innings = ''
	order = ''
	fatigue = ''


class test:
	def __init__(self):
		self.raw = []
		self.card = []
		self.newcard = []
		self.log = []
		self.inns, self.bowls = [], []
		self.teaminnings = []
		self.players = []
		self.log = []
		self.array_counter = 5
		self.first_javascript_array = ''

	def cricket (self):
		t = datetime.datetime.now()
		self.card = []
		self.environment()
		self.conditions()
		self.settings()
		self.playerlog()
		self.header()
		self.pregamestats()
		#print ('scheduledovers', self.scheduledovers, 'gameovers', self.gameovers)
		self.toss()

		if self.odi == True: n = 2
		else: n = 4

		for i in range (n):
			if self.win != '':
				continue
			x = teaminnings (self) 
			self.teaminnings.append(x) 
			self.blank()
			x.run()

		self.teaminnings[-1].endofgame()
		self.stats()
		for i in self.players:
			i.stats(self)
		print ()
		for i in self.log:
			print (i)
		#print(datetime.datetime.now()-t)
	
	def conditions (self):
		Asia = ['India', 'Pakistan', 'Sri Lanka', 'Bangladesh', 'Afghanistan']

		if self.weather == 'default': return

		if self.weather == 'Timeless': 
			print ('Timeless Test')
			self.gameovers = self.scheduledovers = random.choice([900,990,1080,1170,1260,1350,1440,1530,1620,1710,1800])
			if random.random() < 0.02: self.gameovers  = self.scheduledovers*(1-(random.random()*random.random()*random.random()))
			elif random.random() < 0.15: self.gameovers  = random.randrange(round(0.8*self.scheduledovers),self.scheduledovers)

		elif self.weather in ['England','New Zealand','Ireland']:
			if random.random() < 0.1: self.gameovers  = self.scheduledovers *(1-(random.random()*random.random()*random.random()))
			elif random.random() < 0.25: self.gameovers  = random.randrange(round(0.8*self.scheduledovers),self.scheduledovers)

		elif self.weather in ['Australia','India','Pakistan','Afghanistan','Zimbabwe']:
			if random.random() < 0.01: self.gameovers  = self.scheduledovers *(1-(random.random()*random.random()*random.random()))
			elif random.random() < 0.1: self.gameovers  = random.randrange(round(0.8*self.scheduledovers),self.scheduledovers)

		elif self.weather in ['South Africa','New Zealand','Sri Lanka','Bangladesh']:
			if random.random() < 0.03: self.gameovers  = self.scheduledovers *(1-(random.random()*random.random()))
			elif random.random() < 0.15: self.gameovers  = random.randrange(round(0.8*self.scheduledovers),self.scheduledovers)

		self.gameovers = round(self.gameovers)

	def environment (self):
		with open ('eradata.txt') as f:
			for line in f:
			    line = line[:-1]
			    x = line.split(', ')
			    if int(x[0]) == self.year:
			        self.base = float(x[1])

		with open ('er_data.txt') as f:
		    for line in f:
		        line = line[:-1]
		        x = line.split(', ')
		        if int(x[0]) == self.year:
		            self.rpo = float(x[1])

	def settings (self):
		with open ('settings.txt') as f:
			a = []
			for line in f:
				if line[0] == '#' or line == '': continue
				else: pass
				x = line[:-1].split("=")
				if len(x) > 1:
					x[0] = x[0][:-1]
					x[1] = x[1][1:]
					a.append(x)
			if any (x[0] == 'active' and x[1] == 'true' for x in a):
				for i in a:
					if i[1] == 'default': continue
					print (i[0], '-', i[1])
					if i[0] == 'pace': self.pitch[0] = float(i[1])
					elif i[0] == 'spin': self.pitch[1] = float (i[1])
					elif i[0] == 'outfield': self.pitch[2] = float (i[1])
					elif i[0] == 'venue': self.venue = i[1]
					elif i[0] == 'year': 
						self.year = int(i[1])
						self.environment()
					elif i[0] == 'weather': 
						self.weather = i[1]
						self.conditions()
					elif i[0] == 'overs': 
						self.scheduledovers = int(i[1])
						self.gameovers = int (i[1])
					elif i[0] == 'average': self.base = float(i[1])
					elif i[0] == 'runrate': self.rpo = float(i[1])
					elif i[0] == 'homecapt': self.home.gamecapt = namematch (self.home.xi, i[1], self.home.gamecapt)
					elif i[0] == 'homewk': self.home.wk = namematch(self.home.xi, i[1], self.home.wk)
					elif i[0] == 'awaywk': self.away.wk = namematch(self.away.xi, i[1], self.away.wk)
					elif i[0] == 'awaycapt': self.away.gamecapt = namematch (self.home.xi, i[1], self.away.gamecapt)
					elif i[0] == 'toss':
						if i[1] == 'home': self.tosswin = self.home
						elif i[1] == 'away': self.tosswin = self.away
						print (self.tosswin.name)
					elif i[0] == 'choice':
						if i[1] == 'bat': self.choice = True
						elif i[1] == 'bowl': self.choice = False
					elif i[0] == 'showbowlingchanges':
						if i[1] == 'true': self.bowlingchanges = True

			else: return

	def decision (self):
		if self.choice == '':
			if random.random() < 0.8 or (random.random() < 0.5 and self.odi == True): self.choice = True
			else: self.choice = False

		if self.choice == True: self.score ('{} has elected to bat first.'.format(self.tosswin.gamecapt.name))
		else: self.score ('{} has elected to field first.'.format(self.tosswin.gamecapt.name))

	def toss (self):
		if self.tosswin == '': self.tosswin = random.choice([self.home, self.away])
		self.pitchdetails()
		y = 'Pitch Report: Pace Factor of {}, Spin Factor of {} and Outfield Speed of {}\n(The avergae number is 1. The greater the value, the easier it is for the batsmen)\n'.format("{:0.2f}".format(self.pitch[0]), "{:0.2f}".format(self.pitch[1]),"{:0.2f}".format(self.pitch[2])) 
		self.score(y)
		x = '{} has won the toss.'.format(self.tosswin.name)
		self.score(x)
		self.decision()
		if self.choice == True: self.tobat = self.tosswin
		else: self.tobat = [y for y in [self.home, self.away] if y is not self.tosswin][0]


		#### MATCH VIEWER #####
		pitch_array= 'PITCH REPORT<br> Pace Factor of {}<br> Spin Factor of {}<br> Outfield Speed of {}<br>(The avergae number is 1. The greater the value; the easier it is for batting)'.format("{:0.2f}".format(self.pitch[0]), "{:0.2f}".format(self.pitch[1]),"{:0.2f}".format(self.pitch[2])) 
		self.first_javascript_array = f'myArray[1] = ",,,,,,,,,,,,,,,,,,,,,,,,,,,,BEGIN MATCH,{pitch_array},,,,"\n'
		self.first_javascript_array = self.first_javascript_array + f'myArray[2] = ",,,,,,,,,,,,,,,,,,,,,,,,,,,,BEGIN MATCH,{pitch_array},,,,"\n'


	def overcount (self):
		return sum([x.overs for x in self.teaminnings]) + sum([x.balls > 0 for x in self.teaminnings if x is not self.teaminnings[-1]]) + self.lostovers

	def raincheck (self):
		if self.odi == True: return

		if self.lostovers >= self.scheduledovers-self.gameovers: return
		elif random.random() < (self.scheduledovers-self.gameovers)/(10*self.scheduledovers):
			x = random.randrange(0,10) + round(random.random()*(self.scheduledovers-self.gameovers-self.lostovers))
			x = min (x, self.scheduledovers-self.gameovers-self.lostovers)
			if x > 0:
				self.logger('{} overs lost due to bad weather.'.format(x))
				self.logger('')
				#self.logger('scheduledovers {} gameovers {} lostovers {}'.format(self.scheduledovers, self.gameovers, self.lostovers+x))

				n = 90
				while n < self.overcount() + self.lostovers:
					if self.overcount() < n < self.overcount() + x: self.teaminnings[-1].day()
					n = n + 90

				self.lostovers = self.lostovers + x
				if len (self.teaminnings[-1].fatigue) > x:
					for i in range (x): self.teaminnings[-1].fatigue.pop(0)
					else: self.teaminnings[-1].fatigue = []
				#self.logger(str(self.overcount()))
			#if self.overcount() >= self.gameovers: self.teaminnings[-1].active = False
				
	def remaining (self):
		return self.scheduledovers - self.overcount()

	def playerlog (self):
		self.players = [*self.home.xi, *self.away.xi]

	def time (self):
		if self.odi == True: x = self.overcount()
		else: x = (self.overcount() % 90)
		if self.overcount() >= 450 and self.scheduledovers == 450:
			x = (self.overcount() - 360) + 15 + self.teaminnings[-1].balls/6
		if 30 < x <= 60: x = x + 10
		elif 60 < x <= 90: x = x + 15

		y = round(x // 15)
		z = round(4*(x % 15))

		if (x == 0 and self.teaminnings[-1].balls == 0):
			y, z = 7, random.randrange(0,5)

		#print (self.overcount() , round(x), 11+y, z)
		return '{}:{}'.format(11+y,str(z).zfill(2))

	def logger (self, x):
		t = self.time()
		y = self.teaminnings[-1]
		x = [x, t]
		x.append('{} {}-{} ({}.{} overs)'.format(y.team.name, y.runs, y.wickets, y.overs, y.balls))
		n = self.teaminnings[-1].lead()
		if len(self.teaminnings) == 1: x.append('')
		elif len(self.teaminnings) in [2,3]:
			if n > 0: x.append(' lead by {}'.format(n))
			elif n == 0: x.append(' scores level')
			else: x.append(' trail by {}'.format(-n))
		else: x.append(' target {}'.format(self.teaminnings[3].target()+self.teaminnings[3].runs))


		l = [a[0] for a in self.log]
		if x[0] not in l:
			self.log.append(x)

	def logprint (self):
		for i in self.card:
			print (i)
		self.card = []

		y = ['Lunch:', 'Tea:', 'End of innings']
		with open (self.scorecard, 'a') as f:
			for i in self.log:
				b = i[1]
				z = '{} {} {}'.format(b,str(i[2] + i[3]).ljust(45), i[0])
				if i[0] == '':
					f.write('\n')
					print ()
				elif 'Day ' in i[0]:
					f.write('\n')
					print ()
					f.write(str(i[0]))
					print (i[0])
				elif 'Close of play' in i[0]:
					b = '18:00'
					f.write(z)
					print (z)
				else:
					f.write(z)
					print (z)
				f.write('\n')

				if any(x in i[0] for x in y):
					f.write('\n')
					print ()
		self.log = []

	def header (self):
		with open (self.scorecard, 'w') as f:
			pass
		x = '{} vs. {}'.format(self.home.name, self.away.name)
		self.score(x)

	def blank (self):
		with open (self.scorecard, 'a') as f:
			f.write('\n')
		self.card.append('')


	def decorator (self):
		with open (self.scorecard, 'a') as f:
			f.write('-')
		self.card.append('')	



	def cardkeep (self, x, end = '\n'):
		with open (self.scorecard, 'a') as f:
			f.write(x)
			f.write(end)

	def newcardkeep (self, x, end = '\n'):
		inn_no = len(self.teaminnings)
		scoresheet_no = f"{self.folder}/scoresheet{inn_no}.txt"
		with open (scoresheet_no, 'a') as f:
			f.write(x)
			f.write(end)		

	def score (self, x, end = '\n'):
		self.card.append(x)
		self.cardkeep(x, end)

	def newscore (self, x, end = '\n'):
		self.newcard.append(x)
		self.newcardkeep(x, end)	

	def cardsave (self):
		try:
			f = open('{}/scorecard{}.txt'.format(self.folder, self.no))
		except:
			f = open('scorecard.txt','r')
			c = []
			for line in f: c.append(line)
			f.close()

			if self.fullcard == True: 
				y = '{}, {} v. {} at {}, {} {}\n'.format(self.raw[4],self.raw[1],self.raw[2],self.raw[3],self.raw[7],self.raw[8])
				#c.insert(0,y)
				if len (self.series.results) > 0: d = ['Series:\n']
				else: d = []
				for t in self.series.results:
					if t.win in ['Draw', 'Tie']: z = t.win
					else: z = t.win.name + ' won by ' + t.margin
					d.append('Test # {}, {}, {}, {}\n'.format(t.no, t.venue, t.dates, z))

				if len([y for y in self.players if y.games == 1]) > 0 and self.fullcard == True:
					d.append('\nDebut: ')
					for i in [y for y in self.players if y.games == 1]:
						d[-1] = d[-1] + i.name + ', '
					d[-1] = d[-1][:-2]
					d.append('\n')
			else:
				y = '{} v. {} at {} \n'.format(self.raw[1],self.raw[2],self.raw[3])
				#c.insert(0,y)
				if len (self.series.results) > 0: d = ['\nSeries:\n']
				else: d = []
				for t in self.series.results:
					if t.win in ['Draw', 'Tie']: z = t.win
					else: z = t.win.name + ' won by ' + t.margin
					d.append('Test # {}, {}, {}, {}\n'.format(t.no, t.venue, t.dates, z))

			e1 = '{}: {}'.format(self.home.name, showteam(self.home))
			e2 = '{}: {}'.format(self.away.name, showteam(self.away))

			c = [y] + d + ['\n'] + [e1] + ['\n'] + [e2] + ['\n'] + ['\n'] + c[1:]
			with open('scorecard.txt','w') as f:
				for i in c: f.write(str(i))
			shutil.copy('scorecard.txt','{}/scorecard{}.txt'.format(self.folder, self.no))
			
			

		finally:
			f.close()


		###### Ball by Ball Commentary ######
		y = self.teaminnings[0]

		if self.tosswin.name == y.team.name: toss_decision = self.tosswin.name + " will bat first."
		else: toss_decision = self.tosswin.name + " will bowl first."

		commentary_header = '{} v. {} at {} \n\n{}: {}\n{}: {}\n\n{} has won the toss, and {}\n\n\n--Day 1, 1st Session--\n{} - 1st Inning\n\n'.format(self.raw[1],self.raw[2],self.raw[3], self.home.name, showteam(self.home), self.away.name, showteam(self.away), self.tosswin.gamecapt.name, toss_decision, y.team.name)
		f = open (comm_file, "r")
		old_content = f.read()
		f.close()
		f = open (comm_file, "w")
		new_content = commentary_header + old_content
		f.write(new_content)
		f.close()
			

		### Alternate Ball by Ball Commentary####
		ALTCOMM_commentary_header = "<html><p align='center'><table width='80%' style = 'font-family: courier new, monaco, courier,arial;'><tr><td colspan='11'>{} v. {} at {} <br><br>{}: {}<br>{}: {}<br><br>{} has won the toss, and {}<br><br>--Day 1, 1st Session--<br>{} - 1st Inning</td></tr>".format(self.raw[1],self.raw[2],self.raw[3], self.home.name, showteam(self.home), self.away.name, showteam(self.away), self.tosswin.gamecapt.name, toss_decision, y.team.name)
		f = open (alt_comm_file, "r")
		ALTCOMM_old_content = f.read()
		f.close()
		f = open (alt_comm_file, "w")
		ALTCOMM_new_content = ALTCOMM_commentary_header + ALTCOMM_old_content
		f.write(ALTCOMM_new_content)
		f.close()
		



		#### MATCH VIEWER #####
		self.first_javascript_array = self.first_javascript_array + f'myArray[3] = ",,,,,,,,,,,,,,,,,,,,,,,,,,,,BEGIN MATCH,TOSS<br>{self.tosswin.gamecapt.name} has won the toss and {toss_decision},,,,"\n'
		self.first_javascript_array = self.first_javascript_array + f'myArray[4] = ",,,,,,,,,,,,,,,,,,,,,,,,,,,,BEGIN MATCH,TOSS<br>{self.tosswin.gamecapt.name} has won the toss and {toss_decision},,,,"\n'	
		f = open(matchviewer_file, "r")
		matchviewer_old_content = f.read()
		f.close()
		f = open (matchviewer_file, "w")
		matchviewer_new_content = self.first_javascript_array + matchviewer_old_content
		f.write(matchviewer_new_content)
		f.close()




		### ADDITION 7/5: Create Standalone Viewer File Directly From Python ###
		f = open("match_viewer_part1.txt", "r")
		matchviewer_part1 = f.read()
		f.close()

		
		matchviewer_part2 = f'<body><script>\n var strCommentary = "";\n	var strHomeEvents = "";\n 	var myArray = new Array();\n	var home = "{self.home.name}";\n    var homeabb = home.substr(0, 3);\n    var away = "{self.away.name}";\n    var awayabb = away.substr(0, 3);\n'

		f = open(matchviewer_file, "r")
		matchviewer_part3 = f.read()
		f.close()

		os.remove(matchviewer_file)

		f = open("match_viewer_part4.txt", "r")
		matchviewer_part4 = f.read()
		f.close()

		
		if self.home.name in ["West Indies", "England", "Australia", "India", "Pakistan", "Sri Lanka", "Bangladesh", "South Africa", "New Zealand", "Afghanistan", "Ireland", "Zimbabwe"]:
			home_logo = f"{self.home.name}.png"
			home_logo_title = f"Logo is the property of the cricket board in {self.home.name}"
		else:
			home_logo = f"home.png"
			home_logo_title = f"Free clipart"

		if self.away.name in ["West Indies", "England", "Australia", "India", "Pakistan", "Sri Lanka", "Bangladesh", "South Africa", "New Zealand", "Afghanistan", "Ireland", "Zimbabwe"]:
			away_logo = f"{self.away.name}.png"
			away_logo_title = f"Logo is the property of the cricket board in {self.away.name}"
		else:
			away_logo = f"away.png" 
			away_logo_title = f"cricket bowler by ProSymbols from the Noun Project"	
			
		matchviewer_part5 = f'document.getElementById("HomeAbb").innerHTML= "<img src=\'../assets/{home_logo}\' title=\'{home_logo_title}\' height=\'88\'>";\n			document.getElementById("HomeTeamName").innerHTML= home;\n			document.getElementById("Batsman1_name").innerHTML= "<center>" + word[15] + "</center>";\n			document.getElementById("Batsman1_Score").innerHTML= word[16];\n			document.getElementById("AwayAbb").innerHTML= "<img src=\'../assets/{away_logo}\' title=\'{away_logo_title}\' height=\'88\'>";\n			document.getElementById("AwayTeamName").innerHTML= away;\n'


		f = open("match_viewer_part6.txt", "r")
		matchviewer_part6 = f.read()
		f.close()


		f = open ("scorecards/MatchViewer.html", "w")
		matchviewer_html = matchviewer_part1 + matchviewer_part2 + matchviewer_part3 + matchviewer_part4 + matchviewer_part5 + matchviewer_part6
		f.write(matchviewer_html)
		f.close()
		
		######################################




	def gamedesc (self):
		#print ((self.home.name, 'v.', self.away.name).ljust(35), 'at', self.venue.ljust(15), "| Test #", str(self.no).ljust(4),'|', self.dates, '|', y, '| MOTM:', self.motm.name)
		print ('{} {} Test #{} {} MOTM: {}'.format(self.resultdesc.center(75), self.venue.center(20),str(self.no).ljust(4), self.dates.center(30), self.motm.name))

	def pregamestats (self):
		self.home.tests.append(self)
		self.away.tests.append(self)
		for i in self.players:
			if self.series != '' and i not in self.series.players: self.series.players.append(i)
			i.games = i.games+1
			i.end = self.year
			i.motmscore = 0
			if i in [self.home.gamecapt, self.away.gamecapt]: i.captgames.append(self)

	def motmscore (self, p):
		x = 0
		a = [x for x in self.bowls if x.player == p]
		b = [x for x in self.inns if x.player == p]
		x = x + sum([i.wickets for i in a])*self.base + sum([i.overs for i in a])*self.rpo*0.5 - sum([i.runs for i in a])

		x = x + sum([i.runs for i in b])
		if len(self.teaminnings) > 2:
			x = x + 0.5*sum([x.runs for x in self.teaminnings[2].innings if x.player == p])
			if len(self.teaminnings) == 4:
				x = x + sum([x.runs for x in self.teaminnings[3].innings if x.player == p])

		if self.win in ['Draw','Tie']: pass
		elif p in self.win.xi: x += 100

		return x

	def motmpick(self):
		a = self.players
		a.sort(key = lambda x: self.motmscore(x), reverse = True)
		self.motm = [x for x in self.players if self.motmscore(x) == max([self.motmscore(y) for y in self.players])][0]
		self.motm.motm += 1

	def stats (self):
		m = self.margin.split(" ")
		if self.win == 'Tie':
			self.cardsave ()
		elif self.win == 'Draw' and len(self.teaminnings) == 4:
			if self.teaminnings[3].wickets == 9 or self.teaminnings[3].runs >= 300: self.cardsave()
			if self.scheduledovers > 450: self.cardsave()
		elif 'run' in self.margin and 'innings' not in self.margin:
			if int(m[0]) < 6: self.cardsave ()
		elif 'wicket' in self.margin:
			if int(m[0]) == 1: self.cardsave()
			if self.teaminnings[3].runs >= 300: self.cardsave()

	def pitchdetails (self):
		return ' Pace Factor: {}, Spin Factor: {}, Outfield Speed: {}'.format("{:0.2f}".format(self.pitch[0]), "{:0.2f}".format(self.pitch[1]),"{:0.2f}".format(self.pitch[2])) 

	def pitchreport(self):
		a = ['appeared to be', 'looked to be', 'seemed', 'was', 'was described as being']

		if self.pitch[0] < 0.75: b = 'a minefield.'
		elif self.pitch[1] < 0.8: b = "a spinner's paradise."
		elif self.pitch[0] < 0.9 and self.pitch[1] < 0.9: b = 'friendly to bowlers.'
		elif all(x > 1.2 for x in self.pitch): b = 'extremely flat.'
		elif all(x > 1.1 for x in self.pitch): b = 'very flat.'
		elif all(x > 1 for x in self.pitch): b = 'somewhat flat.'
		elif self.pitch[2] < 0.9 and self.pitch[1] > 1.1 and self.pitch[0] > 1.1: b = 'dead.'
		elif self.pitch[2] < 0.9 and self.pitch[1] > 1 and self.pitch[0] > 1: b = 'slow.'
		else: b = 'fair.'

		x = 'The pitch ' + random.choice(a) + ' ' + b

		return x

	def matchreport (self):
		a = []
		a.append('Match Report:')

		if self.venue != self.home.name: a.append('At {}'.format(self.venue))
		if self.dates != '': a.append('{}.'.format(self.dates))

		if self.win not in ['Draw', 'Tie'] and self.loss.name == 'England' and 'innings' in self.margin: a.append('Well, Charles...')
		elif any(x.team.name == 'England' and x.runs < 100 and x.wickets == 10 and self.year > 1900 for x in self.teaminnings): a.append('Well, Charles...') 

		if self.tosswin == self.teaminnings[0].team: a.append('{} of {} won the toss and batted first.'.format(self.tosswin.gamecapt.name, self.tosswin.name))
		else: a.append('{} won the toss and fielded first.'.format(self.tosswin.gamecapt.name))

		if len(self.teaminnings) == 4 and self.win == self.teaminnings[1].team == self.teaminnings[2].team: a.append('The game was a classic.')

		a.append(self.pitchreport())

		if self.win == 'Draw' and self.lostovers > 90: a.append('Unfortunately, the game was spoiled by rain.')
		elif self.win == 'Draw' and self.lostovers > 30: a.append('The game was affected by rain.')
		if sum([x.runs for x in self.teaminnings]) > 1800: a.append('It was a very high-scoring game.')
		elif sum([x.runs for x in self.teaminnings]) > 1400: a.append('It was a high-scoring game.')
		elif sum([x.runs for x in self.teaminnings]) < 600 and len(self.teaminnings)>2: a.append('It was a very low-scoring game.')

		for i in self.teaminnings:
			if i == self.teaminnings[0]: x = 'In the first innings,'
			elif i == self.teaminnings[1]: x = 'In reply,'
			elif i == self.teaminnings[2]: x = 'Batting third,'
			elif i == self.teaminnings[3]: 
				y = sum([x.runs for x in self.teaminnings if x.team == i.team and x is not i])
				z = sum([x.runs for x in self.teaminnings if x.team is not i.team])
				x = 'setting a target of {}.'.format(z-y+1)
			if i.runs < 100 and i.wickets == 10 and i.test.year >= 1900: x = 'Shockingly,'
			
			if i.declare == True: y = ' declared'
			else: y = ''

			z = ['scored', 'made', 'finished with', 'scored', 'totalled']

			a.append('{} {} {} {}{} in {} overs.'.format(x, i.team.name, random.choice(z), scoreformat([i.runs, i.wickets]), y, oversballs(i)))

			b = [x for x in i.innings if x.runs >= 50 or x.runs == max([y.runs for y in i.innings])]
			a.append('{}'.format(listshow([x.report(i) for x in b])))
			c = [x for x in i.order if x.wickets >= 3]
			if len (c) > 0: a.append('{}'.format(listshow([x.report(i) for x in c], end = 'and')))

			if len(self.teaminnings) > 1 and i == self.teaminnings[1]:
				if i.runs > self.teaminnings[0].runs: a.append('meaning that {} led by {}.'.format(i.team.name, i.runs-self.teaminnings[0].runs))
				elif i.runs < self.teaminnings[0].runs: a.append('so {} trailed by {}.'.format(i.team.name, self.teaminnings[0].runs-i.runs))
				else: a.append('so the scores were level.')

			if len(self.teaminnings) > 2 and i == self.teaminnings[1] and i.team == self.teaminnings[2].team: a.append('{} were forced to follow on.'.format(i.team.name))

		if self.weather == 'Timeless' and self.win == 'Draw': a.append('The Timeless Test had to be abandoned.')

		a.append('In the end,{}.'.format(self.resultdesc))
		a.append('The man of the match was {} of {}.'.format(self.motm.name, self.motm.team))

		print ()
		for i in a: 
			if i is a[0]: 
				print (i, end = ' ')
				b = i + ' '
			elif i[-1] == '.': 
				print (i, end = ' ')
				b = b + i + ' '
			else: 
				print (i, end = ', ')
				b = b + i + ', '
		self.score("")
		self.score(b)
		print ()
		print ()


	year = 0
	daytracker = 0
	series = ''
	home = ''
	away = ''
	venue = ''
	no = 0
	dates = ''
	tosswin = ''
	choice = ''
	odi = False
	overslimit = 50

	win = ''
	loss = ''
	margin = ''
	resultdesc = ''
	motm = ''

	scorelog = ''
	inns = ''
	bowls = ''
	weather = ''
	pitch = ''

	raw = ''
	scorecard = 'scorecard.txt'
	card = []
	fullcard = False
	saveallcards = True
	bowlingchanges = False
	log = []
	teaminnings = []
	players = ''
	tobat = ''
	folder = ''
	gameovers = 450
	scheduledovers = 450
	lostovers = 0

class innings:
	def __init__(self, p, t):
		self.name = p.name
		self.player = p
		self.test = t
		self.year = t.year
		self.drops = []
		self.opposition = [x for x in [t.home, t.away] if x.name is not p.name][0]
		self.teaminnings = t.teaminnings[-1]

	def report (self, x):
		if self.balls == 0: return
		SR = self.runs/self.balls
		if self.out == True: score = str(self.runs)
		else: score = str(self.runs) + "*"

		if self.runs == max([q.runs for q in x.innings]) and self.runs < 150 and random.random() < 0.1: return '{} top scored with {}'.format(self.name, score)
		if self.runs % 100 > 90 and self.out == False and random.random() < 1/3: return '{} was stranded on {}'.format(self.name, score)

		a = []
		if self.runs > 150: a = a + ['wonderful','brilliant','fantastic','great','fine', 'Bradman-esque']
		if self.runs == 69: a = a + ['nice','good','fine']
		if SR > 0.9: a = a + ['destructive', 'frightening', 'strong', 'powerful', 'free-flowing']
		if SR > 0.75: a = a + ['hard-hitting', 'dominant', 'brisk', 'very attacking', 'fluid']
		elif SR < 0.4: a = a + ['dogged', 'determined', 'grinding', 'slow', 'tough',]

		if self.chances == 0 and self.runs >= 75: a = a + ['chanceless', 'beautiful', 'fluent']

		v = ['scored', 'made', 'finished with', 'contributed', 'scored', 'made', 'scored', 'made', 'reached']
		if SR > 1: v = v + ['slogged']
		if SR > 0.8: v = v + ['smashed', 'crunched', 'crushed', 'struck','hit']
		elif SR < 0.5: v = v + ['compiled', 'grinded to', 'battled for', 'worked for', 'managed']

		if a == []: x = '{} {} {}'.format(self.name, random.choice(v), score)
		elif SR > 1 or ((SR > 0.75 or SR < 0.4) and random.random() < 1/3): return '{} {} a {} {} from {} balls'.format(self.name, random.choice(v), random.choice(a), score, self.balls)
		
		if random.random() < 1/3 and self.out == True:
			if 'c.' in self.dismissal: howout = 'caught'
			elif 'lbw.' in self.dismissal: howout = 'LBW'
			elif 'st.' in self.dismissal: howout = 'stumped'
			elif 'run out' in self.dismissal: howout = 'run out'
			else: howout = 'bowled'

			x = '{} was {} for {}'.format(self.name, howout, score)

		if a != []: x = '{} {} a {} {}'.format(self.name, random.choice(v), random.choice(a), score)

		if self.player.games == 1 and self.test.fullcard == True and self.player.team == 'Australia' and random.random() < 1/1000: x = x + " on dayboo"
		elif self.player.games == 1 and self.test.fullcard == True and random.random() < 1/3: x = x + ' on debut'

		return x

	def form (self):
		if self.test.overcount() % 90 < 6 or self.test.teaminnings[-1].overs < 10 and 'Open' not in self.player.tag: return 0.95
		else: return 0.95 + min(0.1, self.balls/2000) + min(0.05, self.runs/1000) #- min (0, (200-self.balls)/2000)

	def stats (self):
		self.player.inns.append(self)
		self.test.inns.append(self)
		if 100 > self.runs >= 50: self.player.fifties +=1
		elif self.runs >= 100: self.player.centuries +=1
		if self.runs >= 200: self.player.doubles +=1
		if self.runs > self.player.HS or (self.runs == self.player.HS and self.player.HSNO == ' ' and self.out == False):
			self.player.HS = self.runs
			if self.out == False: self.player.HSNO = '*'
			else: self.player.HSNO = ' '
		
	def desc (self):
		if self.out == True: x = ' '
		else: x = '*'
		return '{}{} ({}) {}x4{}x6'.format(str(self.runs).rjust(3), x, str(self.balls).rjust(3), str(self.fours).rjust(2), str(self.sixes).rjust(2) )

	name = ''
	player = ''
	runs = 0
	balls = 0
	chances = 0
	fours = 0
	sixes = 0
	out = False
	drops = ''
	dismissal = ''
	FOW = ''
	scorecard = ''

	year = 0
	test = ''
	teaminnings = ''
	opposition = ''

class bowling:
	def __init__(self, p, t):
		self.name = p.name
		self.player = p
		self.test = t
		self.year = t.year
		self.teaminnings = t.teaminnings[-1]

	def bowlformat (self):
		a = oversballs(self).rjust(4)
		b = str(self.maidens).rjust(2)
		c = str(self.runs).rjust(3)
		d = str(self.wickets).rjust(2)

		return '{} - {} - {} - {}'.format(a,b,c,d)

	def report (self, x):
		z = self.name
		v = ['bowled', 'bowled', 'bowled', 'worked']
		if self.overs > 20: 
			v = v + ['worked', 'laboured']
			if 'Fast' in self.player.tag: v = v + ['ran in', 'steamed in']

		a = []
		if self.wickets > 3: a = a + ['well', 'effectively', 'smartly', 'well', 'hard']
		elif random.random() < 0.5: return '{} took {}-{}'.format(self.name, self.wickets, self.runs)
		if self.wickets >= 5: a = a + ['beautifully', 'wonderfully', 'magnificantly']
		elif self.overs >= 30: a = a + ['tirelessly', 'relentlessly', 'all day', 'without complaint', 'hard for his captain']
		if a == []: return '{} took {}-{}'.format(self.name, self.wickets, self.runs)

		b = ['taking', 'taking', 'taking', 'he took', 'finishing with', 'taking figures of', 'with figures of', 'for']

		x = '{} {} {}, {} {}-{}'.format(self.name, random.choice(v), random.choice(a), random.choice(b), self.wickets, self.runs)

		if self.player.games == 1 and self.test.fullcard == True and self.player.team == 'Australia' and random.random() < 1/1000: x = x + " on dayboo"
		elif self.player.games == 1 and self.test.fullcard == True and random.random() < 1/3: x = x + ' on debut'

		return x

	def stats (self):
		self.player.bowls.append(self)
		self.test.bowls.append(self)
		if self.wickets >=5: self.player.fives += 1
		if self.wickets > self.player.BBW or (self.wickets == self.player.BBW and self.runs < self.player.BBR):
			self.player.BBW = self.wickets
			self.player.BBR = self.runs
		if any((self.player == y.player and self.wickets + y.wickets >= 10 and self is not y) for y in self.test.bowls): self.player.tens +=1
		

	name = ''
	player = ''
	opposition = ''
	overs = 0
	balls = 0
	maidens = 0
	runs = 0
	wickets = 0
	chances = 0
	spell = 0
	year = 0
	test = ''
	teaminnings = ''

class team:
	def __init__(self):
		self.players, self.active, self.squad, self.xi, self.lastxi, self.tests = [], [], [], [], [], []

	name = ''
	players = []
	active = []
	squad = []
	unav = ''
	captain = ''
	xi = []
	lastxi = []
	lastcapt = ''
	gamecapt = ''
	wk = ''
	inj = ''
	tests = []
	rating = 0

class player:
	def overcount (self):
		self.overs = self.ballsbowled//6
		self.ballsbowled = self.ballsbowled%6

	def stats (self, test):
		self.inns = list(dict.fromkeys(self.inns))
		self.bowls = list(dict.fromkeys(self.bowls))

		self.runs = sum([x.runs for x in self.inns])
		self.outs = sum([x.out for x in self.inns])
		self.balls = sum([x.balls for x in self.inns])
		if self.outs > 0: self.batav = round(self.runs/self.outs, 2)
		else: self.batav = self.runs
		if self.balls > 0: self.batsr = round(100*self.runs/self.balls,1)

		self.ballsbowled = 6*sum([x.overs for x in self.bowls]) + sum([x.balls for x in self.bowls])
		self.wickets = sum([x.wickets for x in self.bowls])
		self.bowlruns = sum([x.runs for x in self.bowls])
		self.maidens = sum([x.maidens for x in self.bowls])

		if self.wickets > 0:
			self.bowlav = round(self.bowlruns/self.wickets, 2)
			self.bowlsr = round(self.ballsbowled/self.wickets, 1)
		if self.ballsbowled > 0:
			self.bowler = round(self.bowlruns/(self.ballsbowled/6), 2)
			if self.ballsbowled % 6 == 0: self.overs = str(self.ballsbowled/6)
			else: self.overs = '{}.{}'.format(self.ballsbowled//6, self.ballsbowled % 6)

	def batdesc (self, current):
		if self.end+1 < current: y = '{}-{}'.format(self.debut, self.end)
		else: y = '{}-    '.format(self.debut)
		return 'Age{} {} {} Tests {} runs @{} SR{}{}x200{}x100{}x50 HS {}{}{}ct{}st Rating{}'.format(str(current-self.dob).rjust(3), y, str(self.games).rjust(3), str(self.runs).rjust(5), "{:0.2f}".format(self.batav).rjust(6), "{:0.1f}".format(self.batsr).rjust(5), str(self.doubles).rjust(2), str(self.centuries).rjust(3), str(self.fifties).rjust(3), str(self.HS).rjust(3),self.HSNO, str(self.catches).rjust(3), str(self.stumpings).rjust(2), "{:0.2f}".format(self.batform).rjust(6))

	def bowldesc (self, current):
		if self.BBR == float('inf'): BB = '-'.center(6)
		else: BB = str(self.BBW).rjust(2) + '-' + str(self.BBR).ljust(3)

		if self.end == 9999: y = '         '
		elif self.end+1 < current: y = '{}-{}'.format(self.debut, self.end)
		else: y = '{}-    '.format(self.debut)
		return ('Age{} {} {} Tests {} wickets @{} {} overs {}x5w {}x10w BB{} SR{} ER {} Rating {}'.format(str(current-self.dob).rjust(3), y, str(self.games).rjust(3), str(self.wickets).rjust(3), "{:0.2f}".format(self.bowlav).rjust(6), str(self.overs).rjust(6), str(self.fives).rjust(2), str(self.tens).rjust(2), BB, "{:0.1f}".format(self.bowlsr).rjust(5), "{:0.2f}".format(self.bowler).rjust(4), "{:0.2f}".format(self.bowlform).rjust(6)))

	def shortbowldesc (self):
		if self.BBR == float('inf'): BB = '-'.center(6)
		else: BB = str(self.BBW).rjust(2) + '-' + str(self.BBR).ljust(3)
		return ('{} wickets @{} {}x5w {}x10w BB{} SR{} ER {} Rating{}'.format(str(self.wickets).rjust(3), "{:0.2f}".format(self.bowlav).rjust(6), str(self.fives).rjust(2), str(self.tens).rjust(2), BB, "{:0.1f}".format(self.bowlsr).rjust(5), "{:0.2f}".format(self.bowler).rjust(4), "{:0.2f}".format(self.bowlform).rjust(6)))

	def statscsv (self):
		'Name, Team, Debut, Last, Tests, Inns, NO, Runs, BF, Bat. Av., Bat. SR, 200s, 100s, 50s, HS, , Balls, Maidens, Runs, Wickets, Bowl. Av, Bowl. ER, Bowl. SR, 5xW, 10xW, Best, Bowling, Catches, Stumpings, Captained, MOTM'
		x = [self.name, self.team, self.debut, self.end, self.games]
		x.append(len([y for y in self.inns if y.balls > 0]))
		x.append(len([y for y in self.inns if y.out == False]))
		x = x + [self.runs, self.balls, self.batav, self.batsr, self.doubles, self.centuries, self.fifties, self.HS, self.HSNO]
		x = x + [self.ballsbowled, self.maidens, self.bowlruns, self.wickets, self.bowlav, self.bowler, self.bowlsr, self.fives, self.tens, self.BBR, '-', self.BBW]
		x = x + [self.catches, self.stumpings, self.motm]
		x.append(len(self.captgames))
		x.append(len([y for y in self.captgames if isinstance(y.win, team) and y.win.name == self.team]))
		x.append(len([y for y in self.captgames if isinstance(y.loss, team)and y.loss.name == self.team]))
		#print (x)
		return x


	name = ''
	team = ''
	secondteam = ''
	status = ''
	basebat = 0
	basebowl = 500
	bat = 0
	bowl = 500
	batform = 25
	bowlform = 0
	tag = ''
	dob = 0
	first = 0
	last = 0
	age = 0
	debut = ''.center(4)
	end = 9999
	dropdate = 0
	realfirst = 0
	reallast = 0
	sr = 0
	er = 0
	capt = 0
	mod = 1

	inns = []
	bowls = []
	games = 0
	captgames = []
	motm = 0

	runs = 0
	balls = 0
	outs = 0
	batav = 0
	batsr = 0
	fifties = 0
	centuries = 0
	doubles = 0
	HS = 0
	HSNO = ' '

	ballsbowled = 0
	overs = 0
	maidens = 0
	bowlruns = 0
	wickets = 0
	bowlav = float('inf')
	bowler = float('inf')
	bowlsr = float('inf')
	fives = 0
	tens = 0
	BBR = float('inf')
	BBW = 0

	catches = 0
	stumpings = 0
	innings = ''
	bowling = ''
	motmscore = 0

if __name__ == "__main__":
	pass
