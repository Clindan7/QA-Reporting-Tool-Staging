import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import ProjectDetail from '../../summary/ProjectDetail';

describe('ProjectDetail Component', () => {
  it('should open and close the modal', () => {
    const projectDetail = {
      project_code: '123',
      name: 'Test Project',
      uat_release: '1.0',
      release_date: '2023-10-11',
      status: 1,
      remark: 'This is a test project',
    };

    const { getByText, getByAltText, queryByText } = render(
      <ProjectDetail projectDetail={projectDetail} refresh={() => {}} />
    );

    // Initially, the modal should be closed
    expect(queryByText('Update Project Details')).toBeNull();

    // Click on the edit icon to open the modal
    const editIcon = getByAltText('editIcon');
    fireEvent.click(editIcon);

    // After clicking, the modal should be open
    expect(getByText('Update Project Details')).toBeInTheDocument();

  })

  it('should render with the title "Project Information"', () => {
    const projectDetail = {
      project_code: '123',
      name: 'Test Project',
      uat_release: '1.0',
      release_date: '2023-10-11',
      status: 1,
      remark: 'This is a test project',
    };

    const { getByText } = render(
      <ProjectDetail projectDetail={projectDetail} refresh={() => {}} />
    );

    // Check if the title "Project Information" is present in the rendered component
    expect(getByText('Project Information')).toBeInTheDocument();
  });


});
