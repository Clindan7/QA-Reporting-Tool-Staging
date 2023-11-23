import React from 'react';
import { render, screen } from '@testing-library/react';
import ErrorModal from './ErrorModal';

const errorMessage = {
  error_code: 1100,
  message: 'This is an error message.'
};
const handleClose = jest.fn();

describe('ErrorModal', () => {
  it('renders the ErrorModal component with the provided error message', () => {
    render(<ErrorModal isOpen={true} handleClose={handleClose} errorMessage={errorMessage} />);

    const errorMessages = screen.getByText(errorMessage.message);
    expect(errorMessages).toBeInTheDocument();

  });

  it('does not render the ErrorModal when isOpen is false', () => {
   
    render(<ErrorModal isOpen={false} handleClose={handleClose} errorMessage={errorMessage} />);

    const modal = screen.queryByRole('presentation');
    expect(modal).not.toBeInTheDocument();
  });

  it('render the ErrorModal with a list of errors when "errorMessage" is an array of objects', () => {
    const errorArray = [
      {
        errors: {
          field1: { message: 'Error 1' },
          field2: { message: 'Error 2' },
        },
      },
      {
        errors: {
          field3: { message: 'Error 3' },
          field4: { message: 'Error 4' },
        },
      },
    ];
    render(<ErrorModal isOpen={true} handleClose={handleClose} errorMessage={errorArray} />);

    const modal = screen.getByRole('presentation');
    expect(modal).toBeInTheDocument();
    expect(screen.getByText('Error 1')).toBeInTheDocument();
    expect(screen.getByText('Error 2')).toBeInTheDocument();
    expect(screen.getByText('Error 3')).toBeInTheDocument();
    expect(screen.getByText('Error 4')).toBeInTheDocument();
  });
});
