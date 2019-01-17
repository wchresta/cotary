# Copyright (C) 2019 Wanja Chresta
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Publish a given checksum to Twitter.
"""
import twitter
from twitter.error import TwitterError

import cotary.checksum

class PublisherError(Exception):
    pass

class Publisher(object):
    def __init__(self, config):
        self.consumer_key = config["twitter.consumer.key"]
        self.consumer_secret = config["twitter.consumer.secret"]
        self.access_token_key = config["twitter.access_token.key"]
        self.access_token_secret = config["twitter.access_token.secret"]

        self.message = config["twitter.message"]

        self.api = None
        if self.is_configured():
            self.setup_api()

    def is_configured(self):
        return (self.consumer_key
                and self.consumer_secret
                and self.access_token_key
                and self.access_token_secret)

    def setup_api(self):
        self.api = twitter.Api(consumer_key=self.consumer_key,
                               consumer_secret=self.consumer_secret,
                               access_token_key=self.access_token_key,
                               access_token_secret=self.access_token_secret)

    def is_checksum(self, cs):
        return isinstance(cs, checksum.Checksum)

    def publish(self, cs):
        if not self.api:
            raise PublisherError("API is not configured. Check the config file")

        if self.is_checksum(cs):
            return self.api.PostUpdate(self.message.format(checksum=cs))
        else:
            raise PublisherError("{} is not a checksum".format(cs))

if __name__=="__main__":
    import cotary.config
    config = cotary.config.Config()

    content = b"Hello World!"
    checksum = cotary.checksum.Checksum([content])

    publisher = Publisher(config)
    status = publisher.publish(checksum)

    import datetime
    publish_datetime = datetime.datetime.fromtimestamp(status.created_at_in_seconds)
    print("Status published at", publish_datetime)

