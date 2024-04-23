python_add_library(_fitting MODULE WITH_SOABI fit.cc fitting.cc)

python_add_library(_functionals MODULE WITH_SOABI functional.cc functionals.cc)

python_add_library(_images MODULE WITH_SOABI images.cc pyimages.cc)

python_add_library(_measures MODULE WITH_SOABI pymeas.cc pymeasures.cc)

python_add_library(
  _quanta
  MODULE
  WITH_SOABI
  quanta.cc
  quantamath.cc
  quantity.cc
  quantvec.cc)

python_add_library(
  _tables
  MODULE
  WITH_SOABI
  pytable.cc
  pytableindex.cc
  pytableiter.cc
  pytablerow.cc
  tables.cc
  pyms.cc)

get_directory_property(_targets BUILDSYSTEM_TARGETS)
foreach(_target ${_targets})
  string(REGEX REPLACE "^_" "casacore/" _destination "${_target}")
  target_include_directories(${_target} PRIVATE ${Boost_INCLUDE_DIRS}
                                                ${CASACORE_INCLUDE_DIRS})
  target_link_directories(${_target} PRIVATE ${CASACORE_LIBRARY_DIRS})
  target_link_libraries(${_target} PRIVATE ${CASACORE_LIBRARIES})
  target_link_options(${_target} PRIVATE "LINKER:--as-needed")
  install(TARGETS ${_target} LIBRARY DESTINATION ${_destination}
                                     COMPONENT libraries)
endforeach()
