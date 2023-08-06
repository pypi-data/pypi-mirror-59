python-actransit
================

A simple `Alameda-Contra Costa Transit District <http://www.actransit.org/>`__ API wrapper.

License: `MIT <https://en.wikipedia.org/wiki/MIT_License>`__.

Installation
------------

::

    pip install python-actransit

API
---

Retrieve a Vehicle Position `GTFS <https://gtfs.org/>`__-Realtime feed.

.. code:: python

    from actransit import ACTransit
    ac_transit = ACTransit()
    realtime_vehicles = ac_transit.gtfsrt.vehicles()

    print(realtime_vehicles)

    {'entity': [{'id': '1',
                'vehicle': {'position': {'bearing': 116.0,
                                        'latitude': 37.80388259887695,
                                        'longitude': -122.276611328125,
                                        'speed': 0.0},
                            'timestamp': 1579463770,
                            'trip': {'route_id': '19',
                                    'schedule_relationship': 0,
                                    'trip_id': '751100010'},
                            'vehicle': {'id': '5020'}}},
                # ...
                ],
    'header': {'gtfs_realtime_version': '1.0',
                'incrementality': 0,
                'timestamp': 1579463788}}

Retrieve a list with information for any existing schedule: current, past and future.

.. code:: python

    from actransit import ACTransit
    ac_transit = ACTransit()
    existing_schedules = ac_transit.gtfs.all()

    print(existing_schedules)

    [{'BookingId': '1912WR',
    'EarliestServiceDate': '2019-12-14T00:00:00',
    'LatestServiceDate': '2020-03-28T00:00:00',
    'UpdatedDate': '2019-12-11T07:45:25.96'},
    {'BookingId': '1908FA',
    'EarliestServiceDate': '2019-08-10T00:00:00',
    'LatestServiceDate': '2019-12-14T00:00:00',
    'UpdatedDate': '2019-08-01T15:20:19.587'},
    # ...
    ]

