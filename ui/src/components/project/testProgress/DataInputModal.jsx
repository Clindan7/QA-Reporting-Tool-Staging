import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from "react-redux";
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import './TestProgress.css'
import InputRow from './InputRow';
import PropTypes from 'prop-types';
import { toast } from "react-toastify";
import ChartActions from "../../../redux/actions/chartActions";
import { chartService } from "../../../redux/services/ChartService";
import LoadingScreen from '../../ui/loader/Loader';

const DataInputModal = ({ isOpen, handleClose, projectid, docType }) => {
    const dispatch = useDispatch();
    const inputData = useSelector((state) => state?.TCCountInputReducer?.TCInputData || {});
    const isLoading = useSelector((state) => state?.TCCountInputReducer?.isLoading || false);
    const [loading, setLoading] = useState(false);
    const [todayData, setTodayData] = useState([]);


    const handleSave = (date, executed_test_case_count, passed_test_case_count) => {
        const updatedData = todayData.map((item) => {
          if (item.date_of_execution === date) {
            return {
              ...item,
              executed_test_case_count,
              passed_test_case_count,
            };
          }
          return item;
        });
        setTodayData([...updatedData]);
      };


    const saveChanges = async () => {
        handleClose();
        try {
            setLoading(true);
            const response = await chartService.updateTestInputData(projectid, docType, todayData);
            if (response?.status === 200) {
                toast.success("Test progress data updated! Updating Report.....")
                fetchData()
            } else {
                toast.error("Failed to update Test progress data")
            }
        } catch (error) {
            console.log(error);
            toast.error("An error occurred while update Test progress data");
        }
        finally {
            setLoading(false);
        }
    }

    const fetchData = async () => {
        try {

            const testCaseCategory = docType === "1" ? "UI" : "API";
            dispatch(ChartActions.TestInputDataAsync(projectid, testCaseCategory));
            setTodayData(inputData?.today);
        } catch (error) {
            console.error("error", error);
        }
    };

    useEffect(() => {
        if (isOpen) {
            fetchData();
        }
    }, [projectid, isOpen, docType]);

    return (
        <Modal
            open={isOpen}
            onClose={handleClose}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
        >
            <Box
                sx={{
                    borderRadius: "10px",
                    width: "50%",
                    backgroundColor: "white",
                    border: "none",
                    height: "500px",
                    overflowY: "auto",
                    scrollbarWidth: "thin",
                    top: "50%",
                    left: "50%",
                    transform: "translate(-50%, -50%)",
                    position: "absolute",
                }}
            >
                {(isLoading || loading) && <LoadingScreen />}
                <div className="modal-container">
                    <div className="modal-content">
                        <h3 className='head-style'>Test Progress data</h3>
                        <p className='head-style'>Enter the TC counts corresponding to the given dates</p>
                    </div>
                    <table className="styled-table">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>TC Executed/day</th>
                                <th>TC Passed/day</th>
                            </tr>
                        </thead>

                        <tbody>
                            {inputData?.previous && Object.keys(inputData?.previous).length > 0 ? (
                                Object.values(inputData?.previous).flatMap((weekData) =>
                                    weekData.map((item) => (
                                        <InputRow
                                            key={item.date_of_execution} 
                                            data={item}
                                            onDataUpdate={handleSave}
                                            editable={false}
                                        />
                                    ))
                                )
                            ) : (
                                <tr></tr>
                            )}
                            {inputData?.today?.length > 0 ? inputData?.today?.map((item) => (
                                <InputRow
                                    key={item.date_of_execution}
                                    data={item}
                                    onDataUpdate={handleSave}
                                    editable={true}
                                />
                            )) : <tr></tr>}
                        </tbody>
                    </table>
                    <div className='d-grid gap-2 d-md-flex bottom-right-button'>
                        <button
                            className="btn btn-enter me-md-2 "
                            type="button"
                            onClick={saveChanges}>
                            Save Data
                        </button></div>
                </div>
            </Box>
        </Modal>
    );
};
DataInputModal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    handleClose: PropTypes.func.isRequired,
    projectid: PropTypes.any.isRequired,
    docType: PropTypes.any.isRequired
};
export default DataInputModal;