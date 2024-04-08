python_add_library(_tConvert MODULE WITH_SOABI tConvert.cc)
target_include_directories(_tConvert PRIVATE ${Boost_INCLUDE_DIRS}
                                             ${CASACORE_INCLUDE_DIRS})
target_link_directories(_tConvert PRIVATE ${CASACORE_LIBRARY_DIRS})
target_link_libraries(_tConvert PRIVATE ${CASACORE_LIBRARIES})
target_link_options(_tConvert PRIVATE "LINKER:--as-needed")
install(TARGETS _tConvert LIBRARY DESTINATION casacore COMPONENT libraries)
