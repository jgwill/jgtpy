"""Entry point for ``python -m jgtpy``.

This simply forwards execution to :mod:`jgtpy.jgtcli` so running the
package with ``-m`` behaves like invoking ``jgtcli`` directly.
"""

from .jgtcli import main

if __name__ == "__main__":
    main()
