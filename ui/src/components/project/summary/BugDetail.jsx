import React from 'react'
import "./detail.css"
import DetailContent from './modal/DetailContent';
import PropTypes from 'prop-types';

const BugDetail = ({projectDetail}) => {
  return (
    <>
    <div className="projectBox">
    <div className='title'>
            Bug Statistics
        </div>
       <DetailContent title="Total Bugs reported" content={projectDetail?.total_bugs_reported} />
       <DetailContent title="Open Bugs" content={projectDetail?.open_bugs} />
       <DetailContent title="Closed Bugs" content={projectDetail?.closed_bugs} />
       <DetailContent title="Bugs InProgress" content={projectDetail?.bugs_in_progress} />
       <DetailContent title="Resolved Bugs" content={projectDetail?.resolved_bugs} />
       <DetailContent title="Bugs Reports by Client" content={projectDetail?.bugs_reported_by_client} />

    </div>
 </>
  )
}

BugDetail.propTypes={
  projectDetail:PropTypes.any
}


export default BugDetail
