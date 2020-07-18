#!/usr/bin/python
from bot_class import Bot
import requests, re
import json
import discord
import random

class LyricsBot(Bot):
    lyrics = {}
    lyrics_words = {}
    song_names = {}

    async def on_ready(self):
        self.load()
        await super().on_ready()

    async def on_message(self, msg):
        await super().on_message(msg)
        if msg.author != self.user and not msg.content.startswith(self.prefix):
            words = [s.lower() for s in [s.replace(' ', '') for s in re.split('\;|\,|\.|\-|\*|\?|\!|\'|\"|\„|\“|\(|\)|\s', msg.content) if s not in ' ']]
            line = ''
            for artist in self.lyrics_words:
                for song in self.lyrics_words[artist]:
                    for i in range(len(self.lyrics_words[artist][song])):
                        word_count = 0
                        for word in words:
                            if word in self.lyrics_words[artist][song][i]:
                                word_count += 1
                        if word_count / len(self.lyrics_words[artist][song][i]) > 0.5:
                            line = self.lyrics[artist][song][i+1]
                            print(words)
                            print(line)
            if line != '':
                await msg.channel.send(line)

    @Bot.command
    async def add(self, command, args, msg):
        if args[0] == 'song':
            title = args[1]
            if args[2] == 'artist':
                artist = args[3]
                success = await self.scraper(artist, title, msg)
                if success:
                    self.save()
                    await msg.channel.send('The song was added successfully.')
            else:
                await msg.channel.send('You have to specify an artist.')
                await self.usage_song(msg)
        if args[0] == 'artist':
            await self.get_all_songs(args[1], msg)

    @Bot.command
    async def list(self, command, args, msg):
        if args[0] == 'songs':
            for artist in self.song_names:
                songs = ''
                for s in self.song_names[artist]:
                    songs += '" ' + str(s) + ' "\n'
                hex_digits = '0123456789ABCDEF'
                await msg.channel.send(embed=discord.Embed(title=artist, description=songs, color=int(''.join(random.choice(hex_digits) for _ in range(6)), 16)))


    def load(self):
        with open(self.path('lyrics.txt'), 'r') as file:
            content = file.read()
            if len(content) > 0:
                self.lyrics = json.loads(content)[0]
                self.song_names = json.loads(content)[1]
            else:
                self.lyrics = {}
                self.song_names = {}
        print(self.lyrics)
        if len(self.lyrics) > 0:
            for artist in self.lyrics:
                try:
                    if len(self.lyrics_words[artist]) == 0:
                        self.lyrics_words.update({artist:{}})
                except KeyError:
                    self.lyrics_words.update({artist:{}})
                for song in self.lyrics[artist]:
                    self.lyrics_words[artist].update({song: [_ for _ in range(len(self.lyrics[artist][song]))]})
                    for i in range(len(self.lyrics[artist][song])):
                        self.lyrics_words[artist][song][i] = [s.lower() for s in [a.replace(' ', '') for a in re.split('\;|\,|\.|\-|\*|\?|\'|\"|\„|\“|\!|\(|\)|\s', self.lyrics[artist][song][i]) if a not in ' ']]
        print(self.lyrics_words)
        print(self.song_names)

    def save(self):
        with open(self.path('lyrics.txt'), 'w') as file:
            file.write(json.dumps((self.lyrics, self.song_names)))

    async def song_not_found(self, msg):
        await msg.channel.send('The song you wanted to add does not exist. (wrong artist/ song name)')

    async def usage_song(self, msg):
        await msg.channel.send('Usage: .add song <song name> artist <artist name>')

    async def get_all_songs(self, artist, msg):
        url = 'https://genius.com/artists/' + artist.replace(' ', '-')

        r = requests.request('get', url)

        artist_id = re.findall('\<meta\scontent\=\"\/artists\/(\d*)\"\sname\=\"newrelic\-resource\-path\"\s\/\>', r.text)[0]
        base_url_song_list = 'https://genius.com/artists/songs?for_artist_page=' + artist_id + '&page='

        i = 1
        song_urls = []
        while True:
            r = requests.request('get', base_url_song_list + str(i))
            links = re.findall('https\:\/\/genius\.com\/[\S]*\-lyrics', r.text)
            song_urls.extend(links)

            if len(links) == 0:
                break

            i += 1

        for url in song_urls:
            await self.scrape_by_url(artist, url, msg)
        print(len(song_urls))
        print(self.song_names)


    async def scrape_by_url(self, artist, url, msg):
        return await self.scraper(url[19:-len(url)+19+len(artist)], url[20+len(artist):-7], msg)

    async def scraper(self, artist, title, msg):
        url = 'https://genius.com/' + artist.replace(' ', '-') + '-' + title + '-lyrics'

        artist_full = ''
        title_full = ''

        r = requests.request('get', url)

        artist_full = re.findall('\<title\>([\S\s]*)\sLyrics\s\|\sGenius\sLyrics\<\/title\>', r.text)[0].split(' – ')[0]
        title_full = re.findall('\<title\>([\S\s]*)\sLyrics\s\|\sGenius\sLyrics\<\/title\>', r.text)[0].split(' – ')[1]

        reg = re.findall('\<\!\-\-sse\-\-\>([\S\s]*)\<\!\-\-\/sse\-\-\>', re.findall('\<\!\-\-sse\-\-\>([\S\s]*\<\!\-\-\/sse\-\-\>)', r.text)[0])
        if len(reg) == 0:
            await self.song_not_found(msg)
            return False

        try:
            if not self.song_names[artist_full]:
                self.song_names[artist_full] = []
        except KeyError:
            self.song_names[artist_full] = []

        if not title_full in self.song_names[artist_full]:
            self.song_names[artist_full].append(title_full)

        lines = reg[0].split('\n')
        lines2 = []
        del_line = False
        for l in lines:
            new_l = ''
            go_on = True
            is_closed = False
            if del_line:
                go_on = False
            for c in l:
                if c == '<' or c == '[':
                    go_on = False
                    is_closed = False
                if go_on:
                    new_l += c
                if c == '>' or c == ']':
                    go_on = True
                    is_closed = True
            if not is_closed:
                del_line = True
            else:
                del_line = False
            new_l.replace(' ', '')
            new_l.replace('\t', '')
            if len(new_l) > 0 and '[' not in new_l and ']' not in new_l and '<' not in new_l and '>' not in new_l:
                lines2.append(new_l)
        self.lyrics[artist.lower()] = {}
        self.lyrics[artist.lower()][title] = lines2
        self.lyrics_words[artist.lower()] = {}
        self.lyrics_words[artist.lower()][title] = [re.split('\;|\,|\.|\-|\*|\"|\„|\“|\'|\?|\!|\(|\)|\s', line) for line in [s.replace(' ', '') for s in [s.lower() for s in lines2] if s not in ' ']]
        return True

if __name__ == '__main__':
    lyrics_bot = LyricsBot('urff_bot', '$')
    lyrics_bot.run(lyrics_bot.get_token())
