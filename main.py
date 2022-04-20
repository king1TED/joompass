import requests
import xml.etree.ElementTree as ET
from colorama import Fore

class joomla_fuzz():
	def __init__(self):
		self.scan_type = {'0':[200],
'1':[200,403],
'2':[200,403,401]}
		self.url = input('enter your joomla web url (example : http://example.com/joomla_path/ ): --->')
		for i in self.scan_type:
			print(i,'---->',self.scan_type[i])
		self.statuslist = input('select your status list : --->')
		self.words = open('joomla.txt','r').read().split("\n")
		self.check_function = lambda target,word:requests.get(target+word).status_code

	def get_version(self,query):
		v = requests.get(query)
		xml = ET.fromstring(v.content)
		for c in xml:
			if c.tag == 'version':
				version = c.text
				break
		return version

	def main(self):
		for i in self.words:
			result = self.check_function(self.url,i)
			if result in self.scan_type[self.statuslist]:
				if result == 200:
					if 'components' in i :
						name = i.split('com_')[1][:-1]
						version = self.get_version(f'{self.url}administrator/{i+name}.xml')
						print(f'{self.url+i} status is '+Fore.GREEN + str(result) + Fore.RESET,f' and version is : {Fore.BLUE + version + Fore.RESET}')
					elif 'modules' in i:
						name = i.split('mod_')[1][:-1]
						version = self.get_version(self.url+'modules/mod_'+name+f'/mod_{name}.xml')
						print(f'{self.url+i} status is {Fore.GREEN + str(result) + Fore.RESET} and version is : {Fore.BLUE + version + Fore.RESET}')
					# elif 'plugins/' in i:
					# 	psplit = i.split('/')
					# 	name = psplit[2]
					# 	ptype = psplit[1]
					# 	version = self.get_version()
					elif 'templates/' in i:
						name = i.split('/')[1]
						version = self.get_version(self.url+'templates/'+name+'/'+'templateDetails.xml')
						print(f'{self.url+i} status is {Fore.GREEN + str(result) + Fore.RESET} and version is : {Fore.BLUE + version + Fore.RESET}')
					else:
						print(f'{self.url+i} status is '+Fore.GREEN + str(result) + Fore.RESET)

				else:
					print(f'{self.url+i} status is '+Fore.GREEN + str(result) + Fore.RESET)
				
		return





if __name__ == "__main__":
	joomla = joomla_fuzz()
	joomla.main()