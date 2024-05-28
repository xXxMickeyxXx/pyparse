from ..library import RootError, use_docstring


#############################################################################
#    Package's top level error and parent class for all following errors    #
#    which should provide the ability to generalize error handling in the   #
#    event that it's preferable to catch all package related errors, and    #
#    possibly allowing other package/applicaiton errors to come through.    #
#############################################################################
@use_docstring
class PyParseError(RootError):
	"""PyParse Error"""


@use_docstring
class TokenError(PyParseError):
	"""Token Error"""


@use_docstring
class TimeOutError(PyParseError):
    """Time Out Error"""


if __name__ == "__main__":
	pass
