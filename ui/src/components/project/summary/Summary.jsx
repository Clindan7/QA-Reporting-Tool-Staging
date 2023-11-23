import { useDispatch, useSelector } from "react-redux";
import PropTypes from "prop-types";
import BugDetail from "./BugDetail";
import OtherDetail from "./OtherDetail";
import ProjectDetail from "./ProjectDetail";
import classes from "./Summary.module.css";
import TestCaseDetail from "./TestCaseDetail";
import { useCallback, useEffect, useState } from "react";
import ProjectActions from "../../../redux/actions/ProjectActions";
import LoadingScreen from "../../ui/loader/Loader";
import RadioButton from "../../ui/buttons/RadioButton";

const Summary = ({ id }) => {

  const dispatch = useDispatch();
  const projectDetail = useSelector((state) => state?.ProjectReducer?.ProjectData || {})
  const bugDetail =useSelector((state)=>state?.BugDetailReducer?.BugData || {})
  const TcDetail =useSelector((state)=>state?.TcDetailReducer?.TcData || {})
  const isLoading = useSelector((state) => state?.ProjectReducer?.isLoading)
  const [docType, setDocType] = useState("1");

  const getProjectDetailData = useCallback(async () => {
    const testCaseCategory = docType === "1" ? "UI" : "API";
    dispatch(ProjectActions.ProjectDetailAsync(id))
    dispatch(ProjectActions.BugDetailAsync(id,testCaseCategory))
    dispatch(ProjectActions.TcDetailAsync(id,testCaseCategory))
  }, [dispatch, id,docType])

  useEffect(() => {
    getProjectDetailData();
  }, [id,docType])

  const refresh = (() => {
    getProjectDetailData()
  })

  return (
    <>
      {isLoading && <LoadingScreen />}

      <div className={classes.mainBox}>
        <RadioButton docType={docType} setDocType={setDocType} />
        
        <div className={classes.contentDiv}>
          <div className={classes.topBox}>
            <div className={classes.detailBox}>
              <div className={classes.project}>
                <ProjectDetail projectDetail={projectDetail} refresh={refresh} />
              </div>
              <div className={classes.project}>
                <BugDetail projectDetail={bugDetail} />
              </div>
            </div>
          </div>
          <div className={classes.lowerBox}>
            <div className={classes.detailBox}>
              <div className={classes.project}>
                <TestCaseDetail projectDetail={TcDetail} projectid={id} />
              </div>
              <div className={classes.project}>
                <OtherDetail projectDetail={projectDetail} refresh={refresh} />
              </div>
            </div>
          </div>
        </div>
      </div>

    </>
  )
}

Summary.propTypes = {
  id: PropTypes.any.isRequired,
};

export default Summary
