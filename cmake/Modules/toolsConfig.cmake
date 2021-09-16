if(NOT PKG_CONFIG_FOUND)
    INCLUDE(FindPkgConfig)
endif()
PKG_CHECK_MODULES(PC_TOOLS tools)

FIND_PATH(
    TOOLS_INCLUDE_DIRS
    NAMES tools/api.h
    HINTS $ENV{TOOLS_DIR}/include
        ${PC_TOOLS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    TOOLS_LIBRARIES
    NAMES gnuradio-tools
    HINTS $ENV{TOOLS_DIR}/lib
        ${PC_TOOLS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/toolsTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(TOOLS DEFAULT_MSG TOOLS_LIBRARIES TOOLS_INCLUDE_DIRS)
MARK_AS_ADVANCED(TOOLS_LIBRARIES TOOLS_INCLUDE_DIRS)
