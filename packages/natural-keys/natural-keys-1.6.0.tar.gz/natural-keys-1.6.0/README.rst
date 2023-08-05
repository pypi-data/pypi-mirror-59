Django Natural Keys
===================

Enhanced support for `natural
keys <https://docs.djangoproject.com/en/2.0/topics/serialization/#natural-keys>`__
in Django and `Django REST
Framework <http://www.django-rest-framework.org/>`__. Extracted from
`wq.db <https://wq.io/wq.db>`__ for general use.

*Django Natural Keys* provides a number of useful model methods (e.g.
``get_or_create_by_natural_key()``) that speed up working with natural
keys in Django. The module also provides a couple of serializer classes
that streamline creating REST API support for models with natural keys.

|Latest PyPI Release| |Release Notes| |License| |GitHub Stars| |GitHub
Forks| |GitHub Issues|

|Travis Build Status| |Python Support| |Django Support|

Usage
-----

*Django Natural Keys* is available via PyPI:

.. code:: bash

    # Recommended: create virtual environment
    # python3 -m venv venv
    # . venv/bin/activate
    pip install natural-keys

Model API
~~~~~~~~~

To use `natural
keys <https://docs.djangoproject.com/en/2.0/topics/serialization/#natural-keys>`__
in vanilla Django, you need to define a ``natural_key()`` method on your
Model class and a ``get_natural_key()`` method on the Manager class.
With *Django Natural Keys*, you can instead extend ``NaturalKeyModel``
and define a ``unique_together`` property on your Model's ``Meta`` class
or use a field with ``unique=True``. The first ``unique_together`` entry
or the first ``unique`` field (except an AutoField) will be treated as
the natural key for the model, and all of the necessary functions for
working with natural keys will automatically work.

.. code:: python

    from natural_keys import NaturalKeyModel

    class Event(NaturalKeyModel):
        name = models.CharField(max_length=255)
        date = models.DateField()
        class Meta:
            unique_together = (('name','date'),)
            
    class Note(models.Model):
        event = models.ForeignKey(Event)
        note = models.TextField()

or

.. code:: python

    from natural_keys import NaturalKeyModel

    class Event(NaturalKeyModel):
        name = models.CharField(unique=True)

The following methods will then be available on your Model and its
Manager:

.. code:: python

    # Default Django methods
    instance = Event.objects.get_by_natural_key('ABC123', date(2016, 1, 1))
    instance.natural_key == ('ABC123', date(2016, 1, 1))

    # get_or_create + natural keys
    instance, is_new = Event.objects.get_or_create_by_natural_key('ABC123', date(2016, 1, 1))

    # Like get_or_create_by_natural_key, but discards is_new
    # Useful for quick lookup/creation when you don't care whether the object exists already
    instance = Event.objects.find('ABC123', date(2016, 1, 1))
    note = Note.objects.create(
         event=Event.objects.find('ABC123', date(2016, 1, 1)),
         note="This is a note"
    )
    instance == note.event

    # Inspect natural key fields on a model without instantiating it
    Event.get_natural_key_fields() == ('name', 'date')

Nested Natural Keys
^^^^^^^^^^^^^^^^^^^

One key feature of *Django Natural Keys* is that it will automatically
traverse ``ForeignKey``\ s to related models (which should also be
``NaturalKeyModel`` classes). This makes it possible to define complex,
arbitrarily nested natural keys with minimal effort.

.. code:: python

    class Place(NaturalKeyModel):
        name = models.CharField(max_length=255, unique=True)

    class Event(NaturalKeyModel):
        place = models.ForeignKey(Place)
        date = models.DateField()
        class Meta:
            unique_together = (('place', 'date'),)

.. code:: python

    Event.get_natural_key_fields() == ('place__name', 'date')
    instance = Event.find('ABC123', date(2016, 1, 1))
    instance.place.name == 'ABC123'

Serializers
~~~~~~~~~~~

*Django Natural Keys* provides two ``ModelSerializer`` classes for use
with `Django REST Framework <http://www.django-rest-framework.org/>`__.
The first is ``NaturalKeySerializer``, which is meant to be used with
``NaturalKeyModel`` classes. The second serializer class,
``NaturalKeyModelSerializer``, handles the more common use case:
serializing a model that has a foreign key to a ``NaturalKeyModel`` but
is not a ``NaturalKeyModel`` itself. (One concrete example of this is
the `vera.Report <https://github.com/wq/vera#report>`__ model, which has
a ForeignKey to `vera.Event <https://github.com/wq/vera#event>`__, which
is a ``NaturalKeyModel``).

You can use these serializer classes with `Django REST
Framework <http://www.django-rest-framework.org/>`__ and/or
`wq.db <https://wq.io/wq.db>`__ just like any other serializer:

.. code:: python

    # Django REST Framework usage example
    from rest_framework import viewsets
    from rest_framework import routers
    from natural_keys import NaturalKeySerializer, NaturalKeyModelSerializer
    from .models import Event, Note

    class EventSerializer(NaturalKeySerializer):
        class Meta:
            model = Event
            
    class NoteSerializer(NaturalKeyModelSerializer):
        class Meta:
            model = Note

    class EventViewSet(viewsets.ModelViewSet):
        queryset = Event.objects.all()
        serializer_class = EventSerializer

    class NoteViewSet(viewsets.ModelViewSet):
        queryset = Note.objects.all()
        serializer_class = NoteSerializer

    router = routers.DefaultRouter()
    router.register(r'events', EventViewSet)
    router.register(r'notes', NoteViewSet)

    # wq.db usage example
    from wq.db import rest
    from natural_keys import NaturalKeySerializer, NaturalKeyModelSerializer
    from .models import Event, Note

    rest.router.register_model(Event, serializer=NaturalKeySerializer)
    rest.router.register_model(Note, serializer=NaturalKeyModelSerializer)

Once this is set up, you can use your REST API to create and view your
``NaturalKeyModel`` instances and related data. To facilitate
integration with regular HTML Forms, *Django Natural Keys* is integrated
with the `HTML JSON Forms <https://github.com/wq/html-json-forms>`__
package, which supports nested keys via an array naming convention, as
the examples below demonstrate.

.. code:: html

    <form action="/events/" method="post">
      <input name="place[name]">
      <input type="date" name="date">
    </form>

.. code:: js

    // /events.json
    [
        {
            "id": 123,
            "place": {"name": "ABC123"},
            "date": "2016-01-01"
        }
    ]

.. code:: html

    <form action="/notes/" method="post">
      <input name="event[place][name]">
      <input type="date" name="event[date]">
      <textarea name="note"></textarea>
    </form>

.. code:: js

    // /notes.json
    [
        {
            "id": 12345,
            "event": {
                "place": {"name": "ABC123"},
                "date": "2016-01-01"
            },
            "note": "This is a note"
        }
    ]

Natural Key Slugs
~~~~~~~~~~~~~~~~~

As an alternative to using ``NaturalKeySerializer`` /
``NaturalKeyModelSerializer``, you can also use a single slug-like field
for lookup and serialization. ``NaturalKeyModel`` (and its associated
queryset) defines a pseudo-field, ``natural_key_slug``, for this
purpose.

.. code:: python

    class Place(NaturalKeyModel):
        name = models.CharField(max_length=255, unique=True)
        
    class Room(NaturalKeyModel)
        place = models.ForeignKey(Place, models.ON_DELETE)
        name = models.CharField(max_length=255)
        
        class Meta:
            unique_together = (('place', 'name'),)

.. code:: python

    room = Room.objects.find("ABC123", "MainHall")
    assert(room.natural_key_slug == "ABC123-MainHall")
    assert(room == Room.objects.get(natural_key_slug="ABC123-MainHall"))

You can expose this functionality in your REST API to expose natural
keys instead of database-generated ids. To do this, you will likely want
to do the following:

1. Create a regular serializer with
   ``id = serializers.ReadOnlyField(source='natural_key_slug')``
2. Set ``lookup_field = 'natural_key_slug'`` on your ``ModelViewSet``
   (or similar generic class) and update the URL registration
   accordingly
3. Ensure foreign keys on any related models are serialized with
   ``serializers.SlugRelatedField(slug_field='natural_key_slug')``

In `wq.db <https://wq.io/wq.db>`__, all three of the above can be
achieved by setting the ``"lookup"`` attribute when registering with the
`router <https://wq.io/docs/router>`__:

.. code:: python

    # myapp/rest.py
    from wq.db import rest
    from .models import Room

    rest.router.register_model(
        Room,
        fields='__all__',
        lookup='natural_key_slug',
    )

Note that the ``natural_key_slug`` may not behave as expected if any of
the component values contain the delimiter character (``-`` by default).
To mitigate this, you can set ``natural_key_separator`` on the model
class to another character.

.. |Latest PyPI Release| image:: https://img.shields.io/pypi/v/natural-keys.svg
   :target: https://pypi.org/project/natural-keys/
.. |Release Notes| image:: https://img.shields.io/github/release/wq/django-natural-keys.svg
   :target: https://github.com/wq/django-natural-keys/releases
.. |License| image:: https://img.shields.io/pypi/l/natural-keys.svg
   :target: https://github.com/wq/django-natural-keys/blob/master/LICENSE
.. |GitHub Stars| image:: https://img.shields.io/github/stars/wq/django-natural-keys.svg
   :target: https://github.com/wq/django-natural-keys/stargazers
.. |GitHub Forks| image:: https://img.shields.io/github/forks/wq/django-natural-keys.svg
   :target: https://github.com/wq/django-natural-keys/network
.. |GitHub Issues| image:: https://img.shields.io/github/issues/wq/django-natural-keys.svg
   :target: https://github.com/wq/django-natural-keys/issues
.. |Travis Build Status| image:: https://img.shields.io/travis/wq/django-natural-keys/master.svg
   :target: https://travis-ci.org/wq/django-natural-keys
.. |Python Support| image:: https://img.shields.io/pypi/pyversions/natural-keys.svg
   :target: https://pypi.org/project/natural-keys/
.. |Django Support| image:: https://img.shields.io/badge/Django-1.8%2C%201.11%2C%202.0-blue.svg
   :target: https://pypi.org/project/natural-keys/
