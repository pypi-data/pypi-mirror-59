# EMACS settings: -*-	tab-width: 2; indent-tabs-mode: t; python-indent-offset: 2 -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
# ==============================================================================
#            __     ___   _ ____  _     ____
#  _ __  _   \ \   / / | | |  _ \| |   |  _ \ __ _ _ __ ___  ___ _ __
# | '_ \| | | \ \ / /| |_| | | | | |   | |_) / _` | '__/ __|/ _ \ '__|
# | |_) | |_| |\ V / |  _  | |_| | |___|  __/ (_| | |  \__ \  __/ |
# | .__/ \__, | \_/  |_| |_|____/|_____|_|   \__,_|_|  |___/\___|_|
# |_|    |___/
# ==============================================================================
# Authors:            Patrick Lehmann
#
# Python package:     A streaming-based VHDL parser.
#
# Description:
# ------------------------------------
#		TODO:
#
# License:
# ==============================================================================
# Copyright 2017-2019 Patrick Lehmann - Boetzingen, Germany
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
#
import sys

__all__ = [
	'Export',
]
__api__ = __all__


def Export(entity):
	"""
	Register the given entity as public accessible in a module.
	"""

	# * Based on an idea by Duncan Booth:
	#   http://groups.google.com/group/comp.lang.python/msg/11cbb03e09611b8a
	# * Improved via a suggestion by Dave Angel:
	#   http://groups.google.com/group/comp.lang.python/msg/3d400fb22d8a42e1

	module = sys.modules[entity.__module__]
	if hasattr(module, '__all__'):
		if entity.__name__ not in module.__all__:
			module.__all__.append(entity.__name__)
	else:
		module.__all__ = [ entity.__name__ ]

	return entity
