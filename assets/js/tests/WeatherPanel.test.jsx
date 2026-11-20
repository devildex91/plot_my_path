
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import WeatherPanel from "../components/WeatherPanel.jsx";

const mockDay = {
  day_number: 1,
  date: "2026-06-15",
};

const mockWeather = [
  {
    date: "2026-06-15",
    conditions: "Sunny",
    tempmax: 24,
    tempmin: 15,
    precipprob: 10,
  },
  {
    date: "2026-06-16",
    conditions: "Cloudy",
    tempmax: 19,
    tempmin: 12,
    precipprob: 60,
  },
];

describe("WeatherPanel", () => {
  it("displays the destination and selected itinerary day", () => {
    render(
      <WeatherPanel
        destinationName="Paris"
        day={mockDay}
        weather={mockWeather}
        error={null}
      />
    );

    expect(
      screen.getByRole("heading", {
        name: "Weather in Paris · Day 1 (2026-06-15)",
      })
    ).toBeInTheDocument();
  });

  it("displays the forecast matching the selected day", () => {
    render(
      <WeatherPanel
        destinationName="Paris"
        day={mockDay}
        weather={mockWeather}
        error={null}
      />
    );

    expect(screen.getByText("Sunny")).toBeInTheDocument();
    expect(screen.getByText("24 °C")).toBeInTheDocument();
    expect(screen.getByText("15 °C")).toBeInTheDocument();
    expect(screen.getByText("10%")).toBeInTheDocument();
  });

  it("does not display weather for a different day", () => {
    render(
      <WeatherPanel
        destinationName="Paris"
        day={mockDay}
        weather={mockWeather}
        error={null}
      />
    );

    expect(screen.queryByText("Cloudy")).not.toBeInTheDocument();
    expect(screen.queryByText("19 °C")).not.toBeInTheDocument();
  });

  it("displays an error message when an error is provided", () => {
    render(
      <WeatherPanel
        destinationName="Paris"
        day={mockDay}
        weather={mockWeather}
        error="Unable to load weather data."
      />
    );

    expect(
      screen.getByRole("status")
    ).toHaveTextContent("Unable to load weather data.");

    expect(screen.queryByText("Sunny")).not.toBeInTheDocument();
  });

  it("displays a message when no weather data is available", () => {
    render(
      <WeatherPanel
        destinationName="Paris"
        day={mockDay}
        weather={[]}
        error={null}
      />
    );

    expect(
      screen.getByRole("status")
    ).toHaveTextContent("No weather data available for this day.");
  });

  it("displays a message when weather data does not match the selected day", () => {
    render(
      <WeatherPanel
        destinationName="Paris"
        day={mockDay}
        weather={[
          {
            date: "2026-06-16",
            conditions: "Cloudy",
            tempmax: 19,
            tempmin: 12,
            precipprob: 60,
          },
        ]}
        error={null}
      />
    );

    expect(
      screen.getByRole("status")
    ).toHaveTextContent("No weather data available for this day.");
  });
});
