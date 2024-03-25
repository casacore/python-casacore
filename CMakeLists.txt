cmake_minimum_required(VERSION 3.15...3.26)
project(python-casacore)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

# Find Casacore and its dependencies
find_package(PkgConfig REQUIRED)
pkg_check_modules(Casacore REQUIRED casacore)
find_package(Boost REQUIRED COMPONENTS python)

# If environment variable CASACORE_DATA is set, assume it points to a directory
# containing the cascacore data files, and install its contents.
if (DEFINED ENV{CASACORE_DATA})
    install(DIRECTORY $ENV{CASACORE_DATA} DESTINATION casacore COMPONENT data)
endif()

python_add_library(_fitting MODULE WITH_SOABI
    src/fit.cc
    src/fitting.cc)
target_include_directories(_fitting PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS}
)
target_link_directories(_fitting PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_fitting PRIVATE ${Casacore_LIBRARIES})
install(TARGETS _fitting LIBRARY DESTINATION casacore/fitting COMPONENT libraries)

python_add_library(_functionals MODULE WITH_SOABI
    src/functional.cc
    src/functionals.cc
)
target_include_directories(_functionals PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS}
)
target_link_directories(_functionals PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_functionals PRIVATE ${Casacore_LIBRARIES})
install(TARGETS _functionals LIBRARY DESTINATION casacore/functionals COMPONENT libraries)

python_add_library(_images MODULE WITH_SOABI
    src/images.cc
    src/pyimages.cc
)
target_include_directories(_images PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS}
)
target_link_directories(_images PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_images PRIVATE ${Casacore_LIBRARIES})
install(TARGETS _images LIBRARY DESTINATION casacore/images COMPONENT libraries)

python_add_library(_measures MODULE WITH_SOABI
    src/pymeas.cc
    src/pymeasures.cc
)
target_include_directories(_measures PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS}
)
target_link_directories(_measures PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_measures PRIVATE ${Casacore_LIBRARIES})
install(TARGETS _measures LIBRARY DESTINATION casacore/measures COMPONENT libraries)

python_add_library(_quanta MODULE WITH_SOABI
    src/quanta.cc
    src/quantamath.cc
    src/quantity.cc
    src/quantvec.cc
)
target_include_directories(_quanta PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS}
)
target_link_directories(_quanta PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_quanta PRIVATE ${Casacore_LIBRARIES})
install(TARGETS _quanta LIBRARY DESTINATION casacore/quanta COMPONENT libraries)

python_add_library(_tables MODULE WITH_SOABI
    src/pytable.cc
    src/pytableindex.cc
    src/pytableiter.cc
    src/pytablerow.cc
    src/tables.cc
    src/pyms.cc
)
target_include_directories(_tables PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS}
)
target_link_directories(_tables PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_tables PRIVATE ${Casacore_LIBRARIES})
install(TARGETS _tables LIBRARY DESTINATION casacore/tables COMPONENT libraries)

python_add_library(_tConvert MODULE WITH_SOABI
    tests/tConvert.cc
)
target_include_directories(_tConvert PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS}
)
target_link_directories(_tConvert PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_tConvert PRIVATE ${Casacore_LIBRARIES})
install(TARGETS _tConvert LIBRARY DESTINATION casacore COMPONENT libraries)
