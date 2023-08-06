GPIO\_Calculator
================

Simple GPIO calculator for ``libgpiod`` based on its chardev using the formula
chardev = (alphabet_index - 1) * 32 + pin which is also used on ``sysfs``.

Installation
------------

.. code-block:: console

    pip install git+https://github.com/yeyeto2788/GPIO_Calculator

Usage
-----

.. code-block:: python

    from gpio_calculator import Calculator

    calculator = Calculator()

    # Get chardev based on pin letter and pin number.
    # Return should be 242
    calculator.get_chardev("H", 18)

    # Get chardev from list.
    # Returns a list of converted items [242, 243, 244].
    calculator.get_chardevs(["H18", "H19", "H20"])

    # Get pin from chardev.
    # Returns the pin number H18.
    calculator.get_pin(242)

    # Get all pins from chardevs.
    # Returns all pins found H18, H19, H20.
    calculator.get_pins([242, 243, 244])


Contributing
------------

**All contributions, pull requests and comments are welcome!**

When contributing it is important to test the module in order to make sure
everything is working as expected. For that install dependencies to run the tests.

.. code-block:: console

   pip install pytest pytest-cov mock pylint

Running tests and see coverage.

.. code-block:: console

   py.test --cov -v --cov-config=.coveragerc --cov-report=html

This will generate a report with the coverage which is at **98%** now, let's try to keep
it at the same percentage.