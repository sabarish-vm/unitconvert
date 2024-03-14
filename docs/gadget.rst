.. _gadget:

GAGDET-2 units
===================

Function to convert back and forth between standard units and units used in the :math:`N`-body code ``GADGET-2``.
You are importing Gadget-2 units. For more information about the unit system have a look at Gadget-2 user manual online. Gadget-2 defines mass(gM), length(gL), and velocity(gV) as fundamental units. Therefore time(gT) is a derived unit. The units are also defined in terms of hubble parameter. This is neglected here for reasons explained in the manual. Remember to the graviational constant(gG) as well, when doing calculations. That is, import gM,gL,gT,gV,gG from this module 

.. automodule:: unitconvert.gadget
   :members: