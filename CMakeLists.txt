cmake_minimum_required(VERSION 3.18)
project(python-casacore)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

if(SKBUILD)
    message(STATUS "The project is built using scikit-build")
else()
  # If skbuild is not the driver; include its utilities in CMAKE_MODULE_PATH
  execute_process(
    COMMAND "${Python_EXECUTABLE}"
    -c "import os, skbuild; print(os.path.dirname(skbuild.__file__))"
    OUTPUT_VARIABLE SKBLD_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
    RESULT_VARIABLE STATUS
  )
  if(NOT STATUS EQUAL 0)
    message(FATAL_ERROR
        "You need scikit-build to build python-casacore.\n"
        "Use `pip install scikit-build` to install it.\n"
    )
  endif()
  list(APPEND CMAKE_MODULE_PATH "${SKBLD_DIR}/resources/cmake")
  message(STATUS "Looking in ${SKBLD_DIR}/resources/cmake for CMake modules")
endif()

# Scikit-build extensions
find_package(PythonExtensions REQUIRED)

# Find Casacore and its dependencies
find_package(PkgConfig REQUIRED)
pkg_check_modules(Casacore REQUIRED casacore)
find_package(Boost REQUIRED COMPONENTS python)

# If environment variable CASACORE_DATA is set, it is assumed that it points to the
# directory containing the casacore data files. Create a symlink to that directory.
if (DEFINED ENV{CASACORE_DATA})
    execute_process(COMMAND ${CMAKE_COMMAND} -E create_symlink
        $ENV{CASACORE_DATA} ${CMAKE_SOURCE_DIR}/casacore/data
        RESULT_VARIABLE STATUS
        ERROR_VARIABLE STDERR
    )
    if(NOT STATUS EQUAL 0)
        message(FATAL_ERROR "Failed to create symlink.\n${STDERR}")
    else()
        # message(STATUS "Data files in $ENV{CASACORE_DATA} will be included in the python-casacore package")
        message(STATUS "Created symlink: ${CMAKE_SOURCE_DIR}/casacore/data -> $ENV{CASACORE_DATA}")
    endif()
else()
    message(WARNING
        "Environment variable CASACORE_DATA is not defined. "
        "Casacore data files will not be included in the python-casacore package."
    )
endif()

add_library(_fitting MODULE
    src/fit.cc
    src/fitting.cc)
target_include_directories(_fitting PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS} 
    ${Python_INCLUDE_DIRS}
)
target_link_directories(_fitting PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_fitting ${Casacore_LIBRARIES})
python_extension_module(_fitting)
install(TARGETS _fitting LIBRARY DESTINATION casacore/fitting)

add_library(_functionals MODULE
    src/functional.cc
    src/functionals.cc
)
target_include_directories(_functionals PRIVATE 
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS} 
    ${Python_INCLUDE_DIRS}
)
target_link_directories(_functionals PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_functionals ${Casacore_LIBRARIES})
python_extension_module(_functionals)
install(TARGETS _functionals LIBRARY DESTINATION casacore/functionals)

add_library(_images MODULE
    src/images.cc
    src/pyimages.cc
)
target_include_directories(_images PRIVATE 
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS} 
    ${Python_INCLUDE_DIRS}
)
target_link_directories(_images PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_images ${Casacore_LIBRARIES})
python_extension_module(_images)
install(TARGETS _images LIBRARY DESTINATION casacore/images)

add_library(_measures MODULE
    src/pymeas.cc
    src/pymeasures.cc
)
target_include_directories(_measures PRIVATE 
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS} 
    ${Python_INCLUDE_DIRS}
)
target_link_directories(_measures PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_measures ${Casacore_LIBRARIES})
python_extension_module(_measures)
install(TARGETS _measures LIBRARY DESTINATION casacore/measures)

add_library(_quanta MODULE
    src/quanta.cc
    src/quantamath.cc
    src/quantity.cc
    src/quantvec.cc
)
target_include_directories(_quanta PRIVATE 
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS} 
    ${Python_INCLUDE_DIRS}
)
target_link_directories(_quanta PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_quanta ${Casacore_LIBRARIES})
python_extension_module(_quanta)
install(TARGETS _quanta LIBRARY DESTINATION casacore/quanta)

add_library(_tables MODULE
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
    ${Python_INCLUDE_DIRS}
)
target_link_directories(_tables PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_tables ${Casacore_LIBRARIES})
python_extension_module(_tables)
install(TARGETS _tables LIBRARY DESTINATION casacore/tables)


add_library(_tConvert MODULE
    tests/tConvert.cc
)
target_include_directories(_tConvert PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS}
    ${Python_INCLUDE_DIRS}
)
target_link_directories(_tConvert PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_tConvert ${Casacore_LIBRARIES})
python_extension_module(_tConvert)
install(TARGETS _tConvert LIBRARY DESTINATION casacore)
