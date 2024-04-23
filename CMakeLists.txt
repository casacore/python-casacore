cmake_minimum_required(VERSION 3.15...3.26)
project(python-casacore)

find_package(
  Python
  COMPONENTS Interpreter Development.Module
  REQUIRED)

# Find Casacore and its dependencies
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)
find_package(Casacore REQUIRED)
find_package(Boost REQUIRED COMPONENTS python)

# If environment variable CASACORE_DATA is set, assume it points to a directory
# containing the cascacore data files, and install its contents.
if(DEFINED ENV{CASACORE_DATA})
  foreach(_dir ephemerides geodetic)
    if(NOT IS_DIRECTORY $ENV{CASACORE_DATA}/${_dir})
      message(
        SEND_ERROR
          "Directory $ENV{CASACORE_DATA}/${_dir} does not exist. "
          "Does environment variable CASACORE_DATA point to a valid data directory?"
      )
    endif()
  endforeach()
  install(
    DIRECTORY $ENV{CASACORE_DATA}
    DESTINATION casacore
    COMPONENT data)
else()
  message(
    WARNING
      "Environment variable CASACORE_DATA is not defined. "
      "Casacore data files will not be included in the python-casacore package."
  )
endif()

add_subdirectory(src)
if(BUILD_TESTING)
  add_subdirectory(tests)
endif()
