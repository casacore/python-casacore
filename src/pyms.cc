#include <casacore/tables/Tables/TableProxy.h>

#include <casacore/python/Converters/PycBasicData.h>
#include <casacore/python/Converters/PycValueHolder.h>
#include <casacore/python/Converters/PycRecord.h>

#include <boost/python.hpp>
#include <boost/python/args.hpp>

#include <casacore/casa/Containers/RecordInterface.h>
#include <casacore/tables/Tables/SetupNewTab.h>
#include <casacore/ms/MeasurementSets/MeasurementSet.h>
#include <casacore/tables/Tables/TableDesc.h>
#include <casacore/tables/Tables/TableError.h>
#include <casacore/tables/Tables/TableRecord.h>


using namespace boost::python;

namespace casacore {

  // Get the required table descriptions for the given table.
  // If "" or "MAIN", the table descriptions for a Measurement Set
  // will be supplied, otherwise table should be some valid
  // MeasurementSet subtable
  TableDesc required_table_desc(const String & table)
  {
    String table_ = table;

    // Upper case things to be sure
    table_.upcase();

    if(table_.empty() || table_ == "MAIN") {
      TableDesc tabdesc = MeasurementSet::requiredTableDesc();

      // Remove the CATEGORY keyword from the FLAG_CATEGORY column
      // This empty Vector<String> gets converted to a python dictionary as
      // 'FLAG_CATEGORY' : {
      //     ...
      //     keywords': {'CATEGORY' : []},
      //     ...
      // }
      //
      // Due to the missing type information this gets converted
      // into something like Vector<int> when passed to the C++ layer,
      // which results in Table Conformance errors
      // This is an OK solution since the C++ layer always adds this keyword
      // if it is missing from the MS
      // (see addCat())

      tabdesc.rwColumnDesc("FLAG_CATEGORY")
             .rwKeywordSet().removeField("CATEGORY");

      return tabdesc;
    } else if(table_ == "ANTENNA") {
      return MSAntenna::requiredTableDesc();
    } else if(table_ == "DATA_DESCRIPTION") {
      return MSDataDescription::requiredTableDesc();
    } else if(table_ == "DOPPLER") {
      return MSDoppler::requiredTableDesc();
    } else if(table_ == "FEED") {
      return MSFeed::requiredTableDesc();
    } else if(table_ == "FIELD") {
      return MSField::requiredTableDesc();
    } else if(table_ == "FLAG_CMD") {
      return MSFlagCmd::requiredTableDesc();
    } else if(table_ == "FREQ_OFFSET") {
      return MSFreqOffset::requiredTableDesc();
    } else if(table_ == "HISTORY") {
      return MSHistory::requiredTableDesc();
    } else if(table_ == "OBSERVATION") {
      return MSObservation::requiredTableDesc();
    } else if(table_ == "POINTING") {
      return MSPointing::requiredTableDesc();
    } else if(table_ == "POLARIZATION") {
      return MSPolarization::requiredTableDesc();
    } else if(table_ == "PROCESSOR") {
      return MSProcessor::requiredTableDesc();
    } else if(table_ == "SOURCE") {
      return MSSource::requiredTableDesc();
    } else if(table_ == "SPECTRAL_WINDOW") {
      return MSSpectralWindow::requiredTableDesc();
    } else if(table_ == "STATE") {
      return MSState::requiredTableDesc();
    } else if(table_ == "SYSCAL") {
      return MSSysCal::requiredTableDesc();
    } else if(table_ == "WEATHER") {
      return MSWeather::requiredTableDesc();
    }

    throw TableError("Unknown table type: " + table_);
  }

  // Get the required table descriptions for the given table.
  // If "" or "MAIN", the table descriptions for a Measurement Set
  // will be supplied, otherwise table should be some valid
  // MeasurementSet subtable
  Record required_ms_desc(const String & table)
  {
    return TableProxy::getTableDesc(required_table_desc(table), true);
  }

  // Merge required and user supplied Table Descriptions
  TableDesc merge_required_and_user_table_descs(const TableDesc & required_td,
                                                const TableDesc & user_td)
  {
    TableDesc result = required_td;

    // Overwrite required columns with user columns
    for(uInt i=0; i < user_td.ncolumn(); ++i) {
      const String & name = user_td[i].name();

      // Remove if present in required
      if(result.isColumn(name)) {
        result.removeColumn(name);
      }

      // Add the column
      result.addColumn(user_td[i]);
    }

    // Overwrite required hypercolumns with user hypercolumns
    // In practice this shouldn't be necessary as requiredTableDesc
    // doesn't define hypercolumns by default...
    Vector<String> user_hc = user_td.hypercolumnNames();

    for(uInt i=0; i < user_hc.size(); ++i) {
      // Remove if hypercolumn is present
      if(result.isHypercolumn(user_hc[i])) {
        result.removeHypercolumnDesc(user_hc[i]);
      }

      Vector<String> dataColumnNames;
      Vector<String> coordColumnNames;
      Vector<String> idColumnNames;

      // Get the user hypercolumn
      uInt ndims = user_td.hypercolumnDesc(user_hc[i],
          dataColumnNames, coordColumnNames, idColumnNames);
      // Place it in result
      result.defineHypercolumn(user_hc[i], ndims,
          dataColumnNames, coordColumnNames, idColumnNames);
    }

    // Overwrite required keywords with user keywords
    result.rwKeywordSet().merge(user_td.keywordSet(),
      RecordInterface::OverwriteDuplicates);

    return result;
  }

  SetupNewTable default_ms_factory(const String & name,
                                  const String & subtable,
                                  const Record & table_desc,
                                  const Record & dminfo)
  {
    String msg;
    TableDesc user_td;

    // Create Table Description object from extra user table description
    if(!TableProxy::makeTableDesc(table_desc, user_td, msg)) {
      throw TableError("Error Making Table Description " + msg);
    }

    // Merge required and user table descriptions
    TableDesc final_desc = merge_required_and_user_table_descs(
                        required_table_desc(subtable), user_td);

    // Return SetupNewTable object
    SetupNewTable setup = SetupNewTable(name, final_desc, Table::New);

    // Apply any data manager info
    setup.bindCreate(dminfo);

    return setup;
  }

  TableProxy default_ms_subtable(const String & subtable,
                                String name,
                                const Record & table_desc,
                                const Record & dminfo)
  {
    String table_ = subtable;
    table_.upcase();

    if(name.empty() || name == "MAIN") {
      name = "MeasurementSet.ms";
    }

    SetupNewTable setup_new_table = default_ms_factory(name,
      subtable, table_desc, dminfo);

    if(table_.empty() || subtable == "MAIN") {
      return TableProxy(MeasurementSet(setup_new_table));
    } else if(table_ == "ANTENNA") {
      return TableProxy(MSAntenna(setup_new_table));
    } else if(table_ == "DATA_DESCRIPTION") {
      return TableProxy(MSDataDescription(setup_new_table));
    } else if(table_ == "DOPPLER") {
      return TableProxy(MSDoppler(setup_new_table));
    } else if(table_ == "FEED") {
      return TableProxy(MSFeed(setup_new_table));
    } else if(table_ == "FIELD") {
      return TableProxy(MSField(setup_new_table));
    } else if(table_ == "FLAG_CMD") {
      return TableProxy(MSFlagCmd(setup_new_table));
    } else if(table_ == "FREQ_OFFSET") {
      return TableProxy(MSFreqOffset(setup_new_table));
    } else if(table_ == "HISTORY") {
      return TableProxy(MSHistory(setup_new_table));
    } else if(table_ == "OBSERVATION") {
      return TableProxy(MSObservation(setup_new_table));
    } else if(table_ == "POINTING") {
      return TableProxy(MSPointing(setup_new_table));
    } else if(table_ == "POLARIZATION") {
      return TableProxy(MSPolarization(setup_new_table));
    } else if(table_ == "PROCESSOR") {
      return TableProxy(MSProcessor(setup_new_table));
    } else if(table_ == "SOURCE") {
      return TableProxy(MSSource(setup_new_table));
    } else if(table_ == "SPECTRAL_WINDOW") {
      return TableProxy(MSSpectralWindow(setup_new_table));
    } else if(table_ == "STATE") {
      return TableProxy(MSState(setup_new_table));
    } else if(table_ == "SYSCAL") {
      return TableProxy(MSSysCal(setup_new_table));
    } else if(table_ == "WEATHER") {
      return TableProxy(MSWeather(setup_new_table));
    }

    throw TableError("Unknown table type: " + table_);
  }

  TableProxy default_ms(const String & name,
                        const Record & table_desc,
                        const Record & dminfo)
  {
    // Create the main Measurement Set
    SetupNewTable setup_new_table = default_ms_factory(name,
      "MAIN", table_desc, dminfo);
    MeasurementSet ms(setup_new_table);

    // Create the MS default subtables
    ms.createDefaultSubtables(Table::New);

    // Create a table proxy
    return TableProxy(ms);
  }

namespace python {

  void pyms()
  {
    def("_default_ms", &default_ms, (
      boost::python::arg("name"),
      boost::python::arg("table_desc")));
    def("_default_ms_subtable", &default_ms_subtable, (
      boost::python::arg("subtable"),
      boost::python::arg("table_desc")));
    def("_required_ms_desc", &required_ms_desc, (
      boost::python::arg("table")));
  }

}
}