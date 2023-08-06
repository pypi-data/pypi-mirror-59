# Part of project: https://github.com/hotoffthehamster/config-decorator
# Copyright © 2019-2020 Landon Bouma. All rights reserved.
#
# This program is free software:  you can redistribute it and/or modify
# it  under  the  terms  of  the  GNU Affero General Public License  as
# published by the  Free Software Foundation, either  version 3  of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY;  without even the implied warranty of
# MERCHANTABILITY or  FITNESS FOR A PARTICULAR PURPOSE.  See  the
# GNU   Affero   General   Public   License   for   more  details.
#
# If you lost the GNU Affero General Public License that ships with
# this code (the 'LICENSE' file), see <http://www.gnu.org/licenses/>.

"""Root module package-level alias to :func:`config_decorator.config_decorator.section`.

- So you can call, e.g.,

  .. code-block:: python

      from config_decorator import section

  instead of

  .. code-block:: python

      from config_decorator.config_decorator import section
"""

from .config_decorator import section, ConfigDecorator
from .key_chained_val import KeyChainedValue

__all__ = (
    'section',
    'ConfigDecorator',
    'KeyChainedValue',
)

