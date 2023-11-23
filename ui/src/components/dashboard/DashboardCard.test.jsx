
import { render } from "@testing-library/react";
import DashboardCard from './DashboardCard';

const project = {
  name: 'Test Project',
  release_date: '2023-10-10',
  issue_count: 5,
  bugsByClient: 2,
  notes: 'Some notes',
  risk: 'Some risks',
};

describe('<DashboardCard>', () => {
  it('Test 1: should render component with props', () => {
    render(<DashboardCard project={project} />);
      expect(<DashboardCard />).toBeTruthy();
  });

  it('Test 2: renders with project data', () => {
    const { getByText } = render(<DashboardCard project={project} />);
    expect(getByText('Test Project')).toBeInTheDocument();
    expect(getByText('Release Date')).toBeInTheDocument();
    expect(getByText('Open bugs')).toBeInTheDocument();
    expect(getByText('Bugs reported by Client')).toBeInTheDocument();
    expect(getByText('Notes')).toBeInTheDocument();
    expect(getByText('Risk')).toBeInTheDocument();
    expect(getByText('2023-10-10')).toBeInTheDocument();
    expect(getByText('5')).toBeInTheDocument();
    expect(getByText('2')).toBeInTheDocument();
    expect(getByText('Some notes')).toBeInTheDocument();
    expect(getByText('Some risks')).toBeInTheDocument();
  });

  it('Test 3: renders without project data', () => {
    const { getByText, queryAllByText } = render(<DashboardCard project={null} />);
    const emptyContent = queryAllByText('')
    expect(emptyContent.length).not.toBe(0);
    expect(getByText('Release Date')).toBeInTheDocument();
    expect(getByText('Open bugs')).toBeInTheDocument();
    expect(getByText('Bugs reported by Client')).toBeInTheDocument();
    expect(getByText('Notes')).toBeInTheDocument();
  });
});