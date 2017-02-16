###############################################################################
##
##  Copyright (C) 2014, Tavendo GmbH and/or collaborators. All rights reserved.
##
##  Redistribution and use in source and binary forms, with or without
##  modification, are permitted provided that the following conditions are met:
##
##  1. Redistributions of source code must retain the above copyright notice,
##     this list of conditions and the following disclaimer.
##
##  2. Redistributions in binary form must reproduce the above copyright notice,
##     this list of conditions and the following disclaimer in the documentation
##     and/or other materials provided with the distribution.
##
##  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
##  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
##  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
##  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
##  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
##  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
##  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
##  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
##  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
##  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
##  POSSIBILITY OF SUCH DAMAGE.
##
###############################################################################

from twisted.internet.defer import inlineCallbacks

from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession



class appBackend(ApplicationSession):

    def __init__(self, config):
        ApplicationSession.__init__(self, config)
        self.init()

    def init(self):

        self._actions = {
            'lastAction': "",
            'currentAction': "",
        }

        self._votes = {
            'Banana': 0,
            'Chocolate': 0,
            'Lemon': 0
        }

    @wamp.register(u'io.crossbar.app.get')
    def getVotes(self):
        return [{'subject': key, 'votes': value} for key, value in self._votes.items()]

    @wamp.register(u'io.crossbar.app.getn')
    def getVotesn(self):
        return [{'subject': key, 'action': value} for key, value in self._actions.items()]



    @wamp.register(u'io.crossbar.app.voten')
    def submitVoten(self, subject):
        self._actions[subject] = 1
        result = {'subject': subject, 'votes': self._votes[subject]}
        self.publish('io.crossbar.app.onvoten', result)
        return result

    @wamp.register(u'io.crossbar.app.vote')
    def submitVote(self, subject):
        self._votes[subject] += 1
        result = {'subject': subject, 'votes': self._votes[subject]}
        self.publish('io.crossbar.app.onvote', result)
        return result


    @wamp.register(u'io.crossbar.app.reset')
    def resetVotes(self):
        self.init()
        self.publish('io.crossbar.app.onreset')


    @inlineCallbacks
    def onJoin(self, details):
        res = yield self.register(self)
        print("appBackend: {} procedures registered!".format(len(res)))
