
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import AddActivityForm from "../components/AddActivityForm.jsx";

const mockAttractions = [
  {
    id: 1,
    name: "Eiffel Tower",
    matches_preferences: true,
  },
  {
    id: 2,
    name: "Louvre Museum",
    matches_preferences: false,
  },
];

const mockActivities = [];

describe("AddActivityForm", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
    vi.stubGlobal("alert", vi.fn());

    document.cookie = "csrftoken=test-token";
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders the attraction selector and time inputs", () => {
    render(
      <AddActivityForm
        attractions={mockAttractions}
        preferences={[]}
        activities={mockActivities}
        addUrl="/add-activity/"
        onAdded={vi.fn()}
      />,
    );

    expect(screen.getByRole("combobox")).toBeInTheDocument();
    expect(screen.getByLabelText(/start time/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/end time/i)).toBeInTheDocument();
  });

  it("displays the available attractions", () => {
    render(
      <AddActivityForm
        attractions={mockAttractions}
        preferences={[]}
        activities={mockActivities}
        addUrl="/add-activity/"
        onAdded={vi.fn()}
      />,
    );

    expect(
      screen.getByRole("option", { name: /eiffel tower/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("option", { name: /louvre museum/i }),
    ).toBeInTheDocument();
  });

  it("displays a validation error when no attraction is selected", async () => {
    const user = userEvent.setup();

    render(
      <AddActivityForm
        attractions={mockAttractions}
        preferences={[]}
        activities={mockActivities}
        addUrl="/add-activity/"
        onAdded={vi.fn()}
      />,
    );

    await user.click(screen.getByRole("button", { name: /add activity/i }));

    expect(screen.getByRole("alert")).toBeInTheDocument();
  });

  it("displays a validation error when the start time is after the end time", async () => {
    const user = userEvent.setup();

    render(
      <AddActivityForm
        attractions={mockAttractions}
        preferences={[]}
        activities={mockActivities}
        addUrl="/add-activity/"
        onAdded={vi.fn()}
      />,
    );

    await user.selectOptions(screen.getByRole("combobox"), "1");
    await user.clear(screen.getByLabelText(/start time/i));
    await user.type(screen.getByLabelText(/start time/i), "11:00");
    await user.clear(screen.getByLabelText(/end time/i));
    await user.type(screen.getByLabelText(/end time/i), "10:00");

    await user.click(screen.getByRole("button", { name: /add activity/i }));

    expect(screen.getByRole("alert")).toBeInTheDocument();
  });

  it("filters attractions when the For you checkbox is selected", async () => {
    const user = userEvent.setup();

    render(
      <AddActivityForm
        attractions={mockAttractions}
        preferences={[]}
        activities={[]}
        addUrl="/add-activity/"
        onAdded={vi.fn()}
      />,
    );

    await user.click(screen.getByText("For you"));

    expect(
      screen.getByRole("option", { name: /eiffel tower/i }),
    ).toBeInTheDocument();

    expect(
      screen.queryByRole("option", { name: /louvre museum/i }),
    ).not.toBeInTheDocument();
  });

  it("submits the selected activity successfully", async () => {
    const user = userEvent.setup();
    const onAdded = vi.fn();

    fetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        activity: { id: 101 },
      }),
    });

    render(
      <AddActivityForm
        attractions={mockAttractions}
        preferences={[]}
        activities={mockActivities}
        addUrl="/add-activity/"
        onAdded={onAdded}
      />,
    );

    await user.selectOptions(screen.getByRole("combobox"), "1");

    await user.click(screen.getByRole("button", { name: /add activity/i }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalled();
      expect(onAdded).toHaveBeenCalledWith({ id: 101 });
    });
  });

  it("sends the correct request details when adding an activity", async () => {
    const user = userEvent.setup();

    fetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        activity: { id: 101 },
      }),
    });

    render(
      <AddActivityForm
        attractions={mockAttractions}
        preferences={[]}
        activities={mockActivities}
        addUrl="/add-activity/"
        onAdded={vi.fn()}
      />,
    );

    await user.selectOptions(screen.getByRole("combobox"), "1");

    await user.click(screen.getByRole("button", { name: /add activity/i }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "/add-activity/",
        expect.objectContaining({
          method: "POST",
          headers: expect.objectContaining({
            "Content-Type": "application/json",
            "X-CSRFToken": "test-token",
          }),
          body: JSON.stringify({
            attraction_id: 1,
            start_time: "09:00",
            end_time: "10:00",
          }),
        }),
      );
    });
  });

  it("displays an error when the API request fails", async () => {
    const user = userEvent.setup();

    fetch.mockResolvedValue({
      ok: false,
      json: async () => ({}),
    });

    render(
      <AddActivityForm
        attractions={mockAttractions}
        preferences={[]}
        activities={mockActivities}
        addUrl="/add-activity/"
        onAdded={vi.fn()}
      />,
    );

    await user.selectOptions(screen.getByRole("combobox"), "1");
    await user.click(screen.getByRole("button", { name: /add activity/i }));

    expect(await screen.findByRole("alert")).toBeInTheDocument();
  });
});
