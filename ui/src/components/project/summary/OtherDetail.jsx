import "./detail.css"
import PropTypes from 'prop-types';
import edit from "../../../assets/edit.svg"
import EditOtherModal from './modal/EditOtherModal';
import { useState } from "react";
import DetailContent from "./modal/DetailContent";

const OtherDetail = ({projectDetail,refresh}) => {

  const[isModalOpen,setIsModalOpen] =useState(false);
  const openModal =()=>{
    setIsModalOpen(true)
  }
  const closeModal=()=>{
    setIsModalOpen(false)
    refresh()
  }
  return (
    <>
    <div className="projectBox">
    <div className='title'>
            Other Details
            <img className="editIcon" src={edit} alt="editIcon" title="edit" onClick={() => {
            openModal();
            }} />
        </div>
         <DetailContent title="Risk" content={projectDetail?.risk} />
        <DetailContent title="Notes" content={projectDetail?.notes}  />
    </div>
    <EditOtherModal isOpen={isModalOpen} onClose={closeModal} projectDetail={projectDetail} />
 </>
  )
}

OtherDetail.propTypes={
  projectDetail:PropTypes.any
}

export default OtherDetail