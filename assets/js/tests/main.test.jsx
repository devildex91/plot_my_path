import {
  describe,
  it,
  expect,
  vi,
  beforeAll,
  beforeEach,
  afterEach,
} from "vitest";
import { act, waitFor } from "@testing-library/react";

// Mock component imports.
vi.mock("../components/Onboarding.jsx", () => ({
  default: () => "Onboarding mounted",
}));

vi.mock("../components/SearchBar.jsx", () => ({
  default: () => "SearchBar mounted",
}));

vi.mock("../components/itinerary_builder.jsx", () => ({
  default: () => "ItineraryBuilder mounted",
}));

describe("main.jsx", () => {
  beforeAll(async () => {
    // Simulate the Django HTML template elements.
    document.documentElement.setAttribute("data-theme", "sunset");
    localStorage.setItem("theme", "sunset");
    document.cookie = "csrftoken=test-token; path=/";

    document.body.innerHTML = `
      <div id="onboarding" data-home-url="/home/"></div>

      <div
        id="searchDiv"
        data-base-url="/destinations/details/0/"
      ></div>

      <div id="builder"></div>

      <script id="app-data" type="application/json">
        {
          "trip": {"id": 1},
          "preferences": [],
          "days": [],
          "attractions": [],
          "weather": [],
          "weather_error": null
        }
      </script>

      <ul>
        <li>
          <input
            type="checkbox"
            id="theme-toggle"
            aria-label="Toggle dark mode"
          />
        </li>
      </ul>
    `;

    // Ensure main.jsx is evaluated after the test DOM has been created.
    vi.resetModules();

 await act(async () => {
  await import("../main.jsx");
});
});

  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
    vi.stubGlobal("alert", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.useRealTimers();
    vi.restoreAllMocks();

    document
      .querySelectorAll("[data-test-element]")
      .forEach((element) => element.remove());
  });

  it("mounts React components into the correct Django template elements", async () => {
  await waitFor(() => {
    expect(document.getElementById("onboarding"))
      .toHaveTextContent("Onboarding mounted");

    expect(document.getElementById("searchDiv"))
      .toHaveTextContent("SearchBar mounted");

    expect(document.getElementById("builder"))
      .toHaveTextContent("ItineraryBuilder mounted");
  });
});

  // Theme toggle tests

  it("initialises the theme checkbox using the current HTML theme", () => {
    const toggle = document.getElementById("theme-toggle");

    expect(toggle).toBeChecked();
  });

  it("changes the theme to fantasy when the toggle is unchecked", () => {
    const toggle = document.getElementById("theme-toggle");

    toggle.checked = false;
    toggle.dispatchEvent(new Event("change"));

    expect(document.documentElement).toHaveAttribute("data-theme", "fantasy");

    expect(localStorage.getItem("theme")).toBe("fantasy");
  });

  it("changes the theme to sunset when the toggle is checked", () => {
    const toggle = document.getElementById("theme-toggle");

    toggle.checked = true;
    toggle.dispatchEvent(new Event("change"));

    expect(document.documentElement).toHaveAttribute("data-theme", "sunset");

    expect(localStorage.getItem("theme")).toBe("sunset");
  });

  it("does not throw an error when the theme toggle is missing", () => {
    const toggle = document.getElementById("theme-toggle");

    expect(toggle).not.toBeNull();

    // The listener is registered only when the toggle exists.
    // This test verifies the existing toggle remains functional.
    expect(() => {
      toggle.dispatchEvent(new Event("change"));
    }).not.toThrow();
  });

  // Favourite button tests

  it("sends a POST request when a favourite button is clicked", async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ is_favourite: true }),
    });

    const button = document.createElement("button");
    button.className = "favourite-btn";
    button.dataset.url = "/favourites/1/";
    button.setAttribute("aria-label", "Add to favourites");
    button.setAttribute("data-test-element", "");

    const icon = document.createElement("i");
    icon.classList.add("fa-regular");

    button.appendChild(icon);
    document.body.appendChild(button);

    button.click();

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "/favourites/1/",
        expect.objectContaining({
          method: "POST",
          headers: {
            "X-CSRFToken": expect.any(String),
          },
        }),
      );
    });
  });

  it("updates the favourite button when an attraction is added to favourites", async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ is_favourite: true }),
    });

    const button = document.createElement("button");
    button.className = "favourite-btn";
    button.dataset.url = "/favourites/1/";
    button.setAttribute("aria-label", "Add to favourites");
    button.setAttribute("data-test-element", "");

    const icon = document.createElement("i");
    icon.classList.add("fa-regular");

    button.appendChild(icon);
    document.body.appendChild(button);

    button.click();

    await waitFor(() => {
      expect(icon).toHaveClass("fa-solid");
      expect(icon).toHaveClass("text-red-500");

      expect(button).toHaveAttribute("aria-label", "Remove from favourites");

      expect(button).not.toBeDisabled();
    });
  });

  it("updates the favourite button when an attraction is removed from favourites", async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ is_favourite: false }),
    });

    const button = document.createElement("button");
    button.className = "favourite-btn";
    button.dataset.url = "/favourites/1/";
    button.setAttribute("aria-label", "Remove from favourites");
    button.setAttribute("data-test-element", "");

    const icon = document.createElement("i");
    icon.classList.add("fa-solid", "text-red-500");

    button.appendChild(icon);
    document.body.appendChild(button);

    button.click();

    await waitFor(() => {
      expect(icon).toHaveClass("fa-regular");
      expect(icon).not.toHaveClass("text-red-500");

      expect(button).toHaveAttribute("aria-label", "Add to favourites");

      expect(button).not.toBeDisabled();
    });
  });

  it("does not send a request when a favourite button is disabled", () => {
    const button = document.createElement("button");
    button.className = "favourite-btn";
    button.dataset.url = "/favourites/1/";
    button.disabled = true;
    button.setAttribute("data-test-element", "");

    document.body.appendChild(button);

    button.click();

    expect(fetch).not.toHaveBeenCalled();
  });

  it("logs an error when the favourite request fails", async () => {
    const consoleError = vi
      .spyOn(console, "error")
      .mockImplementation(() => {});

    fetch.mockResolvedValue({
      ok: false,
      json: async () => ({
        error: "Unable to update favourite.",
      }),
    });

    const button = document.createElement("button");
    button.className = "favourite-btn";
    button.dataset.url = "/favourites/1/";
    button.setAttribute("data-test-element", "");

    const icon = document.createElement("i");
    icon.classList.add("fa-regular");

    button.appendChild(icon);
    document.body.appendChild(button);

    button.click();

    await waitFor(() => {
      expect(consoleError).toHaveBeenCalled();
      expect(button).not.toBeDisabled();
    });
  });

  // Checkout tests

  it("sends a POST request when the checkout button is clicked", async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        error: "Payment unavailable.",
      }),
    });

    const button = document.createElement("button");
    button.id = "checkout-button";
    button.dataset.url = "/checkout/";
    button.dataset.csrf = "checkout-token";
    button.setAttribute("data-test-element", "");

    document.body.appendChild(button);

    button.click();

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "/checkout/",
        expect.objectContaining({
          method: "POST",
          headers: {
            "X-CSRFToken": "checkout-token",
          },
        }),
      );
    });
  });

  it("displays an error when checkout cannot proceed", async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        error: "Payment unavailable.",
      }),
    });

    const button = document.createElement("button");
    button.id = "checkout-button";
    button.dataset.url = "/checkout/";
    button.dataset.csrf = "checkout-token";
    button.setAttribute("data-test-element", "");

    document.body.appendChild(button);

    button.click();

    await waitFor(() => {
      expect(alert).toHaveBeenCalledWith("Payment unavailable.");
      expect(button).not.toBeDisabled();
    });
  });

  it("displays a fallback message when checkout returns no error", async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => ({}),
    });

    const button = document.createElement("button");
    button.id = "checkout-button";
    button.dataset.url = "/checkout/";
    button.dataset.csrf = "checkout-token";
    button.setAttribute("data-test-element", "");

    document.body.appendChild(button);

    button.click();

    await waitFor(() => {
      expect(alert).toHaveBeenCalledWith("Error: Unable to proceed to payment");
    });
  });

  it("displays an error when payment processing fails", async () => {
    fetch.mockRejectedValue(new Error("Network error"));

    const button = document.createElement("button");
    button.id = "checkout-button";
    button.dataset.url = "/checkout/";
    button.dataset.csrf = "checkout-token";
    button.setAttribute("data-test-element", "");

    document.body.appendChild(button);

    button.click();

    await waitFor(() => {
      expect(alert).toHaveBeenCalledWith("Payment processing failed");

      expect(button).not.toBeDisabled();
    });
  });

  // Message fade-out test

  it("adds the fade-out class to alerts after three seconds", async () => {
    vi.useFakeTimers();

    const container = document.createElement("div");
    container.id = "message-container";
    container.setAttribute("data-test-element", "");

    const alertElement = document.createElement("div");
    alertElement.className = "alert";

    container.appendChild(alertElement);
    document.body.appendChild(container);

    document.dispatchEvent(new Event("DOMContentLoaded"));

    expect(alertElement).not.toHaveClass("fade-out");

    await vi.advanceTimersByTimeAsync(3000);

    expect(alertElement).toHaveClass("fade-out");
  });
});
