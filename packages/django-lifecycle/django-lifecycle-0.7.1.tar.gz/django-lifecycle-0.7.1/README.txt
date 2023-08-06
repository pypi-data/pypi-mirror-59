Django Lifecycle Hooks
======================

|Package version| |Python versions|

Overview
========

This project provides a ``@hook`` decorator as well as a base model or
mixin to add lifecycle hooks to your Django models. Django's built-in
approach to offering lifecycle hooks is
`Signals <https://docs.djangoproject.com/en/2.0/topics/signals/>`__.
However, in the projects I've worked on, my team often finds that
Signals introduce unnesseary indirection and are at odds with Django's
"fat models" approach of including related logic in the model class
itself\*.

In short, you can write model code that looks like this:

.. code:: python

    from django_lifecycle import LifecycleModel, hook


    class UserAccount(LifecycleModel):
        username = models.CharField(max_length=100)
        password = models.CharField(max_length=200)
        password_updated_at = models.DateTimeField(null=True)
        
        @hook('before_update', when='password', has_changed=True)
        def timestamp_password_change(self):
            self.password_updated_at = timezone.now()

Instead of overriding ``save`` and ``__init___`` in a clunky way that
hurts readability:

.. code:: python

        # same class and field declarations as above ...
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__original_password = self.password
            
            
        def save(self, *args, **kwargs):
            if self.pk is not None and self.password != self.__original_password:
                self.password_updated_at = timezone.now()
            super().save(*args, **kwargs)

\*This is not to say Signals are never useful; my team prefers to use
them for incidental concerns not related to the business domain, like
cache invalidation.

Table of Contents:
==================

-  `Installation <#installation>`__
-  `Requirements <#requirements>`__
-  `Usage <#usage>`__
-  `Examples <#examples>`__
-  `Simple Hook - No Conditions <#ex-simple-hook>`__
-  `Hook with Transition Conditions: Part I <#ex-condition-hook-1%22>`__
-  `Hook with Transition Conditions: Part
   II <#ex-condition-hook-2%22>`__
-  `Hook with Simple Change Condition <#ex-simple-change>`__
-  `Hook with "Is Not" Condition <#ex-is-not>`__
-  `Custom Condition <#ex-custom-condition>`__
-  `Multiple decorators, same method <#ex-multiple-decorators>`__
-  `Documentation <#docs>`__
-  

   -  `Lifecycle Hook <#lifecycle-hooks-doc>`__

-  

   -  `Condition Arguments <#condition-args-doc>`__

-  

   -  `Utility Methods <#utility-method-doc>`__

-  

   -  `Suppressing Hooked Methods <#suppressing>`__

-  

   -  `Limitations <#limitations>`__

-  `Changelog <#changelog>`__
-  `Testing <#testing>`__
-  `License <#license>`__

Installation
============

::

    pip install django-lifecycle

Requirements
============

-  Python (3.3, 3.4, 3.5, 3.6)
-  Django (1.8, 1.9, 1.10, 1.11, 2.0)

Usage
=====

Either extend the provided abstract base model class:

.. code:: python

    from django_lifecycle import LifecycleModel, hook


    class YourModel(LifecycleModel):
        name = models.CharField(max_length=50)

Or add the mixin to your Django model definition:

.. code:: python

    from django.db import models
    from django_lifecycle import LifecycleModelMixin, hook


    class YourModel(LifecycleModelMixin, models.Model):
        name = models.CharField(max_length=50)

:exclamation: *If you are using **Django 1.8 or below** and want to
extend the base model, you also have to add ``django_lifecycle`` to
``INSTALLED_APPS``*.

Great, now we can start adding lifecycle hooks! Let's do a few examples
that illustrate the ability to not only hook into certain events, but to
add basic conditions that can replace the need for boilerplate
conditional code.

Examples
========

Simple Hook - No conditions 
----------------------------

Say you want to process a thumbnail image in the background and send the
user an email when they first sign up:

.. code:: python

        @hook('after_create')
        def do_after_create_jobs(self):
            enqueue_job(process_thumbnail, self.picture_url)

            mail.send_mail(
                'Welcome!', 'Thank you for joining.',
                'from@example.com', ['to@example.com'],
            )

Or say you want to email a user when their account is deleted. You could
add the decorated method below:

.. code:: python

        @hook('after_delete')
        def email_deleted_user(self):
            mail.send_mail(
                'We have deleted your account', 'Thank you for your time.',
                'customerservice@corporate.com', ['human@gmail.com'],
            )

Hook with Transition Conditions: Part I 
----------------------------------------

Maybe you only want the hooked method to run only under certain
circumstances related to the state of your model. Say if updating a
model instance changes a "status" field's value from "active" to
"banned", you want to send them an email:

.. code:: python

        @hook('after_update', when='status', was='active', is_now='banned')
        def email_banned_user(self):
            mail.send_mail(
                'You have been banned', 'You may or may not deserve it.',
                'communitystandards@corporate.com', ['mr.troll@hotmail.com'],
            )

The ``was`` and ``is_now`` keyword arguments allow you to compare the
model's state from when it was first instantiated to the current moment.
You can also pass an ``*`` to indicate any value - these are the
defaults, meaning that by default the hooked method will fire. The
``when`` keyword specifies which field to check against.

Hook with Transition Conditions: Part II 
-----------------------------------------

You can also enforce certain dissallowed transitions. For example, maybe
you don't want your staff to be able to delete an active trial because
they should always expire:

.. code:: python

        @hook('before_delete', when='has_trial', is_now=True)
        def ensure_trial_not_active(self):
            raise CannotDeleteActiveTrial('Cannot delete trial user!')

We've ommitted the ``was`` keyword meaning that the initial state of the
``has_trial`` field can be any value ("\*").

Hook with Simple Change Condition 
----------------------------------

As we saw in the very first example, you can also pass the keyword
argument ``has_changed=True`` to run the hooked method if a field has
changed, regardless of previous or current value.

.. code:: python

        @hook('before_update', when='address', has_changed=True)
        def timestamp_address_change(self):
            self.address_updated_at = timezone.now()

Hook with "Is Not" Condition 
-----------------------------

You can also have a hooked method fire when a field's value IS NOT equal
to a certain value. See a common example below involving lowercasing a
user's email.

.. code:: python

        @hook('before_save', when='email', is_not=None)
        def lowercase_email(self):
            self.email = self.email.lower()

Custom Condition 
-----------------

If you need to hook into events with more complex conditions, you can
take advantage of ``has_changed`` and ``initial_value`` methods:

``python     @hook('after_update')     def on_update(self):         if self.has_changed('username') and not self.has_changed('password'):             # do the thing here             if self.initial_value('login_attempts') == 2:                 do_thing()             else:                 do_other_thing()``

Multiple decorators, same method 
---------------------------------

You can decorate the same method multiple times if you want.

.. code:: python

        @hook('after_create')
        @hook('after_delete')
        def db_rows_changed(self):
            do_something()

Documentation 
==============

Lifecycle Hooks 
----------------

The hook name is passed as the first positional argument to the @hook
decorator, e.g. ``@hook('before_create)``.

``@hook(hook_name: str, **kwargs)``

+------------------+--------------------------------------------------------------------------+
| Hook name        | When it fires                                                            |
+==================+==========================================================================+
| before\_save     | Immediately before ``save`` is called                                    |
+------------------+--------------------------------------------------------------------------+
| after\_save      | Immediately after ``save`` is called                                     |
+------------------+--------------------------------------------------------------------------+
| before\_create   | Immediately before ``save`` is called, if ``pk`` is ``None``             |
+------------------+--------------------------------------------------------------------------+
| after\_create    | Immediately after ``save`` is called, if ``pk`` was initially ``None``   |
+------------------+--------------------------------------------------------------------------+
| before\_update   | Immediately before ``save`` is called, if ``pk`` is NOT ``None``         |
+------------------+--------------------------------------------------------------------------+
| after\_update    | Immediately after ``save`` is called, if ``pk`` was NOT ``None``         |
+------------------+--------------------------------------------------------------------------+
| before\_delete   | Immediately before ``delete`` is called                                  |
+------------------+--------------------------------------------------------------------------+
| after\_delete    | Immediately after ``delete`` is called                                   |
+------------------+--------------------------------------------------------------------------+

Condition Arguments 
--------------------

``@hook(hook_name: str, when: str = None, was='*', is_now='*', has_changed: bool = None, is_not = None):``

+------------------+------------------+------------------+
| Keywarg arg      | Type             | Details          |
+==================+==================+==================+
| when             | str              | The name of the  |
|                  |                  | field that you   |
|                  |                  | want to check    |
|                  |                  | against;         |
|                  |                  | required for the |
|                  |                  | conditions below |
|                  |                  | to be checked    |
+------------------+------------------+------------------+
| was              | any              | Only fire the    |
|                  |                  | hooked method if |
|                  |                  | the value of the |
|                  |                  | ``when`` field   |
|                  |                  | was equal to     |
|                  |                  | this value when  |
|                  |                  | first            |
|                  |                  | initialized;     |
|                  |                  | defaults to      |
|                  |                  | ``*``.           |
+------------------+------------------+------------------+
| is\_now          | any              | Only fire the    |
|                  |                  | hooked method if |
|                  |                  | the value of the |
|                  |                  | ``when`` field   |
|                  |                  | is currently     |
|                  |                  | equal to this    |
|                  |                  | value; defaults  |
|                  |                  | to ``*``.        |
+------------------+------------------+------------------+
| has\_changed     | bool             | Only fire the    |
|                  |                  | hooked method if |
|                  |                  | the value of the |
|                  |                  | ``when`` field   |
|                  |                  | has changed      |
|                  |                  | since the model  |
|                  |                  | was initialized  |
+------------------+------------------+------------------+
| is\_not          | any              | Only fire the    |
|                  |                  | hooked method if |
|                  |                  | the value of the |
|                  |                  | ``when`` field   |
|                  |                  | is NOT equal to  |
|                  |                  | this value       |
+------------------+------------------+------------------+

Other Utility Methods 
----------------------

These are available on your model when you use the mixin or extend the
base model.

+------------------+------------------+
| Method           | Details          |
+==================+==================+
| ``has_changed(fi | Return a boolean |
| eld_name: str) - | indicating       |
| > bool``         | whether the      |
|                  | field's value    |
|                  | has changed      |
|                  | since the model  |
|                  | was initialized  |
+------------------+------------------+
| ``initial_value( | Return the value |
| field_name: str) | of the field     |
|  -> bool``       | when the model   |
|                  | was first        |
|                  | initialized      |
+------------------+------------------+

Suppressing Hooked Methods 
---------------------------

To prevent the hooked methods from being called, pass
``skip_hooks=True`` when calling save:

.. code:: python

       account.save(skip_hooks=True)

Limitations 
------------

Foreign key fields on a lifecycle model can only be checked with the
``has_changed`` argument. That is, this library only checks to see if
the value of the foreign key has changed. If you need more advanced
conditions, consider omiting the run conditions and accessing the
related model's fields in the hooked method.

Changelog 
==========

0.3.2 (February 2019)
---------------------

-  Fixes bug preventing hooks from firing for custom PKs. Thanks
   @atugushev!

0.3.1 (August 2018)
-------------------

-  Fixes m2m field bug, in which accessing auto-generated reverse field
   in ``before_create`` causes exception b/c PK does not exist yet.
   Thanks @garyd203!

0.3.0 (April 2018)
------------------

-  Resets model's comparison state for hook conditions after ``save``
   called.

0.2.4 (April 2018)
------------------

-  Fixed support for adding multiple ``@hook`` decorators to same
   method.

0.2.3 (April 2018)
------------------

-  Removes residual mixin methods from earlier implementation.

0.2.2 (April 2018)
------------------

-  Save method now accepts ``skip_hooks``, an optional boolean keyword
   argument that controls whether hooked methods are called.

0.2.1 (April 2018)
------------------

-  Fixed bug in ``_potentially_hooked_methods`` that caused unwanted
   side effects by accessing model instance methods decorated with
   ``@cache_property`` or ``@property``.

0.2.0 (April 2018)
------------------

-  Added Django 1.8 support. Thanks @jtiai!
-  Tox testing added for Python 3.4, 3.5, 3.6 and Django 1.8, 1.11 and
   2.0. Thanks @jtiai!

Testing
=======

Tests are found in a simplified Django project in the ``/tests`` folder.
Install the project requirements and do ``./manage.py test`` to run
them.

License
=======

See `License <LICENSE.md>`__.

.. |Package version| image:: https://badge.fury.io/py/django-lifecycle.svg
   :target: https://pypi.python.org/pypi/django-lifecycle
.. |Python versions| image:: https://img.shields.io/pypi/status/django-lifecycle.svg
   :target: https://img.shields.io/pypi/status/django-lifecycle.svg/
