Exceptions
==========

The ``m209`` library defines an exception hierarchy, rooted at the
``M209Error`` class. These exceptions are briefly described below.

.. class:: m209.M209Error()

   The base exception in the hierarchy. It inherits from the built in
   Python ``Exception`` class.

.. class:: m209.drum.DrumError()

   Inherits from :class:`~m209.M209Error`. This exception is used to report
   drum related errors.

.. class:: m209.key_wheel.KeyWheelError()

   Inherits from :class:`~m209.M209Error`. This exception is used to report key
   wheel related errors.

.. class:: m209.keylist.generate.KeyListGenError()

   Inherits from :class:`~m209.M209Error`. This is public exception, used
   to report errors during the key list generation process.

.. class:: m209.procedure.ProcedureError()

   Inherits from :class:`~m209.M209Error`. This is public exception, used
   to report errors during :class:`~m209.procedure.StdProcedure` operations.
