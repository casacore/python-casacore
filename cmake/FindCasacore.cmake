# - Try to find Casacore include dirs and libraries
# Usage:
#   find_package(Casacore [REQUIRED] [COMPONENTS components...])
# Valid components are:
#   casa, coordinates, derivedmscal, fits, images, lattices, meas, measures,
#   mirlib, ms, msfits, python3, scimath, scimath_f, tables
#
# Note that most components are dependent on other (more basic) components.
# In that case, it suffices to specify the "top-level" components; dependent
# components will be searched for automatically.
#
# The dependency tree can be generated using the script get_casacore_deps.sh.
# For this, you need to have a complete casacore installation, built with shared
# libraries, at your disposal.
#
# The dependencies in this macro were generated against casacore release 1.7.0.
#
# Variables used by this module:
#  CASACORE_ROOT_DIR         - Casacore root directory.
#  BLAS_LIBS                 - override BLAS library
#  LAPACK_LIBS               - override LAPACK library
#
# Variables defined by this module:
#  CASACORE_FOUND            - System has Casacore, which means that the
#                              include dir was found, as well as all
#                              libraries specified (not cached)
#  CASACORE_INCLUDE_DIR      - Casacore include directory (cached)
#  CASACORE_INCLUDE_DIRS     - Casacore include directories (not cached)
#                              identical to CASACORE_INCLUDE_DIR
#  CASACORE_LIBRARIES        - The Casacore libraries (not cached)
#  CASA_${COMPONENT}_LIBRARY - The absolute path of Casacore library
#                              "component" (cached)
#  HAVE_AIPSPP               - True if system has Casacore (cached)
#                              for backward compatibility with AIPS++
#  HAVE_CASACORE             - True if system has Casacore (cached)
#                              identical to CASACORE_FOUND
#  TAQL_EXECUTABLE           - The absolute path of the TaQL executable
#                              (cached)
#
# ATTENTION: The component names need to be in lower case, just as the
# casacore library names. However, the CMake variables use all upper case.

# Copyright (C) 2020 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: GPL-3.0-or-later

# - casacore_resolve_dependencies(_result)
#
# Resolve the Casacore library dependencies for the given components.
# The list of dependent libraries will be returned in the variable result.
# It is sorted from least dependent to most dependent library, so it can be
# directly fed to the linker.
#
#   Usage: casacore_resolve_dependencies(result components...)
#
macro(casacore_resolve_dependencies _result)
  set(${_result} ${ARGN})
  set(_index 0)
  # Do a breadth-first search through the dependency graph; append to the
  # result list the dependent components for each item in that list.
  # Duplicates will be removed later.
  while(1)
    list(LENGTH ${_result} _length)
    if(NOT _index LESS _length)
      break()
    endif(NOT _index LESS _length)
    list(GET ${_result} ${_index} item)
    list(APPEND ${_result} ${Casacore_${item}_DEPENDENCIES})
    math(EXPR _index "${_index}+1")
  endwhile(1)
  # Remove all duplicates in the current result list, while retaining only the
  # last of each duplicate.
  list(REVERSE ${_result})
  list(REMOVE_DUPLICATES ${_result})
  list(REVERSE ${_result})
endmacro(casacore_resolve_dependencies _result)


# - casacore_find_library(_name)
#
# Search for the library ${_name}.
# If library is found, add it to CASACORE_LIBRARIES; if not, add ${_name}
# to CASACORE_MISSING_COMPONENTS and set CASACORE_FOUND to false.
#
#   Usage: casacore_find_library(name)
#
macro(casacore_find_library _name)
  string(TOUPPER ${_name} _NAME)
  find_library(${_NAME}_LIBRARY ${_name}
    HINTS ${CASACORE_ROOT_DIR} PATH_SUFFIXES lib)
  mark_as_advanced(${_NAME}_LIBRARY)
  if(${_NAME}_LIBRARY)
    list(APPEND CASACORE_LIBRARIES ${${_NAME}_LIBRARY})
  else(${_NAME}_LIBRARY)
    set(CASACORE_FOUND FALSE)
    list(APPEND CASACORE_MISSING_COMPONENTS ${_name})
  endif(${_NAME}_LIBRARY)
endmacro(casacore_find_library _name)


# - casacore_find_package(_name)
#
# Search for the package ${_name}.
# If the package is found, add the contents of ${_name}_INCLUDE_DIRS to
# CASACORE_INCLUDE_DIRS and ${_name}_LIBRARIES to CASACORE_LIBRARIES.
#
# If Casacore itself is required, then, strictly speaking, the packages it
# requires must be present. However, when linking against static libraries
# they may not be needed. One can override the REQUIRED setting by switching
# CASACORE_MAKE_REQUIRED_EXTERNALS_OPTIONAL to ON. Beware that this might cause
# compile and/or link errors.
#
#   Usage: casacore_find_package(name [REQUIRED])
#
macro(casacore_find_package _name)
  if("${ARGN}" MATCHES "^REQUIRED$" AND
      Casacore_FIND_REQUIRED AND
      NOT CASACORE_MAKE_REQUIRED_EXTERNALS_OPTIONAL)
    find_package(${_name} REQUIRED)
  else()
    find_package(${_name})
  endif()
  if(${_name}_FOUND)
    list(APPEND CASACORE_INCLUDE_DIRS ${${_name}_INCLUDE_DIRS})
    list(APPEND CASACORE_LIBRARIES ${${_name}_LIBRARIES})
  endif(${_name}_FOUND)
endmacro(casacore_find_package _name)

# Define the Casacore components.
set(Casacore_components
  casa
  coordinates
  derivedmscal
  fits
  images
  lattices
  meas
  measures
  mirlib
  ms
  msfits
  python3
  scimath
  scimath_f
  tables
)

# Define the Casacore components' inter-dependencies.
set(Casacore_casa_DEPENDENCIES)
set(Casacore_coordinates_DEPENDENCIES   fits measures casa)
set(Casacore_derivedmscal_DEPENDENCIES  ms measures tables casa)
set(Casacore_fits_DEPENDENCIES          measures tables casa)
set(Casacore_images_DEPENDENCIES        coordinates mirlib lattices fits measures scimath tables casa)
set(Casacore_lattices_DEPENDENCIES      scimath tables casa)
set(Casacore_meas_DEPENDENCIES          measures tables casa)
set(Casacore_measures_DEPENDENCIES      tables casa)
set(Casacore_mirlib_DEPENDENCIES)
set(Casacore_ms_DEPENDENCIES            measures scimath tables casa)
set(Casacore_msfits_DEPENDENCIES        ms fits measures scimath tables casa)
set(Casacore_python3_DEPENDENCIES       casa)
set(Casacore_scimath_DEPENDENCIES       scimath_f casa)
set(Casacore_scimath_f_DEPENDENCIES)
set(Casacore_tables_DEPENDENCIES        casa)

# Initialize variables.
set(CASACORE_FOUND FALSE)
set(CASACORE_DEFINITIONS)
set(CASACORE_LIBRARIES)
set(CASACORE_MISSING_COMPONENTS)

# Search for the header file first.
if(NOT CASACORE_INCLUDE_DIR)
  find_path(CASACORE_INCLUDE_DIR casacore/casa/aips.h
    HINTS ${CASACORE_ROOT_DIR} PATH_SUFFIXES include)
  mark_as_advanced(CASACORE_INCLUDE_DIR)
endif(NOT CASACORE_INCLUDE_DIR)

# Fallback for systems that have old casacore installed in directory not called 'casacore'
# This fallback can be removed once we move to casacore 2.0 which always puts headers in 'casacore'
if(NOT CASACORE_INCLUDE_DIR)
  find_path(CASACORE_INCLUDE_DIR casa/aips.h
    HINTS ${CASACORE_ROOT_DIR} PATH_SUFFIXES include)
  mark_as_advanced(CASACORE_INCLUDE_DIR)
endif(NOT CASACORE_INCLUDE_DIR)

if(NOT CASACORE_INCLUDE_DIR)
  set(CASACORE_ERROR_MESSAGE "Casacore: unable to find the header file casa/aips.h.\nPlease set CASACORE_ROOT_DIR to the root directory containing Casacore.")
else(NOT CASACORE_INCLUDE_DIR)
  # We've found the header file; let's continue.
  set(CASACORE_FOUND TRUE)
  # Note that new Casacore uses #include<casacore/casa/...>, while
  # LOFAR still uses #include<casa/...>. Hence use both in -I path.
  set(CASACORE_INCLUDE_DIRS ${CASACORE_INCLUDE_DIR} ${CASACORE_INCLUDE_DIR}/casacore)

  # Search for some often used binaries.
  find_program(TAQL_EXECUTABLE taql
    HINTS ${CASACORE_ROOT_DIR}/bin)
  mark_as_advanced(TAQL_EXECUTABLE)

  # If the user specified components explicity, use that list; otherwise we'll
  # assume that the user wants to use all components.
  if(NOT Casacore_FIND_COMPONENTS)
    set(Casacore_FIND_COMPONENTS ${Casacore_components})
  endif(NOT Casacore_FIND_COMPONENTS)

  # Get a list of all dependent Casacore libraries that need to be found.
  casacore_resolve_dependencies(_find_components ${Casacore_FIND_COMPONENTS})

  # Find the library for each component, and handle external dependencies
  foreach(_comp ${_find_components})
    casacore_find_library(casa_${_comp})
    if(${_comp} STREQUAL casa)
      casacore_find_package(HDF5)
      casacore_find_library(m)
      list(APPEND CASACORE_LIBRARIES ${CMAKE_DL_LIBS})
    elseif(${_comp} STREQUAL coordinates)
      casacore_find_package(WCSLIB REQUIRED)
    elseif(${_comp} STREQUAL fits)
      casacore_find_package(CFITSIO REQUIRED)
    elseif(${_comp} STREQUAL scimath_f)
      # If only looking for LAPACK, no library will be added if LAPACK
      # is part of BLAS, as it is customary nowadays. So look for both
      # to avoid confusing linker errors on symbols used in headers/templates.
      if(DEFINED ENV{BLAS_LIBS})
        set(BLAS_FOUND YES)
        list(APPEND CASACORE_LIBRARIES $ENV{BLAS_LIBS})
      else()
        casacore_find_package(BLAS   REQUIRED)
      endif()
      if(DEFINED ENV{LAPACK_LIBS})
        set(LAPACK_FOUND YES)
        list(APPEND CASACORE_LIBRARIES $ENV{LAPACK_LIBS})
      else()
        casacore_find_package(LAPACK REQUIRED)
      endif()
    endif(${_comp} STREQUAL casa)
  endforeach(_comp ${_find_components})
endif(NOT CASACORE_INCLUDE_DIR)

# Set HAVE_CASACORE; and HAVE_AIPSPP (for backward compatibility with AIPS++).
if(CASACORE_FOUND)
  set(HAVE_CASACORE TRUE CACHE INTERNAL "Define if Casacore is installed")
  set(HAVE_AIPSPP TRUE CACHE INTERNAL "Define if AIPS++/Casacore is installed")
endif(CASACORE_FOUND)

# Compose diagnostic message if not all necessary components were found.
if(CASACORE_MISSING_COMPONENTS)
  set(CASACORE_ERROR_MESSAGE "Casacore: the following components could not be found:\n     ${CASACORE_MISSING_COMPONENTS}")
endif(CASACORE_MISSING_COMPONENTS)

# Print diagnostics.
if(CASACORE_FOUND)
  if(NOT Casacore_FIND_QUIETLY)
    message(STATUS "Found the following Casacore components: ")
    foreach(_comp ${_find_components})
      string(TOUPPER casa_${_comp} _COMP)
      message(STATUS "  ${_comp}: ${${_COMP}_LIBRARY}")
    endforeach(_comp ${_find_components})
  endif(NOT Casacore_FIND_QUIETLY)
else(CASACORE_FOUND)
  if(Casacore_FIND_REQUIRED)
    message(FATAL_ERROR "${CASACORE_ERROR_MESSAGE}")
  else(Casacore_FIND_REQUIRED)
    message(STATUS "${CASACORE_ERROR_MESSAGE}")
  endif(Casacore_FIND_REQUIRED)
endif(CASACORE_FOUND)
