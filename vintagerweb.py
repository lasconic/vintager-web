#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import json

from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True)
# [END imports]


# [START symbol]
class Label(ndb.Model):
    """Sub model for representing an author."""
    name = ndb.StringProperty(indexed=True)
    probability = ndb.FloatProperty(indexed=True)
    voteYes = ndb.IntegerProperty(default=0)
    voteNo = ndb.IntegerProperty(default=0)
    voteCount = ndb.IntegerProperty(default=0)


class Symbol(ndb.Model):
    """A main model for representing an individual Symbol."""
    name = ndb.StringProperty(indexed=True)
    image = ndb.TextProperty(indexed=False)
    insert_date = ndb.DateTimeProperty(auto_now_add=True)
    update_date = ndb.DateTimeProperty(auto_now=True)
    algorithm = ndb.StringProperty(indexed=True)
    labels = ndb.StructuredProperty(Label, repeated=True)

    def toJson(self):
        sdict = self.to_dict()
        sdict["key"] = self.key.urlsafe()
        sdict["insert_date"] = sdict["insert_date"].isoformat()
        sdict["update_date"] = sdict["update_date"].isoformat()
        return json.dumps(sdict)
# [END symbol]


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]


# [START Confirmation]
class Confirmation(webapp2.RequestHandler):

    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('confirmation.html')
        self.response.write(template.render(template_values))
# [END Confirmation]


# [START symbollist]
class SymbolListRequest(webapp2.RequestHandler):

    def get(self):
        page = self.request.get("page", '')
# [END symbollist]


# [START symbol]
class SymbolRequest(webapp2.RequestHandler):

    def get(self):
        name = self.request.get('name', '')
        key = self.request.get('key', '')
        if key:
            s_key = ndb.Key(urlsafe=key)
            s = s_key.get()
            result = ''
            if s:
                result = s.toJson()
            self.response.out.write(result)
        elif name:
            query = Symbol.query(Symbol.name == name)
            s = query.get()
            if s:
                result = s.toJson()
            self.response.out.write(result)
        else:
            query = Symbol.query().order(Symbol.update_date)
            s = query.get(use_cache=False, use_memcache=False)
            result = ""
            if s:
                print s.name
                print s.update_date.isoformat()
                result = s.toJson()
            self.response.out.write(result)

    def put(self):
        js = self.request.body
        s = json.loads(js)
        symbol = Symbol()
        symbol.name = s["name"]
        symbol.image = s["image"]
        symbol.algorithm = s["algorithm"]
        labels = []
        for l in s["labels"]:
            label = Label()
            label.name = l["name"]
            label.probability = float(l["probability"])
            labels.append(label)
        symbol.labels = labels
        key = symbol.put()
        rDict = dict()
        rDict["key"] = key.urlsafe()
        self.response.out.write(json.dumps(rDict))

    def post(self):
        key = self.request.get('key', '')
        yes = self.request.get('yes', '')
        no = self.request.get('no', '')
        label = self.request.get('label', '')
        if not key or not label:
            #return error
            self.response.set_status(500)
            return
        else:
            s_key = ndb.Key(urlsafe=key)
            s = s_key.get()
            matching = [lbl for lbl in s.labels if lbl.name == label]
            if s and len(matching) == 1:
                mLabel = matching[0]
                if yes:
                    mLabel.voteYes = mLabel.voteYes + 1
                elif no:
                    mLabel.voteNo = mLabel.voteNo + 1
                else:
                    mLabel.voteCount = mLabel.voteCount + 1
                s.put()
                s = s_key.get()
                s.put()
                rDict = dict()
                rDict["key"] = key
                self.response.out.write(json.dumps(rDict))
            else:
                self.response.set_status(500)

    def delete(self):
        key = self.request.get('key', '')
        if key:
            s_key = ndb.Key(urlsafe=key)
            s_key.delete()
# [END symbol]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/symbol', SymbolRequest),
    ('/symbols', SymbolListRequest),
    ('/confirmation', Confirmation)
], debug=True)
# [END app]
