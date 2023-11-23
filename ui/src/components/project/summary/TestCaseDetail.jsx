import "./detail.css"
import DetailContent from '../summary/modal/DetailContent';
import PropTypes from 'prop-types';


const TestCaseDetail = ({projectDetail, projectid}) => {

const progress = projectDetail?.project_progress || 0; 

const formattedProgress = parseFloat(progress).toFixed(2);
  return (
    <>
       <div className="projectBox">
       <div className='title'>
            Test Case Summary
        </div>
      <DetailContent title="Total No of TC" content={projectDetail?.total_test_cases} />
       <DetailContent title="Executed" content={projectDetail?.executed_test_cases} />
       <DetailContent title="Passed" content={projectDetail?.passed_test_cases} />
       <DetailContent title="Failed" content={projectDetail?.failed_test_cases} />
       <DetailContent title="Not Executed" content={projectDetail?.not_executed_test_cases} />
       <DetailContent title="Project Progress" content={`${formattedProgress} %`} />
       <DetailContent title="Not yet Tested" content={projectDetail?.not_yet_tested} />
       <DetailContent title="Remaining Tc to Execute" content={projectDetail?.remaining_tc_to_execute} />
      <a href={`/project/${projectid}/testcase`} style={{paddingLeft: "25px"}}>Go to Testcase document</a>
       </div>
    </>
  )
}


TestCaseDetail.propTypes={
  projectDetail:PropTypes.any,
  projectid : PropTypes.string
}

export default TestCaseDetail
