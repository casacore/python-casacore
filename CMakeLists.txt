cmake_minimum_required(VERSION 3.18)
project(python-casacore)

find_package(PkgConfig REQUIRED)
pkg_check_modules(Casacore REQUIRED casacore)
# find_package(Casacore REQUIRED)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
find_package(PythonExtensions REQUIRED)

if(SKBUILD)
    message(STATUS "The project is built using scikit-build")
endif()

message(STATUS "Python_INCLUDE_DIRS=${Python_INCLUDE_DIRS}")

add_library(_fitting MODULE
    src/fit.cc
    src/fitting.cc)
target_include_directories(_fitting PRIVATE 
    ${Casacore_INCLUDE_DIRS} 
    ${Python_INCLUDE_DIRS}
)
target_link_directories(_fitting PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_fitting ${Casacore_LIBRARIES})
python_extension_module(_fitting)

add_library(_functionals MODULE
    src/functional.cc
    src/functionals.cc
)
target_include_directories(_functionals PRIVATE 
    ${Casacore_INCLUDE_DIRS} 
    ${Python_INCLUDE_DIRS}
)
target_link_directories(_functionals PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_functionals ${Casacore_LIBRARIES})
python_extension_module(_functionals)

add_library(_images MODULE
    src/images.cc
    src/pyimages.cc
)
target_include_directories(_images PRIVATE 
    ${Casacore_INCLUDE_DIRS} 
    ${Python_INCLUDE_DIRS}
)
target_link_directories(_images PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_images ${Casacore_LIBRARIES})
python_extension_module(_images)

add_library(_measures MODULE
    src/pymeas.cc
    src/pymeasures.cc
)
target_include_directories(_measures PRIVATE 
    ${Casacore_INCLUDE_DIRS} 
    ${Python_INCLUDE_DIRS}
)
target_link_directories(_measures PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_measures ${Casacore_LIBRARIES})
python_extension_module(_measures)

add_library(_quanta MODULE
    src/quanta.cc
    src/quantamath.cc
    src/quantity.cc
    src/quantvec.cc
)
target_include_directories(_quanta PRIVATE 
    ${Casacore_INCLUDE_DIRS} 
    ${Python_INCLUDE_DIRS}
)
target_link_directories(_quanta PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_quanta ${Casacore_LIBRARIES})
python_extension_module(_quanta)

add_library(_tables MODULE
    src/pytable.cc
    src/pytableindex.cc
    src/pytableiter.cc
    src/pytablerow.cc
    src/tables.cc
    src/pyms.cc
)
target_include_directories(_tables PRIVATE 
    ${Casacore_INCLUDE_DIRS} 
    ${Python_INCLUDE_DIRS}
)
target_link_directories(_tables PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_tables ${Casacore_LIBRARIES})
python_extension_module(_tables)
