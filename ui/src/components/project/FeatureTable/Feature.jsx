import React, { useEffect, useState } from 'react';
import TableActions from '../../../redux/actions/TableActions';
import { useDispatch, useSelector } from "react-redux";
import "./Feature.css";
import RadioButton from "../../ui/buttons/RadioButton";
import LoadingScreen from '../../ui/loader/Loader';
import PropTypes from "prop-types";

const Feature = ({ id }) => {
  const [docType, setDocType] = useState("1");
  const tableData = useSelector((state) => state?.FeatureTblReducer?.tableData);
  const loading = useSelector((state) => state?.FeatureTblReducer?.isLoading);
  const dispatch = useDispatch()

  useEffect(() => {
    const fetchTblData = async () => {
      try {
        const testCaseCategory = docType === "1" ? "UI" : "API";
        dispatch(TableActions.FeatureTableAsync(id, testCaseCategory))
      } catch (error) {
        console.log(error);
      }
    }
    fetchTblData()

  }, [id, docType])

  return (
    <>
      {loading && <LoadingScreen />}
      <div className="mainBox">
        <RadioButton docType={docType} setDocType={setDocType} />
        <div className='ChartTbl'>
          {
            tableData.length > 0 ?
              (
                <table className='styledtable1'>
                  <thead>
                    <tr>
                      <th rowSpan="2">Feature</th>
                      <th colSpan="3">Number of functional testcases</th>
                      <th colSpan="3">Bugs</th>
                    </tr>
                    <tr>
                      <th>Total Tc</th>
                      <th>TC passed</th>
                      <th>Progress</th>
                      <th>Total Bugs</th>
                      <th>Detection rate</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tableData.map((row) => (
                      <tr key={row.feature}>
                        <td>{row.feature}</td>
                        <td style={{ backgroundColor: "#e8dcec" }}>{row?.total_tc}</td>
                        <td style={{ backgroundColor: "#e8dcec" }}>{row?.passed_tc}</td>
                        <td>{row?.progress}</td>
                        <td style={{ backgroundColor: "#ff9eac" }}>{row?.no_of_bugs}</td>
                        <td style={{ backgroundColor: "#ff9eac" }}>{row?.detection_rate}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <p className='noData'>No Table Data Found !!</p>
              )
          }
        </div>
      </div>
    </>
  );
};

Feature.propTypes = {
  id: PropTypes.any.isRequired,
};

export default Feature;
