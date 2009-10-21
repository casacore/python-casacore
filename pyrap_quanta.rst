====================
Module :mod:`quanta`
====================

.. automodule:: pyrap.quanta
   :members: quantity, is_quantity


.. class:: pyrap.quanta.Quantity

   A unit-value based physical quantity

   .. method:: get(unit)

      Convert the quantity into another (conformant one)

      :param unit: a conformant unit to convert the quantity to.

      Example::

          q = quantity('1km/s')
	  print q.get('m/s')
	  >>> 1000.0 m/s

   .. method:: get_value(unit)

      Get the vale of the quantity suing the optiona unit

      :param unit: a conformant unit to convert the quantity to.

      Example::

          q = quantity('1km/s')
	  print q.get_value()
	  >>> 1.0
