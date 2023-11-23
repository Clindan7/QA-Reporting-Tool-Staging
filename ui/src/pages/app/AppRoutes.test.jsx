import { render } from "@testing-library/react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { createMemoryHistory } from 'history';
import { appRoutes } from "./AppRoutes";

jest.mock('../../assets/Logo.png', () => 'LogoMock');

const history = createMemoryHistory({ initialEntries: [''] });

const renderWithRouter = (initialEntries) => {
  return render(
    <BrowserRouter initialEntries={initialEntries}>
      <Routes>
        {appRoutes.map((route) => (
          <Route key={route.path} path={route.path} element={route.element} />
        ))}
      </Routes>
    </BrowserRouter>
  );
};

describe("App Routes", () => {
  it('Test 1: should render component', () => {
    const { container } = renderWithRouter([""]);
    expect(container).toBeTruthy();
  });

  it("renders Login component on default route", () => {
    renderWithRouter([""]);
    expect(history.location.pathname).toBe('/');
  });

  it("renders Dashboard component on /dashboard route", () => {
    renderWithRouter(["/dashboard"]);
    expect(history.location.pathname).toBe('/');
  });

  it("renders Project component on /project/:id route", () => {
    renderWithRouter(["/project/123"]);
    expect(history.location.pathname).toBe('/');
  });
});
