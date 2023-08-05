.. image:: http://pyplan.com/wp-content/uploads/2018/10/logo_pyplan-1.png

**Pyplan** allows consolidating into a single graphical environment all corporate Data Analytics and Decision Support needs. 
It is meant to simplify Business Analyst introduction to Data Science with Python, and provide at the same time, computer power, robustness, huge quantity of open source tools and corporate governance.

Among its most prominent features you will find:

- Assisted drag and drop graphical programming
- Visual Influence Diagram to represent logic flow
- Easy creation of interactive user interfaces
- Empowered collaboration by one click publishing and sharing
- Secure and scalable with corporate standards
- On cloud or on-premise deployment

https://pyplan.org


Requirements
------------
- `python 3.7 <https://www.python.org/downloads/release/python-375/>`_


Installation alterantives
-------------------------

Using **pip**:

Linux/Mac::

  python3.7 -m venv pyplan
  . pyplan/bin/activate
  pip install pyplan-ide

Windows::

  python3.7 -m venv pyplan
  pyplan\Scripts\activate.bat
  pip install pyplan-ide


Using **conda**::

  conda config --append channels pyplan
  conda config --append channels conda-forge
  conda create -n pyplan-ide python=3.7
  conda activate pyplan-ide
  conda install pyplan-ide

Using **Anaconda Navigator**::

  1. Create and select new environment "pyplan-ide"
  2. Add pyplan and conda-forge channels
  3. Find pyplan-ide app on Home section and click Install

  Important:

    If doing an upgrade, first restart Anaconda Navigator in order to close any active Pyplan process.
    A message will appear, make sure that pyplan-ide is selected.

Run Pyplan
------------

You can run **Pyplan** with these commands:

Linux/Mac::

  . pyplan/bin/activate
  pyplan

Windows::

  pyplan\Scripts\activate.bat
  pyplan

Conda::

  conda activate
  pyplan

Anaconda Navigator::

  Click launch on pyplan-ide app

User Guide
===========

For User Guide please visit `docs.pyplan.org <http://docs.pyplan.org>`_

Community Support
==================

For Community Support please visit `community.pyplan.org <http://community.pyplan.org>`_
