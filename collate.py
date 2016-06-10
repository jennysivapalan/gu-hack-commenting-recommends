import urllib2
import json
import time
import sys


class Collate:
	def fetch(self, id, apiKey):
			url = "https://discussion.theguardian.com/discussion-api/profile/"+id+"/comments"
			groups = []
			try:
				response = urllib2.urlopen(url)
				data = response.read()
				jsonResp = json.loads(data, "utf-8")
				userName = jsonResp.get('userProfile', {}).get('displayName', '')

				comments = jsonResp.get('comments', {})
				for comment in comments:
					contentKey = comment.get('discussion', {}).get('key', '')
					capSection = self.capSection(contentKey, apiKey)
					
					numRecommends = comment.get('numRecommends', '')
					
					group = Group(capSection, numRecommends)
					groups.append(group)
				
				sortedGroup = sorted(groups, key=lambda group: group.numRecommends, reverse=True)
				
				mostRecGroup = filter(lambda group: group.numRecommends > 20, sortedGroup)
				
				print id + " username: " + userName + " has good reputation in the following sections:"
				for g in mostRecGroup:
					print g.section + " (number of recommends:" + str(g.numRecommends) + ")"

			except urllib2.HTTPError, e:
				print id + ":" + str(e.code)

	def capSection(self, id, apiKey):
			url = "http://content.guardianapis.com"+id+"?api-key="+apiKey+"&show-tags=true"
			try:
				response = urllib2.urlopen(url)
				data = response.read()
				responseJson = json.loads(data, "utf-8").get('response', {})
				section = responseJson.get('content', {}).get('sectionId', '')
				return section
			except urllib2.HTTPError, e:
				print id + ":" + str(e.code)

class Group:
	def __init__(self, section, numRecommends):
		self.section = section
		self.numRecommends = numRecommends
 

profileId = sys.argv[1] 
apiKey =  sys.argv[2] 			
foo = Collate()	
foo.fetch(profileId, apiKey)
