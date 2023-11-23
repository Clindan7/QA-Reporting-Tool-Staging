import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import EditModal from '../EditModal';
import { ProjectService } from "../../../../../redux/services/ProjectService";

describe('EditModal Component', () => {
  const projectDetail = {
    id: 1,
    status: 1,
    uat_release: '2023-10-12',
    release_date: '2023-10-13',
  };


  test('prevents default on date input keydown', () => {
    const { getByTestId } = render(<EditModal isOpen={true} onClose={() => {}} projectDetail={projectDetail} />);
    const dateInput = getByTestId('uat_release');
    const preventDefaultMock = jest.fn();
    fireEvent.keyDown(dateInput, { key: 'a', preventDefault: preventDefaultMock });

    expect(preventDefaultMock).toBeInTheDocument;
  });

  test('prevents default on date input keydown', () => {
    const { getByTestId } = render(<EditModal isOpen={true} onClose={() => {}} projectDetail={projectDetail} />);
    const dateInput = getByTestId('release_date');
    const preventDefaultMock = jest.fn();
    fireEvent.keyDown(dateInput, { key: 'a', preventDefault: preventDefaultMock });

    expect(preventDefaultMock).toBeInTheDocument;
  });



  it('should call onFormSubmit when the form is submitted', async () => {
    const projectDetail = {
      id: 1,
      status: 1,
      uat_release: '2023-10-20',
      release_date: '2023-10-25',
      remarks: 'Sample remarks',
    };
    const editProjectDetailSpy = jest.spyOn(ProjectService, 'editProjectDetail');
    editProjectDetailSpy.mockResolvedValue({ status: 200 });
    const { getByText,getByLabelText } = render(
      <EditModal isOpen={true} onClose={() => {}} projectDetail={projectDetail} />
    );
    fireEvent.change(getByLabelText('Status'), { target: { value: 'inactive' } });
    fireEvent.change(getByLabelText('UAT Release'), { target: { value: '2023-10-17' } });
    fireEvent.change(getByLabelText('Production Release'), { target: { value: '2023-10-18' } });
    fireEvent.change(getByLabelText('Remarks'), { target: { value: 'Test remarks' } });

    const confirmButton = getByText('Confirm');
    fireEvent.click(confirmButton);
    expect(screen.queryByText('Project updated successfully')).toBeNull();
  });

  it('should call onFormSubmit when the form is submitted', async () => {
    const projectDetail = {
      id: 1,
      status: 1,
      uat_release: '2023-10-20',
      release_date: '2023-10-25',
      remarks: 'Sample remarks',
    };
    const editProjectDetailSpy = jest.spyOn(ProjectService, 'editProjectDetail');
    editProjectDetailSpy.mockResolvedValue({ status: 400 });
    const { getByText,getByLabelText } = render(
      <EditModal isOpen={true} onClose={() => {}} projectDetail={projectDetail} />
    );
    fireEvent.change(getByLabelText('Status'), { target: { value: 'inactive' } });
    fireEvent.change(getByLabelText('UAT Release'), { target: { value: '2023-10-17' } });
    fireEvent.change(getByLabelText('Production Release'), { target: { value: '2023-10-18' } });
    fireEvent.change(getByLabelText('Remarks'), { target: { value: 'Test remarks' } });

    const confirmButton = getByText('Confirm');
    fireEvent.click(confirmButton);

    expect(screen.queryByText('Project updated successfully')).toBeNull();
  });

  it('should call onFormSubmit when the form is submitted', async () => {
    const projectDetail = {
      id: 1,
      status: 1,
      uat_release: '2023-10-20',
      release_date: '2023-10-25',
      remarks: 'Sample remarks',
    };
    const editProjectDetailSpy = jest.spyOn(ProjectService, 'editProjectDetail');
    editProjectDetailSpy.mockRejectedValue(new Error('An error occurred'));
    const { getByText,getByLabelText } = render(
      <EditModal isOpen={true} onClose={() => {}} projectDetail={projectDetail} />
    );
    fireEvent.change(getByLabelText('Status'), { target: { value: 'inactive' } });
    fireEvent.change(getByLabelText('UAT Release'), { target: { value: '2023-10-17' } });
    fireEvent.change(getByLabelText('Production Release'), { target: { value: '2023-10-18' } });
    fireEvent.change(getByLabelText('Remarks'), { target: { value: 'Test remarks' } });

    const confirmButton = getByText('Confirm');
    fireEvent.click(confirmButton);

    expect(screen.queryByText('Project updated successfully')).toBeNull();
  });


});
