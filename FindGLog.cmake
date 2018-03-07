#
# Find GLOG
#
#  GLOG_INCLUDE_DIRS - where to find glog/glog.h, etc.
#  GLOG_LIBRARIES     - List of libraries when using libglog.
#  GLOG_FOUND       - True if libglog found.

FIND_PATH(GLOG_INCLUDE_DIRS glog/glog.h)

FIND_LIBRARY(GLOG_LIBRARIES NAMES glog)

# handle the QUIETLY and REQUIRED arguments and set GLOG_FOUND to TRUE if
# all listed variables are TRUE
INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GLOG DEFAULT_MSG GLOG_LIBRARIES GLOG_INCLUDE_DIRS)

MARK_AS_ADVANCED(GLOG_LIBRARIES GLOG_INCLUDE_DIRS)

