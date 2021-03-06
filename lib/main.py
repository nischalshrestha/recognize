#!/usr/bin/python2.4
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line example for Custom Search.

Command-line application that does a search.
"""

__author__ = 'jcgregorio@google.com (Joe Gregorio)'

import pprint
import json
import urllib2

from apiclient.discovery import build

def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey="AIzaSyAN3l_irEsAG2kT3isRzL8R-baMkOcZgZs")

  num = 4
  res = service.cse().list(
      q='cat',
      cx='008947772147471846402:fdhywbjbitw',
      # num=num,
      searchType="image",
      imgColorType='color',
      siteSearchFilter='e',
      siteSearch='https://pixabay.com', # Sites like these don't allow URLs on external sites
      # imgSize='medium', #Let's not restrict size for now
      imgType='photo',
      safe='high',
      rights='cc_publicdomain',
      filter='1'
      ).execute()
  parsed_res = json.dumps(res)
  json_res = json.loads(parsed_res)
  # image_url = json_res['items'][0]['pagemap']['cse_image'][0]['src']
  # for i in range(num):
  # image_url = json_res['items'][0]['link']
  pprint.pprint(json_res['items'])

  # try:
  #   img_file = urllib2.urlopen(image_url)
  #   pprint.pprint(result.read())
  # except urllib2.URLError, e:
  #   handleError(e)
    # pprint.pprint(image_url)

if __name__ == '__main__':
  main()
