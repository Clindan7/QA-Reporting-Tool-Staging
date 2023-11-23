import React, { useRef, useState, useEffect } from "react";
import PropTypes from 'prop-types';
import { useSelector, useDispatch } from 'react-redux';
import { GoUpload } from 'react-icons/go';
import fileActions from "../../../redux/actions/fileActions";
import ErrorModal from "./ErrorModal/ErrorModal";
import './ImportExport.css'
import LoadingScreen from "../../ui/loader/Loader";
import { clearImportExportError } from "../../../redux/reducers/fileReducer";
import RadioButton from "../../ui/buttons/RadioButton";

const ImportExport = ({ id, docType, onDocTypeChange }) => {
    const inputRef = useRef(null);
    const [isError, setIsError] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const isLoading = useSelector((state) => state?.FileReducer?.isLoading)
    const fileError = useSelector((state) => state?.FileReducer?.errors || {})
    const dispatch = useDispatch();
    const [sweepCount, setSweepCount] = useState("");

    const openModal = () => {
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
        dispatch(clearImportExportError())
    };

    const handleDocTypeChangeChild = (newDocType) => {
        onDocTypeChange(newDocType);
    };

    const isNumberKey = (evt) => {
        let charCode = evt.which ? evt.which : evt.keyCode;

        if (
            (charCode > 31 &&
                (charCode < 48 || charCode > 57) &&
                (charCode < 96 || charCode > 105)) ||
            evt.shiftKey
        ) {
            evt.preventDefault();
        }
        return true;
    };

    const handleClick = () => {
        if ((docType === "1" || docType === "2") && (!sweepCount)) {
            setIsError('Sweep Count is required');
            openModal();
        }
        else if(sweepCount && sweepCount > 4){
            setIsError('Sweep Count cannot be greater than 4');
            openModal();
        }
        else {
            inputRef.current.click();
        }
    };

    const handleFileChange = async (event) => {
        const fileObj = event.target.files ? event.target.files[0] : null;
        if (!fileObj) {
            setIsError('No file selected');
            openModal();
            return;
        }
        const fileType = fileObj.name.split('.').pop().toLowerCase();
        if (fileType !== 'xlsx') {
            setIsError('File type must be xlsx');
            openModal();
            return;
        }

        try {
            dispatch(fileActions.ImportExportAsync(fileObj, id, docType, sweepCount));
        } catch (error) {
            console.error('Error while importing the file', error);
        }
        event.target.value = null;
        setSweepCount('');
    };

    useEffect(() => {
        if (Object.keys(fileError)?.length > 0) {
            setIsError(fileError);
            openModal();
        }
    }, [fileError, isModalOpen]);

    return (
        <>
            {isLoading && <LoadingScreen />}
            <div className="d-grid gap-2 d-md-flex justify-content-end pad-rite">
                <div className="form-floating">
                    <input className="form-control custom-input" id="sweepCount"
                        value={sweepCount} onKeyDown={isNumberKey}
                        onChange={(e) => setSweepCount(e.target.value)} />
                    <label htmlFor="sweepCount">
                        Sweep Count<span style={{ color: "red" }}>&nbsp;*</span>
                    </label>
                </div>
                <RadioButton docType={docType} setDocType={handleDocTypeChangeChild} />
                <input
                    style={{ display: 'none' }}
                    ref={inputRef}
                    type="file"
                    accept=".xlsx"
                    data-testid="file-input"
                    onChange={handleFileChange}
                />
                <button
                    className="btn btn-import me-md-2"
                    type="button" data-testid="import-btn"
                    onClick={handleClick}>
                    <GoUpload className="icn-import" />Import
                </button>
            </div>

            {isError ? (
                <ErrorModal isOpen={isModalOpen} handleClose={closeModal} errorMessage={isError} />
            ) : null}
        </>
    )
}

ImportExport.prototypes = {
    id: PropTypes.any.isRequired,
    docType: PropTypes.any.isRequired,
    onDocTypeChange: PropTypes.func.isRequired,
}

export default ImportExport;
