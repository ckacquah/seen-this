import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders seen this text", () => {
  render(<App />);
  const linkElement = screen.getByText(/Seen this/i);
  expect(linkElement).toBeInTheDocument();
});
