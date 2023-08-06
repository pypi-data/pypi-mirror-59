from datetime import datetime

import requests

from .enturcommon import EnturCommon


class EnturApi(EnturCommon):
    def __init__(self, client):
        super().__init__(client)

    # https://gist.github.com/gbaman/b3137e18c739e0cf98539bf4ec4366ad
    # A simple function to use requests.post to make the API call.
    # Note the json= section.
    def run_query(self, query):
        headers = {'ET-Client-Name': self.client}
        request = requests.post(
            'https://api.entur.io/journey-planner/v2/graphql',
            json={'query': query},
            headers=headers)
        if request.status_code == 200:
            json = request.json()
            if 'errors' in json:
                raise Exception('Entur returned error: %s' %
                                json['errors'][0]['message'])
            return request.json()
        else:
            raise Exception('Query failed to run by returning code of {}. {}'.
                            format(request.status_code, query))

    def stop_departures(self, stop_id, start_time='',
                        departures=10, time_range=72100):
        if start_time:
            start_time = datetime.now().strftime('%Y-%m-%dT') + start_time
            start_time = \
                '(startTime:"%s" timeRange: %d, numberOfDepartures: %d)' % \
                (start_time, time_range, departures)
        query = '''{
          stopPlace(id: "%s") {
            id
            name
            estimatedCalls%s {
              aimedArrivalTime
              aimedDepartureTime
              expectedArrivalTime
              expectedDepartureTime
              realtime
              date
              forBoarding
              forAlighting
              destinationDisplay {
                frontText
              }
              quay {
                id
              }
              serviceJourney {
              id
                journeyPattern {
                  id
                  name
                  line {
                    id
                    name
                    transportMode
                  }
                }
              }
            }
          }
        }''' % (stop_id, start_time)
        # print(query)
        return self.run_query(query)

    def stop_departures_app(self, stop_id, limit=100):
        query = '''query GetLinesFromStopPlaceProps {
        stopPlace(id:"%s") {
            estimatedCalls(
                numberOfDepartures: %d,
                omitNonBoarding: true,
            ) {
                quay {
                    id
                    name
                    description
                    publicCode
                }
                destinationDisplay { frontText }
                serviceJourney { id journeyPattern { line { ...lineFields } } }
                realtime
                expectedDepartureTime
                aimedDepartureTime
            }
        }
    }

    fragment lineFields on Line {
        id
        authority { id name }
        name
        publicCode
        transportMode
        transportSubmode
    }''' % (stop_id, limit)
        return self.run_query(query)

    def stop_info(self, stop_id):
        query = '''query GetLinesFromStopPlaceProps {
                  stopPlace(id: "%s") {
                    name
                    description
                    latitude
                    longitude
                    id
                    transportMode
                    transportSubmode
                    adjacentSites
                    timezone
                    adjacentSites
                    quays(filterByInUse: true) {
                      id
                      name
                      description
                      publicCode
                      situations {
                        id
                        summary {
                          value
                          language
                        }
                        description {
                          value
                          language
                        }
                        validityPeriod {
                          startTime
                          endTime
                        }
                        reportType
                        severity
                      }
                    }
                  }
                }
                ''' % stop_id
        return self.run_query(query)
