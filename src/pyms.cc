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

  Record required_ms_desc(const String & table)
  {
    String table_ = table;

    // Upper case things to be sure
    table_.upcase();

    if(table_.empty() || table_ == "MAIN")
    {
      return TableProxy::getTableDesc(MeasurementSet::requiredTableDesc(), true);
    }
    else if(table_ == "ANTENNA")
    {
      return TableProxy::getTableDesc(MSAntenna::requiredTableDesc(), true);
    }
    else if(table_ == "DATA_DESCRIPTION")
    {
      return TableProxy::getTableDesc(MSDataDescription::requiredTableDesc(), true);
    }
    else if(table_ == "DOPPLER")
    {
      return TableProxy::getTableDesc(MSDoppler::requiredTableDesc(), true);
    }
    else if(table_ == "FEED")
    {
      return TableProxy::getTableDesc(MSFeed::requiredTableDesc(), true);
    }
    else if(table_ == "FIELD")
    {
      return TableProxy::getTableDesc(MSField::requiredTableDesc(), true);
    }
    else if(table_ == "FLAG_CMD")
    {
      return TableProxy::getTableDesc(MSFlagCmd::requiredTableDesc(), true);
    }
    else if(table_ == "FREQ_OFFSET")
    {
      return TableProxy::getTableDesc(MSFreqOffset::requiredTableDesc(), true);
    }
    else if(table_ == "HISTORY")
    {
      return TableProxy::getTableDesc(MSHistory::requiredTableDesc(), true);
    }
    else if(table_ == "OBSERVATION")
    {
      return TableProxy::getTableDesc(MSObservation::requiredTableDesc(), true);
    }
    else if(table_ == "POINTING")
    {
      return TableProxy::getTableDesc(MSPointing::requiredTableDesc(), true);
    }
    else if(table_ == "POLARIZATION")
    {
      return TableProxy::getTableDesc(MSPolarization::requiredTableDesc(), true);
    }
    else if(table_ == "PROCESSOR")
    {
      return TableProxy::getTableDesc(MSProcessor::requiredTableDesc(), true);
    }
    else if(table_ == "SOURCE")
    {
      return TableProxy::getTableDesc(MSSource::requiredTableDesc(), true);
    }
    else if(table_ == "SPECTRAL_WINDOW")
    {
      return TableProxy::getTableDesc(MSSpectralWindow::requiredTableDesc(), true);
    }
    else if(table_ == "STATE")
    {
      return TableProxy::getTableDesc(MSState::requiredTableDesc(), true);
    }
    else if(table_ == "SYSCAL")
    {
      return TableProxy::getTableDesc(MSSysCal::requiredTableDesc(), true);
    }
    else if(table_ == "WEATHER")
    {
      return TableProxy::getTableDesc(MSWeather::requiredTableDesc(), true);
    }

    throw TableError("Unknown table type: " + table_);
  }

  TableProxy default_ms(const String & name, const Record & table_desc)
  {
    String msg;
    TableDesc user_td;

    // Create Table Description object from extra user table description
    if(!TableProxy::makeTableDesc(table_desc, user_td, msg))
    {
      throw TableError("Error Making Table Description " + msg);
    }

    user_td.show(std::cout);


    TableDesc required_td = MeasurementSet::requiredTableDesc();

    // Overwrite required columns with user columns
    for(uInt i=0; i < user_td.ncolumn(); ++i)
    {
      const String & name = user_td[i].name();

      // Remove if present in required
      if(required_td.isColumn(name))
      {
        required_td.removeColumn(name);
      }

      // Add the column
      required_td.addColumn(user_td[i]);
    }

    // Overwrite required hypercolumns with user hypercolumns
    // In practice this shouldn't be necessary as requiredTableDesc
    // doesn't define hypercolumns by default...
    Vector<String> user_hc = user_td.hypercolumnNames();

    for(uInt i=0; i < user_hc.size(); ++i)
    {
      // Remove if hypercolumn is present
      if(required_td.isHypercolumn(user_hc[i]))
      {
        required_td.removeHypercolumnDesc(user_hc[i]);
      }

      Vector<String> dataColumnNames;
      Vector<String> coordColumnNames;
      Vector<String> idColumnNames;

      // Get the user hypercolumn
      uInt ndims = user_td.hypercolumnDesc(user_hc[i],
          dataColumnNames, coordColumnNames, idColumnNames);
      // Place it in required_td
      required_td.defineHypercolumn(user_hc[i], ndims,
          dataColumnNames, coordColumnNames, idColumnNames);
    }

    // Overwrite required keywords with user keywords
    required_td.rwKeywordSet().merge(user_td.keywordSet(),
      RecordInterface::OverwriteDuplicates);

    required_td.show(std::cout);

    // Setup table definition
    SetupNewTable new_table(name, required_td, Table::New);

    // Create the MS
    MeasurementSet ms(new_table);

    // Create the default subtables
    ms.createDefaultSubtables(Table::New);

    // Create a table proxy
    return TableProxy(ms);
  }

namespace python {

  void pyms()
  {
    def("_default_ms", &default_ms, (boost::python::arg("name")));
    def("_required_ms_desc", &required_ms_desc, (boost::python::arg("column")));
  }

}
}