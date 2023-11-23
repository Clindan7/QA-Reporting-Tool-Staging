import React, { useEffect, useState } from 'react';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import { useForm } from 'react-hook-form';
import { toast } from 'react-toastify';
import LoadingScreen from '../../../ui/loader/Loader';
import { ProjectService } from '../../../../redux/services/ProjectService';
import "./editModal.css";


const EditModal = ({ isOpen, onClose, projectDetail }) => {
  const [isLoading, setIsLoading] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    reset,
    watch
  } = useForm();

  useEffect(() => {
    const defaultStatus = projectDetail?.status === 1 ? "active" : "inactive";
    setValue("status", defaultStatus);
    setValue("uat_release", projectDetail?.uat_release || "");
    setValue("release_date", projectDetail?.release_date || "");
    setValue("remarks", projectDetail?.remarks || "");
  }, [setValue, projectDetail, isOpen]);

  const id = projectDetail?.id || "";

  const onFormSubmit = async (data) => {
    setIsLoading(true);
    data.status = data.status === "active" ? 1 : 0;
    try {
      const res = await ProjectService.editProjectDetail(id, data);
      if (res?.status === 200) {
        toast.success("Project updated successfully");
      } else {
        toast.error("Project update failed!!");
      }
      onClose();
    } catch (error) {
      toast.error(error?.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    onClose();
    reset();
  };

  let requiredRemarks =
    (projectDetail?.status === 0 && watch('status') === 'active') ||
    (projectDetail?.uat_release !== watch('uat_release') && projectDetail?.uat_release !== null) ||
    (projectDetail?.release_date !== watch('release_date') && projectDetail?.release_date !== null);


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
          width: "35%",
          backgroundColor: "white",
          border: "none",
          height: "660px",
          top: "50%",
          left: "50%",
          transform: "translate(-50%,-50%)",
          padding: "30px",
          position: "absolute",
        }}
      >
        <div className="titleDiv">
          <p className="modalTitle">Update Project Details</p>
        </div>

        <form id='EditForm' onSubmit={handleSubmit(onFormSubmit)} >
          <br />
          <div className='formDiv'>
            <label htmlFor='status' className='formLabel'>
              Status
            </label>
            <select
              id={"status"}
              style={{ "background": "white" }}
              className='textField'
              autoComplete='off'
              {...register("status", {
                required: true,
              })}
            >
              <option value="active">Ongoing</option>
              <option value="inactive">Completed</option>
            </select>
          </div>
          <br />
          <div className='formDiv'>
            <label htmlFor='uat_release' className='formLabel'>
              UAT Release
            </label>
            <input
              id={"uat_release"}
              type={"date"}
              className='textField'
              autoComplete='off'
              data-testid="uat_release"
              onKeyDown={(e) => {
                e.preventDefault();
              }}
              {...register("uat_release", {
                required: true,
              })}
            />
          </div>
          <p className="errors">
            {errors.uat_release?.type === "required" &&
              "select a valid UAT release date"}
          </p>
          <div className='formDiv'>
            <label htmlFor='release_date' className='formLabel'>
              Production Release
            </label>
            <input
              id={"release_date"}
              type={"date"}
              className='textField'
              autoComplete='off'
              data-testid="release_date"
              onKeyDown={(e) => {
                e.preventDefault();
              }}
              {...register("release_date", {
                required: true,
              })}
            />
          </div>
          <p className="errors">
            {errors?.release_date?.type === "required" &&
              "select a valid production release date"}
          </p>

          <div className='formDiv1'>
            <label htmlFor='remarks' className='formLabel'>
              Remarks
            </label>
            <textarea
              id='remarks'
              name='remarks'
              className='textField1'
              autoComplete='off'
              {...register('remarks', {
                pattern: {
                  // value: /^(?! )(\S(.*\S)?)(?! )$/,
                  value: /^(?![ \t\r\n])[\s\S]*(?<![ \t\r\n])$/,
                  message: 'Please enter valid remark',
                },
                maxLength: {
                  value: 100,
                  message: 'Remark should be at most 100 characters',
                },
                minLength: {
                  value: 4,
                  message: "Remark should be at least 4 characters",
                },
                required: {
                  value: requiredRemarks,
                  message: 'Remarks is required',
                },
              })}
              style={{ resize: 'none' }}
            />
          </div>
          <p className='errors'>
            {errors?.remarks && errors?.remarks?.message}
          </p>
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

export default EditModal;
