.. proovikeneeetika documentation master file, created by
   sphinx-quickstart on Wed Dec 11 12:39:19 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Kinetics
============================================
.. toctree::
   :maxdepth: 6

   index
	      
.. _base codes:

.. module:: iocbio.kinetics.constants
   
      
.. module:: iocbio.kinetics.global_vars
   

##########
Apps
##########

.. automodule:: iocbio.kinetics.app.__init__
   :members:

.. automodule:: iocbio.kinetics.app.gui
   :members:


.. automodule:: iocbio.kinetics.app.fetch
   :members:

.. automodule:: iocbio.kinetics.app.fetch_repeated
   :members:

.. automodule:: iocbio.kinetics.app.banova
   :members:
  

.. _codes:

##########
codes
##########


.. _calc:

==========
Calc
==========
.. automodule:: iocbio.kinetics.calc.xy
   :members:
      
.. automodule:: iocbio.kinetics.calc.mm
   :members:

.. automodule:: iocbio.kinetics.calc.mean_med_std
   :members:

.. automodule:: iocbio.kinetics.calc.linreg
   :members:

.. automodule:: iocbio.kinetics.calc.__init__
   :members:

.. automodule:: iocbio.kinetics.calc.generic
   :members:

.. automodule:: iocbio.kinetics.calc.explin_fit
   :members:

.. automodule:: iocbio.kinetics.calc.current
   :members:      

.. automodule:: iocbio.kinetics.calc.composer
   :members:       

.. automodule:: iocbio.kinetics.calc.bump
   :members:


.. _handler:

==========
Handler
==========

.. automodule:: iocbio.kinetics.handler.experiment_generic
   :members:

.. automodule:: iocbio.kinetics.handler.__init__
   :members:

.. automodule:: iocbio.kinetics.handler.roi
   :members: 


      
.. _gui:

==========
Gui
==========

.. automodule:: iocbio.kinetics.gui
   :members:

.. automodule:: iocbio.kinetics.gui.experiment_plot
   :members:

.. automodule:: iocbio.kinetics.gui.__init__
   :members:

.. automodule:: iocbio.kinetics.gui.mainwindow
   :members:


.. automodule:: iocbio.kinetics.gui.roi_list
   :members:

.. automodule:: iocbio.kinetics.gui.stats_widget
   :members:

.. automodule:: iocbio.kinetics.gui.xy_plot
   :members:

     

.. _io:

==========
io
==========
.. automodule:: iocbio.kinetics.io.data
   :members:

.. automodule:: iocbio.kinetics.io.db
   :members:

.. automodule:: iocbio.kinetics.io.modules
   :members:      

      
.. _modules:

========
Modules
========

.. _sysbio:

----------
Sysbio
----------



.. _confocal_catransient:

^^^^^^^^^^^^^^^^^^^^^
Confocal-catransient
^^^^^^^^^^^^^^^^^^^^^

.. automodule:: iocbio.kinetics.modules.sysbio.confocal_catransient.analyzer
   :members:

.. automodule:: iocbio.kinetics.modules.sysbio.confocal_catransient.reader
   :members:


.. _electrophysiology:

^^^^^^^^^^^^^^^^^^^^^
Electrophysiology
^^^^^^^^^^^^^^^^^^^^^
      
.. automodule:: iocbio.kinetics.modules.sysbio.electrophysiology.elec_current_analyzer
   :members:
      
.. automodule:: iocbio.kinetics.modules.sysbio.electrophysiology.elec_current_fluo_analysers
   :members:
      
.. automodule:: iocbio.kinetics.modules.sysbio.electrophysiology.elec_fluo_analyzer
   :members:
      
.. automodule:: iocbio.kinetics.modules.sysbio.electrophysiology.reader
   :members:

.. _mechanics:

^^^^^^^^^^^^^^^^^^^^^
Mechanics
^^^^^^^^^^^^^^^^^^^^^
.. automodule:: iocbio.kinetics.modules.sysbio.mechanics.experiment_mechanics
   :members:

.. automodule:: iocbio.kinetics.modules.sysbio.mechanics.mech_ufreqcasl
   :members:


.. automodule:: iocbio.kinetics.modules.sysbio.mechanics.mech_ufreqcasl_lowhigh
   :members:


.. automodule:: iocbio.kinetics.modules.sysbio.mechanics.reader
   :members:

  

.. _misc:

^^^^^^^^^^^^^^^^^^^^^
Misc
^^^^^^^^^^^^^^^^^^^^^
.. automodule:: iocbio.kinetics.modules.sysbio.misc.set_prepid
   :members:

.. _respiration:

^^^^^^^^^^^^^^^^^^^^^
Respiration
^^^^^^^^^^^^^^^^^^^^^
.. automodule:: iocbio.kinetics.modules.sysbio.respiration.analyzer_post
   :members:

.. automodule:: iocbio.kinetics.modules.sysbio.respiration.analyzer_primary
   :members:

.. automodule:: iocbio.kinetics.modules.sysbio.respiration.experiment_strathkelvin
   :members:

.. automodule:: iocbio.kinetics.modules.sysbio.respiration.reader
   :members:
      

.. _spectro:

^^^^^^^^^^^^^^^^^^^^^
Spectro
^^^^^^^^^^^^^^^^^^^^^
.. automodule:: iocbio.kinetics.modules.sysbio.spectro.analyzer_primary
   :members:

.. automodule:: iocbio.kinetics.modules.sysbio.spectro.experiment_spectro
   :members:


.. automodule:: iocbio.kinetics.modules.sysbio.spectro.reader
   :members:





      


Indices and tables
==================


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
