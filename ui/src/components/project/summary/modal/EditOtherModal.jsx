import React, {useEffect,useState} from 'react';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import { useForm } from 'react-hook-form';
import "./editModal.css";
import { ProjectService } from '../../../../redux/services/ProjectService';
import { toast } from 'react-toastify';
import LoadingScreen from '../../../ui/loader/Loader';

const EditOtherModal=({ isOpen, onClose,projectDetail })=> {
    const {
        register,
        handleSubmit,
        formState: { errors },
        setValue,
        reset
      } = useForm();

      useEffect(() => {
        setValue("notes",projectDetail?.notes || "" ); 
        setValue("risk",projectDetail?.risk || "")
      }, [setValue,projectDetail,isOpen]);

      const id=projectDetail?.id || ""

    const [isLoading, setIsLoading] = useState(false);

    const onFormSubmit = async (data) => {
      setIsLoading(true);
    
      try {
        const res = await ProjectService.editProjectDetail(id, data);
    
        if (res?.status === 200) {
          toast.success("Project updated successfully");
          setIsLoading(false);
        } else {
          setIsLoading(false);
          toast.error("Project update failed!!");
        }
    
        onClose();
      } catch (error) {
        setIsLoading(false);
        toast.error(error.message);
      }
    };
    
      const handleClose=()=>{
        onClose()
        reset()
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
          borderRadius:"10px",
          width:"35%",
          backgroundColor:"white",
          border:"none",
          height:"550px",
          top:"50%",
          left:"50%",
          transform:"translate(-50%,-50%)",
          padding:"30px",
          position:"absolute"
        }}>

        <div className="titleDiv">
            <p className="modalTitle">Update Project Details</p>
          </div>

        <form id='EditForm' onSubmit={handleSubmit(onFormSubmit)} > 
              <br />
             
        <div className='formDiv1'>
        <label htmlFor='risk' className='formLabel'>
          Risk
        </label>
        <textarea
          id='risk'
          name='risk'
          className='textField1'
          autoComplete='off'
          {...register('risk', {
            pattern: {
              // value: /^(?!^\s+|\s+$).*$/, 
              value: /^(?![ \t\r\n])[\s\S]*(?<![ \t\r\n])$/,
              message: 'Please enter valid risk',
            },
            maxLength: {
              value: 100, 
              message: 'Risk should be at most 100 characters',
            },
          })}
          style={{ resize: 'none' }}
        />
      </div>

      <p className='errors'>{errors?.risk && errors?.risk?.message}</p>

        <div className='formDiv1'>
        <label htmlFor='notes' className='formLabel'>
          Notes
        </label>
        <textarea
          id='notes'
          name='notes'
          className='textField1'
          autoComplete='off'
          {...register('notes', {
            pattern: {
              // value: /^\S(.*\S)?$/, 
              value: /^(?![ \t\r\n])[\s\S]*(?<![ \t\r\n])$/,
              message: 'Please enter valid notes',
            },
            maxLength: {
              value: 100, 
              message: 'Notes should be at most 100 characters',
            },
          })}
          style={{ resize: 'none' }}
        />
      </div>

      <p className='errors'>{errors?.notes && errors?.notes?.message}</p>
            <div
              style={{
                width: "100%",
                display: "flex",
                justifyContent: "end",
              }}
            >
              <button className="button" type="submit">
                Confirm
              </button>
            </div>
        </form>
        {isLoading && <LoadingScreen />}
      </Box>
    </Modal>
  );
}

export default EditOtherModal;
