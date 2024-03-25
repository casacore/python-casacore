python_add_library(_fitting MODULE WITH_SOABI
    fit.cc
    fitting.cc)
target_include_directories(_fitting PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS}
)
target_link_directories(_fitting PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_fitting PRIVATE ${Casacore_LIBRARIES})
install(TARGETS _fitting LIBRARY DESTINATION casacore/fitting COMPONENT libraries)

python_add_library(_functionals MODULE WITH_SOABI
    functional.cc
    functionals.cc
)
target_include_directories(_functionals PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS}
)
target_link_directories(_functionals PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_functionals PRIVATE ${Casacore_LIBRARIES})
install(TARGETS _functionals LIBRARY DESTINATION casacore/functionals COMPONENT libraries)

python_add_library(_images MODULE WITH_SOABI
    images.cc
    pyimages.cc
)
target_include_directories(_images PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS}
)
target_link_directories(_images PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_images PRIVATE ${Casacore_LIBRARIES})
install(TARGETS _images LIBRARY DESTINATION casacore/images COMPONENT libraries)

python_add_library(_measures MODULE WITH_SOABI
    pymeas.cc
    pymeasures.cc
)
target_include_directories(_measures PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS}
)
target_link_directories(_measures PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_measures PRIVATE ${Casacore_LIBRARIES})
install(TARGETS _measures LIBRARY DESTINATION casacore/measures COMPONENT libraries)

python_add_library(_quanta MODULE WITH_SOABI
    quanta.cc
    quantamath.cc
    quantity.cc
    quantvec.cc
)
target_include_directories(_quanta PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS}
)
target_link_directories(_quanta PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_quanta PRIVATE ${Casacore_LIBRARIES})
install(TARGETS _quanta LIBRARY DESTINATION casacore/quanta COMPONENT libraries)

python_add_library(_tables MODULE WITH_SOABI
    pytable.cc
    pytableindex.cc
    pytableiter.cc
    pytablerow.cc
    tables.cc
    pyms.cc
)
target_include_directories(_tables PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${Casacore_INCLUDE_DIRS}
)
target_link_directories(_tables PRIVATE ${Casacore_LIBRARY_DIRS})
target_link_libraries(_tables PRIVATE ${Casacore_LIBRARIES})
install(TARGETS _tables LIBRARY DESTINATION casacore/tables COMPONENT libraries)
