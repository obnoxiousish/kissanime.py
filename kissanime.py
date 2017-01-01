import cfscrape
import argparse
import re
import sys
import subprocess

"""
authored by ob,
due to kissanime having a constant im under attack mode on this
will take awhile to work

creds: anorov for cfscrape

usage: C:\kissanime.py>kissanime.py obbyasf cocksinmyass http://kissanime.ru/Anime/Black-Bullet/Special-001?id=110715 -q 1080p
"""

parser = argparse.ArgumentParser(description='kissanime script')
parser.add_argument('username', help='username for kissanime, mandatory')
parser.add_argument('password', help='password for kissanime, mandatory')
parser.add_argument('url', help='url for anime, mandatory')
parser.add_argument('-q', '--quality', help='quality for anime, mandatory [360p, 480p, 720p, 1080p]', default='720p')
parser.add_argument('-P', '--player', help='player to pipe to, mandatory', default='mpv')
args = parser.parse_args()

class main():
	def __init__(self):
		self.args = args
		self.session = cfscrape.create_scraper()
		
		if 'http://kissanime.ru/Login' in self.login().url:
			print('[-] USERNAME OR PASSWORD INCORRECT')
		else:
			print('[+] LOGIN SUCCESSFUL')
		
		try:
			self.scrape()
		except:
			print('[-] ERROR PARSING ANIME URLS')
			sys.exit(0)

		print('[+] FOUND %d ANIME URLS'%(len(self.parsedURLs)))

		try:
			self.player()
		except:
			print('[-] FAILED TO PIPE')
			sys.exit(0)

		print('[+] LAUNCHED PIPED PLAYER')

	def player(self):
		self.subprocess = subprocess.Popen([self.args.player, self.parsedURLs[self.args.quality]])

	def scrape(self):
		self.parsedURLs = {}
		self.qualities = ['1080p', '720p', '480p', '360p']
		self.scrapeData =self.session.get(
			self.args.url
			)
		self.videoURLs = self.scrapeData.text.split('(Save link as...):')[1].split('</div>')[0].split(' - ')
		for url in range(len(self.videoURLs)):
			parsing = self.videoURLs[url].split('href="')[1].split('"')[0]
			self.parsedURLs[self.qualities[url]] = parsing
		
	def login(self):
		self.loginRequest = self.session.post(
			'http://kissanime.ru/Login',
				data={
					'username': self.args.username,
					'password': self.args.password,
			}
		)
		return self.loginRequest
		
if __name__ == "__main__":
	main()