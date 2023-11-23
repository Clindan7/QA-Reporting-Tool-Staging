import { useState, useCallback, useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from "react-router-dom";
import "./Testcase.css";
import Sheet from "../../components/testcase/tcsheet/Sheet";
import ImportExport from "../../components/testcase/import-export/ImportExport";
import TestCaseAction from "../../redux/actions/TestCaseActions";
import LoadingScreen from '../../components/ui/loader/Loader';
import { setTCSheetListData } from "../../redux/reducers/TCSheetListReducer";

const Testcase = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [currentSheet, setCurrentSheet] = useState(0);
  const [docType, setDocType] = useState("1"); // Lifted state of radio button
  const tcSheetList = useSelector((state) => state?.TCSheetListReducer?.TCSheetList || {});
  const isLoading = useSelector((state) => state?.TCSheetListReducer?.isLoading);
  const errorMessage = useSelector((state) => state?.TCSheetListReducer?.errors.message);
  const importResponse = useSelector((state) => state?.FileReducer?.importResponse);
  const dispatch = useDispatch();
  const { id } = useParams();

  const getTCSheetList = useCallback(async (id, docType) => {
    dispatch(TestCaseAction.SheetListAsync(id, docType))
  }, [dispatch])

  useEffect(() => {
    getTCSheetList(id, docType);
    setCurrentSheet(tcSheetList ? (tcSheetList[0]) : "");
    setActiveTab(0);
    return(()=>{
      dispatch(setTCSheetListData([]));
    });
  }, [importResponse,docType])

  const handleTabClick = (index) => {
    setActiveTab(index);
    setCurrentSheet(tcSheetList[index]);
  };

   // Callback function to update docType in Testcase component
   const handleDocTypeChange = (newDocType) => {
    setDocType(newDocType);
  };

  useEffect(()=>{
    setCurrentSheet(tcSheetList ? (tcSheetList[0]) : "");
  },[tcSheetList])

  return (
    <div className="container">
      <ImportExport id={id} docType={docType} onDocTypeChange={handleDocTypeChange}/>
      <div className="tab-style">
        {isLoading && <LoadingScreen />}
        <ul className="nav nav-tabs nav-style" id="myTab" role="tablist">
          {tcSheetList?.length > 0 ?
            (tcSheetList.map((tab, index) => (
              <li className="nav-item" role="presentation" key={tab}>
                <button
                  className={`${index === activeTab ? 'nav-link active tab-btn btn' : 'nav-link tab-btn btn'}`}
                  onClick={() => handleTabClick(index)}
                  id={tab} data-bs-toggle="tab" data-bs-target={tab} type="button" role="tab"
                  aria-controls={tab} aria-selected="true">{tab} </button>
              </li>
            ))) : <p className='no_data'>Testcase Document Not Found</p>}
        </ul>
        {!errorMessage && <div className="tab-content" style={{ paddingTop: "4rem", overflowY:"scroll !important" , position:"relative"}} id="myTabContent">
          <div
            className="tab-pane fade show active"
            id="current-tab" role="tabpanel" aria-labelledby="current-tab">
            <Sheet sheetName={currentSheet} projectId={id} docType={docType}/>
          </div>
        </div>}
        
      </div>
    </div>
  )
}

export default Testcase
