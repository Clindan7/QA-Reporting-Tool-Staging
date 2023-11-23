import "./detail.css"
import DetailContent from './modal/DetailContent';
import PropTypes from 'prop-types';
import edit from "../../../assets/edit.svg"
import { useState } from "react";
import EditModal from "./modal/EditModal";


const ProjectDetail = ({projectDetail,refresh}) => {


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
        <div className='title' >
            Project Information       
            <img className="editIcon" src={edit} alt="editIcon" title="edit"  onClick={() => {
            openModal();
        }}/>
        </div>
      <DetailContent title="Project Code" content={projectDetail?.project_code} />
      <DetailContent title="Project Title" content={projectDetail?.name} />
      <DetailContent title="UAT Release" content={projectDetail?.uat_release} />
      <DetailContent title="Production Release" content={projectDetail?.release_date} />
      <DetailContent title="Project Status" content={projectDetail?.status === 1 ? "Ongoing" : "Completed"} />
      {
        projectDetail?.remarks && <DetailContent title="Remarks" content={projectDetail?.remarks} />
      }
       </div>
       <EditModal isOpen={isModalOpen} onClose={closeModal} projectDetail={projectDetail}/>
    </>
  )
}

ProjectDetail.propTypes = {
  projectDetail : PropTypes.any
}


export default ProjectDetail
