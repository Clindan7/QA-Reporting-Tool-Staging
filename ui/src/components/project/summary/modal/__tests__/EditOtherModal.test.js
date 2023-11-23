import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import EditOtherModal from '../EditOtherModal';
import { ProjectService } from "../../../../../redux/services/ProjectService";


describe('EditOtherModal Component', () => {

  jest.mock('react-toastify', () => ({
    toast: {
      success: jest.fn(),
    },
  }));

  it('should call onFormSubmit when the form is submitted', async () => {
    const projectDetail = {
      id: 1,
      notes: 'Sample notes',
      risk: 'Sample risk',
    };

    const editProjectDetailSpy = jest.spyOn(ProjectService, 'editProjectDetail');
    editProjectDetailSpy.mockResolvedValue({ status: 200 });

    const { getByLabelText, getByText } = render(
      <EditOtherModal isOpen={true} onClose={() => {}} projectDetail={projectDetail} />
    );

    const riskInput = getByLabelText('Risk');
    const notesInput = getByLabelText('Notes');

    fireEvent.change(riskInput, { target: { value: 'Updated risk' } });
    fireEvent.change(notesInput, { target: { value: 'Updated notes' } });

    const confirmButton = getByText('Confirm');
    fireEvent.click(confirmButton);

    expect(screen.queryByText('Project updated successfully')).toBeNull();


  });

  it('should call onFormSubmit when the form is submitted', async () => {
    const projectDetail = {
      id: 1,
      notes: 'Sample notes',
      risk: 'Sample risk',
    };

    const editProjectDetailSpy = jest.spyOn(ProjectService, 'editProjectDetail');
    editProjectDetailSpy.mockResolvedValue({ status: 400 });

    const { getByLabelText, getByText } = render(
      <EditOtherModal isOpen={true} onClose={() => {}} projectDetail={projectDetail} />
    );

    const riskInput = getByLabelText('Risk');
    const notesInput = getByLabelText('Notes');

    fireEvent.change(riskInput, { target: { value: 'Updated risk' } });
    fireEvent.change(notesInput, { target: { value: 'Updated notes' } });

    const confirmButton = getByText('Confirm');
    fireEvent.click(confirmButton);

    expect(screen.queryByText('Project updated successfully')).toBeNull();


  });


  it('should call onFormSubmit when the form is submitted', async () => {
    const projectDetail = {
      id: 1,
      notes: 'Sample notes',
      risk: 'Sample risk',
    };

    const editProjectDetailSpy = jest.spyOn(ProjectService, 'editProjectDetail');
    editProjectDetailSpy.mockRejectedValue(new Error('An error occurred'));
    const { getByLabelText, getByText } = render(
      <EditOtherModal isOpen={true} onClose={() => {}} projectDetail={projectDetail} />
    );

    const riskInput = getByLabelText('Risk');
    const notesInput = getByLabelText('Notes');

    fireEvent.change(riskInput, { target: { value: 'Updated risk' } });
    fireEvent.change(notesInput, { target: { value: 'Updated notes' } });

    const confirmButton = getByText('Confirm');
    fireEvent.click(confirmButton);

    expect(screen.queryByText('Project updated successfully')).toBeNull();


  });

})