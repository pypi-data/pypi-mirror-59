==========
CleverFool
==========

This is an extremely thin convenience wrapper (just 40 lines of code) to load Foolbox-native attacks in Cleverhans 4 (currently both in beta as of 10.01.2020).

Even without this wrapper, it should generally be possible to switch between the two frameworks with minimal changes to your code.

Installation
------------

.. code-block:: bash

   pip install cleverfool


Basic usage
-----------

.. code-block:: python

   import foolbox.ext.native as fbn
   from cleverfool import convert_foolbox_attack
   
   attack = convert_foolbox_attack(fbn.attacks.LinfinityBasicIterativeAttack)
   
   # ... use attack just like any other CleverHans attack
   
