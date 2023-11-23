import React from 'react';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import ErrorIcon from "../../../../assets/docError.svg";
import "./ErrorModal.css"
import PropTypes from 'prop-types';

const ErrorModal = ({ isOpen, handleClose, errorMessage }) => {
  let errorMessageContent;

  if (Array.isArray(errorMessage) && errorMessage.every(item => typeof item === 'object')) {
    errorMessageContent = 'data_mismatch';
  } else if (errorMessage.message) {
    errorMessageContent = errorMessage.message;
  } else {
    errorMessageContent = errorMessage;
  }


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
          width: "600px",
          backgroundColor: "white",
          border: "none",
          height: "400px",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          position: "absolute",
        }}
      >
        <div className="modal">
          <div className="modalContent">
            <img src={ErrorIcon} alt='Error' className='errorLogo' />
            <p className='font'>Oops, something went wrong !!</p>
          </div>
          {(errorMessageContent === 'data_mismatch') ?
            errorMessage.map((item) => (
              <span key={item} className='list-error'>
                {Object.keys(item.errors).map((key) => (
                  <p key={key}>{item.errors[key].message}</p>
                ))}
              </span>
            )) :
            <div className='errorMessages'>{errorMessageContent}</div>
          }

        </div>
      </Box>
    </Modal>
  );
};

ErrorModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  handleClose: PropTypes.func.isRequired,
  errorMessage: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.arrayOf(PropTypes.object),
    PropTypes.shape({
      message: PropTypes.string,
    }),
  ]).isRequired,
};

export default ErrorModal;
