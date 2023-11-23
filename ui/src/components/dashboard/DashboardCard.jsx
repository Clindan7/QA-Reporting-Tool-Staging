import PropTypes from 'prop-types';
import CardContent from "./CardContent";
import './DashboardCard.css'

const DashboardCard = ({ project }) => {

  return (
    <div>
      <div className="card-body">
        <h5 className="card-title card_title_style"  >
          {project?.name}
        </h5>
        <CardContent title="Release Date" content={project?.release_date} />
        <CardContent title="Open bugs" content={project?.issue_count} />
        <CardContent title="Bugs reported by Client" content={project?.bugsByClient} />
        <CardContent title="Notes" content={project?.notes} />
        {project?.risk && <CardContent title="Risk" content={project?.risk} />}
      </div>
    </div>
  )
}

DashboardCard.propTypes = {
  project: PropTypes.any
}

export default DashboardCard
