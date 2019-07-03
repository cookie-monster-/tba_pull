import time
import tbapy
import csv

tba = tbapy.TBA('gtVK43e2dXPoDOOvQnCmHQqxbbGRZOKcXcU5qzOVJONwOjHiiTHF3IQ2gmPsIdct')
eventKey = "2019iri"
eTeams = [33,48,51,88,107,111,118,195,217,225,234,319,330,340,364,461,548,868,910,930,1023,1024,1073,1114,1241,1410,1676,1684,1690,1718,1720,1730,1747,1807,1923,2056,2075,2168,2200,2337,2403,2468,2481,2614,2767,2910,3357,3478,3538,3604,3641,3707,3847,3940,4028,4265,4362,4607,4776,5190,5205,5406,5460,5511,5801,6443,7457,7498]
#eTeams = tba.event_teams(eventKey,keys=True)
filename = "Scout_"+eventKey+'.csv'
#print(eTeams)
with open(filename, 'w', newline='') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',')
	spamwriter.writerow(['team','rockets','qualRockets','lvlOneClimbs','lvlTwoClimbs','lvlThreeClimbs','lvlOneStarts','lvlTwoStarts','totalMatches','multiClimbs'])
	for teamx in eTeams:
		team = "frc" + str(teamx)
		teamMatches = tba.team_matches(team, year=2019)#event=eventKey)
		oneClimbs = 0
		twoClimbs = 0
		threeClimbs = 0
		teamMultiClimbs = []
		climbPts = 0
		rockets = 0
		qualRockets = 0
		oneStarts = 0
		twoStarts = 0
		matchesPlayed = 0
		if len(teamMatches) > 0:
			print(team)
			for match in teamMatches:
				
				if match['score_breakdown'] != None:
					matchesPlayed += 1
					alliance = 'yellow'
					robotNum = 0

					if team in match['alliances']['blue']['team_keys']:
						alliance = 'blue'
					else:
						alliance = 'red'

					if team == match['alliances'][alliance]['team_keys'][0]:
						robotNum = 1
					if team == match['alliances'][alliance]['team_keys'][1]:
						robotNum = 2
					if team == match['alliances'][alliance]['team_keys'][2]:
						robotNum = 3

					teamClimb = match['score_breakdown'][alliance]['endgameRobot'+str(robotNum)]
					if match['score_breakdown'][alliance]['completedRocketFar']:
						rockets+=1
						if match['comp_level'] == 'qm':
							qualRockets += 1
					if match['score_breakdown'][alliance]['completedRocketNear']:
						rockets+=1
						if match['comp_level'] == 'qm':
							qualRockets += 1

					if match['score_breakdown'][alliance]['habLineRobot'+str(robotNum)] == "CrossedHabLineInSandstorm":
						if match['score_breakdown'][alliance]['preMatchLevelRobot'+str(robotNum)] == "HabLevel2":
							twoStarts += 1
						else:
							oneStarts += 1
					
					if teamClimb == "HabLevel1":
						oneClimbs += 1
						climbPts += 3
					elif teamClimb == "HabLevel2":
						twoClimbs += 1
						climbPts += 6
					elif teamClimb == "HabLevel3":
						climb1 = match['score_breakdown'][alliance]['endgameRobot1']
						climb2 = match['score_breakdown'][alliance]['endgameRobot2']
						climb3 = match['score_breakdown'][alliance]['endgameRobot3']
						multiClimbs = 0
						if climb1 == "HabLevel3":
							multiClimbs += 1
						if climb2 == "HabLevel3":
							multiClimbs += 1
						if climb3 == "HabLevel3":
							multiClimbs += 1
						if multiClimbs > 1:
							teamMultiClimbs.append("https://www.thebluealliance.com/match/"+match['key'])
						threeClimbs += 1
						climbPts += 12
		toWrite = [team,rockets,qualRockets,oneClimbs,twoClimbs,threeClimbs,oneStarts,twoStarts,matchesPlayed,len(teamMultiClimbs)]
		for m in teamMultiClimbs:
			toWrite.append(m)
		spamwriter.writerow(toWrite)
		