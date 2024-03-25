python_add_library(_tConvert MODULE WITH_SOABI tConvert.cc)
target_include_directories(_tConvert PRIVATE ${Boost_INCLUDE_DIRS}
                                             ${Casacore_INCLUDE_DIRS})
target_link_directories(_tConvert PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_tConvert PRIVATE ${Casacore_LIBRARIES})
install(TARGETS _tConvert LIBRARY DESTINATION casacore COMPONENT libraries)
