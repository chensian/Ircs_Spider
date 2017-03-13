# encoding=utf-8
import base64
import csv
import random

from os.path import dirname

from spidersina.entity.cookies import cookies
from spidersina.entity.user_agents import agents


class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent

