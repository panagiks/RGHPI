#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""Generate index.html to change GH preview Image"""
import json
from urllib2 import urlopen
from bs4 import BeautifulSoup
import argparse

class Handler(object):
    """docstring for Handler."""
    def __init__(self, interactive):
        self.interactive = interactive

    def start(self):
        if self.interactive:
            gh_url = raw_input("Repo's URL: ")
            img_url = raw_input("Preview image URL: ")
        else:
            with open('config.json','r') as json_config:
                settings = json.load(json_config)
            gh_url = settings["repo_url"]
            img_url = settings["image_url"]
        #Split URL at all "/"
        gh_ar = gh_url.split("/")
        #Get rid of empty slots
        gh_ar = [x for x in gh_ar if x is not '']
        repo = gh_ar[-1]
        name = gh_ar[-2]
        name_repo = ("%s/%s"%(name, repo))
        final_url = ("https://%s.github.io/%s/" % (name, repo))
        base_url = ("github.com/%s/%s" % (name, repo))
        rdr_url = ("https://%s" % base_url)
        gh_repo = urlopen(rdr_url)
        soup = BeautifulSoup(gh_repo, "lxml")
        title = soup.title.string
        git_url = ("%s.git" % rdr_url)
        with open('sample.html','r') as smpl:
            sample = smpl.read()
        result = (sample % (title, img_url, name_repo, title, img_url,
                            name_repo, final_url, title, title, base_url,
                            git_url, rdr_url))
        with open('index.html','w') as indx:
            indx.write(result)


def main():
    parser = argparse.ArgumentParser(description='Automate html generation in order to change GitHub repo preview image.')
    parser.add_argument("--interactive", action='store_true', help="Trigger interactive console mode.")
    args = parser.parse_args()
    handler = Handler(args.interactive)
    handler.start()


if __name__ == '__main__':
    main()
