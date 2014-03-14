#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import webapp2, jinja2, os, random, csv

jinja_environment = jinja2.Environment(autoescape = True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')))

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		page = jinja_environment.get_template('index.html')
		template_values ={}
		template = page.render(template_values)
		self.response.out.write(template)

	def post(self):
		start = int(self.request.get('start'))
		end = int(self.request.get('end'))
		number = int(self.request.get('number'))
		randos = self.build_list(start, end, number)
		self.write_to_csv(randos)
		self.response.out.write(randos)


	def build_list(self, start, end, number):
		randos = random.sample([x for x in range(start, end+1)],  number)
		return randos

	def write_to_csv(self, randos):
		self.response.headers['Content-Type'] = 'application/csv'
		self.response.headers['Content-Disposition'] = 'attachment; filename=random_numbers.csv'
		c = csv.writer(self.response.out)
		c.writerow(["Numbers"])
		for x in randos:
			c.writerow([x])
			
		self.response.out.write(c)
			
			
			

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)