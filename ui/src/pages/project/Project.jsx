import { useState} from "react";
import { useParams } from "react-router-dom";
import classes from "./Project.module.css";
import Summary from "../../components/project/summary/Summary";
import TestProgress from "../../components/project/testProgress/TestProgress";
import Severity from "../../components/project/Severity/Severity";
import FeatureTable from "../../components/project/FeatureTable/Feature";
import BugCount from "../../components/project/FeatureBugCount/BugCount";

const Project = () => {
  const [activeTab, setActiveTab] = useState('Summary');
  const { id } = useParams();

  const handleTabClick = (tab) => {
    setActiveTab(tab);
  };

  const tabDefinitions = [
    { key: 'Summary', label: 'Summary Report', component: <Summary id={id} /> },
    { key: 'Progress', label: 'Test Progress Report', component: <TestProgress id={id}/> },
    { key: 'Severity', label: 'Severity Wise Report', component: <Severity id={id}/> },
    { key: 'feature', label: 'Feature Wise Summary Report', component: <FeatureTable id={id}/> },
    { key: 'bugcount', label: 'Feature Wise Bug Count', component: <BugCount id={id}/> },
  ];

  const tabList = tabDefinitions.map(({ key, label }) => (
    <li
      key={key} data-testid={key}
      className={`${classes.listElement} ${activeTab === key ? classes.active : classes.inactive}`}
      onClick={() => handleTabClick(key)}
    >
      {label}
    </li>
  ));

  const activeComponent = tabDefinitions.find(({ key }) => key === activeTab)?.component;

  return (
    <div>
      <div className={classes.tab}>
        <ul className={classes.listStyle}>{tabList}</ul>
      </div>

      {activeComponent}
    </div>
  );
};

export default Project;