import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import OtherDetail from '../../summary/OtherDetail';

describe('OtherDetail Component', () => {
  it('should open and close the modal', () => {
    const projectDetail = {
      notes:"Client Meeting",
      risks:"High"
    };

    const { getByText, getByAltText, queryByText } = render(
      <OtherDetail projectDetail={projectDetail} refresh={() => {}} />
    );

    // Initially, the modal should be closed
    expect(queryByText('Update Project Details')).toBeNull();

    // Click on the edit icon to open the modal
    const editIcon = getByAltText('editIcon');
    fireEvent.click(editIcon);

    // After clicking, the modal should be open
    expect(getByText('Update Project Details')).toBeInTheDocument();

  })

  it('should render with the title "Other Details"', () => {
    const projectDetail = {
        notes:"Client Meeting",
        risks:"High"
    };

    const { getByText } = render(
      <OtherDetail projectDetail={projectDetail} refresh={() => {}} />
    );

    // Check if the title "Project Information" is present in the rendered component
    expect(getByText('Other Details')).toBeInTheDocument();
  });




});
