
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ItineraryBuilder from "../components/itinerary_builder.jsx";

// Mock the child components so these tests focus on ItineraryBuilder.
vi.mock("../components/ActivityList.jsx", () => ({
  default: ({ activities, onRemove, error }) => (
    <div data-testid="activity-list">
      <p>Activities: {activities.length}</p>

      {activities.map((activity) => (
        <button
          key={activity.id}
          type="button"
          onClick={() => onRemove(activity.id)}
        >
          Remove {activity.id}
        </button>
      ))}

      {error && <p role="alert">{error}</p>}
    </div>
  ),
}));

vi.mock("../components/AddActivityForm.jsx", () => ({
  default: ({ onAdded }) => (
    <button
      type="button"
      onClick={() =>
        onAdded({
          id: 99,
          attraction_id: 1,
          start_time: "11:00",
          end_time: "12:00",
        })
      }
    >
      Add mock activity
    </button>
  ),
}));

vi.mock("../components/ItineraryMap.jsx", () => ({
  default: () => <div data-testid="itinerary-map">Map</div>,
}));

vi.mock("../components/WeatherPanel.jsx", () => ({
  default: () => <div data-testid="weather-panel">Weather</div>,
}));

const mockAttractions = [
  {
    id: 1,
    name: "Eiffel Tower",
    category: "historic",
    entry_cost: 25,
    lng: 2.2945,
    lat: 48.8584,
  },
  {
    id: 2,
    name: "Louvre Museum",
    category: "culture",
    entry_cost: 10,
    lng: 2.3376,
    lat: 48.8606,
  },
];
const mockDays = [
  {
    id: 2,
    day_number: 2,
    date: "2026-06-02",
    activities: [],
    add_activity_url: "/add-day-2/",
  },
  {
    id: 1,
    day_number: 1,
    date: "2026-06-01",
    activities: [
      {
        id: 10,
        attraction_id: 1,
        start_time: "09:00",
        end_time: "10:00",
      },
    ],
    add_activity_url: "/add-day-1/",
  },
];

const mockTrip = {
  id: 5,
  budget: 200,
  trip_days: mockDays,
  destination: {
    name: "Paris",
    latitude: "48.8566",
    longitude: "2.3522",
  },
};

const renderItinerary = (overrides = {}) => {
  return render(
    <ItineraryBuilder
      trip={mockTrip}
      preferences={{ history: true }}
      days={mockDays}
      attractions={mockAttractions}
      weather={[]}
      weatherError={null}
      {...overrides}
    />,
  );
};

describe("ItineraryBuilder", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
    document.cookie = "csrftoken=test-token";
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders the first itinerary day in day-number order", () => {
    renderItinerary();

    expect(
      screen.getByRole("heading", { name: "Day 1" }),
    ).toBeInTheDocument();

    expect(screen.getByText("Day 1 of 2")).toBeInTheDocument();
    expect(screen.getByTestId("activity-list")).toBeInTheDocument();
  });

  it("displays a message when no itinerary days are available", () => {
    renderItinerary({
      trip: { ...mockTrip, trip_days: [] },
      days: [],
    });

    expect(
      screen.getByText("No itinerary days available."),
    ).toBeInTheDocument();
  });

  it("allows the user to move between itinerary days", async () => {
    const user = userEvent.setup();

    renderItinerary();

    const previousButton = screen.getByRole("button", {
      name: "Previous day",
    });

    const nextButton = screen.getByRole("button", {
      name: "Next day",
    });

    expect(previousButton).toBeDisabled();
    expect(nextButton).toBeEnabled();

    await user.click(nextButton);

    expect(
      screen.getByRole("heading", { name: "Day 2" }),
    ).toBeInTheDocument();

    expect(screen.getByText("Day 2 of 2")).toBeInTheDocument();
    expect(previousButton).toBeEnabled();
    expect(nextButton).toBeDisabled();

    await user.click(previousButton);

    expect(
      screen.getByRole("heading", { name: "Day 1" }),
    ).toBeInTheDocument();
  });

  it("calculates the daily budget and remaining budget", () => {
    renderItinerary();

    // £200 divided across two days gives £100 per day.
    // The Roman Baths activity costs £25.
    expect(screen.getByText("Today's budget: £100.00")).toBeInTheDocument();
    expect(screen.getByText("Remaining budget: £75.00")).toBeInTheDocument();
  });

  it("adds a new activity to the selected day", async () => {
    const user = userEvent.setup();

    renderItinerary();

    expect(screen.getByText("Activities: 1")).toBeInTheDocument();

    await user.click(
      screen.getByRole("button", { name: "Add mock activity" }),
    );

    expect(screen.getByText("Activities: 2")).toBeInTheDocument();
  });

  it("deletes an activity successfully", async () => {
    const user = userEvent.setup();

    fetch.mockResolvedValue({
      ok: true,
    });

    renderItinerary();

    await user.click(
      screen.getByRole("button", { name: "Remove 10" }),
    );

    await waitFor(() => {
      expect(screen.getByText("Activities: 0")).toBeInTheDocument();
    });

    expect(fetch).toHaveBeenCalledWith(
      "/trips/5/itinerary/activities/10/delete/",
      {
        method: "DELETE",
        headers: {
          "X-CSRFToken": "test-token",
        },
      },
    );
  });

  it("displays an error when deleting an activity fails", async () => {
    const user = userEvent.setup();

    fetch.mockResolvedValue({
      ok: false,
      json: async () => ({
        error: "Unable to delete activity.",
      }),
    });

    renderItinerary();

    await user.click(
      screen.getByRole("button", { name: "Remove 10" }),
    );

    expect(
      await screen.findByRole("alert"),
    ).toHaveTextContent("Unable to delete activity.");

    // The activity should remain in the itinerary.
    expect(screen.getByText("Activities: 1")).toBeInTheDocument();
  });

  it("renders the map and weather components", () => {
    renderItinerary();

    expect(screen.getByTestId("itinerary-map")).toBeInTheDocument();
    expect(screen.getByTestId("weather-panel")).toBeInTheDocument();
  });
});
