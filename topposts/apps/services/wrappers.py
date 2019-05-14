# coding: utf-8

import logging
import re

from django.conf import settings
from django.utils import timezone

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class AbstractBaseClient:
    def __init__(self):
        self.headers = {'user-agent': 'woid/1.0'}


class HackerNewsClient(AbstractBaseClient):
    base_url = 'https://hacker-news.firebaseio.com'

    def request(self, endpoint):
        r = requests.get(endpoint, headers=self.headers)
        result = r.json()
        return result

    def get_top_stories(self):
        endpoint = '%s/v0/topstories.json' % self.base_url
        return self.request(endpoint)

    def get_story(self, code):
        endpoint = '%s/v0/item/%s.json' % (self.base_url, code)
        return self.request(endpoint)

    def get_max_item(self):
        endpoint = '%s/v0/maxitem.json' % self.base_url
        return self.request(endpoint)


class RedditClient(AbstractBaseClient):

    def get_front_page_stories(self):
        stories = list()

        try:
            r = requests.get('https://www.reddit.com/.json',
                             headers=self.headers)
            result = r.json()
            stories = result['data']['children']
        except ValueError:
            logger.exception(
                'An error occurred while executing RedditClient.get_front_page_stories')

        return stories


class GithubClient(AbstractBaseClient):

    def get_today_trending_repositories(self):
        r = requests.get(
            'https://github.com/trending?since=daily', headers=self.headers)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        repos = soup.select('ol.repo-list li')
        data = list()
        for repo in repos:
            repo_data = dict()
            repo_data['name'] = repo.h3.a.get('href')
            if repo.p:
                description = repo.p.text
                if description:
                    description = description.strip()
                else:
                    description = ''
                repo_data['description'] = description

            lang = repo.find(attrs={'itemprop': 'programmingLanguage'})
            if lang:
                repo_data['language'] = lang.text.strip()
            else:
                repo_data['language'] = ''

            stars_text = repo.findAll(text=re.compile('stars today'))
            stars_numbers_only = re.findall(r'\d+', stars_text[0])
            repo_data['stars'] = int(stars_numbers_only[0])

            data.append(repo_data)

        return data
