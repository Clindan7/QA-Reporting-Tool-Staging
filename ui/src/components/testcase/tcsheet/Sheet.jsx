import { useMemo, useRef, useCallback, useEffect, useState } from "react";
import { useDispatch, useSelector } from 'react-redux';
import PropTypes from 'prop-types';
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

import './Sheet.css';
import TestCaseAction from "../../../redux/actions/TestCaseActions";
import LoadingScreen from '../../ui/loader/Loader';

const Sheet = ({ sheetName, projectId, docType }) => {
  const tcSheetList = useSelector((state) => state?.TCSheetListReducer?.TCSheetList || {});
  const sheetData = useSelector((state) => state?.TCSheetDetailReducer?.SheetData || {});
  const isLoading = useSelector((state) => state?.TCSheetDetailReducer?.isLoading)
  const [rowData, setRowData] = useState();
  const dispatch = useDispatch();

  const getSheetData = useCallback(async (sheet, id, docType) => {
    dispatch(TestCaseAction.SheetDetailAsync(sheet, id, docType))
  }, [dispatch])

  useEffect(() => {
    console.log(sheetName);
    if(tcSheetList?.length > 0){
      (sheetName ) ? getSheetData(sheetName, projectId, docType) : getSheetData(tcSheetList[0], projectId,docType);
      if (sheetData && docType)
          onGridReady()
    }
  }, [sheetName, projectId, tcSheetList,docType])

  const gridRef = useRef();
  const defaultColDef = useMemo(() => ({
    editable: false,
    sortable: false,
    wrapHeaderText: true
  }));

  const getRowId = useMemo(() => {
    return (params) => params.data.id;
  }, []);

  const onGridReady = useCallback(() => {
    const newData = sheetData?.rows?.map((item, index) => ({
      ...item,
      id: index
    }));
    setRowData(newData);
    console.log(rowData);
  }, [sheetData]);

  return (
    <>
      {isLoading && <LoadingScreen />}
      <div className="outerBox" >
        <div className="content">
          <div className="ag-theme-alpine pl-5 grid-styl" >
            <AgGridReact
              ref={gridRef}
              rowData={(sheetData?.rows) ? sheetData?.rows : []}
              columnDefs={(sheetData?.columns) ? sheetData?.columns : []}
              defaultColDef={defaultColDef}
              stopEditingWhenCellsLoseFocus
              getRowId={getRowId}
              readOnlyEdit={true}
              onGridReady={onGridReady}
              tooltipShowDelay={0}
            ></AgGridReact>
          </div>
        </div>
      </div>
    </>
  )
}

Sheet.propTypes = {
  sheetName: PropTypes.any,
  projectId: PropTypes.any,
  docType: PropTypes.any
}

export default Sheet